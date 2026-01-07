#!/bin/bash
# Stop Docker containers

echo "🛑 Stopping Tikr Docker containers..."
docker compose down

echo ""
echo "✅ Containers stopped!"
echo ""
echo "To start again, run: ./docker-start.sh"
echo ""

