#!/usr/bin/env python3
"""
Скрипт для создания стандартных пользователей в системе.
Создает супер-администратора и нескольких менеджеров фондов.
"""

import os
import uuid
import psycopg2
from datetime import datetime
from passlib.context import CryptContext

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для подключения к базе данных
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB", "app"),
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
            host=os.environ.get("POSTGRES_SERVER", "db"),
            port=os.environ.get("POSTGRES_PORT", "5432")
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

# Функция для хеширования пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Функция для проверки существования пользователя
def user_exists(conn, email: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists

# Функция для проверки существования фонда
def fund_exists(conn, fund_name: str) -> str:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM funds WHERE name = %s", (fund_name,))
    fund = cursor.fetchone()
    cursor.close()
    
    if fund:
        return fund[0]
    return None

# Функция для создания фонда
def create_fund(conn, name: str) -> str:
    fund_id = str(uuid.uuid4())
    cursor = conn.cursor()
    now = datetime.utcnow()
    
    cursor.execute(
        "INSERT INTO funds (id, name, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING id",
        (fund_id, name, now, now)
    )
    
    conn.commit()
    cursor.close()
    return fund_id

# Функция для создания пользователя
def create_user(conn, email: str, password: str, full_name: str, fund_id: str, role: str) -> None:
    if user_exists(conn, email):
        print(f"Пользователь {email} уже существует. Пропускаю.")
        return
    
    user_id = str(uuid.uuid4())
    cursor = conn.cursor()
    hashed_password = get_password_hash(password)
    now = datetime.utcnow()
    
    cursor.execute(
        """
        INSERT INTO users 
        (id, email, hashed_password, full_name, fund_id, role, is_active, created_at, updated_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (user_id, email, hashed_password, full_name, fund_id, role, True, now, now)
    )
    
    conn.commit()
    cursor.close()
    print(f"Создан пользователь: {email}, роль: {role}")

# Основная функция
def main():
    conn = get_db_connection()
    if not conn:
        print("Не удалось подключиться к базе данных. Выход.")
        return
    
    try:
        # Создаем фонды если они не существуют
        admin_fund_name = "Главный фонд"
        admin_fund_id = fund_exists(conn, admin_fund_name)
        if not admin_fund_id:
            admin_fund_id = create_fund(conn, admin_fund_name)
            print(f"Создан фонд: {admin_fund_name}")
        
        fund1_name = "Фонд поддержки №1"
        fund1_id = fund_exists(conn, fund1_name)
        if not fund1_id:
            fund1_id = create_fund(conn, fund1_name)
            print(f"Создан фонд: {fund1_name}")
        
        fund2_name = "Фонд поддержки №2"
        fund2_id = fund_exists(conn, fund2_name)
        if not fund2_id:
            fund2_id = create_fund(conn, fund2_name)
            print(f"Создан фонд: {fund2_name}")
        
        # Создаем супер-администратора
        create_user(
            conn=conn,
            email="admin@example.com",
            password="admin123",  # в реальном приложении использовать более сложный пароль
            full_name="Главный Администратор",
            fund_id=admin_fund_id,
            role="admin"
        )
        
        # Создаем менеджеров для разных фондов
        create_user(
            conn=conn,
            email="manager1@example.com",
            password="manager123",
            full_name="Менеджер Фонда 1",
            fund_id=fund1_id,
            role="fund_manager"
        )
        
        create_user(
            conn=conn,
            email="manager2@example.com",
            password="manager123",
            full_name="Менеджер Фонда 2",
            fund_id=fund2_id,
            role="fund_manager"
        )
        
        create_user(
            conn=conn,
            email="manager_admin@example.com",
            password="manager123",
            full_name="Менеджер Главного Фонда",
            fund_id=admin_fund_id,
            role="fund_manager"
        )
        
        print("Инициализация пользователей завершена успешно!")
    
    except Exception as e:
        print(f"Ошибка при инициализации пользователей: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 