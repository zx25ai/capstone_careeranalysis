#!/bin/bash
set -e

echo "▶ Creating tables..."
python - << 'EOF'
from database import Base, engine
import models
Base.metadata.create_all(bind=engine)
EOF

echo "▶ Running ingestion..."
python data_ingestion.py

echo "▶ Starting FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 8000
