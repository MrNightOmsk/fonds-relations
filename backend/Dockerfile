FROM python:3.9

WORKDIR /app

# Установка зависимостей
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . /app

# Создание необходимых директорий
RUN python setup.py

# Делаем start.sh исполняемым
RUN chmod +x /app/start.sh
# Принудительно устанавливаем права на выполнение и записываем дополнительную информацию
RUN ls -la /app/start.sh && chmod 755 /app/start.sh && echo "Permissions set for start.sh"

# Создаем запасную команду для запуска приложения
RUN echo '#!/bin/bash\npython wait_for_services.py\nalembic upgrade head\nuvicorn app.main:app --host 0.0.0.0 --port 8000 --reload-exclude ".*" --reload-include "*.py"' > /app/backup_start.sh
RUN chmod 755 /app/backup_start.sh

# Запуск приложения через start.sh
# Если start.sh не выполняется, то используем запасной вариант
CMD (bash -c /app/start.sh) || (echo "start.sh failed, using backup script" && bash -c /app/backup_start.sh) 