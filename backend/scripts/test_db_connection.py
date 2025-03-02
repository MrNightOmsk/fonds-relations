import psycopg2
from urllib.parse import quote_plus
from app.core.config import settings

def test_connection():
    try:
        # Экранируем специальные символы в пароле
        password = quote_plus(settings.POSTGRES_PASSWORD)
        
        conn = psycopg2.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=password,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT
        )
        print("Подключение к базе данных успешно установлено!")
        
        # Проверяем версию PostgreSQL
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()
        print(f"Версия PostgreSQL: {version[0]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {str(e)}")

if __name__ == "__main__":
    test_connection() 