from tempfile import NamedTemporaryFile
from openai import OpenAI
from pathlib import Path

def speech_to_text(audio_bytes):
    client = OpenAI()
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio_bytes)
        temp_file.flush()
        with open(temp_file.name, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe", 
            file=audio_file
            )
    return transcription.text


def get_AI_Response(text):
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4o-mini",
        input=text
    )

    print(response.output_text)
    return response.output_text


def text_to_speech(text):
    client = OpenAI()
    speech_file_path = Path(__file__).parent / "speech.mp3"

    response=client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="sage",
        input=text,
        instructions="You are a customer support center female operator.Please speak slowly and politely.",
    ) 
    response.stream_to_file(speech_file_path)
