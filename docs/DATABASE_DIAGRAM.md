# Диаграмма базы данных FondsRelations

Ниже представлена диаграмма базы данных в формате Mermaid, которая визуализирует структуру и связи между таблицами.

```mermaid
erDiagram
    FUND {
        uuid id PK
        string name
        text description
        jsonb contact_info
        timestamp created_at
        timestamp updated_at
    }
    
    USER {
        uuid id PK
        string email
        string hashed_password
        string full_name
        uuid fund_id FK
        string role
        bool is_active
        timestamp created_at
        timestamp updated_at
    }
    
    PLAYER {
        uuid id PK
        string first_name
        string last_name
        string middle_name
        string full_name
        date birth_date
        jsonb contact_info
        jsonb additional_info
        text health_notes
        uuid created_by_user_id FK
        uuid created_by_fund_id FK
        timestamp created_at
        timestamp updated_at
    }
    
    PLAYER_NICKNAME {
        uuid id PK
        uuid player_id FK
        string nickname
        string room
        string discipline
        timestamp created_at
        timestamp updated_at
    }
    
    PLAYER_CONTACT {
        uuid id PK
        uuid player_id FK
        string type
        string value
        text description
        timestamp created_at
        timestamp updated_at
    }
    
    PLAYER_LOCATION {
        uuid id PK
        uuid player_id FK
        string country
        string city
        text address
        timestamp created_at
        timestamp updated_at
    }
    
    PLAYER_PAYMENT_METHOD {
        uuid id PK
        uuid player_id FK
        string type
        string value
        text description
        timestamp created_at
        timestamp updated_at
    }
    
    PLAYER_SOCIAL_MEDIA {
        uuid id PK
        uuid player_id FK
        string type
        string value
        text description
        timestamp created_at
        timestamp updated_at
    }
    
    CASE {
        uuid id PK
        uuid player_id FK
        string title
        text description
        string status
        string arbitrage_type
        decimal arbitrage_amount
        string arbitrage_currency
        uuid created_by_user_id FK
        uuid created_by_fund_id FK
        timestamp closed_at
        uuid closed_by_user_id FK
        timestamp created_at
        timestamp updated_at
    }
    
    CASE_EVIDENCE {
        uuid id PK
        uuid case_id FK
        string type
        text description
        string file_path
        uuid uploaded_by_id FK
        timestamp created_at
    }
    
    CASE_COMMENT {
        uuid id PK
        uuid case_id FK
        text comment
        uuid created_by_id FK
        timestamp created_at
    }
    
    FUND ||--o{ USER : "has"
    USER ||--o{ PLAYER : "creates"
    FUND ||--o{ PLAYER : "created by"
    PLAYER ||--o{ PLAYER_NICKNAME : "has"
    PLAYER ||--o{ PLAYER_CONTACT : "has"
    PLAYER ||--o{ PLAYER_LOCATION : "has"
    PLAYER ||--o{ PLAYER_PAYMENT_METHOD : "has"
    PLAYER ||--o{ PLAYER_SOCIAL_MEDIA : "has"
    PLAYER ||--o{ CASE : "has"
    CASE ||--o{ CASE_EVIDENCE : "has"
    CASE ||--o{ CASE_COMMENT : "has"
    USER ||--o{ CASE : "creates"
    FUND ||--o{ CASE : "created by"
    USER ||--o{ CASE_EVIDENCE : "uploads"
    USER ||--o{ CASE_COMMENT : "creates"
```

Данная диаграмма показывает все основные сущности системы и их связи:

1. **Fund (Фонд)** - базовая организационная единица
2. **User (Пользователь)** - пользователи системы, привязанные к фондам
3. **Player (Игрок)** - информация об игроках
4. **PlayerNickname/Contact/Location/PaymentMethod/SocialMedia** - связанная информация о игроках
5. **Case (Дело)** - дела, связанные с игроками
6. **CaseEvidence (Доказательства)** - доказательства, прикрепленные к делам
7. **CaseComment (Комментарии)** - комментарии к делам

## Основные отношения

- Фонд может иметь множество пользователей
- Пользователь может создавать игроков и дела
- Игрок может иметь множество связанных данных (ники, контакты, локации и т.д.)
- Дело связано с одним игроком, но у игрока может быть множество дел
- К делу можно прикреплять доказательства и комментарии

## Изоляция данных

Важным аспектом системы является изоляция данных между фондами. Это реализовано через:

1. Привязку пользователей к фондам (поле `fund_id` в таблице `USER`)
2. Сохранение информации о создателе для каждого игрока и дела (поля `created_by_user_id` и `created_by_fund_id`)
3. Программную проверку принадлежности всех сущностей к фонду текущего пользователя при доступе к данным

## Изменения в схеме

Последние изменения в схеме базы данных:

1. Добавлены поля для структурированного имени игрока (`first_name`, `last_name`, `middle_name`)
2. Добавлено поле `health_notes` для хранения заметок о здоровье игрока
3. Добавлены таблицы для методов оплаты (`PLAYER_PAYMENT_METHOD`) и социальных сетей (`PLAYER_SOCIAL_MEDIA`)
4. Добавлены поля для информации об арбитраже в таблице `CASE` (`arbitrage_type`, `arbitrage_amount`, `arbitrage_currency`)
5. Добавлено поле `description` в таблицу `CASE_EVIDENCE`
6. Создана новая таблица `CASE_COMMENT` для комментариев к делам 