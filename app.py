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







# from flask import Flask, request, jsonify, send_file
# from pyngrok import ngrok
# from gtts import gTTS
# from io import BytesIO
# from PIL import Image
# from ultralytics import YOLO
# import os

# app = Flask(__name__)
# port_no = 5000

# # Set your NGROK token
# ngrok.set_auth_token("2yzjjShepI3rvFK5x43D2Xl90rD_9rsvPPnRXPedqpPgmfM7")
# public_url = ngrok.connect(port_no).public_url

# # Save the public URL to a file
# with open("public_url.txt", "w") as f:
#     f.write(public_url)

# # Load model
# model = YOLO("best.pt")

# @app.route('/')
# def welcome():
#     return "Welcome to Currency Note Classifier"

# @app.route('/prediction', methods=['POST'])
# def predict():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'})

#     image = request.files['image']
#     image = Image.open(image.stream)
#     results = model.predict(image)
#     predicted_note_value = results[0].names[results[0].probs.top1]
    
#     if '_' in predicted_note_value:
#         predicted_note_value = predicted_note_value.split("_")[0]
#         model_output_text = f"{predicted_note_value} روپے"
#     else:
#         model_output_text = "اِن ویلیڈ دوبارہ کوشش کریں"

#     tts = gTTS(text=model_output_text, lang="ur")
#     audio_stream = BytesIO()
#     tts.write_to_fp(audio_stream)
#     audio_stream.seek(0)

#     return send_file(audio_stream, mimetype='audio/mp3')

# print(f"For public access please visit: {public_url}/prediction")
# app.run(port=port_no)
