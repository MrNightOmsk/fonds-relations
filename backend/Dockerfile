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

# Запуск приложения через start.sh
CMD ["/app/start.sh"] 