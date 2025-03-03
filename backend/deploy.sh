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

echo "Checking if app container is running..."
if [ "$(docker ps -q -f name=backend-app)" ]; then
    echo "App container is running!"
else
    echo "App container is not running!"
    docker-compose logs
    exit 1
fi

echo "Deployment completed successfully!" 