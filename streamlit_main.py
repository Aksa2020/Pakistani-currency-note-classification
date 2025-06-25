import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import base64
import os

# Read public URL from file
with open("public_url.txt", "r") as f:
    api_url = f.read().strip()

st.title("💵 Pakistani Currency Note Detector")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Predict & Play Audio"):
        files = {"image": uploaded_image.getvalue()}
        response = requests.post(f"{api_url}/prediction", files={"image": uploaded_image})

        if response.status_code == 200:
            st.audio(response.content, format='audio/mp3')
        else:
            st.error("Prediction failed. Please try again.")
