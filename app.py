import gdown
import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 🟢 Allow CORS for all routes

# 📁 Google Drive model file ID
file_id = '1ECe_6QcQAzaoAe64tYHLT346bxXPonAe'
output = 'model.pth'

# ✅ Download model if not exists
try:
    if not os.path.exists(output):
        print("📥 Downloading model from Google Drive...")
        gdown.download(f'https://drive.google.com/uc?id={file_id}', output, quiet=False)
except Exception as e:
    print("❌ Failed to download model:", e)
    exit(1)

# ✅ Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet50(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 206)  # 🔁 Change if number of classes differ

try:
    model.load_state_dict(torch.load(output, map_location=device))
    model.to(device)
    model.eval()
except Exception as e:
    print("❌ Failed to load model:", e)
    exit(1)

# 🌀 Image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "🟢 API is live"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    try:
        file = request.files["file"]
        image = Image.open(file).convert("RGB")
        image = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)

        return jsonify({"predicted_class": int(predicted.item())})

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)