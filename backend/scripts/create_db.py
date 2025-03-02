import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        # Подключаемся к postgres напрямую
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='postgres',
            user='postgres',
            password='Brintarok38eg'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cur = conn.cursor()
        
        # Проверяем существование базы данных
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'fonds_relations'")
        exists = cur.fetchone()
        
        if not exists:
            # Создаем базу данных
            cur.execute('CREATE DATABASE fonds_relations')
            print("База данных fonds_relations успешно создана!")
        else:
            print("База данных fonds_relations уже существует.")
        
        # Создаем пользователя, если он не существует
        cur.execute("SELECT 1 FROM pg_roles WHERE rolname = 'fond_dbuser'")
        user_exists = cur.fetchone()
        
        if not user_exists:
            cur.execute("CREATE USER fond_dbuser WITH PASSWORD 'testpass123'")
            print("Пользователь fond_dbuser создан!")
        else:
            print("Пользователь fond_dbuser уже существует.")
        
        # Даем права пользователю на базу данных
        cur.execute('GRANT ALL PRIVILEGES ON DATABASE fonds_relations TO fond_dbuser')
        print("Права доступа выданы пользователю fond_dbuser!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Ошибка при создании базы данных: {str(e)}")
        print(f"Тип ошибки: {type(e)}")

if __name__ == "__main__":
    create_database() 