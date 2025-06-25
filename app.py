from flask import Flask, request, jsonify, send_file
from pyngrok import ngrok
from gtts import gTTS
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
import os

app = Flask(__name__)
port_no = 5000

# Set your NGROK token
ngrok.set_auth_token("2eKELCCL3WBzNrI1pjqbc0H0uMY_3NoChfFaVsZAyy5HK9ENr")
public_url = ngrok.connect(port_no).public_url

# Save the public URL to a file
with open("public_url.txt", "w") as f:
    f.write(public_url)

# Load model
model = YOLO("best.pt")

@app.route('/')
def welcome():
    return "Welcome to Currency Note Classifier"

@app.route('/prediction', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    image = request.files['image']
    image = Image.open(image.stream)
    results = model.predict(image)
    predicted_note_value = results[0].names[results[0].probs.top1]
    
    if '_' in predicted_note_value:
        predicted_note_value = predicted_note_value.split("_")[0]
        model_output_text = f"{predicted_note_value} روپے"
    else:
        model_output_text = "اِن ویلیڈ دوبارہ کوشش کریں"

    tts = gTTS(text=model_output_text, lang="ur")
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)

    return send_file(audio_stream, mimetype='audio/mp3')

print(f"For public access please visit: {public_url}/prediction")
app.run(port=port_no)
