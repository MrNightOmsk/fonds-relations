import psycopg2

def test_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='postgres',  # пробуем подключиться к стандартной базе
            user='postgres',      # используем стандартного пользователя
            password='Brintarok38eg'   # обновленный пароль
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
        print(f"Тип ошибки: {type(e)}")
        if hasattr(e, 'pgcode'):
            print(f"Код ошибки PostgreSQL: {e.pgcode}")
        if hasattr(e, 'pgerror'):
            print(f"Сообщение об ошибке PostgreSQL: {e.pgerror}")

if __name__ == "__main__":
    test_connection() 