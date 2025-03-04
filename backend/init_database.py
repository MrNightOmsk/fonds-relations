#!/usr/bin/env python3
"""
Скрипт для ручной инициализации базы данных и создания первого суперпользователя.
Запуск:
    docker exec -it fondsrelations-backend-1 python -m backend.init_database
"""

import logging
from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    """
    Инициализирует базу данных.
    """
    db = SessionLocal()
    try:
        logger.info("Создание начальных данных")
        init_db(db)
        logger.info("Инициализация базы данных завершена")
    finally:
        db.close()


def main() -> None:
    logger.info("Запуск ручной инициализации базы данных")
    init()
    logger.info("Инициализация базы данных успешно завершена")


if __name__ == "__main__":
    main() 