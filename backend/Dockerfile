# backend/Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of backend code
COPY . /app

# Run DB init + ingestion + model training automatically
CMD ["bash", "-c", "python init_db.py && python data_ingestion.py && python train_model.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
