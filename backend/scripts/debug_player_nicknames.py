#!/usr/bin/env python
import json
import logging
import sys
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug_player_nicknames.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Константы
API_BASE_URL = "http://localhost:8000/api/v1"
TOKEN_URL = f"{API_BASE_URL}/auth/login"

def get_access_token() -> str:
    """Получение токена доступа"""
    username = os.environ.get("API_USERNAME", "admin@example.com")
    password = os.environ.get("API_PASSWORD", "admin")
    
    data = {"username": username, "password": password}
    
    try:
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            logger.error("Токен доступа не найден в ответе API")
            sys.exit(1)
            
        logger.info("Токен доступа успешно получен")
        return access_token
    except requests.RequestException as e:
        logger.error(f"Ошибка при получении токена доступа: {e}")
        sys.exit(1)

def get_player_details(token: str, player_id: str) -> Dict[str, Any]:
    """Получить детальную информацию о игроке по ID"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{API_BASE_URL}/players/{player_id}"
    
    try:
        logger.info(f"Получение информации о игроке с ID {player_id}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        player_data = response.json()
        logger.info(f"Данные игрока успешно получены: {player_data.get('full_name', 'Имя не указано')}")
        
        # Проверяем наличие и структуру никнеймов
        if "nicknames" in player_data:
            nicknames = player_data["nicknames"]
            logger.info(f"Никнеймы в ответе API: {len(nicknames)} шт.")
            
            # Вывести каждый никнейм
            for i, nickname in enumerate(nicknames):
                logger.info(f"Никнейм #{i+1}: {nickname}")
        else:
            logger.warning("Поле 'nicknames' отсутствует в ответе API")
        
        return player_data
    except requests.RequestException as e:
        logger.error(f"Ошибка при получении информации о игроке: {e}")
        return {}

def get_players_list(token: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Получить список игроков"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{API_BASE_URL}/players?limit={limit}"
    
    try:
        logger.info(f"Получение списка игроков (limit={limit})")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        players_data = response.json()
        if isinstance(players_data, list):
            player_count = len(players_data)
            logger.info(f"Получено {player_count} игроков")
            
            # Статистика по никнеймам
            players_with_nicknames = sum(1 for p in players_data if p.get("nicknames") and len(p.get("nicknames", [])) > 0)
            logger.info(f"Игроков с никнеймами: {players_with_nicknames} из {player_count} ({players_with_nicknames/player_count*100:.2f}%)")
            
            return players_data
        else:
            logger.error(f"Неожиданный формат ответа API: {players_data}")
            return []
    except requests.RequestException as e:
        logger.error(f"Ошибка при получении списка игроков: {e}")
        return []

def check_frontend_player_details() -> None:
    """Инструкция, как проверить детали игрока на фронтенде"""
    logger.info("=== ИНСТРУКЦИЯ ДЛЯ ПРОВЕРКИ НИКНЕЙМОВ НА ФРОНТЕНДЕ ===")
    logger.info("1. Откройте браузер и войдите в приложение")
    logger.info("2. Откройте инструменты разработчика (F12 или Ctrl+Shift+I)")
    logger.info("3. Перейдите на вкладку 'Network'")
    logger.info("4. Очистите журнал сетевых запросов")
    logger.info("5. Откройте страницу детального просмотра игрока")
    logger.info("6. Найдите запрос к API players/{id} в журнале сетевых запросов")
    logger.info("7. Проверьте, содержит ли ответ поле 'nicknames' и его значения")
    logger.info("8. Сравните с тем, что отображается на странице")
    logger.info("=== КОНЕЦ ИНСТРУКЦИИ ===")

def main():
    logger.info("=== НАЧАЛО ДИАГНОСТИКИ НИКНЕЙМОВ ИГРОКОВ ===")
    
    # Получаем токен доступа
    access_token = get_access_token()
    
    # Получаем список игроков
    players = get_players_list(access_token)
    
    # Проверяем детали для первых 3 игроков с никнеймами и без них
    players_with_nicknames = [p for p in players if p.get("nicknames") and len(p.get("nicknames", [])) > 0]
    players_without_nicknames = [p for p in players if not p.get("nicknames") or len(p.get("nicknames", [])) == 0]
    
    logger.info("\n=== ПРИМЕРЫ ИГРОКОВ С НИКНЕЙМАМИ ===")
    for i, player in enumerate(players_with_nicknames[:3]):
        logger.info(f"\nПример #{i+1}:")
        logger.info(f"ID: {player.get('id')}")
        logger.info(f"Имя: {player.get('full_name')}")
        logger.info(f"Количество никнеймов: {len(player.get('nicknames', []))}")
        
        # Получаем полные детали игрока
        player_details = get_player_details(access_token, player.get('id'))
    
    logger.info("\n=== ПРИМЕРЫ ИГРОКОВ БЕЗ НИКНЕЙМОВ ===")
    for i, player in enumerate(players_without_nicknames[:3]):
        logger.info(f"\nПример #{i+1}:")
        logger.info(f"ID: {player.get('id')}")
        logger.info(f"Имя: {player.get('full_name')}")
        
        # Получаем полные детали игрока
        player_details = get_player_details(access_token, player.get('id'))
    
    # Вывод инструкции для проверки фронтенда
    check_frontend_player_details()
    
    logger.info("\n=== ДИАГНОСТИКА ЗАВЕРШЕНА ===")
    logger.info("Проверьте файл debug_player_nicknames.log для получения полной информации")

if __name__ == "__main__":
    main() 