from unittest import result

import streamlit as st
import anthropic
import base64
import requests

st.title('Pokemon Recognizer')

ROBOFLOW_MODEL = '/Users/gustavwilquin/Desktop/KEA Filer/4. Semester/Eksamen/ml-python-exam-project/machine_learning/roboflow_model/Pokemon-1'


uploaded = st.file_uploader("Upload a picture", type=["jpg", "png", "jpeg", "webp"])

if uploaded:
    st.image(uploaded)

    b64 = base64.b64encode(uploaded.getbuffer()).decode("utf-8")
    mime = uploaded.type or "image/jpeg"

    with st.spinner("Downloading picture..."):
        response = requests.post(
            f'http://localhost:9001/{ROBOFLOW_MODEL}',
            data=b64,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        response = response.json()

        prediction = result.get("prediction", [])

        if not prediction:
            st.warning('No pokemon detected')
        else:
            top = max(prediction, key=lambda p: p['confidence'])
            detected_name = top['category_id']
            confidence = round(top['confidence'] * 100, 2)

            st.write(f'**Pokemon detected:** {detected_name} ({confidence}% confidence)' )

            uploaded.seek(0)
            b64 = base64.b64encode(uploaded.getbuffer()).decode("utf-8")
            mime = uploaded.type or "image/jpeg"

            with st.spinner("Getting picture..."):
                claude = anthropic.Anthropic()
                message = claude.message.create(
                    model='claude-sonnet-4-20250514',
                    max_tokens=256,
                    messages=[{
                        "role": "user",
                        "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}},
                        {"type": "text",
                        "text": f"My model identified this as {detected_name}. Give a short Pokédex-style description."},
                        ],
                    }],
                )

            st.write(message.content[0].text)