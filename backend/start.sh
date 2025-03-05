#!/bin/bash

# Делаем скрипт исполняемым при каждом запуске для надежности
# Если скрипт выполняется, значит у него уже есть права на выполнение,
# но мы все равно попытаемся выполнить chmod для файла и запишем это в лог
echo "Starting script with self-check for permissions..."
chmod +x "$0" 2>/dev/null || echo "Could not chmod self, but continuing anyway"

# Ждем, пока база данных и Elasticsearch будут готовы
python wait_for_services.py

# Применяем миграции
alembic upgrade head

# Запускаем приложение
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload-exclude ".*" --reload-include "*.py" 