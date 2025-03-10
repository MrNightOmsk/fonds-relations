#!/usr/bin/env python
import requests
import json
import logging
import sys
import uuid

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_api.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

API_BASE_URL = "http://localhost:8000/api/v1"

def get_access_token(username: str, password: str) -> str:
    """
    Получает токен доступа через API аутентификации
    """
    auth_url = f"{API_BASE_URL}/login/access-token"
    
    # Данные для запроса токена
    auth_data = {
        "username": username,
        "password": password
    }
    
    try:
        logger.info(f"Запрос токена для пользователя {username}")
        response = requests.post(auth_url, data=auth_data)
        if response.status_code != 200:
            raise Exception(f"Ошибка аутентификации: {response.status_code}, {response.text}")
        
        # Получаем токен из ответа
        token_data = response.json()
        logger.info("Токен успешно получен")
        return token_data["access_token"]
    except Exception as e:
        logger.error(f"Ошибка при получении токена: {str(e)}")
        sys.exit(1)

def get_headers(token: str) -> dict:
    """
    Создает заголовки для запросов с токеном авторизации
    """
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def create_test_player(headers: dict, fund_id: str) -> str:
    """
    Создает тестового игрока с никнеймами
    """
    # Тестовые данные для создания игрока
    player_data = {
        "first_name": "Тест",
        "last_name": "Никнейм",
        "middle_name": "Тестович",
        "full_name": "Тест Никнейм Тестович",
        "created_by_fund_id": fund_id,
        "contact_info": {},
        "additional_info": {"test": True},
        "nicknames": [
            {
                "nickname": "TestNick1",
                "room": "PokerStars",
                "discipline": "MTT"
            },
            {
                "nickname": "TestNick2",
                "room": "PokerDom",
                "discipline": "Cash"
            }
        ],
        "contacts": [
            {
                "type": "email",
                "value": "test@example.com",
                "description": "Test email"
            }
        ]
    }
    
    players_url = f"{API_BASE_URL}/players/"
    
    logger.info("Отправка данных игрока:")
    logger.info(json.dumps(player_data, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(players_url, headers=headers, json=player_data)
        
        if response.status_code == 201:
            player = response.json()
            logger.info("Игрок успешно создан:")
            logger.info(json.dumps(player, indent=2, ensure_ascii=False))
            
            if "nicknames" in player and player["nicknames"]:
                logger.info(f"Никнеймы в ответе: {player['nicknames']}")
            else:
                logger.warning("Никнеймы отсутствуют в ответе API")
                
            return player["id"]
        else:
            logger.error(f"Ошибка при создании игрока: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logger.error(f"Исключение при создании игрока: {str(e)}")
        return None

def get_player(headers: dict, player_id: str) -> dict:
    """
    Получает данные игрока по ID
    """
    players_url = f"{API_BASE_URL}/players/{player_id}"
    
    try:
        logger.info(f"Запрос данных игрока с ID {player_id}")
        response = requests.get(players_url, headers=headers)
        
        if response.status_code == 200:
            player = response.json()
            logger.info("Данные игрока получены:")
            logger.info(json.dumps(player, indent=2, ensure_ascii=False))
            
            if "nicknames" in player and player["nicknames"]:
                logger.info(f"Никнеймы: {player['nicknames']}")
            else:
                logger.warning("Никнеймы отсутствуют в ответе API")
                
            return player
        else:
            logger.error(f"Ошибка при получении игрока: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logger.error(f"Исключение при получении игрока: {str(e)}")
        return None

def get_funds(headers: dict) -> list:
    """
    Получает список фондов
    """
    funds_url = f"{API_BASE_URL}/funds/"
    
    try:
        logger.info("Запрос списка фондов")
        response = requests.get(funds_url, headers=headers)
        
        if response.status_code == 200:
            funds = response.json()
            logger.info(f"Получено {len(funds)} фондов")
            return funds
        else:
            logger.error(f"Ошибка при получении фондов: {response.status_code}, {response.text}")
            return []
    except Exception as e:
        logger.error(f"Исключение при получении фондов: {str(e)}")
        return []

def main():
    # Запрашиваем учетные данные
    username = input("Введите имя пользователя (администратора): ")
    password = input("Введите пароль: ")
    
    # Получаем токен
    token = get_access_token(username, password)
    headers = get_headers(token)
    
    # Получаем список фондов
    funds = get_funds(headers)
    if not funds:
        logger.error("Не удалось получить список фондов")
        return
    
    # Используем первый фонд из списка
    fund_id = funds[0]["id"]
    logger.info(f"Используем фонд с ID: {fund_id}")
    
    # Создаем тестового игрока
    player_id = create_test_player(headers, fund_id)
    if not player_id:
        logger.error("Не удалось создать тестового игрока")
        return
    
    # Получаем данные созданного игрока
    player = get_player(headers, player_id)
    if not player:
        logger.error("Не удалось получить данные тестового игрока")
        return
    
    # Проверяем наличие никнеймов
    if "nicknames" not in player or not player["nicknames"]:
        logger.warning("Тестовый игрок не содержит никнеймов в ответе API, хотя они были отправлены при создании")
    else:
        logger.info(f"Тестовый игрок содержит {len(player['nicknames'])} никнеймов")
        
    logger.info("Тест завершен")

if __name__ == "__main__":
    main() 