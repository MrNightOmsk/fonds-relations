#!/bin/bash

# Простой скрипт для удаления индекса players в Elasticsearch
# Можно выполнить из контейнера backend или на хосте, если curl установлен

ELASTICSEARCH_HOST=${ELASTICSEARCH_HOST:-elasticsearch}
ELASTICSEARCH_PORT=${ELASTICSEARCH_PORT:-9200}
ELASTICSEARCH_URL="http://${ELASTICSEARCH_HOST}:${ELASTICSEARCH_PORT}"

echo "Очистка индекса Elasticsearch по адресу: $ELASTICSEARCH_URL"

# Проверяем доступность Elasticsearch
echo "Проверка подключения к Elasticsearch..."
if curl -s -f -o /dev/null -X HEAD "$ELASTICSEARCH_URL"; then
    echo "Успешное подключение к Elasticsearch!"
else
    echo "Не удалось подключиться к Elasticsearch. Выход."
    exit 1
fi

# Проверяем существование индекса players
echo "Проверка существования индекса 'players'..."
if curl -s -f -o /dev/null -X HEAD "$ELASTICSEARCH_URL/players"; then
    echo "Индекс 'players' существует, удаляем..."
    
    # Удаляем индекс
    DELETE_RESULT=$(curl -s -X DELETE "$ELASTICSEARCH_URL/players")
    
    if echo "$DELETE_RESULT" | grep -q '"acknowledged" *: *true'; then
        echo "Индекс 'players' успешно удален!"
    else
        echo "Ошибка при удалении индекса 'players':"
        echo "$DELETE_RESULT"
        exit 1
    fi
else
    echo "Индекс 'players' не существует, пропускаем."
fi

echo "Очистка Elasticsearch завершена!" 