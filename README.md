# Fonds Relations

Система обмена информацией о недобросовестных игроках между покерными фондами.

## Версия
- Backend: 0.3.13
- Frontend: 0.3.1

## О проекте

Fonds Relations - это современная веб-платформа, разработанная для покерных фондов с целью обмена информацией о недобросовестных игроках (арбитражниках). Система предоставляет удобный интерфейс для добавления, поиска и управления информацией об игроках, а также API для интеграции с внешними системами.

## Основные возможности

- 🔍 Продвинутый поиск игроков с поддержкой Elasticsearch
- 📝 Управление данными об игроках и историей изменений
- 🔐 Система аутентификации и авторизации
- 🔄 REST API для интеграции
- 📱 Адаптивный современный интерфейс

## Технологии

### Backend
- FastAPI
- PostgreSQL
- Elasticsearch
- SQLAlchemy
- Alembic
- Poetry

### Frontend
- Vue 3
- TypeScript
- Vite
- Pinia
- Tailwind CSS

## Документация

- [Требования к проекту](docs/PROJECT_REQUIREMENTS.md)
- [Рекомендации по разработке](docs/DEVELOPMENT_GUIDELINES.md)
- [Схема базы данных](docs/DATABASE_SCHEMA.md)
- [Диаграмма базы данных](docs/DATABASE_DIAGRAM.md)
- [Документация по API](docs/API_DOCUMENTATION.md)
- [Сетевая конфигурация и решение проблем](docs/NETWORK_CONFIGURATION.md)
- [API документация (Swagger UI)](http://localhost:8000/docs)
- [API документация (ReDoc)](http://localhost:8000/redoc)

## Установка и запуск

### Backend

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
.\venv\Scripts\activate  # Windows

# Установка зависимостей
poetry install

# Применение миграций
alembic upgrade head

# Запуск сервера
uvicorn app.main:app --reload
```

### Frontend

```bash
# Установка зависимостей
npm install

# Запуск dev сервера
npm run dev

# Сборка для production
npm run build
```

## Настройка Git

Для работы с репозиторием используется SSH-подключение. Чтобы настроить:

1. Создайте SSH-ключ:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. Добавьте публичный ключ в GitHub (Settings -> SSH and GPG keys)

3. Клонируйте репозиторий:
```bash
git clone git@github.com:MrNightOmsk/fonds-relations.git
```

## Лицензия

MIT 