#!/bin/sh

echo "🚀 Starting Enclov-AI..."

# Start FastAPI backend in background
echo "🔧 Launching FastAPI backend on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Start Nginx frontend (runs in foreground)
echo "🎨 Serving React frontend with Nginx on port 80..."
nginx -g "daemon off;"
