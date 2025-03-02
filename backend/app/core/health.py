from typing import Dict

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from app.db.session import SessionLocal


async def check_db_status() -> bool:
    """
    Проверяет состояние подключения к базе данных
    """
    try:
        db = SessionLocal()
        # Простой запрос для проверки соединения
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except SQLAlchemyError:
        return False


async def get_health_status() -> Dict[str, bool]:
    """
    Возвращает статус всех сервисов
    """
    return {
        "api_status": True,  # API работает, если мы можем выполнить этот запрос
        "db_status": await check_db_status()
    } 