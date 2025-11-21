# backend/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies required by some Python packages (psycopg2, scikit-learn build, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install (cached layer)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose port
EXPOSE 8000

# Start-up command: init DB, ingest data, train model, then start FastAPI.
# Using a bash -c chain ensures that we run each step in order.
CMD ["bash", "-c", "python init_db.py && python data_ingestion.py && python train_model.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
