import streamlit as st
import streamlit.components.v1 as stc
from audio_recorder_streamlit import audio_recorder
from tempfile import NamedTemporaryFile
import os
from GenerativeAI import GenerativeAI
from pathlib import Path
import base64
import time


def sound_audio():
    audio_path1 = './voice/speech.mp3' #入力する音声ファイル

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

def chat_bot():
    # ——————————————
    # ２. セッションステートの初期化
    # ——————————————
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if 'model' not in st.session_state:
        st.session_state.model=chat_AI=GenerativeAI()

    #2つのカラムを作成
    col1, col2 = st.columns(2)


    # ユーザー入力欄
    #prompt = st.chat_input("メッセージを入力してください…")

    with col2:
        # Record audio using Streamlit widget
        audio_bytes = audio_recorder('record',pause_threshold=30)

        if st.button('セッション初期化'):
            if st.session_state.model:
                st.session_state.model.init_session()
                st.session_state.messages=[]
            audio_bytes=None
    # ——————————————
    # ４. ユーザー入力を受けてモデルへ問い合わせ
    # ——————————————
    if audio_bytes:
        print('音声入力検知')
        # ① ユーザー発話をセッションに追加
        prompt=st.session_state.model.speech_to_text(audio_bytes)
        st.session_state.messages.append({"role": "user", "content": prompt})
        print(prompt)
        # ③ アシスタントの応答をセッションに追加
        reply=st.session_state.model.get_AI_Response(prompt)
        if reply:
            st.session_state.messages.append({"role": "assistant", "content": reply})
        #音声変換
        st.session_state.model.text_to_speech(reply)
        sound_audio()
    with col1:
    # 過去のやり取りをチャット形式で表示
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            elif msg["role"] == "assistant":
                st.chat_message("assistant").write(msg["content"])

if __name__ == "__main__":
    st.set_page_config(page_title="About", page_icon="📈")
    chat_bot()
