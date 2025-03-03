FROM python:3.9

WORKDIR /app/

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . /app/

# Добавляем пакет alembic, если его нет в requirements.txt
RUN pip install --no-cache-dir alembic psycopg2-binary

# Создаем скрипт для запуска и применения миграций
RUN echo '#!/bin/bash\n\
echo "Waiting for services to be ready..."\n\
python wait_for_services.py\n\
echo "Applying database migrations..."\n\
alembic upgrade head\n\
echo "Starting application..."\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"] 