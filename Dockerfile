# Use a slim Python image to keep Docker size small
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install packages
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Run the app
CMD ["python", "app.py"]
