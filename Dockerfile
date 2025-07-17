# Use a lightweight image
FROM python:3.10-alpine

# Install dependencies for PyTorch & Flask
RUN apk add --no-cache --update \
    build-base \
    libffi-dev \
    python3-dev \
    py3-pip \
    jpeg-dev \
    zlib-dev \
    libjpeg \
    openblas-dev \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your application
COPY app.py .

# Run your app
CMD ["python", "app.py"]
