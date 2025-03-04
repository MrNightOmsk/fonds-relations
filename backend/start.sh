#!/bin/bash

# Ждем, пока база данных и Elasticsearch будут готовы
python wait_for_services.py

# Применяем миграции
alembic upgrade head

# Запускаем приложение
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload-exclude ".*" --reload-include "*.py" 