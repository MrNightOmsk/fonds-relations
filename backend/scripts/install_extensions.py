import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def install_extensions():
    try:
        # Подключаемся к базе данных fonds_relations
        conn = psycopg2.connect(
            dbname="fonds_relations",
            user="postgres",
            password="Brintarok38eg",
            host="localhost",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Создаем курсор
        cur = conn.cursor()
        
        # Устанавливаем расширение pg_trgm
        cur.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
        print("Расширение pg_trgm успешно установлено!")
        
        # Закрываем соединение
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    install_extensions() 