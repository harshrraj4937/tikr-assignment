#!/bin/bash
# Quick start script for Docker full stack

echo "🐳 Starting Tikr Full Stack with Docker..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 Building and starting containers..."
docker compose up --build

echo ""
echo "✅ Application is running!"
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"

