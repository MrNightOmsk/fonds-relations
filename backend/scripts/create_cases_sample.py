#!/usr/bin/env python
import json
import uuid
import random
from datetime import datetime, timedelta

"""
Скрипт для создания примера JSON-файла с данными о кейсах.
Этот файл можно использовать как шаблон для подготовки реальных данных.
"""

# Список возможных статусов кейсов
STATUS_OPTIONS = ["open", "in_progress", "resolved", "closed"]

# Список возможных типов арбитража
ARBITRAGE_TYPES = [
    "Долг", 
    "Скам",
    "Мошенничество", 
    "Искажение информации", 
    "Неоплата услуг",
    "Нарушение правил", 
    "Другое"
]

# Список валют
CURRENCIES = ["USD", "EUR", "RUB"]

def generate_sample_case(player_id: str, fund_name: str, index: int) -> dict:
    """
    Генерирует пример данных о кейсе
    """
    # Создаем случайную дату в прошлом (до 1 года назад)
    days_ago = random.randint(1, 365)
    case_date = datetime.now() - timedelta(days=days_ago)
    date_str = case_date.strftime("%Y-%m-%d")
    
    # Выбираем случайный статус с вероятностью
    status = random.choices(
        STATUS_OPTIONS, 
        weights=[0.4, 0.3, 0.2, 0.1],  # Больше открытых кейсов
        k=1
    )[0]
    
    # Выбираем случайный тип арбитража
    arbitrage_type = random.choice(ARBITRAGE_TYPES)
    
    # Генерируем случайную сумму арбитража
    amount = round(random.uniform(100, 10000), 2)
    
    # Выбираем валюту
    currency = random.choice(CURRENCIES)
    
    # Генерируем случайное количество комментариев (0-5)
    comment_count = random.randint(0, 5)
    comments = []
    
    for i in range(comment_count):
        comment_days_ago = random.randint(0, days_ago)
        comment_date = datetime.now() - timedelta(days=comment_days_ago)
        comment_date_str = comment_date.strftime("%Y-%m-%d %H:%M:%S")
        
        comments.append({
            "text": f"Комментарий #{i+1} к кейсу. Добавлен {comment_date_str}",
            "date": comment_date_str
        })
    
    # Формируем данные кейса
    case_data = {
        "player_id": player_id,
        "fund_name": fund_name,
        "title": f"Кейс #{index}: {arbitrage_type}",
        "description": f"Описание кейса #{index} типа '{arbitrage_type}', созданного {date_str}. Это пример описания для демонстрации формата данных.",
        "status": status,
        "arbitrage_type": arbitrage_type,
        "arbitrage_amount": amount,
        "arbitrage_currency": currency,
        "created_date": date_str,
        "comments": comments
    }
    
    return case_data


def generate_sample_cases(output_file: str, count: int = 10):
    """
    Генерирует примеры кейсов и сохраняет их в JSON-файл
    """
    # Пример ID игроков (нужно заменить на реальные)
    sample_player_ids = [str(uuid.uuid4()) for _ in range(5)]
    
    # Пример названий фондов (нужно заменить на реальные)
    sample_fund_names = ["Фонд покерной взаимопомощи", "Альфа Фонд", "Бета Фонд", "Гамма Фонд"]
    
    # Генерация данных
    cases = []
    for i in range(count):
        player_id = random.choice(sample_player_ids)
        fund_name = random.choice(sample_fund_names)
        case = generate_sample_case(player_id, fund_name, i+1)
        cases.append(case)
    
    # Запись в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)
    
    print(f"Создан пример файла с {count} кейсами: {output_file}")
    print(f"Примечание: Замените ID игроков и названия фондов на реальные перед импортом!")


if __name__ == "__main__":
    output_file = "cases_sample.json"
    generate_sample_cases(output_file, count=10)
    
    # Выводим структуру первого кейса как пример
    with open(output_file, 'r', encoding='utf-8') as f:
        sample_data = json.load(f)
        
    print("\nПример структуры кейса:")
    print(json.dumps(sample_data[0], ensure_ascii=False, indent=2))
    
    print("\nИнструкция:")
    print("1. Используйте этот файл как шаблон для подготовки реальных данных.")
    print("2. Замените ID игроков на реальные ID из вашей системы.")
    print("3. Замените названия фондов на существующие в вашей системе.")
    print("4. Для импорта используйте скрипт import_cases.py.") 