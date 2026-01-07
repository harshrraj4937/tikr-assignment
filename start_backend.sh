#!/bin/bash
cd backend
echo "Starting FastAPI backend on http://localhost:7000..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 7000

