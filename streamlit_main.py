import streamlit as st
import requests
import base64

st.title("Pakistani Currency Note Detector 🎧")

uploaded_file = st.file_uploader("Upload currency note image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with st.spinner("Analyzing note..."):
        response = requests.post(
            "http://localhost:5000/prediction",  # or your public ngrok URL
            files={"image": uploaded_file}
        )
        result = response.json()
        label = result["label"]
        audio_data = base64.b64decode(result["audio_base64"])

        st.success(f"Detected: {label}")
        st.audio(audio_data, format="audio/mp3")
