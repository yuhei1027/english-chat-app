from tempfile import NamedTemporaryFile
from pathlib import Path
from dotenv import load_dotenv
import os
from typing import Any

from util import MyLogger,get_datetime

import openai
from openai import OpenAI

from langchain.chat_models import init_chat_model
from langchain.callbacks import get_openai_callback

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.outputs.llm_result import LLMResult
from langchain_core.runnables import ConfigurableField

class GenerativeAI:
    def __init__(self):
        #環境変数でOPENAIのAPIを読み込み
        self.initialize_session()
        self.init_chat_model()
        self.mylogger=MyLogger(header='datetime,model,total_tokens')
        self.prompt_template = ChatPromptTemplate.from_messages(
            [(
                "system",
                "You are a english teacher. Plase reply answer in English.However, it should be brief, not exceeding 100 words.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ])

    def initialize_session(self):
        load_dotenv()
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.client=OpenAI()

    def init_chat_model(self):
        self.chat_model = init_chat_model("gpt-4o-mini", model_provider="openai")

        # Define a new graph
        workflow = StateGraph(state_schema=MessagesState)

        # Define the (single) node in the graph
        workflow.add_edge(START, "model")
        workflow.add_node("model", self.call_model)

        # Add memory
        memory = MemorySaver()
        self.app = workflow.compile(checkpointer=memory)
    
    def init_session(self):
        self.init_chat_model()

    # Define the function that calls the model
    def call_model(self,state: MessagesState):
        prompt = self.prompt_template.invoke(state)
        response = self.chat_model.invoke(prompt)
        return {"messages": response}

    def speech_to_text(self,audio_bytes):
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_bytes)
            temp_file.flush()
            with open(temp_file.name, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe", 
                file=audio_file
                )
        print('-----STT-----')
        print(transcription)
        return transcription.text


    def get_AI_Response(self,query):

        output_parser = StrOutputParser()
        count_tokens_handler = CountTokensHandler(mylogger=self.mylogger,model_name='gpt-4o-mini')
        input_messages = [HumanMessage(query)]
        output = self.app.invoke(
            {"messages": input_messages},
            config={"callbacks": [count_tokens_handler],
            "configurable": {"thread_id": "abc123"}}
            )
        print('-----内部処理-----')
        print(output)
        count_tokens_handler.show_cost()
        return output_parser.invoke(output['messages'][-1])

    def text_to_speech(self,text):
        speech_file_path ='./voice/speech.mp3'

        response=self.client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="sage",
            input=text,
            instructions="You are a customer support center female operator.Please speak slowly and politely.",
        )
        print('----TTS-----')
        print(response)
        response.stream_to_file(speech_file_path)

# BaseCallbackHandlerを継承したカスタムコールバックハンドラ
class CountTokensHandler(BaseCallbackHandler):
    def __init__(self,mylogger,model_name):
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_tokens = 0
        self.invoke_count = 0
        self.mylogger=mylogger
        self.model_name=model_name

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        self.invoke_count += 1
        token_usage = (
            response.llm_output.get("token_usage", {})
            if response.llm_output is not None
            else {}
        )
        self.input_tokens += token_usage.get("prompt_tokens", 0)
        self.output_tokens += token_usage.get("completion_tokens", 0)
        self.total_tokens += token_usage.get("total_tokens", 0)

    def show_cost(self):
        s=f'{get_datetime()},{self.model_name},{self.total_tokens}'
        self.mylogger.write_log(s)
        print("\n******* OUTPUT SUMMARY *******")
        print(f"# of invoke:        {self.invoke_count}")
        print(f"# of input tokens:  {self.input_tokens}")
        print(f"# of output tokens: {self.output_tokens}")
        print(f"# of total tokens:  {self.total_tokens}")
        print("******************************")
