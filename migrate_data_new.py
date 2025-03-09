#!/usr/bin/env python3
import json
import requests
import uuid
import time
import re
import os
import sys
import argparse
from typing import Dict, List, Any, Optional, Tuple, Set

# Добавляем парсер аргументов командной строки
def parse_args():
    parser = argparse.ArgumentParser(description='Migrate data to the system')
    parser.add_argument('--clean', action='store_true', help='Only clean the database without importing data')
    parser.add_argument('--use-id-as-name', action='store_true', help='Use fund ID as fund name for unknown funds')
    return parser.parse_args()

# Конфигурация
BASE_URL = "http://localhost:8000/api/v1"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin"  # Пароль админа для доступа к API

# Маппинг ID авторов на названия фондов с правильными названиями
AUTHOR_TO_FUND_NAME = {
    "603801502528de31d1decf74": "Фонд покерной взаимопомощи",
    "603801562528de31d1decf75": "SV Backing",
    "603801592528de31d1decf76": "FS Team",
    "603801602528de31d1decf77": "Покерная Семья",
    "603801652528de31d1decf78": "BBTC",
    # Значения по умолчанию для неизвестных авторов
    "default": "Неизвестный фонд"
}

# Стандартные румы, которые должны быть в системе
STANDARD_ROOMS = [
    "PokerStars", "GGPokerOK", "PartyPoker", "888Poker", "Winamax", 
    "RedStar", "PokerDom", "WPN", "iPoker", "Chico", "PokerKing",
    "PokerMatch", "TigerGaming"
]

# Словарь для нормализации названий румов
ROOM_NORMALIZATION = {
    "ps": "PokerStars",
    "stars": "PokerStars",
    "pokerstars": "PokerStars",
    "pses": "PokerStars",
    "gg": "GGPokerOK",
    "ggpoker": "GGPokerOK",
    "ggpokerok": "GGPokerOK",
    "ggnetwork": "GGPokerOK",
    "partypoker": "PartyPoker",
    "party": "PartyPoker",
    "888": "888Poker",
    "888poker": "888Poker",
    "winamax": "Winamax",
    "wmx": "Winamax",
    "redstar": "RedStar",
    "red": "RedStar",
    "pokerdom": "PokerDom",
    "pd": "PokerDom",
    "wpn": "WPN",
    "acr": "WPN",
    "americascardroom": "WPN",
    "ipoker": "iPoker",
    "chico": "Chico",
    "pokerking": "PokerKing",
    "pokermatch": "PokerMatch",
    "pokerbets": "PokerMatch",
    "tiger": "TigerGaming",
    "tigergaming": "TigerGaming",
    "pokerok": "PokerOK"
}

# Уникальные румы из данных для создания базы румов
ROOMS_SET = set()

