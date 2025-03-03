import asyncio
import sys
from asyncpg import connect, CannotConnectNowError
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError as ESConnectionError

async def wait_for_postgres(host: str, port: int, user: str, password: str, database: str, max_attempts: int = 60):
    attempt = 0
    last_exception = None
    
    # Сначала подключаемся к postgres для создания базы данных
    while attempt < max_attempts:
        try:
            conn = await connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database='postgres'
            )
            
            # Проверяем существует ли база данных
            exists = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1",
                database
            )
            
            if not exists:
                # Создаем базу если её нет
                await conn.execute(f'CREATE DATABASE {database}')
                print(f"Database {database} created successfully")
            
            await conn.close()
            
            # Теперь подключаемся к созданной базе данных
            conn = await connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            
            # Проверяем существует ли таблица fund
            table_exists = await conn.fetchval(
                "SELECT 1 FROM information_schema.tables WHERE table_name = 'fund' AND table_schema = 'public'"
            )
            
            if table_exists:
                print("Таблица fund найдена, выполняем миграцию для переименования в funds...")
                # Переименовываем таблицу fund в funds
                await conn.execute("ALTER TABLE IF EXISTS fund RENAME TO funds")
                # Обновляем первичный ключ
                await conn.execute("ALTER INDEX IF EXISTS fund_pkey RENAME TO funds_pkey")
                # Обновляем уникальный индекс на name, если он существует
                await conn.execute("ALTER INDEX IF EXISTS fund_name_key RENAME TO funds_name_key")
                
                # Обновляем внешние ключи в других таблицах
                fk_tables = ['users', 'players', 'cases']
                for table in fk_tables:
                    table_exists = await conn.fetchval(
                        f"SELECT 1 FROM information_schema.tables WHERE table_name = '{table}' AND table_schema = 'public'"
                    )
                    if table_exists:
                        constraints = await conn.fetch(
                            f"SELECT conname FROM pg_constraint WHERE conrelid = '{table}'::regclass AND contype = 'f' AND confrelid = 'funds'::regclass"
                        )
                        for constraint in constraints:
                            await conn.execute(f"ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {constraint['conname']}")
                
                print("Миграция успешно выполнена")
            
            await conn.close()
            print("Successfully connected to PostgreSQL")
            return
        except (CannotConnectNowError, OSError) as e:
            last_exception = e
            print(f"Attempt {attempt + 1}/{max_attempts} failed to connect to PostgreSQL: {str(e)}")
            await asyncio.sleep(1)
            attempt += 1
    
    print(f"Could not connect to PostgreSQL after {max_attempts} attempts")
    print(f"Last exception: {str(last_exception)}")
    sys.exit(1)

async def wait_for_elasticsearch(host: str, port: int, max_attempts: int = 60):
    attempt = 0
    last_exception = None
    
    while attempt < max_attempts:
        try:
            es = AsyncElasticsearch([{'host': host, 'port': port, 'scheme': 'http'}])
            await es.ping()
            print("Successfully connected to Elasticsearch")
            await es.close()
            return
        except ESConnectionError as e:
            last_exception = e
            print(f"Attempt {attempt + 1}/{max_attempts} failed to connect to Elasticsearch: {str(e)}")
            await asyncio.sleep(1)
            attempt += 1
    
    print(f"Could not connect to Elasticsearch after {max_attempts} attempts")
    print(f"Last exception: {str(last_exception)}")
    sys.exit(1)

async def main():
    # Параметры подключения из переменных окружения
    pg_host = 'db'
    pg_port = 5432
    pg_user = 'postgres'
    pg_password = 'postgres'
    pg_database = 'test_fonds_relations'
    
    es_host = 'elasticsearch'
    es_port = 9200
    
    await asyncio.gather(
        wait_for_postgres(pg_host, pg_port, pg_user, pg_password, pg_database),
        wait_for_elasticsearch(es_host, es_port)
    )
    print("All services are ready!")

if __name__ == '__main__':
    asyncio.run(main()) 