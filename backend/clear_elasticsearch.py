#!/usr/bin/env python
"""
Скрипт для очистки индексов Elasticsearch.
Удаляет индексы игроков для чистого перезапуска.
"""

import os
import sys
import time
import requests
from requests.exceptions import ConnectionError, Timeout

# Получение параметров подключения из переменных окружения или использование значений по умолчанию
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT", "9200")
ELASTICSEARCH_URL = f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"

# Список индексов для удаления
INDICES = ["players"]

def wait_for_elasticsearch(max_retries=30, retry_interval=2):
    """Ожидание готовности Elasticsearch."""
    print(f"Проверка подключения к Elasticsearch: {ELASTICSEARCH_URL}")
    retries = 0
    while retries < max_retries:
        try:
            response = requests.head(ELASTICSEARCH_URL, timeout=5)
            if response.status_code == 200:
                print("Успешное подключение к Elasticsearch!")
                return True
            else:
                retries += 1
                print(f"Elasticsearch не готов (код: {response.status_code}), попытка {retries}/{max_retries}")
        except (ConnectionError, Timeout) as e:
            retries += 1
            print(f"Не удалось подключиться к Elasticsearch (попытка {retries}/{max_retries}): {e}")
        
        if retries < max_retries:
            print(f"Повторная попытка через {retry_interval} секунд...")
            time.sleep(retry_interval)
        else:
            print("Превышено максимальное количество попыток. Выход.")
            return False
    
    return False

def delete_indices():
    """Удаление индексов Elasticsearch."""
    for index in INDICES:
        print(f"Проверка существования индекса '{index}'...")
        response = requests.head(f"{ELASTICSEARCH_URL}/{index}")
        
        if response.status_code == 200:
            print(f"Удаление индекса '{index}'...")
            response = requests.delete(f"{ELASTICSEARCH_URL}/{index}")
            
            if response.status_code == 200:
                print(f"Индекс '{index}' успешно удален.")
            else:
                print(f"Ошибка при удалении индекса '{index}': {response.status_code}")
                print(response.text)
                return False
        elif response.status_code == 404:
            print(f"Индекс '{index}' не существует, пропускаем.")
        else:
            print(f"Неожиданный ответ при проверке индекса '{index}': {response.status_code}")
            print(response.text)
            return False
    
    print("Все указанные индексы были проверены и удалены (если существовали).")
    return True

if __name__ == "__main__":
    print("Запуск скрипта очистки Elasticsearch...")
    
    # Ожидание готовности Elasticsearch
    if not wait_for_elasticsearch():
        print("Не удалось подключиться к Elasticsearch. Выход.")
        sys.exit(1)
    
    # Предупреждение и подтверждение
    print("\n" + "!"*80)
    print("ВНИМАНИЕ! Этот скрипт удалит ВСЕ индексы Elasticsearch, указанные в скрипте!")
    print("Будут удалены следующие индексы:", INDICES)
    print("Эта операция НЕ МОЖЕТ БЫТЬ ОТМЕНЕНА!")
    print("!"*80 + "\n")
    
    # Поскольку скрипт запускается в контейнере, мы можем пропустить запрос подтверждения
    # и просто выполнить очистку
    success = delete_indices()
    
    if success:
        print("Индексы Elasticsearch успешно очищены!")
    else:
        print("Произошла ошибка при очистке индексов Elasticsearch.")
        sys.exit(1)
    
    print("Скрипт завершен.") 