# Преобразование имени
def parse_full_name(full_name: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Разбирает полное имя на отдельные компоненты.
    Возвращает (имя, фамилия, отчество) или только имя если разбор не удается.
    """
    parts = full_name.strip().split()
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    elif len(parts) == 2:
        return parts[0], parts[1], None
    else:
        return full_name, None, None

# Преобразование суммы
def parse_amount(amount_str: str) -> float:
    """
    Преобразует строку с суммой в числовое значение.
    Обрабатывает форматы с запятой и пробелами.
    """
    if not amount_str:
        return 0.0
        
    try:
        # Удаляем символы валюты: $, €, руб и т.д.
        clean_amount = re.sub(r'[$€₽руб\s]', '', amount_str)
        # Заменяем запятую на точку и удаляем пробелы
        clean_amount = clean_amount.replace(",", ".").replace(" ", "")
        return float(clean_amount)
    except (ValueError, TypeError):
        return 0.0

# Преобразование адреса
def parse_location(location_str: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Разбирает строку адреса на составляющие.
    Возвращает (страна, город, адрес).
    """
    if not location_str:
        return None, None, None
    
    # Попытка извлечь страну
    country_match = re.search(r'^([^,]+)', location_str)
    country = country_match.group(1).strip() if country_match else None
    
    # Попытка извлечь город
    city_match = re.search(r'г\.\s*([^,]+)', location_str)
    city = city_match.group(1).strip() if city_match else None
    
    # Оставшаяся часть как адрес
    address = location_str
    
    return country, city, address

# Нормализация названия рума
def normalize_room_name(room_name: str) -> str:
    """
    Нормализует название рума, приводя его к стандартному виду.
    """
    if not room_name:
        return "Другой"
    
    # Очищаем строку и приводим к нижнему регистру
    cleaned_name = room_name.strip().lower()
    
    # Проверяем наличие в словаре нормализации
    if cleaned_name in ROOM_NORMALIZATION:
        return ROOM_NORMALIZATION[cleaned_name]
    
    # Проверяем частичное совпадение
    for standard, normalized in ROOM_NORMALIZATION.items():
        if standard in cleaned_name or cleaned_name in standard:
            return normalized
    
    # Возвращаем оригинальное имя, если не найдено совпадений
    return room_name

# Функции для работы с API
def get_token() -> str:
    """Получает токен доступа к API"""
    response = requests.post(
        f"{BASE_URL}/login/access-token",
        data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    if response.status_code != 200:
        raise Exception(f"Не удалось получить токен. Статус: {response.status_code}, Ответ: {response.text}")
    
    return response.json()["access_token"]

def get_headers(token: str) -> Dict[str, str]:
    """Возвращает заголовки для запросов к API"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def clear_database(token: str) -> None:
    """Очищает таблицы в базе данных"""
    headers = get_headers(token)
    
    # Получаем все кейсы
    print("Удаляем все кейсы...")
    response = requests.get(f"{BASE_URL}/cases/", headers=headers)
    if response.status_code == 200:
        cases = response.json()
        print(f"Найдено {len(cases)} кейсов для удаления")
        for case in cases:
            case_id = case["id"]
            # Удаляем каждый кейс
            delete_response = requests.delete(f"{BASE_URL}/cases/{case_id}", headers=headers)
            if delete_response.status_code != 204:
                print(f"Ошибка при удалении кейса {case_id}: {delete_response.status_code}")
            else:
                print(f"Кейс {case_id} удален.")
    
    # Получаем всех игроков
    print("Удаляем всех игроков...")
    response = requests.get(f"{BASE_URL}/players/", headers=headers)
    if response.status_code == 200:
        players = response.json()
        print(f"Найдено {len(players)} игроков для удаления")
        for player in players:
            player_id = player["id"]
            # Удаляем каждого игрока
            delete_response = requests.delete(f"{BASE_URL}/players/{player_id}", headers=headers)
            if delete_response.status_code != 204:
                print(f"Ошибка при удалении игрока {player_id}: {delete_response.status_code}")
            else:
                print(f"Игрок {player_id} удален.")
    
    # Очищаем фонды
    print("Удаляем все фонды (кроме Admin Fund)...")
    response = requests.get(f"{BASE_URL}/funds/", headers=headers)
    if response.status_code == 200:
        funds = response.json()
        print(f"Найдено {len(funds)} фондов для проверки")
        for fund in funds:
            # Пропускаем системный фонд администратора
            if fund["name"] == "Admin Fund":
                print(f"Фонд Admin Fund ({fund['id']}) сохранен.")
                continue
                
            fund_id = fund["id"]
            # Удаляем каждый фонд
            delete_response = requests.delete(f"{BASE_URL}/funds/{fund_id}", headers=headers)
            if delete_response.status_code != 204:
                print(f"Ошибка при удалении фонда {fund_id}: {delete_response.status_code}")
            else:
                print(f"Фонд {fund_id} удален.")
    
    print("База данных очищена.")

def get_or_create_fund(token: str, author_id: str) -> str:
    """
    Получает или создает фонд с указанным идентификатором автора.
    Возвращает ID фонда.
    """
    headers = get_headers(token)
    
    # Определяем название фонда
    fund_name = AUTHOR_TO_FUND_NAME.get(author_id, AUTHOR_TO_FUND_NAME["default"])
    
    # Проверяем существующие фонды по названию
    response = requests.get(f"{BASE_URL}/funds/", headers=headers)
    if response.status_code == 200:
        funds = response.json()
        for fund in funds:
            if fund["name"] == fund_name:
                print(f"Найден существующий фонд: {fund_name} ({fund['id']})")
                return fund["id"]
    
    # Создаем новый фонд
    fund_data = {
        "name": fund_name,
        "description": f"Покерный фонд: {fund_name}"
    }
    response = requests.post(
        f"{BASE_URL}/funds/",
        headers=headers,
        json=fund_data
    )
    
    if response.status_code != 201:
        raise Exception(f"Не удалось создать фонд. Статус: {response.status_code}, Ответ: {response.text}")
    
    fund_id = response.json()["id"]
    print(f"Создан новый фонд: {fund_name} ({fund_id})")
    return fund_id

def get_or_create_room(token: str, room_name: str) -> str:
    """
    Получает или создает рум с указанным именем.
    Возвращает ID рума.
    """
    if not room_name:
        room_name = "Другой"
    
    # Нормализуем название рума
    normalized_room_name = normalize_room_name(room_name)
    
    headers = get_headers(token)
    
    # Пытаемся найти рум по имени
    try:
        room_name_encoded = requests.utils.quote(normalized_room_name)
        response = requests.get(f"{BASE_URL}/rooms/by-name/{room_name_encoded}", headers=headers)
        
        if response.status_code == 200:
            room_data = response.json()
            print(f"Найден существующий рум: {normalized_room_name} ({room_data['id']})")
            return room_data["id"]
    except Exception as e:
        print(f"Ошибка при поиске рума {normalized_room_name}: {str(e)}")
    
    # Если не нашли, создаем новый рум
    try:
        room_data = {
            "name": normalized_room_name,
            "description": f"Покер-рум {normalized_room_name}",
            "is_active": True
        }
        
        response = requests.post(f"{BASE_URL}/rooms/", headers=headers, json=room_data)
        
        if response.status_code in [200, 201]:
            room_id = response.json()["id"]
            print(f"Создан новый рум: {normalized_room_name} ({room_id})")
            return room_id
        else:
            print(f"Ошибка при создании рума {normalized_room_name}: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Ошибка при создании рума {normalized_room_name}: {str(e)}")
        return None

def create_standard_rooms(token: str) -> Dict[str, str]:
    """
    Создает стандартные румы в системе.
    Возвращает словарь {название_рума: id_рума}
    """
    print("Создаем стандартные покерные румы...")
    room_ids = {}
    
    for room_name in STANDARD_ROOMS:
        room_id = get_or_create_room(token, room_name)
        if room_id:
            room_ids[room_name] = room_id
    
    print(f"Создано {len(room_ids)} стандартных румов")
    return room_ids

def get_or_create_player(token: str, player_data: Dict[str, Any], fund_id: str) -> str:
    """
    Получает или создает игрока с указанными данными.
    Возвращает ID игрока.
    """
    headers = get_headers(token)
    
    # Извлекаем ФИО
    full_name = ""
    if player_data.get("FIO") and len(player_data["FIO"]) > 0:
        full_name = player_data["FIO"][0].get("firstname", "")
    
    # Если имя не указано, пропускаем
    if not full_name:
        raise ValueError("Не указано имя игрока")
    
    first_name, last_name, middle_name = parse_full_name(full_name)
    
    # Вместо использования эндпоинта search, получим всех игроков и проверим по имени
    try:
        # Получаем список игроков по фонду (используем новый эндпоинт)
        response = requests.get(f"{BASE_URL}/players/by-fund/{fund_id}", headers=headers)
        if response.status_code == 200:
            fund_players = response.json()
            
            # Создаем строку для поиска
            name_parts = [part for part in [first_name, middle_name, last_name] if part]
            search_query = " ".join(name_parts).lower()
            
            # Проверяем совпадение имени
            for player in fund_players:
                if player["full_name"] and search_query in player["full_name"].lower():
                    print(f"Найден существующий игрок в фонде: {player['full_name']} ({player['id']})")
                    return player["id"]
    except Exception as e:
        print(f"Ошибка при поиске игрока в фонде: {str(e)}")
    
    # Подготавливаем контакты
    contacts = []
    
    # Телефоны
    for phone in player_data.get("phone", []):
        contacts.append({
            "type": "phone",
            "value": phone,
            "description": "Импортировано из старой системы"
        })
    
    # Email
    for email in player_data.get("mail", []):
        contacts.append({
            "type": "email",
            "value": email,
            "description": "Импортировано из старой системы"
        })
    
    # Skype
    for skype in player_data.get("skype", []):
        contacts.append({
            "type": "skype",
            "value": skype,
            "description": "Импортировано из старой системы"
        })
    
    # Местоположение
    locations = []
    if player_data.get("location") and len(player_data["location"]) > 0:
        location_str = player_data["location"][0].get("country", "")
        country, city, address = parse_location(location_str)
        
        if country or city or address:
            locations.append({
                "country": country or "",
                "city": city or "",
                "address": address or ""
            })
    
    # Никнеймы
    nicknames = []
    for nick in player_data.get("nickname", []):
        nick_value = nick.get("value", "")
        room_name = nick.get("room", "")
        discipline = nick.get("discipline", "")
        
        if nick_value:
            # Получаем или создаем рум
            if room_name:
                room_id = get_or_create_room(token, room_name)
            else:
                room_id = None
            
            nickname_data = {
                "nickname": nick_value,
                "room": normalize_room_name(room_name) if room_name else "Другой",
                "discipline": discipline or ""
            }
            nicknames.append(nickname_data)
    
    # Платежные методы
    payment_methods = []
    for payment_type in ["skrill", "neteller", "webmoney", "ecopayz"]:
        for payment in player_data.get(payment_type, []):
            if isinstance(payment, str) and payment:
                payment_methods.append({
                    "type": payment_type,
                    "value": payment,
                    "description": "Импортировано из старой системы"
                })
    
    # Социальные сети
    social_media = []
    for social_type in ["vk", "facebook", "instagram", "gipsyteam", "pokerstrategy", "google", "blog", "forum"]:
        for social in player_data.get(social_type, []):
            if isinstance(social, str) and social:
                social_media.append({
                    "type": social_type,
                    "value": social,
                    "description": "Импортировано из старой системы"
                })
    
    # Создаем нового игрока
    player_data = {
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "full_name": full_name,
        "contacts": contacts,
        "locations": locations,
        "nicknames": nicknames,
        "payment_methods": payment_methods,
        "social_media": social_media,
        "additional_info": {
            "imported": True, 
            "import_date": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "created_by_fund_id": fund_id  # Важно! Указываем фонд при создании игрока
    }
    
    response = requests.post(
        f"{BASE_URL}/players/",
        headers=headers,
        json=player_data
    )
    
    if response.status_code != 201:
        print(f"Ошибка создания игрока {full_name}: {response.status_code}, {response.text}")
        raise Exception(f"Не удалось создать игрока. Статус: {response.status_code}, Ответ: {response.text}")
    
    player_id = response.json()["id"]
    print(f"Создан новый игрок: {full_name} ({player_id})")
    return player_id

def create_case(
    token: str, *, case_data: Dict[str, Any], player_id: str, fund_id: str
) -> str:
    """
    Создает новый кейс арбитража.
    Возвращает ID созданного кейса.
    """
    headers = get_headers(token)
    
    description = case_data.get("descr", "")
    
    # Преобразуем сумму
    amount_str = case_data.get("amount", "0")
    amount = parse_amount(amount_str)
    if amount < 0:
        amount = 0.0  # Нельзя создавать кейсы с отрицательной суммой
    
    # Определим валюту из строки суммы
    currency = "USD"  # По умолчанию USD
    if "€" in str(amount_str) or "euro" in str(amount_str).lower():
        currency = "EUR"
    elif "₽" in str(amount_str) or "руб" in str(amount_str).lower():
        currency = "RUB"
    
    arbitrage_type = case_data.get("arbitrage", "Арбитраж")
    if not arbitrage_type:
        arbitrage_type = "Арбитраж"
    
    # Формируем заголовок кейса
    title = f"Арбитраж: {description[:30]}{'...' if len(description) > 30 else ''}"
    if not description:
        title = f"Арбитраж: {arbitrage_type}"
    
    case_data = {
        "title": title,
        "description": description,
        "player_id": str(player_id),
        "status": "open",  # Обязательное поле, теперь должно быть явно указано
        "arbitrage_type": arbitrage_type,
        "arbitrage_amount": amount,
        "arbitrage_currency": currency,
        "created_by_fund_id": str(fund_id)  # Явно указываем ID фонда
    }
    
    print(f"Отправляем данные для создания кейса: {case_data}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/cases/",
            headers=headers,
            json=case_data
        )
        
        if response.status_code != 201:
            print(f"Ошибка при создании кейса. Статус: {response.status_code}, Ответ: {response.text}")
            raise Exception(f"Не удалось создать кейс. Статус: {response.status_code}, Ответ: {response.text}")
        
        case_id = response.json()["id"]
        print(f"Создан новый кейс: {case_data['title']} ({case_id})")
        return case_id
    except Exception as e:
        print(f"Ошибка при создании кейса: {str(e)}")
        raise

def main():
    # Парсим аргументы командной строки
    args = parse_args()
    
    try:
        # Получаем токен для доступа к API
        token = get_token()
        print("Токен получен успешно.")
        
        # Очищаем базу данных
        clear_database(token)
        print("База данных очищена успешно.")
        
        # Если указан только флаг очистки, завершаем работу
        if args.clean:
            print("Флаг --clean указан. Работа завершена после очистки базы данных.")
            return
        
        # Если указан флаг использования ID как имени, обновляем словарь маппинга
        if args.use_id_as_name:
            global AUTHOR_TO_FUND_NAME
            AUTHOR_TO_FUND_NAME = {key: key for key in AUTHOR_TO_FUND_NAME.keys()}
            AUTHOR_TO_FUND_NAME["default"] = "default"
            print("Используем ID автора в качестве имени фонда для неизвестных фондов.")
        
        # Создаем стандартные румы
        room_ids = create_standard_rooms(token)
        
        # Проверяем наличие файла
        if not os.path.exists("output.json"):
            print("Ошибка: Файл output.json не найден!")
            return
        
        # Загружаем данные из файла
        with open("output.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print(f"Загружено {len(data)} записей из файла для анализа.")
        
        # Словарь для маппинга author_id -> fund_id
        author_to_fund = {}
        
        # Счетчики для статистики
        stats = {
            "total_records": len(data),
            "players_created": 0,
            "cases_created": 0,
            "errors": 0
        }
        
        # Обрабатываем каждую запись
        for record_idx, record in enumerate(data):
            try:
                # Проверяем наличие автора
                author_id = record.get("author")
                if not author_id:
                    print("Пропуск записи без автора.")
                    continue
                
                # Получаем или создаем фонд
                if author_id in author_to_fund:
                    fund_id = author_to_fund[author_id]
                else:
                    fund_id = get_or_create_fund(token, author_id)
                    author_to_fund[author_id] = fund_id
                
                # Получаем или создаем игрока
                try:
                    player_id = get_or_create_player(token, record, fund_id)
                    stats["players_created"] += 1
                except Exception as e:
                    print(f"Ошибка при создании игрока: {str(e)}")
                    stats["errors"] += 1
                    continue
                
                # Создаем кейсы арбитража
                case_data = record.get("case", [])
                print(f"Запись {record_idx+1}/{len(data)}: Найдено {len(case_data)} кейсов для игрока {player_id}")
                
                for case_idx, case_item in enumerate(case_data):
                    try:
                        case_id = create_case(
                            token, 
                            case_data=case_item, 
                            player_id=player_id,
                            fund_id=fund_id
                        )
                        stats["cases_created"] += 1
                    except Exception as e:
                        print(f"Ошибка при создании кейса {case_idx+1} для игрока {player_id}: {str(e)}")
                        stats["errors"] += 1
                
                # Отчет о прогрессе каждые 50 записей
                if (record_idx + 1) % 50 == 0:
                    print(f"Обработано {record_idx+1}/{len(data)} записей. "
                          f"Создано {stats['players_created']} игроков, {stats['cases_created']} кейсов. "
                          f"Ошибок: {stats['errors']}")
            
            except Exception as e:
                print(f"Ошибка при обработке записи {record_idx+1}: {str(e)}")
                stats["errors"] += 1
                continue
        
        # Итоговая статистика
        print("\n=== Итоги миграции данных ===")
        print(f"Всего обработано записей: {stats['total_records']}")
        print(f"Создано игроков: {stats['players_created']}")
        print(f"Создано кейсов: {stats['cases_created']}")
        print(f"Ошибок: {stats['errors']}")
        print("============================")
        
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")

if __name__ == "__main__":
    main() 