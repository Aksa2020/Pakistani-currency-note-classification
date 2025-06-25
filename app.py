from flask import Flask, request, jsonify, send_file, make_response
#from flask import Flask, request, jsonify, send_file
from pyngrok import ngrok
from gtts import gTTS
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
import os
import gdown

app = Flask(__name__)
port_no = 5000

# Set your NGROK token
ngrok.set_auth_token("2yzjjShepI3rvFK5x43D2Xl90rD_9rsvPPnRXPedqpPgmfM7")  # ✅ Replace this with your actual token
public_url = ngrok.connect(port_no).public_url

# Save the public URL to a file
with open("public_url.txt", "w") as f:
    f.write(public_url)

# Download model if not present
model_path = "best.pt"
drive_url = "https://github.com/Aksa2020/Pakistani-currency-note-classification/blob/7f577d60ecbf52c2bd806ebab0cbf84e8d5b9ae0/best.pt"  # ✅ Replace this with actual model file ID
if not os.path.exists(model_path):
    print("⏬ Downloading model from Google Drive...")
    gdown.download(drive_url, model_path, quiet=False)

# Load model
model = YOLO(model_path)

@app.route('/')
def welcome():
    return "✅ Flask API is up and model is loaded."

@app.route('/prediction', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = Image.open(request.files['image'].stream)
    results = model.predict(image)
    
    predicted_note_value = results[0].names[results[0].probs.top1]
    
    if '_' in predicted_note_value:
        predicted_note_value = predicted_note_value.split("_")[0]
        model_output_text = f"{predicted_note_value} روپے"
    else:
        model_output_text = "اِن ویلیڈ دوبارہ کوشش کریں"

    # Generate audio
    tts = gTTS(text=model_output_text, lang="ur")
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)

    # Encode audio as base64
    audio_base64 = base64.b64encode(audio_stream.read()).decode("utf-8")

    return jsonify({
        "label": model_output_text,
        "audio_base64": audio_base64
    })



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

#     # Return audio with text in header
#     response = make_response(send_file(audio_stream, mimetype='audio/mp3'))
#     response.headers["X-Label"] = model_output_text  # ✅ Correct way to attach text label
#     return response

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

# print(f"✅ Public URL for prediction: {public_url}/prediction")
# app.run(port=port_no)
