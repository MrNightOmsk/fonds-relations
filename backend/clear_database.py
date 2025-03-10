#!/usr/bin/env python
"""
Скрипт для очистки базы данных.
Удаляет всех игроков, кейсы и связанные с ними данные.
"""

import os
import sys
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Получение параметров подключения из переменных окружения или использование значений по умолчанию
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Строка подключения к базе данных
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

def wait_for_db(max_retries=30, retry_interval=2):
    """Ожидание готовности базы данных."""
    print(f"Подключение к базе данных: {DATABASE_URL}")
    retries = 0
    while retries < max_retries:
        try:
            engine = create_engine(DATABASE_URL)
            connection = engine.connect()
            connection.close()
            print("Успешное подключение к PostgreSQL!")
            return engine
        except OperationalError as e:
            retries += 1
            print(f"Не удалось подключиться к базе данных (попытка {retries}/{max_retries}): {e}")
            if retries < max_retries:
                print(f"Повторная попытка через {retry_interval} секунд...")
                time.sleep(retry_interval)
            else:
                print("Превышено максимальное количество попыток. Выход.")
                sys.exit(1)

def clear_database(engine):
    """Очистка базы данных от игроков и кейсов."""
    with engine.connect() as connection:
        # Начинаем транзакцию
        trans = connection.begin()
        try:
            # Сначала получаем количество записей для отчета
            player_count = connection.execute(text("SELECT COUNT(*) FROM players")).scalar()
            case_count = connection.execute(text("SELECT COUNT(*) FROM cases")).scalar()
            
            print(f"Перед очисткой: {player_count} игроков, {case_count} кейсов")
            
            # Сначала удаляем связанные данные
            print("Удаление связанных данных...")
            
            # Удаление связанных с cases данных
            connection.execute(text("DELETE FROM case_comments"))
            connection.execute(text("DELETE FROM case_evidences"))
            connection.execute(text("DELETE FROM case_logs"))
            connection.execute(text("DELETE FROM case_history"))
            connection.execute(text("DELETE FROM case_actions"))
            
            # Удаление связанных с players данных
            connection.execute(text("DELETE FROM player_aliases"))
            connection.execute(text("DELETE FROM player_contacts"))
            connection.execute(text("DELETE FROM player_nicknames"))
            connection.execute(text("DELETE FROM player_notes"))
            
            # Теперь удаляем основные таблицы
            print("Удаление кейсов...")
            connection.execute(text("DELETE FROM cases"))
            
            print("Удаление игроков...")
            connection.execute(text("DELETE FROM players"))
            
            # Очистка поискового индекса в Elasticsearch (это не часть транзакции БД)
            print("Очистка поискового индекса выполняется отдельно")
            
            # Получаем количество записей после очистки для проверки
            player_count_after = connection.execute(text("SELECT COUNT(*) FROM players")).scalar()
            case_count_after = connection.execute(text("SELECT COUNT(*) FROM cases")).scalar()
            
            # Проверяем результаты
            if player_count_after == 0 and case_count_after == 0:
                print("Успешно удалены все данные!")
                print(f"После очистки: {player_count_after} игроков, {case_count_after} кейсов")
                trans.commit()
            else:
                print(f"ВНИМАНИЕ: Остались записи после очистки! Игроков: {player_count_after}, Кейсов: {case_count_after}")
                trans.rollback()
                return False
            
            return True
        except Exception as e:
            print(f"Ошибка при очистке базы данных: {e}")
            trans.rollback()
            return False

if __name__ == "__main__":
    print("Запуск скрипта очистки базы данных...")
    
    # Ожидание готовности базы данных
    engine = wait_for_db()
    
    # Предупреждение и подтверждение
    print("\n" + "!"*80)
    print("ВНИМАНИЕ! Этот скрипт удалит ВСЕХ игроков и ВСЕ кейсы из базы данных!")
    print("Эта операция НЕ МОЖЕТ БЫТЬ ОТМЕНЕНА!")
    print("!"*80 + "\n")
    
    # Поскольку скрипт запускается в контейнере, мы можем пропустить запрос подтверждения
    # и просто выполнить очистку
    success = clear_database(engine)
    
    if success:
        print("База данных успешно очищена!")
    else:
        print("Произошла ошибка при очистке базы данных.")
        sys.exit(1)
    
    print("Скрипт завершен.") 