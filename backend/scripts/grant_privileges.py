import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def grant_privileges():
    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='fonds_relations',
            user='postgres',
            password='Brintarok38eg'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cur = conn.cursor()
        
        # Даем права на схему public
        cur.execute('GRANT ALL ON SCHEMA public TO fond_dbuser')
        print("Права на схему public выданы!")
        
        # Даем права на все будущие таблицы
        cur.execute('ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO fond_dbuser')
        print("Права на будущие таблицы выданы!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Ошибка при выдаче прав: {str(e)}")
        print(f"Тип ошибки: {type(e)}")

if __name__ == "__main__":
    grant_privileges() 