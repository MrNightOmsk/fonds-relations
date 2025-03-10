#!/bin/bash

# Скрипт для полной очистки базы данных и Elasticsearch
# Запускать внутри контейнера backend

echo "=== Запуск полной очистки данных ==="
echo
echo "Шаг 1: Очистка PostgreSQL..."
python /app/backend/clear_database.py
DB_EXIT_CODE=$?

if [ $DB_EXIT_CODE -ne 0 ]; then
    echo "Ошибка при очистке базы данных!"
    exit 1
fi

echo
echo "Шаг 2: Очистка Elasticsearch..."
python /app/backend/clear_elasticsearch.py
ES_EXIT_CODE=$?

if [ $ES_EXIT_CODE -ne 0 ]; then
    echo "Ошибка при очистке Elasticsearch!"
    exit 1
fi

echo
echo "=== Очистка данных успешно завершена! ==="
echo "База данных PostgreSQL и индексы Elasticsearch успешно очищены."
echo
echo "Теперь вы можете заново импортировать данные." 