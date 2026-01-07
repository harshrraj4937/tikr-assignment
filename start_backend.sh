#!/bin/bash
cd backend
echo "Starting FastAPI backend on http://localhost:8000..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

