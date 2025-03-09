#!/usr/bin/env python3
import json
import requests
import uuid
import time
import re
import os
from typing import Dict, List, Any, Optional, Tuple, Set

# Конфигурация
BASE_URL = "http://localhost:8000/api/v1"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin"  # Пароль админа для доступа к API

# Маппинг ID авторов на названия фондов
AUTHOR_TO_FUND_NAME = {
    # Здесь нужно добавить реальные названия фондов
    # Пример: "603801502528de31d1decf74": "Funfarm",
    "603801502528de31d1decf74": "Pokerfarm",
    "603801562528de31d1decf75": "SV Backing",
    "603801592528de31d1decf76": "FS Team",
    "603801602528de31d1decf77": "Pokerfamily",
    "603801652528de31d1decf78": "BBTC",
    # Для остальных ID используем префикс "Fund_"
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
    response = requests.get(f"{BASE_URL}/cases/", headers=headers)
    if response.status_code == 200:
        cases = response.json()
        for case in cases:
            case_id = case["id"]
            # Удаляем каждый кейс
            delete_response = requests.delete(f"{BASE_URL}/cases/{case_id}", headers=headers)
            if delete_response.status_code != 204:
                print(f"Ошибка при удалении кейса {case_id}: {delete_response.status_code}")
            else:
                print(f"Кейс {case_id} удален.")
    
    # Получаем всех игроков
    response = requests.get(f"{BASE_URL}/players/", headers=headers)
    if response.status_code == 200:
        players = response.json()
        for player in players:
            player_id = player["id"]
            # Удаляем каждого игрока
            delete_response = requests.delete(f"{BASE_URL}/players/{player_id}", headers=headers)
            if delete_response.status_code != 204:
                print(f"Ошибка при удалении игрока {player_id}: {delete_response.status_code}")
            else:
                print(f"Игрок {player_id} удален.")
    
    # Очищаем фонды
    response = requests.get(f"{BASE_URL}/funds/", headers=headers)
    if response.status_code == 200:
        funds = response.json()
        for fund in funds:
            # Пропускаем системный фонд администратора
            if fund["name"] == "Admin Fund":
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
    fund_name = AUTHOR_TO_FUND_NAME.get(author_id, f"Fund_{author_id}")
    
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

def create_room_database(token: str, rooms: Set[str]) -> None:
    """
    Создает базу данных румов.
    """
    headers = get_headers(token)
    
    print(f"Обнаружено {len(rooms)} уникальных румов:")
    for room_name in sorted(rooms):
        if not room_name.strip():
            continue
            
        # Проверяем существует ли уже такой рум
        try:
            room_name_encoded = requests.utils.quote(room_name)
            response = requests.get(f"{BASE_URL}/rooms/by-name/{room_name_encoded}", headers=headers)
            if response.status_code == 200:
                print(f"Рум уже существует: {room_name}")
                continue
            
            # Если рум не существует, создаем его
            room_data = {
                "name": room_name,
                "description": f"Покер-рум {room_name}",
                "is_active": True
            }
            
            response = requests.post(f"{BASE_URL}/rooms/", headers=headers, json=room_data)
            if response.status_code in [200, 201]:
                print(f"Создан новый рум: {room_name}")
            else:
                print(f"Ошибка при создании рума {room_name}: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Ошибка при обработке рума {room_name}: {str(e)}")

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
        # Получаем список всех игроков
        response = requests.get(f"{BASE_URL}/players/", headers=headers)
        if response.status_code == 200:
            all_players = response.json()
            
            # Создаем строку для поиска
            name_parts = [part for part in [first_name, middle_name, last_name] if part]
            search_query = " ".join(name_parts).lower()
            
            # Проверяем совпадение имени
            for player in all_players:
                if player["full_name"] and search_query in player["full_name"].lower():
                    # Проверяем, принадлежит ли игрок нашему фонду
                    if player.get("created_by_fund_id") == fund_id:
                        print(f"Найден существующий игрок: {player['full_name']} ({player['id']})")
                        return player["id"]
    except Exception as e:
        print(f"Ошибка при поиске игрока: {str(e)}")
    
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
        room = nick.get("room", "")
        discipline = nick.get("discipline", "")
        
        if nick_value:
            nicknames.append({
                "nickname": nick_value,
                "room": room,
                "discipline": discipline
            })
            # Добавляем рум в общий набор
            if room:
                ROOMS_SET.add(room)
    
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
        }
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

def create_case(token: str, case_data: Dict[str, Any], player_id: str, fund_id: str) -> str:
    """
    Создает новый кейс арбитража.
    Возвращает ID созданного кейса.
    """
    headers = get_headers(token)
    
    description = case_data.get("descr", "")
    
    # Преобразуем сумму
    amount_str = case_data.get("amount", "0")
    amount = parse_amount(amount_str)
    
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
        "player_id": player_id,
        "status": "open",
        "arbitrage_type": arbitrage_type,
        "arbitrage_amount": amount,
        "arbitrage_currency": currency
    }
    
    print(f"Отправляем данные для создания кейса: {case_data}")
    
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

def main():
    # Проверяем наличие файла
    if not os.path.exists("output.json"):
        print("Ошибка: Файл output.json не найден!")
        return
    
    try:
        # Получаем токен для доступа к API
        token = get_token()
        print("Токен получен успешно.")
        
        # Очищаем базу данных
        clear_database(token)
        
        # Создаем румы заранее
        # Сначала загружаем данные и извлекаем все румы
        with open("output.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print(f"Загружено {len(data)} записей из файла для анализа.")
        
        # Анализируем данные и собираем все уникальные румы
        for record in data:
            for nick in record.get("nickname", []):
                room = nick.get("room")
                if room:
                    ROOMS_SET.add(room)
                    
        # Создаем базу данных румов
        create_room_database(token, ROOMS_SET)
        
        # Теперь обрабатываем игроков и кейсы
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
                        print(f"Создание кейса {case_idx+1}/{len(case_data)} для игрока {player_id}")
                        print(f"Данные кейса: {case_item}")
                        case_id = create_case(token, case_item, player_id, fund_id)
                        stats["cases_created"] += 1
                    except Exception as e:
                        print(f"Ошибка при создании кейса: {str(e)}")
                        stats["errors"] += 1
            
            except Exception as e:
                print(f"Ошибка при обработке записи: {str(e)}")
                stats["errors"] += 1
        
        # Выводим статистику
        print("\nСтатистика миграции:")
        print(f"Всего записей: {stats['total_records']}")
        print(f"Создано игроков: {stats['players_created']}")
        print(f"Создано кейсов: {stats['cases_created']}")
        print(f"Ошибок: {stats['errors']}")
        print(f"Уникальных румов: {len(ROOMS_SET)}")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main() 