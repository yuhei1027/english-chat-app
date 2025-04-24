import openai
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
import os
from openai import OpenAI
from GenerativeAI import speech_to_text,get_AI_Response,text_to_speech
from pathlib import Path
import streamlit.components.v1 as stc
import base64
import time


def initialize_session():
    load_dotenv()
    openai.api_key = os.environ.get("OPENAI_API_KEY")

def sound_audio(text):
    audio_path1 = Path(__file__).parent / "speech.mp3" #入力する音声ファイル

    audio_placeholder = st.empty()

    file_ = open(audio_path1, "rb")
    contents = file_.read()
    file_.close()

    audio_str = "data:audio/ogg;base64,%s"%(base64.b64encode(contents).decode())
    audio_html = """
                    <audio autoplay=True>
                    <source src="%s" type="audio/ogg" autoplay=True>
                    Your browser does not support the audio element.
                    </audio>
                """ %audio_str

    audio_placeholder.empty()
    #time.sleep(0.1) #これがないと上手く再生されません
    audio_placeholder.markdown(audio_html, unsafe_allow_html=True)

# Example usage with Streamlit:
def main():
    st.title("Voice to Text Transcription")
    
    # Record audio using Streamlit widget
    audio_bytes = audio_recorder(pause_threshold=30)
    
    # Convert audio to text using OpenAI Whisper API
    if audio_bytes:
        transcript = speech_to_text(audio_bytes)
        text=get_AI_Response(transcript)
        text_to_speech(text)
        sound_audio(text)
        st.write("Transcribed Text:", text)

if __name__ == "__main__":
    initialize_session()
    main()
