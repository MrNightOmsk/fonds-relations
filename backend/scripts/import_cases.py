#!/usr/bin/env python
import json
import os
import sys
import requests
import time
import logging
import uuid
import locale
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

# Устанавливаем кодировку консоли для Windows
if sys.platform == 'win32':
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleCP(65001)
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        # Устанавливаем локаль для корректного вывода русских символов
        locale.setlocale(locale.LC_ALL, 'Russian_Russia.UTF-8')
    except Exception as e:
        print(f"Предупреждение: не удалось установить кодировку консоли: {e}")

# Настройка логирования
log_file = "import_cases.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def read_output_json(file_path: str = None) -> List[Dict[str, Any]]:
    """
    Читает файл output.json и возвращает его содержимое.
    Пытается найти файл в нескольких возможных расположениях.
    """
    # Проверяем разные возможные пути к файлу
    possible_paths = [
        file_path,                # Переданный путь
        "output.json",            # В текущей директории
        "../output.json",         # В родительской директории
        "backend/output.json",    # В директории backend
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../output.json")  # Абсолютный путь
    ]
    
    # Удаляем None из списка
    possible_paths = [p for p in possible_paths if p]
    
    # Пробуем открыть файл по каждому пути
    for path in possible_paths:
        try:
            if os.path.exists(path):
                logger.info(f"Найден файл output.json по пути: {path}")
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
        except Exception as e:
            logger.warning(f"Не удалось открыть файл по пути {path}: {str(e)}")
    
    # Если файл не найден ни по одному пути
    logger.error("Файл output.json не найден ни в одном из возможных расположений")
    raise FileNotFoundError("Файл output.json не найден")


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
        
        token_data = response.json()
        logger.info("Успешное получение токена доступа")
        return token_data["access_token"]
    except Exception as e:
        logger.error(f"Ошибка при получении токена доступа: {str(e)}")
        sys.exit(1)


