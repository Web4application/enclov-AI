#!/bin/bash
set -e

APP_NAME="enclov-AI"
DOCKER_COMPOSE_FILE="$APP_NAME/docker-compose.yml"

echo "🔎 Checking status of Docker containers..."
docker-compose -f "$DOCKER_COMPOSE_FILE" ps
