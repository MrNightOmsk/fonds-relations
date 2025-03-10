#!/usr/bin/env python
import json
import os
import sys
import requests
from typing import Set, Dict, Any, List, Optional
import time
import logging

# Настройка логирования
log_file = "import_funds.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def read_output_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает файл output.json и возвращает его содержимое
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_fund_ids(data: List[Dict[str, Any]]) -> Set[str]:
    """
    Извлекает уникальные ID фондов из поля "author" в данных
    """
    fund_ids = set()
    for item in data:
        if "author" in item and item["author"]:
            fund_ids.add(item["author"])
    return fund_ids

def get_access_token(base_url: str, username: str, password: str) -> str:
    """
    Получает токен доступа через API аутентификации
    """
    auth_url = f"{base_url}/login/access-token"
    
    # Данные для запроса токена
    auth_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(auth_url, data=auth_data)
        if response.status_code != 200:
            raise Exception(f"Ошибка аутентификации: {response.status_code}, {response.text}")
        
        # Получаем токен из ответа
        token_data = response.json()
        return token_data["access_token"]
    except Exception as e:
        logger.error(f"Ошибка при получении токена: {str(e)}")
        sys.exit(1)

def get_headers(token: str) -> Dict[str, str]:
    """
    Создает заголовки для запросов с токеном авторизации
    """
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def get_or_create_fund(base_url: str, fund_id: str, headers: Dict[str, str]) -> Optional[str]:
    """
    Получает или создает фонд через API
    """
    # Название фонда будет ID фонда из output.json
    fund_name = fund_id
    
    # Проверяем существующие фонды
    funds_url = f"{base_url}/funds/"
    response = requests.get(funds_url, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Ошибка при получении списка фондов: {response.status_code}, {response.text}")
        return None
    
    funds = response.json()
    
    # Проверяем, существует ли уже фонд с таким именем
    for fund in funds:
        if fund.get("name") == fund_name:
            logger.info(f"Фонд с именем '{fund_name}' уже существует (ID: {fund['id']})")
            return fund["id"]
    
    # Создаем новый фонд
    fund_data = {
        "name": fund_name,
        "description": f"Фонд, импортированный из output.json (ID: {fund_id})"
    }
    
    response = requests.post(funds_url, headers=headers, json=fund_data)
    
    if response.status_code != 201:
        logger.error(f"Ошибка при создании фонда '{fund_name}': {response.status_code}, {response.text}")
        return None
    
    new_fund = response.json()
    logger.info(f"Создан новый фонд: {fund_name} (UUID: {new_fund['id']})")
    return new_fund["id"]

def main():
    # Параметры подключения к API
    API_BASE_URL = "http://localhost:8000/api/v1"
    
    logger.info(f"Используется базовый URL API: {API_BASE_URL}")
    
    # Запрашиваем учетные данные
    username = input("Введите имя пользователя (администратора): ")
    password = input("Введите пароль: ")
    
    logger.info("Начало импорта фондов из output.json")
    logger.info(f"Получение токена доступа для пользователя: {username}")
    
    # Получаем токен
    try:
        token = get_access_token(API_BASE_URL, username, password)
        logger.info("Токен доступа получен успешно")
        headers = get_headers(token)
    except Exception as e:
        logger.error(f"Не удалось получить токен доступа: {str(e)}")
        sys.exit(1)
    
    # Пути к файлу output.json (проверяем несколько вариантов)
    possible_paths = [
        "output.json",
        "../output.json",
        "../../output.json",
        "./output.json"
    ]
    
    found = False
    abs_path = None
    
    for output_path in possible_paths:
        abs_path = os.path.abspath(output_path)
        logger.info(f"Проверка пути: {abs_path}")
        if os.path.exists(abs_path):
            found = True
            break
    
    if not found:
        logger.error(f"Файл output.json не найден по проверенным путям")
        return
    
    logger.info(f"Чтение файла {abs_path}...")
    data = read_output_json(abs_path)
    logger.info(f"Файл успешно прочитан. Найдено {len(data)} записей.")
    
    # Извлекаем ID фондов
    fund_ids = extract_fund_ids(data)
    logger.info(f"Найдено {len(fund_ids)} уникальных ID фондов.")
    
    # Словарь для хранения соответствия между оригинальными ID и новыми UUID
    fund_mapping = {}
    
    # Создаем фонды через API
    count_created = 0
    count_existing = 0
    count_error = 0
    
    for fund_id in fund_ids:
        logger.info(f"Обработка фонда с ID: {fund_id}")
        # Добавим небольшую задержку, чтобы не перегрузить API
        time.sleep(0.1)
        
        new_uuid = get_or_create_fund(API_BASE_URL, fund_id, headers)
        if new_uuid:
            fund_mapping[fund_id] = new_uuid
            if "Создан новый фонд" in str(fund_mapping.get(fund_id, "")):
                count_created += 1
            else:
                count_existing += 1
        else:
            count_error += 1
    
    logger.info(f"\nИтоги импорта фондов:")
    logger.info(f"Всего обработано: {len(fund_ids)} фондов")
    logger.info(f"Создано новых: {count_created}")
    logger.info(f"Уже существующих: {count_existing}")
    logger.info(f"Ошибок: {count_error}")
    
    # Сохраняем маппинг в файл для дальнейшего использования
    mapping_file = "fund_mapping.json"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(fund_mapping, f, indent=2, ensure_ascii=False)
    logger.info(f"Соответствие ID фондов сохранено в файл {mapping_file}")
    logger.info("Импорт фондов завершен")

if __name__ == "__main__":
    main()
    # Чтобы PowerShell увидел весь вывод
    sys.stdout.flush()
    time.sleep(1) 