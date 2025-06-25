import streamlit as st
import requests
from PIL import Image
import os

# Step 1: Read the public URL from Flask (created when Flask runs)
try:
    with open("public_url.txt", "r") as f:
        api_url = f.read().strip()
except FileNotFoundError:
    st.error("❌ Flask app is not running. Please start it first.")
    st.stop()

# Step 2: Try a test call to see if model is loaded and reachable
try:
    response = requests.get(f"{api_url}/")
    if response.status_code == 200:
        st.success("✅ Flask API and model are running!")
    else:
        st.warning("⚠️ Could not verify the model from Flask.")
except Exception as e:
    st.error(f"❌ Failed to connect to Flask API: {e}")
    st.stop()

# Step 3: Streamlit frontend
st.title("💵 Pakistani Currency Note Detector")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
    if st.button("Predict & Play Audio"):
        try:
            files = {"image": uploaded_image.getvalue()}
            result = requests.post(f"{api_url}/prediction", files={"image": uploaded_image})
            if result.status_code == 200:
                # Save and play audio
                with open("prediction.mp3", "wb") as f:
                    f.write(result.content)
                st.audio("prediction.mp3", format="audio/mp3")
            else:
                st.error("❌ Prediction failed. Please try again.")
        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")
