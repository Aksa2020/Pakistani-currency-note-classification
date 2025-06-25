import streamlit as st
import requests
from PIL import Image
import base64
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
            result = requests.post(f"{api_url}/prediction", files={"image": uploaded_image})
            if result.status_code == 200:
                result_json = result.json()
                predicted_label = result_json.get("label", "")
                audio_base64 = result_json.get("audio_base64", "")

                if predicted_label:
                    st.markdown(f"🔤 **Predicted Label:** {predicted_label}")

                if audio_base64:
                    audio_binary = base64.b64decode(audio_base64)
                    with open("prediction.mp3", "wb") as f:
                        f.write(audio_binary)
                    st.audio("prediction.mp3", format="audio/mp3")
                else:
                    st.warning("⚠️ No audio returned.")
            else:
                st.error(f"❌ Server error: {result.status_code}")
        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")



# if uploaded_image is not None:
#     st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

#     if st.button("Predict & Play Audio"):
#         try:
#             # Send image to Flask API
#             result = requests.post(
#                 f"{api_url}/prediction",
#                 files={"image": uploaded_image}
#             )

#             if result.status_code == 200:
#                 # Save and play audio
#                 with open("prediction.mp3", "wb") as f:
#                     f.write(result.content)
#                 st.audio("prediction.mp3", format="audio/mp3")

#                 # ✅ Show predicted label text from response header
#                 predicted_label = result.headers.get("X-Label", "🔍 No label returned")
#                 if predicted_label:
#                     st.success(f"🔤 Predicted Label: {predicted_label}")
#             else:
#                 st.error("❌ Prediction failed. Please try again.")

#         except Exception as e:
#             st.error(f"❌ Error during prediction: {e}")

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
