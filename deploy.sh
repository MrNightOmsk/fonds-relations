#!/bin/bash
set -e

echo "Stopping and removing old containers..."
docker-compose down -v || true

echo "Removing old images..."
docker image prune -af || true

echo "Building and starting new containers..."
docker-compose up -d --build

echo "Waiting for services to be ready..."
sleep 10

echo "Checking if backend container is running..."
if [ "$(docker ps -q -f name=backend-app)" ]; then
    echo "Backend container is running!"
else
    echo "Backend container is not running!"
    docker-compose logs
    exit 1
fi

echo "Deployment completed successfully!" 