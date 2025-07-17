import gdown
import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from flask import Flask, request, jsonify

app = Flask(__name__)

# https://drive.google.com/file/d/1ECe_6QcQAzaoAe64tYHLT346bxXPonAe/view?usp=drive_link

# 📁 Google Drive model link
file_id = '1ECe_6QcQAzaoAe64tYHLT346bxXPonAe'
output = 'model.pth'

# ✅ Download model if not exists
if not os.path.exists(output):
    gdown.download(f'https://drive.google.com/uc?id={file_id}', output, quiet=False)

# ✅ Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet50(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 206)  # Update if class count differs
model.load_state_dict(torch.load(output, map_location=device))
model.eval()
model.to(device)

# 🌀 Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["file"]
    image = Image.open(file).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)

    return jsonify({"predicted_class": int(predicted.item())})

if __name__ == "__main__":
    app.run(debug=True)
