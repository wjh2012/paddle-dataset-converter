FROM python:3.12-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1 \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
WORKDIR /workspace

# requirements.txt 복사
COPY ../requirements.txt .

# 파이썬 패키지 설치
RUN pip install --upgrade pip && pip install -r requirements.txt