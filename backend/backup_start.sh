#!/bin/bash

echo "Running backup script..."
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la

# Проверяем переменные окружения
echo "Environment variables:"
echo "POSTGRES_SERVER: $POSTGRES_SERVER"
echo "POSTGRES_PORT: $POSTGRES_PORT" 
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_DB: $POSTGRES_DB"
echo "ELASTICSEARCH_HOST: $ELASTICSEARCH_HOST"
echo "ELASTICSEARCH_PORT: $ELASTICSEARCH_PORT"

# Ждем, пока база данных и Elasticsearch будут готовы
echo "Waiting for database and Elasticsearch to be ready..."
python wait_for_services.py
echo "Database and Elasticsearch are ready."

# Применяем миграции
echo "Applying migrations..."
alembic upgrade head
echo "Migrations applied successfully."

# Запускаем приложение
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload-exclude ".*" --reload-include "*.py" 