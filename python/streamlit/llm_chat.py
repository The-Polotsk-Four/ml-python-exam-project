import streamlit as st
from mistralai.client import Mistral
import os
from dotenv import load_dotenv

load_dotenv()


def mistral_chatting(content):
    with Mistral(
        api_key=os.getenv('MISTRAL_API_KEY'),
    ) as mistral:

        res = mistral.chat.complete(model="mistral-large-latest", messages=[
            {
                "role": "user",
                "content": f"{content}",
            },
        ], stream=False, response_format={
            "type": "text",
        })
        
        # Handle response
        print(res.choices[0].message.content)



mistral_chatting('I am the CHOSEN ONE')


