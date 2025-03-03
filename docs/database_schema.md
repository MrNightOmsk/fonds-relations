# Схема базы данных

## Сущности

### Fund (Фонд)
```sql
CREATE TABLE fund (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### User (Пользователь)
```sql
CREATE TABLE "user" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    fund_id UUID REFERENCES fund(id),
    role VARCHAR(50) NOT NULL, -- admin, manager
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Player (Игрок)
```sql
CREATE TABLE player (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    birth_date DATE,
    contact_info JSONB,  -- телефон, email, другие контакты
    additional_info JSONB,  -- дополнительная информация
    created_by_user_id UUID REFERENCES "user"(id),
    created_by_fund_id UUID REFERENCES fund(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Case (Дело/Кейс)
```sql
CREATE TABLE case (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL REFERENCES player(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL,  -- open, closed
    created_by_user_id UUID REFERENCES "user"(id),
    created_by_fund_id UUID REFERENCES fund(id),
    closed_at TIMESTAMP WITH TIME ZONE,
    closed_by_user_id UUID REFERENCES "user"(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Связи между сущностями

1. **Fund -> User**: One-to-Many
   - Фонд может иметь множество пользователей
   - Каждый пользователь принадлежит только одному фонду

2. **User -> Player**: One-to-Many (created_by)
   - Пользователь может создать множество игроков
   - Каждый игрок создан одним пользователем

3. **Fund -> Player**: One-to-Many (created_by)
   - Фонд может создать множество игроков
   - Каждый игрок привязан к одному фонду-создателю

4. **Player -> Case**: One-to-Many
   - Игрок может иметь множество кейсов
   - Каждый кейс принадлежит только одному игроку

5. **User -> Case**: One-to-Many (created_by)
   - Пользователь может создать множество кейсов
   - Каждый кейс создан одним пользователем

6. **Fund -> Case**: One-to-Many (created_by)
   - Фонд может создать множество кейсов
   - Каждый кейс привязан к одному фонду-создателю

## Права доступа

### Администратор фонда может:
- Управлять пользователями своего фонда
- Создавать/редактировать/просматривать все записи своего фонда
- Закрывать кейсы
- Просматривать статистику по фонду

### Менеджер фонда может:
- Создавать игроков
- Создавать кейсы для игроков
- Просматривать и редактировать кейсы своего фонда
- Просматривать игроков и их историю

## Бизнес-правила

1. **Создание пользователей**:
   - Только администраторы фонда могут создавать новых пользователей
   - Пользователь всегда привязан к конкретному фонду

2. **Работа с игроками**:
   - Игрок может быть создан любым пользователем фонда
   - При создании игрока автоматически фиксируется создавший фонд

3. **Работа с кейсами**:
   - Кейс не может существовать без привязки к игроку
   - Кейс наследует фонд от создавшего пользователя
   - Закрытый кейс нельзя редактировать
   - При закрытии кейса фиксируется время и пользователь

4. **Доступ к данным**:
   - Пользователи видят только данные своего фонда
   - История действий фиксируется в аудит-логе 