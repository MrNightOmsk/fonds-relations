FROM python:3.9

WORKDIR /app

# Установка зависимостей
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Установка netstat для диагностики
RUN apt-get update && apt-get install -y net-tools && apt-get clean

# Копирование кода приложения
COPY . /app

# Создание необходимых директорий
RUN python setup.py

# Делаем start.sh исполняемым
RUN chmod +x /app/start.sh
# Принудительно устанавливаем права на выполнение и записываем дополнительную информацию
RUN ls -la /app/start.sh && chmod 755 /app/start.sh && echo "Permissions set for start.sh"

# Создаем запасную команду для запуска приложения с расширенной диагностикой
RUN echo '#!/bin/bash\necho "Running backup script..."\necho "Current directory: $(pwd)"\necho "Files in current directory:"\nls -la\necho "Environment variables:"\necho "POSTGRES_SERVER: $POSTGRES_SERVER"\necho "POSTGRES_PORT: $POSTGRES_PORT"\necho "POSTGRES_USER: $POSTGRES_USER"\necho "POSTGRES_DB: $POSTGRES_DB"\necho "ELASTICSEARCH_HOST: $ELASTICSEARCH_HOST"\necho "ELASTICSEARCH_PORT: $ELASTICSEARCH_PORT"\necho "Waiting for database and Elasticsearch to be ready..."\npython wait_for_services.py\necho "Database and Elasticsearch are ready."\necho "Applying migrations..."\nalembic upgrade head\necho "Migrations applied successfully."\necho "Starting FastAPI application..."\nuvicorn app.main:app --host 0.0.0.0 --port 8000 --reload-exclude ".*" --reload-include "*.py"' > /app/backup_start.sh
RUN chmod 755 /app/backup_start.sh

# Запуск приложения через start.sh
# Если start.sh не выполняется, то используем запасной вариант
CMD (bash -c /app/start.sh) || (echo "start.sh failed, using backup script" && bash -c /app/backup_start.sh) 