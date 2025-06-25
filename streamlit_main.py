import streamlit as st
import requests
from PIL import Image

# Read the public URL created by Flask
try:
    with open("public_url.txt", "r") as f:
        api_url = f.read().strip()
except FileNotFoundError:
    st.error("❌ Flask app is not running. Please run app.py first.")
    st.stop()

# Test connection
try:
    response = requests.get(f"{api_url}/")
    if response.status_code == 200:
        st.success("✅ Flask API and model are running!")
    else:
        st.warning("⚠️ Could not verify the model from Flask.")
except Exception as e:
    st.error(f"❌ Failed to connect to Flask API: {e}")
    st.stop()

st.title("💵 Pakistani Currency Note Detector")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
    if st.button("Predict & Play Audio"):
    try:
        result = requests.post(
            f"{api_url}/prediction",
            files={"image": uploaded_image}
        )
        if result.status_code == 200:
            # ✅ Save and play audio
            with open("prediction.mp3", "wb") as f:
                f.write(result.content)
            st.audio("prediction.mp3", format="audio/mp3")

            # ✅ Show text output from header
            predicted_label = result.headers.get("X-Label", "")
            if predicted_label:
                st.success(f"🔤 Predicted Label: {predicted_label}")
        else:
            st.error("❌ Prediction failed. Try again.")
    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")
    # if st.button("Predict & Play Audio"):
    #     try:
    #         result = requests.post(
    #             f"{api_url}/prediction",
    #             files={"image": uploaded_image}
    #         )
    #         if result.status_code == 200:
    #             with open("prediction.mp3", "wb") as f:
    #                 f.write(result.content)
    #             st.audio("prediction.mp3", format="audio/mp3")
    #         else:
    #             st.error("❌ Prediction failed. Try again.")
        # except Exception as e:
        #     st.error(f"❌ Error during prediction: {e}")
