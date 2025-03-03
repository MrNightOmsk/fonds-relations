import asyncio
import sys
import os
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
            
            # Теперь подключаемся к созданной базе данных для проверки соединения
            conn = await connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            
            # Проверяем соединение
            await conn.execute("SELECT 1")
            await conn.close()
            
            print("Successfully connected to PostgreSQL")
            
            # Миграции Alembic будут запущены отдельно в start.sh
            return
        except (CannotConnectNowError, OSError) as e:
            last_exception = e
            print(f"Attempt {attempt + 1}/{max_attempts} failed to connect to PostgreSQL: {str(e)}")
            await asyncio.sleep(1)
            attempt += 1
    
    # Если мы здесь, то все попытки подключения не удались
    print(f"Failed to connect to PostgreSQL after {max_attempts} attempts")
    print(f"Last exception: {str(last_exception)}")
    sys.exit(1)


async def wait_for_elasticsearch(host: str, port: int, max_attempts: int = 60):
    attempt = 0
    last_exception = None
    
    while attempt < max_attempts:
        try:
            es = AsyncElasticsearch([f"http://{host}:{port}"])
            await es.info()
            await es.close()
            print("Successfully connected to Elasticsearch")
            return
        except ESConnectionError as e:
            last_exception = e
            print(f"Attempt {attempt + 1}/{max_attempts} failed to connect to Elasticsearch: {str(e)}")
            await asyncio.sleep(1)
            attempt += 1
    
    # Если мы здесь, то все попытки подключения не удались
    print(f"Failed to connect to Elasticsearch after {max_attempts} attempts")
    print(f"Last exception: {str(last_exception)}")
    sys.exit(1)


async def main():
    # Параметры подключения из переменных окружения
    postgres_host = os.environ.get("POSTGRES_SERVER", "localhost")
    postgres_port = int(os.environ.get("POSTGRES_PORT", "5432"))
    postgres_user = os.environ.get("POSTGRES_USER", "postgres")
    postgres_password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    postgres_db = os.environ.get("POSTGRES_DB", "app")
    
    elasticsearch_host = os.environ.get("ELASTICSEARCH_HOST", "localhost")
    elasticsearch_port = int(os.environ.get("ELASTICSEARCH_PORT", "9200"))
    
    # Ожидание готовности сервисов
    await wait_for_postgres(postgres_host, postgres_port, postgres_user, postgres_password, postgres_db)
    try:
        await wait_for_elasticsearch(elasticsearch_host, elasticsearch_port)
    except Exception as e:
        print(f"Warning: Elasticsearch is not available: {str(e)}")
        print("Continuing without Elasticsearch...")


if __name__ == "__main__":
    asyncio.run(main()) 