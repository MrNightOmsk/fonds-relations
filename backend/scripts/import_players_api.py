#!/usr/bin/env python
import json
import os
import sys
import requests
import time
import logging
from typing import Set, Dict, Any, List, Optional, Tuple
import re
from collections import defaultdict

# Настройка логирования
log_file = "import_players.log"
logging.basicConfig(
    level=logging.DEBUG,
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


def parse_fio(fio_data: List[Dict[str, str]]) -> Tuple[str, str, str, str]:
    """
    Разбирает ФИО из структуры данных и возвращает отдельные компоненты
    Возвращает кортеж: (имя, фамилия, отчество, полное_имя)
    """
    if not fio_data or len(fio_data) == 0:
        return "", "", "", ""
        
    # Берем первую запись ФИО
    fio_item = fio_data[0]
    full_name = fio_item.get("firstname", "")
    
    # Если поле содержит полное ФИО, разбираем его
    name_parts = full_name.strip().split()
    
    if len(name_parts) >= 3:
        # Предполагаем формат: Фамилия Имя Отчество
        last_name = name_parts[0]
        first_name = name_parts[1]
        middle_name = ' '.join(name_parts[2:])
    elif len(name_parts) == 2:
        # Предполагаем формат: Фамилия Имя
        last_name = name_parts[0]
        first_name = name_parts[1]
        middle_name = ""
    elif len(name_parts) == 1:
        # Только одно слово (вероятно, имя)
        first_name = name_parts[0]
        last_name = ""
        middle_name = ""
    else:
        # Пустое поле
        first_name = ""
        last_name = ""
        middle_name = ""
    
    return first_name, last_name, middle_name, full_name


def parse_location(location_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Преобразует данные о местоположении в формат, понятный API
    """
    locations = []
    
    if not location_data or len(location_data) == 0:
        return locations
    
    for loc in location_data:
        country_raw = loc.get("country", "").strip()
        
        if not country_raw:
            continue
        
        # Пытаемся разделить адрес на страну, город и улицу
        # Пример: "РФ, г. Санкт-Петербург, ул. Евдокима Огнева д. 4/1, кв. 69"
        parts = re.split(r',\s*', country_raw, 2)
        
        country = parts[0] if len(parts) > 0 else country_raw
        
        # Находим город
        city = ""
        if len(parts) > 1:
            city_match = re.search(r'г\.?\s+([^,]+)', parts[1])
            if city_match:
                city = city_match.group(1).strip()
            else:
                city = parts[1].strip()
        
        # Находим адрес
        address = parts[2].strip() if len(parts) > 2 else ""
        
        locations.append({
            "country": country,
            "city": city,
            "address": address
        })
    
    return locations


def extract_contacts(player_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Извлекает контактные данные из различных полей игрока
    """
    contacts = []
    
    # Телефоны
    for phone in player_data.get("phone", []):
        if phone:
            contacts.append({
                "type": "phone",
                "value": phone,
                "description": "Импортировано из output.json"
            })
    
    # Электронная почта
    for email in player_data.get("mail", []):
        if email:
            contacts.append({
                "type": "email",
                "value": email,
                "description": "Импортировано из output.json"
            })
    
    # Skype
    for skype in player_data.get("skype", []):
        if skype:
            contacts.append({
                "type": "skype",
                "value": skype,
                "description": "Импортировано из output.json"
            })
    
    return contacts


def extract_nicknames(player_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Извлекает данные о никнеймах игрока
    """
    nicknames = []
    
    for nick in player_data.get("nickname", []):
        value = nick.get("value", "").strip()
        room = nick.get("room", "").strip()
        discipline = nick.get("discipline", "").strip()
        
        if value:
            nicknames.append({
                "nickname": value,
                "room": room,
                "discipline": discipline
            })
    
    # Логирование никнеймов для отладки
    if nicknames:
        logger.debug(f"Извлечены никнеймы: {nicknames}")
    
    return nicknames


def extract_payment_methods(player_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Извлекает данные о платежных методах игрока
    """
    payment_methods = []
    
    # Skrill
    for skrill in player_data.get("skrill", []):
        if skrill:
            payment_methods.append({
                "type": "skrill",
                "value": skrill,
                "description": "Импортировано из output.json"
            })
    
    # Neteller
    for neteller in player_data.get("neteller", []):
        if neteller:
            payment_methods.append({
                "type": "neteller",
                "value": neteller,
                "description": "Импортировано из output.json"
            })
    
    # Ecopayz
    for ecopayz in player_data.get("ecopayz", []):
        if ecopayz:
            payment_methods.append({
                "type": "ecopayz",
                "value": ecopayz,
                "description": "Импортировано из output.json"
            })
    
    # WebMoney
    for webmoney in player_data.get("webmoney", []):
        if webmoney:
            payment_methods.append({
                "type": "webmoney",
                "value": webmoney,
                "description": "Импортировано из output.json"
            })
    
    return payment_methods


def extract_social_media(player_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Извлекает данные о социальных сетях игрока
    """
    social_media = []
    
    # VK
    for vk in player_data.get("vk", []):
        if vk:
            social_media.append({
                "type": "vk",
                "value": vk,
                "description": "Импортировано из output.json"
            })
    
    # Facebook
    for fb in player_data.get("facebook", []):
        if fb:
            social_media.append({
                "type": "facebook",
                "value": fb,
                "description": "Импортировано из output.json"
            })
    
    # Instagram
    for instagram in player_data.get("instagram", []):
        if instagram:
            social_media.append({
                "type": "instagram",
                "value": instagram,
                "description": "Импортировано из output.json"
            })
    
    # GipsyTeam
    for gipsyteam in player_data.get("gipsyteam", []):
        if gipsyteam:
            social_media.append({
                "type": "gipsyteam",
                "value": gipsyteam,
                "description": "Импортировано из output.json"
            })
    
    # PokerStrategy
    for pokerstrategy in player_data.get("pokerstrategy", []):
        if pokerstrategy:
            social_media.append({
                "type": "pokerstrategy",
                "value": pokerstrategy,
                "description": "Импортировано из output.json"
            })
    
    # Blog
    for blog in player_data.get("blog", []):
        if blog:
            social_media.append({
                "type": "blog",
                "value": blog,
                "description": "Импортировано из output.json"
            })
    
    # Forum
    for forum in player_data.get("forum", []):
        if forum:
            social_media.append({
                "type": "forum",
                "value": forum,
                "description": "Импортировано из output.json"
            })
    
    return social_media


def prepare_player_data(player_data: Dict[str, Any], fund_id: str) -> Dict[str, Any]:
    """
    Подготавливает данные игрока для отправки в API
    """
    # Разбираем ФИО
    first_name, last_name, middle_name, full_name = parse_fio(player_data.get("FIO", []))
    
    # Если ФИО пустое, используем ID для имени
    if not full_name:
        player_id = player_data.get("id", "unknown")
        first_name = f"Player {player_id}"
        full_name = first_name
    
    # Собираем данные игрока
    player = {
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "full_name": full_name,
        "created_by_fund_id": fund_id,
        "contact_info": {},  # Оставляем пустой для совместимости
        "additional_info": {
            "imported_id": player_data.get("id", ""),
            "import_source": "output.json",
            "import_date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    
    # Добавляем контакты
    contacts = extract_contacts(player_data)
    if contacts:
        player["contacts"] = contacts
        logger.debug(f"Добавлены контакты: {len(contacts)}")
    
    # Добавляем местоположение
    locations = parse_location(player_data.get("location", []))
    if locations:
        player["locations"] = locations
        logger.debug(f"Добавлены местоположения: {len(locations)}")
    
    # Добавляем никнеймы
    nicknames = extract_nicknames(player_data)
    if nicknames:
        player["nicknames"] = nicknames
        logger.debug(f"Добавлены никнеймы: {len(nicknames)} - {nicknames}")
    
    # Добавляем платежные методы
    payment_methods = extract_payment_methods(player_data)
    if payment_methods:
        player["payment_methods"] = payment_methods
        logger.debug(f"Добавлены платежные методы: {len(payment_methods)}")
    
    # Добавляем социальные сети
    social_media = extract_social_media(player_data)
    if social_media:
        player["social_media"] = social_media
        logger.debug(f"Добавлены социальные сети: {len(social_media)}")
    
    return player


def create_player(base_url: str, player_data: Dict[str, Any], headers: Dict[str, str]) -> Optional[str]:
    """
    Создает игрока через API
    """
    players_url = f"{base_url}/players/"
    
    # Логируем данные перед отправкой
    if "nicknames" in player_data:
        logger.debug(f"Отправка никнеймов на сервер: {player_data['nicknames']}")
    
    try:
        response = requests.post(players_url, headers=headers, json=player_data)
        
        if response.status_code == 201:
            player = response.json()
            # Проверяем, вернулись ли никнеймы в ответе
            if "nicknames" in player and player["nicknames"]:
                logger.debug(f"Сервер вернул никнеймы: {player['nicknames']}")
            else:
                logger.warning(f"Сервер не вернул никнеймы в ответе")
            return player["id"]
        else:
            logger.error(f"Ошибка при создании игрока {player_data.get('full_name')}: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logger.error(f"Исключение при создании игрока {player_data.get('full_name')}: {str(e)}")
        return None


def get_fund_mapping(fund_mapping_file: str) -> Dict[str, str]:
    """
    Загружает маппинг фондов из файла
    """
    try:
        with open(fund_mapping_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Файл маппинга фондов {fund_mapping_file} не найден")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Ошибка при чтении файла маппинга фондов {fund_mapping_file}")
        return {}


def main():
    # Параметры подключения к API
    API_BASE_URL = "http://localhost:8000/api/v1"
    
    logger.info(f"Используется базовый URL API: {API_BASE_URL}")
    
    # Запрашиваем учетные данные
    username = input("Введите имя пользователя (администратора): ")
    password = input("Введите пароль: ")
    
    logger.info("Начало импорта игроков из output.json")
    
    # Получаем токен
    try:
        token = get_access_token(API_BASE_URL, username, password)
        logger.info("Токен доступа получен успешно")
        headers = get_headers(token)
    except Exception as e:
        logger.error(f"Не удалось получить токен доступа: {str(e)}")
        sys.exit(1)
    
    # Пути к файлу output.json
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
        logger.error("Файл output.json не найден по проверенным путям")
        return
    
    # Загружаем маппинг фондов
    fund_mapping_file = "fund_mapping.json"
    fund_mapping = get_fund_mapping(fund_mapping_file)
    
    if not fund_mapping:
        logger.error("Не удалось загрузить маппинг фондов. Запустите сначала скрипт import_funds_api.py")
        return
    
    logger.info(f"Загружен маппинг для {len(fund_mapping)} фондов")
    
    # Чтение данных из файла
    logger.info(f"Чтение файла {abs_path}...")
    data = read_output_json(abs_path)
    logger.info(f"Файл успешно прочитан. Найдено {len(data)} записей.")
    
    # Индексируем игроков по ID для избежания дубликатов
    players_by_id = {}
    
    for entry in data:
        player_id = entry.get("id")
        
        if not player_id:
            continue
        
        # Если этот игрок уже был обработан, пропускаем
        if player_id in players_by_id:
            continue
        
        players_by_id[player_id] = entry
    
    logger.info(f"Найдено {len(players_by_id)} уникальных игроков.")
    
    # Статистика для отслеживания процесса
    stats = {
        "total": len(players_by_id),
        "processed": 0,
        "success": 0,
        "error": 0,
        "skipped": 0
    }
    
    # Создаем игроков через API
    player_mapping = {}
    
    for player_id, player_data in players_by_id.items():
        stats["processed"] += 1
        
        # Получаем ID фонда, создавшего запись
        original_fund_id = player_data.get("author")
        
        if not original_fund_id or original_fund_id not in fund_mapping:
            logger.warning(f"Не найден фонд для игрока {player_id}, пропускаем")
            stats["skipped"] += 1
            continue
        
        # Подготавливаем данные игрока
        prepared_data = prepare_player_data(player_data, fund_mapping[original_fund_id])
        
        # Добавляем небольшую задержку, чтобы не перегрузить API
        time.sleep(0.1)
        
        # Создаем игрока
        logger.info(f"Создание игрока: {prepared_data.get('full_name')} (ID: {player_id})")
        new_player_id = create_player(API_BASE_URL, prepared_data, headers)
        
        if new_player_id:
            player_mapping[player_id] = new_player_id
            stats["success"] += 1
            logger.info(f"Игрок успешно создан с ID: {new_player_id}")
        else:
            stats["error"] += 1
        
        # Периодически выводим статистику
        if stats["processed"] % 10 == 0:
            logger.info(f"Прогресс: {stats['processed']}/{stats['total']} (Успешно: {stats['success']}, Ошибок: {stats['error']}, Пропущено: {stats['skipped']})")
    
    # Сохраняем маппинг игроков
    player_mapping_file = "player_mapping.json"
    with open(player_mapping_file, 'w', encoding='utf-8') as f:
        json.dump(player_mapping, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Маппинг игроков сохранен в файл {player_mapping_file}")
    
    # Выводим итоговую статистику
    logger.info("\nИтоги импорта игроков:")
    logger.info(f"Всего записей обработано: {stats['processed']}/{stats['total']}")
    logger.info(f"Успешно создано: {stats['success']}")
    logger.info(f"Ошибок: {stats['error']}")
    logger.info(f"Пропущено: {stats['skipped']}")


if __name__ == "__main__":
    main()
    # Чтобы PowerShell увидел весь вывод
    sys.stdout.flush()
    time.sleep(1) 