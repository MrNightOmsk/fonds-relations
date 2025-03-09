import requests
import json

# Конфигурация для Docker-окружения 
# Используем имя сервиса из docker-compose вместо localhost
API_URL = "http://backend:8000/api/v1"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDE5NDkxOTEsInN1YiI6IjBlMGRjNThmLWYxNjctNGVlMi1iMWI1LTczNTNiMjdlYzBhOSIsImZ1bmRfaWQiOiI4NTljY2M4OC04YTJlLTRhOWMtOWYyZC1lMTFhOTBhZWJjMWIiLCJyb2xlIjoiYWRtaW4ifQ.rNboPrOfFjqKmpTAyHao25beclbbqoJiggRRtkS5CIs"

# Заголовки запроса
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Данные для создания кейса
case_data = {
    "title": "Test Case",
    "description": "Test case description",
    "player_id": "e5f2224c-9b8b-44a2-9b8f-04412bbaa6c7",
    "status": "open",
    "arbitrage_type": "Test Arbitrage",
    "arbitrage_amount": 100.50,
    "arbitrage_currency": "USD",
    "created_by_fund_id": "859ccc88-8a2e-4a9c-9f2d-e11a90aebc1b"
}

# Отправляем запрос на создание кейса
response = requests.post(
    f"{API_URL}/cases/",
    headers=headers,
    json=case_data
)

# Проверяем статус ответа
print(f"Status Code: {response.status_code}")
print("Response Body:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# Проверка ошибки при отсутствии обязательного поля
print("\n\nТестирование ошибки при отсутствии обязательного поля status:")
invalid_case = case_data.copy()
invalid_case.pop("status")  # Удаляем обязательное поле status

response = requests.post(
    f"{API_URL}/cases/",
    headers=headers,
    json=invalid_case
)

print(f"Status Code: {response.status_code}")
print("Response Body:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# Проверка ошибки при отрицательной сумме арбитража
print("\n\nТестирование ошибки при отрицательной сумме арбитража:")
invalid_case = case_data.copy()
invalid_case["arbitrage_amount"] = -100.0  # Отрицательная сумма

response = requests.post(
    f"{API_URL}/cases/",
    headers=headers,
    json=invalid_case
)

print(f"Status Code: {response.status_code}")
print("Response Body:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# Проверка ошибки при несуществующем фонде
print("\n\nТестирование ошибки при несуществующем фонде:")
invalid_case = case_data.copy()
invalid_case["created_by_fund_id"] = "00000000-0000-0000-0000-000000000000"  # Несуществующий фонд

response = requests.post(
    f"{API_URL}/cases/",
    headers=headers,
    json=invalid_case
)

print(f"Status Code: {response.status_code}")
print("Response Body:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# Проверка ошибки при несуществующем игроке
print("\n\nТестирование ошибки при несуществующем игроке:")
invalid_case = case_data.copy()
invalid_case["player_id"] = "00000000-0000-0000-0000-000000000000"  # Несуществующий игрок

response = requests.post(
    f"{API_URL}/cases/",
    headers=headers,
    json=invalid_case
)

print(f"Status Code: {response.status_code}")
print("Response Body:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False)) 