import streamlit as st

def main():

    about = st.Page(
        page="contents/english_chat.py", title="英会話アプリ", icon=":material/apps:"
    )
    tokens = st.Page(
        page="contents/graph_tokens.py", title="トークン利用状況", icon=":material/apps:"
    )

    pg = st.navigation([about,tokens])
    pg.run()

if __name__ == "__main__":
    main()