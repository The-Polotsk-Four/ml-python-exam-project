import streamlit as st
from mistralai.client import Mistral
import os
from dotenv import load_dotenv

load_dotenv()


def mistral_chatting(messages):
    system_message = {
        # prompt for mistral so it know how to act
        "role": "system",
        "content": "You are the wise old pikachu, you shall answer with wisdom of a thousand worlds"
    }
    
    with Mistral(api_key=os.getenv('MISTRAL_API_KEY')) as mistral:
        res = mistral.chat.complete(
            model="mistral-large-latest",
            messages=[system_message] + messages, # message + message history and prompt gets send to mistral
            stream=False, # send the whole message once it is done generating instead of streaming it
            response_format={"type": "text"}
        )
        return res.choices[0].message.content



