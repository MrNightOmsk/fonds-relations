FROM python:3.9

WORKDIR /app

# Установка зависимостей
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . /app

# Создание необходимых директорий
RUN python setup.py

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 