# FondsRelations Backend

## Локальное развертывание

1. Склонируйте репозиторий:
```bash
git clone <your-repository-url>
cd backend
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```
Отредактируйте `.env` файл, установив свои значения для переменных окружения.

3. Запустите проект с помощью Docker:
```bash
docker-compose up --build
```

## Развертывание на сервере

1. Подключитесь к серверу по SSH:
```bash
ssh user@your-server
```

2. Установите Docker и docker-compose, если они еще не установлены:
```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. Склонируйте репозиторий:
```bash
git clone <your-repository-url>
cd backend
```

4. Создайте и настройте `.env` файл:
```bash
cp .env.example .env
nano .env  # или vim .env
```

5. Запустите проект:
```bash
docker-compose up -d --build
```

## Структура проекта

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py
│   │       └── endpoints/
│   │           ├── login.py
│   │           └── users.py
│   ├── core/
│   │   └── config.py
│   ├── crud/
│   ├── db/
│   ├── email-templates/
│   │   └── build/
│   │       ├── new_account.html
│   │       └── reset_password.html
│   ├── models/
│   ├── schemas/
│   └── utils.py
├── docker-compose.yml    # Конфигурация Docker
├── Dockerfile           # Инструкции сборки образа
├── .env.example        # Пример переменных окружения
├── .gitignore         # Игнорируемые Git файлы
├── requirements.txt   # Зависимости Python
├── setup.py          # Скрипт настройки проекта
└── README.md         # Документация
```

## Конфигурация

Основные настройки проекта находятся в файле `.env`. Вы можете изменить следующие параметры:

### Основные настройки
- `PROJECT_NAME`: Название проекта
- `SERVER_HOST`: URL сервера

### База данных
- `POSTGRES_SERVER`: Хост базы данных
- `POSTGRES_USER`: Пользователь PostgreSQL
- `POSTGRES_PASSWORD`: Пароль PostgreSQL
- `POSTGRES_DB`: Имя базы данных

### Почтовый сервер
- `SMTP_TLS`: Использование TLS
- `SMTP_PORT`: Порт SMTP сервера
- `SMTP_HOST`: Хост SMTP сервера
- `SMTP_USER`: Email пользователя
- `SMTP_PASSWORD`: Пароль от почты

### Безопасность
- `SECRET_KEY`: Секретный ключ для JWT
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Время жизни токена доступа
- `EMAIL_RESET_TOKEN_EXPIRE_HOURS`: Время жизни токена сброса пароля

## Разработка

### Добавление новых зависимостей

1. Добавьте зависимость в `requirements.txt`
2. Пересоберите контейнер:
```bash
docker-compose up -d --build
```

### Обновление базы данных

При изменении моделей:
1. Создайте новую миграцию:
```bash
docker-compose exec backend alembic revision --autogenerate -m "описание изменений"
```

2. Примените миграции:
```bash
docker-compose exec backend alembic upgrade head
```

## Мониторинг

### Просмотр логов
```bash
# Все логи
docker-compose logs

# Логи конкретного сервиса
docker-compose logs backend
docker-compose logs db

# Логи в реальном времени
docker-compose logs -f
```

## Дополнительная информация

- Проект использует FastAPI для создания API
- PostgreSQL в качестве базы данных
- Jinja2 для шаблонов email-сообщений
- Docker и docker-compose для контейнеризации
- JWT для аутентификации
- Alembic для миграций базы данных 