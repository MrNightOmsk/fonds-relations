#!/bin/bash

# Делаем скрипт исполняемым при каждом запуске для надежности
# Если скрипт выполняется, значит у него уже есть права на выполнение,
# но мы все равно попытаемся выполнить chmod для файла и запишем это в лог
echo "Starting script with self-check for permissions..."
chmod +x "$0" 2>/dev/null || echo "Could not chmod self, but continuing anyway"

# Выводим информацию о среде выполнения
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