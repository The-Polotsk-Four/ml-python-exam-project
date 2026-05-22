import streamlit as st
from functions.llm_chat_function import mistral_chatting, is_valid_mistral_key
import os
from dotenv import load_dotenv

load_dotenv()

# Sidebar navigation
st.sidebar.page_link('pokedex.py', label='Home')
st.sidebar.page_link('pages/clustering.py', label='Clustering')
st.sidebar.page_link('pages/mistral_streamlit_chat.py', label='Chat with pikachu')
st.sidebar.page_link('pages/pokemon_recogniser.py', label='Pokemon recogniser')

if os.getenv('MISTRAL_API_KEY') is None:
    st.text('This page needs you to have a valid api key for mistral, you can create or find your mistral api keys from: ')
    st.link_button('mistral api key page', 'https://admin.mistral.ai/organization/api-keys')
    api_key = st.text_input("Insert your API key for Mistral")
    if api_key:
        if is_valid_mistral_key(api_key):
            with open(".env", "a") as f:
                f.write(f"\nMISTRAL_API_KEY={api_key}")
            os.environ["MISTRAL_API_KEY"] = api_key
            st.rerun()
        else:
            st.error("Invalid API key. Please check and try again.")
else:
    st.title("Speak with the sage of thunder")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is on your mind youngling?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = mistral_chatting(st.session_state.messages)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})