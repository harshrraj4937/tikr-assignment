#!/bin/bash
# Start Docker full stack in detached mode (background)

echo "🐳 Starting Tikr Full Stack in background mode..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

docker compose up -d --build

echo ""
echo "✅ Application started in background!"
echo ""
echo "🌐 Access points:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:7000"
echo "  API Docs: http://localhost:7000/docs"
echo ""
echo "📊 Useful commands:"
echo "  View logs:        docker compose logs -f"
echo "  View status:      docker compose ps"
echo "  Stop containers:  docker compose down"
echo ""

