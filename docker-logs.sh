#!/bin/bash
# View Docker logs

echo "📋 Viewing Docker logs (Ctrl+C to exit)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$1" == "backend" ]; then
    echo "📦 Backend logs only:"
    docker compose logs -f backend
elif [ "$1" == "frontend" ]; then
    echo "📦 Frontend logs only:"
    docker compose logs -f frontend
else
    echo "📦 All logs:"
    docker compose logs -f
fi

