#!/bin/bash
set -e

# Ждем готовности сервисов
python wait_for_services.py

# Запускаем тесты
exec pytest -v --cov=app --cov-report=term-missing tests/ 