#!/bin/bash
set -e

APP_NAME="enclov-AI"
REPO_URL="https://github.com/Web4application/enclov-AI.git"
FRONTEND_PATH="./index.html"
BACKEND_PATH="./app"
VERCEL_PROJECT_NAME="enclov-ai-frontend"

echo "🚀 Deploying $APP_NAME..."

# Step 1: Pull latest
if [ ! -d "$APP_NAME" ]; then
  git clone $https://github.com/Web4application/enclov-AI.git
else
  echo "🔄 Repo already exists. Pulling latest..."
  cd $APP_NAME && git pull && cd ..
fi

cd $enclove-AI

# Step 2: Check Docker Compose
echo "🐳 Starting Docker Compose stack..."
docker-compose up -d --build

# Step 3: Vercel Frontend Deploy (if installed)
if command -v vercel &> /dev/null; then
  echo "🌐 Deploying static frontend to Vercel..."
  cd frontend || mkdir frontend && cp $FRONTEND_PATH frontend/index.html && cd frontend
  vercel --prod --confirm --name "$VERCEL_PROJECT_NAME"
  cd ..
else
  echo "⚠️ Vercel CLI not found. Skipping frontend deploy."
  echo "Install via: npm i -g vercel"
fi

echo "✅ Deployment complete."