def get_headers(token: str) -> Dict[str, str]:
    """
    Формирует заголовки для запросов к API
    """
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def get_player_id_mapping(base_url: str, headers: Dict[str, str], output_file_path: str = None) -> Dict[str, str]:
    """
    Получает маппинг между исходными ID игроков и ID в системе.
    Пытается сопоставить игроков по:
    1. metadata.imported_id (если есть)
    2. никнеймам
    3. ФИО
    """
    players_url = f"{base_url}/players/?limit=1000"
    
    try:
        response = requests.get(players_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Ошибка получения игроков: {response.status_code}, {response.text}")
        
        # Получаем игроков из системы
        players = response.json()
        logger.info(f"Получено {len(players)} игроков из системы")
        
        # Читаем исходные данные игроков из output.json
        try:
            # Используем уже найденный путь к файлу или ищем заново
            if output_file_path:
                with open(output_file_path, 'r', encoding='utf-8') as f:
                    original_players = json.load(f)
            else:
                original_players = read_output_json()
                
            logger.info(f"Прочитано {len(original_players)} игроков из output.json для маппинга")
        except Exception as e:
            logger.error(f"Ошибка при чтении output.json для маппинга: {str(e)}")
            return {}
        
        # Создаем словари для поиска по никнеймам и ФИО
        original_nicknames_map = {}  # никнейм -> id
        original_names_map = {}  # имя -> id
        
        # Заполняем словари данными из output.json
        for player in original_players:
            player_id = player.get("id")
            if not player_id:
                continue
                
            # Сохраняем никнеймы
            nicknames = player.get("nickname", [])
            for nick in nicknames:
                nickname = nick.get("value", "").lower()
                if nickname:
                    original_nicknames_map[nickname] = player_id
            
            # Сохраняем ФИО
            fio_list = player.get("FIO", [])
            if fio_list and len(fio_list) > 0:
                name = fio_list[0].get("firstname", "").lower()
                if name:
                    original_names_map[name] = player_id
        
        # Создаем итоговый маппинг
        player_mapping = {}
        
        # Сопоставляем игроков
        for player in players:
            # Проверяем маппинг по метаданным
            metadata = player.get("metadata", {})
            imported_id = metadata.get("imported_id", "")
            
            if imported_id:
                player_mapping[imported_id] = player["id"]
                continue
                
            # Проверяем маппинг по никнеймам
            system_nicknames = player.get("nicknames", [])
            matched = False
            
            for nick in system_nicknames:
                nickname = nick.get("nickname", "").lower()
                if nickname in original_nicknames_map:
                    player_mapping[original_nicknames_map[nickname]] = player["id"]
                    matched = True
                    break
                    
            if matched:
                continue
                
            # Проверяем маппинг по ФИО
            full_name = player.get("full_name", "").lower()
            if full_name in original_names_map:
                player_mapping[original_names_map[full_name]] = player["id"]
                
        logger.info(f"Получен маппинг для {len(player_mapping)} игроков")
        return player_mapping
    except Exception as e:
        logger.error(f"Ошибка при получении маппинга игроков: {str(e)}")
        return {}


def get_fund_mapping(base_url: str, headers: Dict[str, str]) -> Dict[str, str]:
    """
    Получает данные о фондах для маппинга
    """
    funds_url = f"{base_url}/funds/"
    
    try:
        response = requests.get(funds_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Ошибка получения фондов: {response.status_code}, {response.text}")
        
        funds = response.json()
        fund_mapping = {}
        
        for fund in funds:
            fund_mapping[fund["name"]] = fund["id"]
            
        logger.info(f"Получен маппинг для {len(fund_mapping)} фондов")
        return fund_mapping
    except Exception as e:
        logger.error(f"Ошибка при получении фондов: {str(e)}")
        return {}


def extract_case_data(player_data: Dict[str, Any], default_fund_name: str) -> List[Dict[str, Any]]:
    """
    Извлекает данные о кейсах из записи об игроке
    """
    cases = []
    
    # Проверяем наличие кейсов в данных игрока
    case_data = player_data.get("case", [])
    if not case_data:
        return cases
    
    player_id = player_data.get("id", "")
    if not player_id:
        return cases
    
    # Извлекаем ФИО игрока для заголовка кейса
    fio_data = player_data.get("FIO", [])
    player_name = ""
    if fio_data and len(fio_data) > 0:
        player_name = fio_data[0].get("firstname", "")
        
        # Проверяем никнеймы для дополнительной информации
        nicknames = player_data.get("nickname", [])
        nick_values = []
        for nick in nicknames:
            if nick.get("value"):
                nick_values.append(nick.get("value"))
                
        # Добавляем никнеймы к имени, если есть
        if nick_values and not player_name:
            player_name = f"{nick_values[0]}"
    
    # Обрабатываем каждый кейс
    for case_item in case_data:
        case_title = "Арбитраж"
        if player_name:
            case_title = f"Арбитраж: {player_name}"
            
        # Описание может быть с форматированием
        description = case_item.get("descr", "")
        if not description:
            description = "Нет описания"
        
        # Формируем данные кейса
        case = {
            "player_id": player_id,
            "title": case_title,
            "description": description,
            "status": "open",  # По умолчанию открытый
            "arbitrage_type": case_item.get("arbitrage", "Арбитраж"),
            "fund_name": default_fund_name,  # Используем выбранный фонд
        }
        
        # Обрабатываем сумму арбитража
        amount_str = case_item.get("amount", "0")
        try:
            # Заменяем запятую на точку для корректного преобразования
            amount_str = amount_str.replace(",", ".")
            case["arbitrage_amount"] = float(amount_str)
        except (ValueError, TypeError):
            case["arbitrage_amount"] = 0.0
        
        case["arbitrage_currency"] = "USD"  # По умолчанию USD
        
        cases.append(case)
    
    return cases


def prepare_case_data(
    case_data: Dict[str, Any], 
    player_mapping: Dict[str, str], 
    fund_mapping: Dict[str, str],
    admin_user_id: str
) -> Optional[Dict[str, Any]]:
    """
    Подготавливает данные кейса для отправки в API
    """
    try:
        # Получаем ID игрока по маппингу
        player_id = case_data.get("player_id", "")
        if not player_id or player_id not in player_mapping:
            logger.warning(f"Не найден игрок для кейса: {case_data.get('title', 'Без заголовка')}")
            return None
            
        mapped_player_id = player_mapping[player_id]
        
        # Получаем ID фонда по имени из маппинга
        fund_name = case_data.get("fund_name", "")
        if not fund_name or fund_name not in fund_mapping:
            logger.warning(f"Не найден фонд для кейса: {case_data.get('title', 'Без заголовка')}")
            return None
            
        fund_id = fund_mapping[fund_name]
        
        # Формируем данные кейса для API
        prepared_data = {
            "title": case_data.get("title", "Без заголовка"),
            "description": case_data.get("description", ""),
            "status": case_data.get("status", "open"),  # По умолчанию открытый
            "player_id": mapped_player_id,
            "created_by_fund_id": fund_id,
            # Добавляем поля арбитража, если они есть
            "arbitrage_type": case_data.get("arbitrage_type", ""),
            "arbitrage_amount": float(case_data.get("arbitrage_amount", 0)),
            "arbitrage_currency": case_data.get("arbitrage_currency", "USD")
        }
        
        return prepared_data
    except Exception as e:
        logger.error(f"Ошибка при подготовке данных кейса {case_data.get('title', 'Без заголовка')}: {str(e)}")
        return None


def create_case(base_url: str, case_data: Dict[str, Any], headers: Dict[str, str]) -> Optional[str]:
    """
    Создает кейс через API
    """
    cases_url = f"{base_url}/cases/"
    
    try:
        response = requests.post(cases_url, json=case_data, headers=headers)
        if response.status_code != 201:
            logger.error(f"Ошибка создания кейса: {response.status_code}, {response.text}")
            return None
        
        case = response.json()
        logger.info(f"Успешно создан кейс: {case['title']} (ID: {case['id']})")
        return case["id"]
    except Exception as e:
        logger.error(f"Ошибка при создании кейса: {str(e)}")
        return None


def main():
    # Запрашиваем параметры подключения у пользователя
    print("Введите параметры подключения к API:")
    base_url = input("URL API (по умолчанию http://localhost:3000/api/v1): ").strip() or "http://localhost:3000/api/v1"
    username = input("Email администратора (по умолчанию admin@example.com): ").strip() or "admin@example.com"
    password = input("Пароль администратора (по умолчанию admin): ").strip() or "admin"
    
    # Показываем список доступных путей для поиска
    print("\nПоиск файла output.json...")
    possible_paths = ["output.json", "../output.json", "backend/output.json", "../../output.json"]
    
    # Получение текущей директории для отладки
    current_dir = os.getcwd()
    print(f"Текущая директория: {current_dir}")
    
    # Вывод содержимого текущей директории
    print("Содержимое текущей директории:")
    try:
        for item in os.listdir(current_dir):
            print(f" - {item}")
    except Exception as e:
        print(f"Ошибка при получении содержимого директории: {e}")
    
    # Получение данных
    try:
        # Ищем файл output.json
        output_file_path = None
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(path):
                output_file_path = path
                print(f"Найден файл: {path} (абсолютный путь: {abs_path})")
                break
            else:
                print(f"Файл не найден: {path} (абсолютный путь: {abs_path})")
        
        # Проверка пути относительно скрипта
        if not output_file_path:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.abspath(os.path.join(script_dir, "../.."))
            output_file_path = os.path.join(root_dir, "output.json")
            print(f"Пробуем путь относительно скрипта: {output_file_path}")
            
            if not os.path.exists(output_file_path):
                raise FileNotFoundError(f"Файл output.json не найден ни в одном из возможных расположений. Проверьте, что файл существует.")
        
        logger.info(f"Найден файл output.json: {output_file_path}")
        
        with open(output_file_path, 'r', encoding='utf-8') as f:
            player_data = json.load(f)
        
        logger.info(f"Прочитано {len(player_data)} записей о игроках из файла")
    except FileNotFoundError as e:
        logger.error(f"Не удалось найти файл output.json: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Ошибка при чтении файла output.json: {str(e)}")
        sys.exit(1)
    
    # Получение токена
    token = get_access_token(base_url, username, password)
    headers = get_headers(token)
    
    # Получение маппинга игроков
    player_mapping = get_player_id_mapping(base_url, headers, output_file_path)
    if not player_mapping:
        logger.error("Не удалось получить маппинг игроков, импорт невозможен")
        sys.exit(1)
    
    # Получение данных о фондах
    fund_mapping = get_fund_mapping(base_url, headers)
    if not fund_mapping:
        logger.error("Не удалось получить данные о фондах, импорт невозможен")
        sys.exit(1)
    
    # Проверяем наличие фонда по умолчанию
    default_fund = "Фонд покерной взаимопомощи"
    
    # Выводим список доступных фондов
    print("\nДоступные фонды в системе:")
    for fund_name in fund_mapping.keys():
        print(f" - {fund_name}" + (" (по умолчанию)" if fund_name == default_fund else ""))
    
    # Если фонда по умолчанию нет, запрашиваем выбор
    if default_fund not in fund_mapping:
        print(f"\nФонд по умолчанию '{default_fund}' не найден в системе.")
        print("Укажите название существующего фонда для использования:")
        user_fund = input("Название фонда: ").strip()
        
        if user_fund and user_fund in fund_mapping:
            default_fund = user_fund
            print(f"Выбран фонд: {default_fund}")
        else:
            logger.error(f"Фонд '{user_fund}' не найден в системе. Импорт невозможен.")
            sys.exit(1)
    
    # Получаем ID пользователя-админа (последний параметр будет использоваться в будущем)
    admin_user_id = "00000000-0000-0000-0000-000000000000"  # Замените на реальный ID админа в системе
    
    # Статистика для отчета
    total_players = len(player_data)
    players_with_cases = 0
    total_cases = 0
    imported_cases = 0
    failed_cases = 0
    
    # Обрабатываем все записи игроков и извлекаем кейсы
    all_cases = []
    for player in player_data:
        cases = extract_case_data(player, default_fund)
        if cases:
            players_with_cases += 1
            total_cases += len(cases)
            all_cases.extend(cases)
    
    # Выводим статистику кейсов и игроков
    print(f"\nСтатистика по данным:")
    print(f"Всего игроков в файле: {total_players}")
    print(f"Игроков с кейсами: {players_with_cases}")
    print(f"Всего кейсов: {total_cases}")
    
    # Предупреждение о возможных проблемах с маппингом
    if len(player_mapping) < players_with_cases:
        print(f"\nВНИМАНИЕ: Найдено меньше маппингов игроков ({len(player_mapping)}), чем игроков с кейсами ({players_with_cases}).")
        print("Некоторые кейсы могут быть пропущены из-за отсутствия соответствия между игроками.")
        proceed = input("Продолжить импорт? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Импорт отменен пользователем.")
            sys.exit(0)
    
    print(f"\nНачинаем импорт {total_cases} кейсов...")
    logger.info(f"Найдено {total_cases} кейсов у {players_with_cases} игроков")
    
    # Импорт кейсов
    for index, case_data in enumerate(all_cases):
        logger.info(f"Импорт кейса {index+1}/{total_cases}: {case_data.get('title', 'Без заголовка')}")
        
        # Подготовка данных кейса
        prepared_case = prepare_case_data(case_data, player_mapping, fund_mapping, admin_user_id)
        if not prepared_case:
            logger.warning(f"Пропуск кейса {index+1}: не удалось подготовить данные")
            failed_cases += 1
            continue
        
        # Создание кейса
        case_id = create_case(base_url, prepared_case, headers)
        if not case_id:
            logger.warning(f"Пропуск кейса {index+1}: не удалось создать кейс")
            failed_cases += 1
            continue
        
        imported_cases += 1
        
        # Делаем паузу между запросами, чтобы не перегрузить API
        time.sleep(0.5)
        
        # Периодически выводим прогресс
        if (index + 1) % 10 == 0 or index + 1 == total_cases:
            print(f"Прогресс: {index + 1}/{total_cases} кейсов ({round((index + 1) / total_cases * 100)}%)")
    
    # Итоговая статистика
    logger.info("=== Итоги импорта ===")
    logger.info(f"Всего игроков в файле: {total_players}")
    logger.info(f"Игроков с кейсами: {players_with_cases}")
    logger.info(f"Всего кейсов: {total_cases}")
    logger.info(f"Успешно импортировано: {imported_cases}")
    logger.info(f"Не удалось импортировать: {failed_cases}")
    logger.info("======================")
    
    # Вывод в консоль
    print("\n=== Итоги импорта ===")
    print(f"Всего игроков в файле: {total_players}")
    print(f"Игроков с кейсами: {players_with_cases}")
    print(f"Всего кейсов: {total_cases}")
    print(f"Успешно импортировано: {imported_cases}")
    print(f"Не удалось импортировать: {failed_cases}")
    print("======================")
    print(f"\nПодробная информация записана в лог-файл: {log_file}")
    
    if imported_cases > 0:
        print("\nИмпорт успешно завершен!")
    else:
        print("\nИмпорт завершен с ошибками!")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nИмпорт прерван пользователем.")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Необработанная ошибка: {str(e)}")
        print(f"\nПроизошла непредвиденная ошибка: {str(e)}")
        sys.exit(1) 