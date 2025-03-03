FROM python:3.9

WORKDIR /app/

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . /app/

# Добавляем пакет alembic, если его нет в requirements.txt
RUN pip install --no-cache-dir alembic psycopg2-binary

# Делаем скрипт запуска исполняемым
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"] 