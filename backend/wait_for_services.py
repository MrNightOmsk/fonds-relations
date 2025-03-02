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