import streamlit as st
import cv2
from functions.model_predict import predict_pokemon as pp
from PIL import Image

image_types = ['jpeg', 'png', 'webd']
image = st.file_uploader('Upload an image of a pokemon from generation 1', type= image_types)

if image is not None:
    pil_image = Image.open(image)
    pokemon_name, confidence, annotated_bgr = pp(pil_image)

    annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)
    st.image(annotated_rgb, caption=f'Predicted: {pokemon_name} ({confidence:.2%})')