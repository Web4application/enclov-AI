#!/bin/sh

# Start FastAPI backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Start Nginx in foreground (so container keeps running)
nginx -g 'daemon off;'
