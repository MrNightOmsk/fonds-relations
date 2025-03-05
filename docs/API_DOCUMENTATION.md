# API Документация

## Основная информация

FondsRelations API построен на основе REST принципов и использует стандартные HTTP-методы для взаимодействия.

- **Базовый URL**: `http://localhost:8000/api/v1/`
- **Формат данных**: JSON
- **Аутентификация**: OAuth2 с Bearer токенами

## Аутентификация

### Получение токена доступа

```
POST /api/v1/login/access-token
```

**Параметры запроса:**
- `username`: Email пользователя
- `password`: Пароль пользователя

**Пример запроса:**
```bash
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin"
```

**Пример ответа:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Игроки (Players)

### Получение списка игроков

```
GET /api/v1/players/
```

**Параметры запроса:**
- `skip`: Смещение (по умолчанию 0)
- `limit`: Лимит записей (по умолчанию 100)

**Ответ:**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "Иван",
    "last_name": "Иванов",
    "middle_name": "Иванович",
    "full_name": "Иванов Иван Иванович",
    "birth_date": "1990-01-01",
    "contact_info": {},
    "additional_info": {},
    "health_notes": "Аллергия на орехи",
    "created_by_user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_by_fund_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "contacts": [],
    "locations": [],
    "nicknames": [],
    "payment_methods": [],
    "social_media": []
  }
]
```

### Создание игрока

```
POST /api/v1/players/
```

**Тело запроса:**
```json
{
  "first_name": "Иван",
  "last_name": "Иванов",
  "middle_name": "Иванович",
  "full_name": "Иванов Иван Иванович",
  "birth_date": "1990-01-01",
  "contact_info": {},
  "additional_info": {},
  "health_notes": "Аллергия на орехи",
  "contacts": [
    {
      "type": "email",
      "value": "ivan@example.com",
      "description": "Личная почта"
    }
  ],
  "locations": [
    {
      "country": "Россия",
      "city": "Москва",
      "address": "ул. Примерная, 1"
    }
  ],
  "nicknames": [
    {
      "nickname": "IvanPoker",
      "room": "PokerStars",
      "discipline": "NLHE"
    }
  ],
  "payment_methods": [
    {
      "type": "bank",
      "value": "1234 5678 9012 3456",
      "description": "Сбербанк"
    }
  ],
  "social_media": [
    {
      "type": "telegram",
      "value": "@ivanpoker",
      "description": "Основной телеграм"
    }
  ]
}
```

## Дела (Cases)

### Получение списка дел

```
GET /api/v1/cases/
```

**Параметры запроса:**
- `skip`: Смещение (по умолчанию 0)
- `limit`: Лимит записей (по умолчанию 100)
- `player_id`: ID игрока (опционально)

**Ответ:**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Арбитраж в PokerStars",
    "description": "Игрок отказался выплачивать долг",
    "player_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "status": "open",
    "arbitrage_type": "debt",
    "arbitrage_amount": 1000.00,
    "arbitrage_currency": "USD",
    "created_by_user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_by_fund_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "closed_at": null,
    "closed_by_user_id": null,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

### Создание дела

```
POST /api/v1/cases/
```

**Тело запроса:**
```json
{
  "title": "Арбитраж в PokerStars",
  "description": "Игрок отказался выплачивать долг",
  "player_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "status": "open",
  "arbitrage_type": "debt",
  "arbitrage_amount": 1000.00,
  "arbitrage_currency": "USD"
}
```

### Получение комментариев к делу

```
GET /api/v1/cases/{case_id}/comments/
```

**Параметры запроса:**
- `skip`: Смещение (по умолчанию 0)
- `limit`: Лимит записей (по умолчанию 100)

**Ответ:**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "case_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "comment": "Игрок связался с нами и обещал вернуть долг до конца месяца",
    "created_by_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```

### Создание комментария к делу

```
POST /api/v1/cases/{case_id}/comments/
```

**Тело запроса:**
```json
{
  "comment": "Игрок связался с нами и обещал вернуть долг до конца месяца",
  "case_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

### Получение доказательств по делу

```
GET /api/v1/cases/{case_id}/evidences/
```

**Параметры запроса:**
- `skip`: Смещение (по умолчанию 0)
- `limit`: Лимит записей (по умолчанию 100)

**Ответ:**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "case_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "type": "document",
    "description": "Скриншот переписки с игроком",
    "file_path": "/uploads/cases/3fa85f64-5717-4562-b3fc-2c963f66afa6/evidence1.jpg",
    "uploaded_by_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```

### Загрузка доказательства к делу

```
POST /api/v1/cases/{case_id}/evidences/
```

**Формат запроса:** `multipart/form-data`

**Параметры запроса:**
- `type`: Тип доказательства (document, image, video, etc)
- `description`: Описание доказательства
- `file`: Файл доказательства

## Фонды (Funds)

### Получение списка фондов

```
GET /api/v1/funds/
```

**Параметры запроса:**
- `skip`: Смещение (по умолчанию 0)
- `limit`: Лимит записей (по умолчанию 100)

**Ответ:**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "Покерный фонд 'Успех'",
    "description": "Фонд для поддержки профессиональных игроков",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

## Коды ответов

- `200 OK`: Запрос выполнен успешно
- `201 Created`: Ресурс успешно создан
- `204 No Content`: Запрос выполнен успешно, данные не возвращаются
- `400 Bad Request`: Ошибка в запросе
- `401 Unauthorized`: Ошибка аутентификации
- `403 Forbidden`: Доступ запрещен
- `404 Not Found`: Ресурс не найден
- `422 Unprocessable Entity`: Ошибка валидации
- `500 Internal Server Error`: Внутренняя ошибка сервера

## Дополнительная документация

Полная интерактивная документация API доступна по адресам:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc) 