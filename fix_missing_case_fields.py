#!/usr/bin/env python
import requests
import os
import sys
from typing import Dict, Any, List

# Конфигурация
BASE_URL = "http://localhost:8000/api/v1"  # Измените, если нужно
TOKEN = None  # Получим через аутентификацию

def authenticate(email: str, password: str) -> str:
    """Аутентификация пользователя и получение токена доступа"""
    auth_data = {
        "username": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/login/access-token", data=auth_data)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Ошибка аутентификации: {response.status_code}, {response.text}")

def get_headers(token: str) -> Dict[str, str]:
    """Получает заголовки с токеном авторизации"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def get_cases(token: str) -> List[Dict[str, Any]]:
    """Получает все кейсы из системы"""
    headers = get_headers(token)
    
    response = requests.get(f"{BASE_URL}/cases/", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка получения кейсов: {response.status_code}, {response.text}")

def update_case(token: str, case_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Обновляет данные кейса"""
    headers = get_headers(token)
    
    response = requests.put(f"{BASE_URL}/cases/{case_id}", headers=headers, json=update_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка обновления кейса {case_id}: {response.status_code}, {response.text}")

def get_fund(token: str, fund_id: str) -> Dict[str, Any]:
    """Получает информацию о фонде по ID"""
    headers = get_headers(token)
    
    response = requests.get(f"{BASE_URL}/funds/{fund_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка получения фонда {fund_id}: {response.status_code}, {response.text}")

def update_fund(token: str, fund_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Обновляет данные фонда"""
    headers = get_headers(token)
    
    response = requests.put(f"{BASE_URL}/funds/{fund_id}", headers=headers, json=update_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка обновления фонда {fund_id}: {response.status_code}, {response.text}")

def main():
    # Запрашиваем учетные данные
    email = input("Введите email администратора: ")
    password = input("Введите пароль: ")
    
    try:
        # Аутентифицируемся и получаем токен
        token = authenticate(email, password)
        print("Аутентификация успешна.")
        
        # Получаем все кейсы
        print("Получение списка кейсов...")
        cases = get_cases(token)
        print(f"Получено {len(cases)} кейсов.")
        
        # Переименовываем фонд "default", если такой существует
        try:
            response = requests.get(f"{BASE_URL}/funds/by-name/default", headers=get_headers(token))
            if response.status_code == 200:
                default_fund = response.json()
                print(f"Найден фонд 'default' с ID {default_fund['id']}")
                
                # Обновляем название фонда
                update_data = {
                    "name": "Непривязанные кейсы",
                    "description": "Фонд для кейсов, созданных во время миграции без привязки к конкретному фонду"
                }
                updated_fund = update_fund(token, default_fund["id"], update_data)
                print(f"Фонд переименован на '{updated_fund['name']}'")
        except Exception as e:
            print(f"Фонд 'default' не найден или произошла ошибка: {str(e)}")
        
        # Обновляем кейсы с отсутствующими полями
        updated_count = 0
        for case in cases:
            update_data = {}
            
            # Проверяем отсутствующие поля
            if case.get("arbitrage_amount") is None:
                update_data["arbitrage_amount"] = 0
            
            if not case.get("arbitrage_currency"):
                update_data["arbitrage_currency"] = "USD"
            
            # Если есть что обновлять
            if update_data:
                try:
                    updated_case = update_case(token, case["id"], update_data)
                    updated_count += 1
                    print(f"Обновлен кейс {updated_case['id']} - {updated_case['title']}")
                except Exception as e:
                    print(f"Ошибка при обновлении кейса {case['id']}: {str(e)}")
        
        print(f"\nОбновлено {updated_count} кейсов из {len(cases)}")
        print("Операция успешно завершена!")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 