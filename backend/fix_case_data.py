#!/usr/bin/env python3
import requests
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Конфигурация
BASE_URL = "http://localhost:8000/api/v1"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin"  # Пароль админа для доступа к API

def get_token() -> str:
    """Получает токен доступа к API"""
    response = requests.post(
        f"{BASE_URL}/login/access-token",
        data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    if response.status_code != 200:
        raise Exception(f"Не удалось получить токен. Статус: {response.status_code}, Ответ: {response.text}")

    return response.json()["access_token"]

def get_headers(token: str) -> dict:
    """Возвращает заголовки для запросов к API"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def update_fund_name(token: str) -> None:
    """
    Обновляет фонд с именем 'default' на 'Непривязанные кейсы'
    """
    headers = get_headers(token)
    
    try:
        # Получаем список всех фондов
        response = requests.get(f"{BASE_URL}/funds/", headers=headers)
        if response.status_code != 200:
            logging.error(f"Не удалось получить список фондов: {response.status_code}, {response.text}")
            return
        
        funds = response.json()
        default_fund = None
        
        # Ищем фонд с именем 'default'
        for fund in funds:
            if fund["name"] == "default":
                default_fund = fund
                break
        
        if default_fund is None:
            logging.info("Фонд с именем 'default' не найден")
            return
        
        # Обновляем название и описание фонда
        fund_data = {
            "name": "Непривязанные кейсы",
            "description": "Фонд для кейсов, созданных во время миграции без привязки к конкретному фонду"
        }
        
        response = requests.put(
            f"{BASE_URL}/funds/{default_fund['id']}",
            headers=headers,
            json=fund_data
        )
        
        if response.status_code == 200:
            logging.info(f"Фонд успешно обновлен: {default_fund['id']}")
        else:
            logging.error(f"Ошибка при обновлении фонда: {response.status_code}, {response.text}")
    
    except Exception as e:
        logging.error(f"Произошла ошибка при обновлении фонда: {str(e)}")

def fix_case_fields(token: str) -> None:
    """
    Обновляет кейсы с пустыми полями arbitrage_amount и arbitrage_currency
    """
    headers = get_headers(token)
    
    try:
        # Получаем все кейсы
        response = requests.get(f"{BASE_URL}/cases/", headers=headers)
        if response.status_code != 200:
            logging.error(f"Не удалось получить список кейсов: {response.status_code}, {response.text}")
            return
        
        cases = response.json()
        cases_updated = 0
        
        for case in cases:
            need_update = False
            case_data = {}
            
            # Проверяем наличие суммы арбитража
            if case.get("arbitrage_amount") is None or case.get("arbitrage_amount") == "":
                case_data["arbitrage_amount"] = 0.0
                need_update = True
            
            # Проверяем наличие валюты арбитража
            if not case.get("arbitrage_currency"):
                case_data["arbitrage_currency"] = "USD"
                need_update = True
            
            # Проверяем наличие типа арбитража
            if not case.get("arbitrage_type"):
                case_data["arbitrage_type"] = "Арбитраж"
                need_update = True
                
            # Проверяем наличие статуса
            if not case.get("status"):
                case_data["status"] = "open"
                need_update = True
            
            # Если нужно обновление, отправляем запрос
            if need_update:
                update_response = requests.patch(
                    f"{BASE_URL}/cases/{case['id']}",
                    headers=headers,
                    json=case_data
                )
                
                if update_response.status_code == 200:
                    cases_updated += 1
                    logging.info(f"Кейс {case['id']} обновлен: {case_data}")
                else:
                    logging.error(f"Ошибка при обновлении кейса {case['id']}: {update_response.status_code}, {update_response.text}")
        
        logging.info(f"Всего обновлено кейсов: {cases_updated}")
    
    except Exception as e:
        logging.error(f"Произошла ошибка при обновлении кейсов: {str(e)}")

def fix_player_fields(token: str) -> None:
    """
    Обновляет игроков с пустыми полями full_name и другими
    """
    headers = get_headers(token)
    
    try:
        # Получаем всех игроков
        response = requests.get(f"{BASE_URL}/players/", headers=headers)
        if response.status_code != 200:
            logging.error(f"Не удалось получить список игроков: {response.status_code}, {response.text}")
            return
        
        players = response.json()
        players_updated = 0
        
        for player in players:
            need_update = False
            player_data = {}
            
            # Если full_name пустой, но есть first_name или last_name
            if not player.get("full_name") and (player.get("first_name") or player.get("last_name")):
                full_name_parts = []
                if player.get("first_name"):
                    full_name_parts.append(player["first_name"])
                if player.get("last_name"):
                    full_name_parts.append(player["last_name"])
                
                player_data["full_name"] = " ".join(full_name_parts)
                need_update = True
            
            # Если first_name пустой, но есть full_name
            if not player.get("first_name") and player.get("full_name"):
                player_data["first_name"] = player["full_name"].split()[0] if player["full_name"].split() else "Неизвестно"
                need_update = True
            
            # Если нужно обновление, отправляем запрос
            if need_update:
                update_response = requests.patch(
                    f"{BASE_URL}/players/{player['id']}",
                    headers=headers,
                    json=player_data
                )
                
                if update_response.status_code == 200:
                    players_updated += 1
                    logging.info(f"Игрок {player['id']} обновлен: {player_data}")
                else:
                    logging.error(f"Ошибка при обновлении игрока {player['id']}: {update_response.status_code}, {update_response.text}")
        
        logging.info(f"Всего обновлено игроков: {players_updated}")
    
    except Exception as e:
        logging.error(f"Произошла ошибка при обновлении игроков: {str(e)}")

def get_data_stats(token: str) -> None:
    """
    Выводит статистику по данным в базе
    """
    headers = get_headers(token)
    
    try:
        # Получаем статистику по кейсам
        response = requests.get(f"{BASE_URL}/cases/", headers=headers)
        if response.status_code != 200:
            logging.error(f"Не удалось получить список кейсов: {response.status_code}, {response.text}")
            return
        
        cases = response.json()
        total_cases = len(cases)
        
        # Считаем кейсы без связанных игроков
        cases_without_player = sum(1 for case in cases if not case.get("player_id"))
        
        # Считаем кейсы без суммы арбитража
        cases_without_amount = sum(1 for case in cases if case.get("arbitrage_amount") is None or case.get("arbitrage_amount") == "")
        
        # Считаем кейсы без валюты арбитража
        cases_without_currency = sum(1 for case in cases if not case.get("arbitrage_currency"))
        
        # Получаем статистику по игрокам
        response = requests.get(f"{BASE_URL}/players/", headers=headers)
        if response.status_code != 200:
            logging.error(f"Не удалось получить список игроков: {response.status_code}, {response.text}")
            return
        
        players = response.json()
        total_players = len(players)
        
        # Считаем игроков без full_name
        players_without_fullname = sum(1 for player in players if not player.get("full_name"))
        
        logging.info("=== Статистика данных ===")
        logging.info(f"Всего кейсов: {total_cases}")
        logging.info(f"Кейсы без игрока: {cases_without_player}")
        logging.info(f"Кейсы без суммы арбитража: {cases_without_amount}")
        logging.info(f"Кейсы без валюты арбитража: {cases_without_currency}")
        logging.info(f"Всего игроков: {total_players}")
        logging.info(f"Игроки без полного имени: {players_without_fullname}")
        logging.info("========================")
    
    except Exception as e:
        logging.error(f"Произошла ошибка при получении статистики: {str(e)}")

def main():
    try:
        logging.info("Начинаем исправление данных...")
        
        # Получаем токен для доступа к API
        token = get_token()
        logging.info("Успешное подключение к API")
        
        # Обновляем название фонда
        update_fund_name(token)
        
        # Выводим начальную статистику
        logging.info("Статистика до исправлений:")
        get_data_stats(token)
        
        # Исправляем поля кейсов
        fix_case_fields(token)
        
        # Исправляем поля игроков
        fix_player_fields(token)
        
        # Выводим конечную статистику
        logging.info("Статистика после исправлений:")
        get_data_stats(token)
        
        logging.info("Исправление данных завершено успешно")
    
    except Exception as e:
        logging.error(f"Критическая ошибка: {str(e)}")

if __name__ == "__main__":
    main() 