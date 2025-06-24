#!/bin/bash
set -e

echo "🧹 Cleaning up stopped containers and dangling images..."
docker container prune -f
docker image prune -f
