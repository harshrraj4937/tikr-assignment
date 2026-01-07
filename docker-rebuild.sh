#!/bin/bash
# Rebuild Docker containers from scratch

echo "🔨 Rebuilding Tikr Docker containers..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🛑 Stopping existing containers..."
docker compose down

echo ""
echo "🗑️  Cleaning up old images..."
docker compose build --no-cache

echo ""
echo "🚀 Starting fresh containers..."
docker compose up -d

echo ""
echo "✅ Rebuild complete!"
echo ""
echo "🌐 Access points:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:7000"
echo "  API Docs: http://localhost:7000/docs"
echo ""
echo "📋 View logs: ./docker-logs.sh"
echo ""

