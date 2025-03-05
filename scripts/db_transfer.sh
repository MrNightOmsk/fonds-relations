#!/bin/bash

# Скрипт для переноса базы данных из локального Docker на боевой сервер
# Использование: ./db_transfer.sh [server_ip] [ssh_user]

# Проверяем наличие аргументов
if [ "$#" -lt 2 ]; then
    echo "Использование: $0 [server_ip] [ssh_user]"
    echo "Пример: $0 123.45.67.89 root"
    exit 1
fi

SERVER_IP=$1
SSH_USER=$2

echo "=== Начинаю процесс переноса базы данных ==="
echo "Сервер: $SERVER_IP"
echo "Пользователь: $SSH_USER"

# 1. Создаем дамп локальной базы данных
echo "=== Создаю дамп локальной базы данных ==="
docker-compose ps
DB_CONTAINER=$(docker-compose ps | grep db | awk '{print $1}')

if [ -z "$DB_CONTAINER" ]; then
    echo "Ошибка: Контейнер с базой данных не найден!"
    exit 1
fi

echo "Найден контейнер базы данных: $DB_CONTAINER"
echo "Создаю дамп базы данных..."
docker exec $DB_CONTAINER pg_dump -U postgres -d app -F c -f /tmp/db_backup.dump

# 2. Копируем дамп из контейнера на локальную машину
echo "=== Копирую дамп на локальную машину ==="
docker cp $DB_CONTAINER:/tmp/db_backup.dump ./db_backup.dump

if [ ! -f "./db_backup.dump" ]; then
    echo "Ошибка: Не удалось скопировать файл дампа из контейнера!"
    exit 1
fi

echo "Дамп базы данных создан: $(ls -lh db_backup.dump)"

# 3. Копируем дамп на сервер
echo "=== Копирую дамп на сервер ==="
scp ./db_backup.dump $SSH_USER@$SERVER_IP:/tmp/db_backup.dump

echo "=== Проверяю состояние CI/CD процесса на сервере ==="
ssh $SSH_USER@$SERVER_IP "cd /var/www/fonds-relations && docker ps"

echo ""
echo "=== Дамп базы данных успешно перенесен на сервер ==="
echo "Путь к дампу на сервере: /tmp/db_backup.dump"
echo ""
echo "При следующем запуске CI/CD процесса база данных будет автоматически восстановлена из дампа."
echo "Если вы хотите запустить процесс восстановления немедленно, выполните следующую команду:"
echo "  ssh $SSH_USER@$SERVER_IP \"cd /var/www/fonds-relations && git pull\"" 