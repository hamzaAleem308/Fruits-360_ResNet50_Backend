# Use a small base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app file (but NOT large files like .pth!)
COPY app.py .

# Run the app
CMD ["python", "app.py"]
