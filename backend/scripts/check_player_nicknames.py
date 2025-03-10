#!/usr/bin/env python
import logging
import os
import sys
from typing import List, Dict, Any, Optional

# Добавляем корневую директорию в путь, чтобы импортировать модули приложения
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import crud, models, schemas
from app.api import deps
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("check_players.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_player_nicknames(db: Session) -> Dict[str, int]:
    """
    Проверяет наличие никнеймов у игроков в базе данных
    """
    # Получаем количество игроков
    total_players = db.query(models.Player).count()
    logger.info(f"Всего найдено {total_players} игроков в базе данных")
    
    # Получаем количество никнеймов
    total_nicknames = db.query(models.PlayerNickname).count()
    logger.info(f"Всего найдено {total_nicknames} никнеймов в базе данных")
    
    # Проверяем, сколько игроков имеют никнеймы
    # Используем нативный SQL для более эффективного запроса
    result = db.execute(text("""
        SELECT COUNT(DISTINCT player_id) 
        FROM player_nicknames
    """))
    players_with_nicknames = result.scalar()
    
    # Проверяем, сколько игроков не имеют никнеймов
    players_without_nicknames = total_players - players_with_nicknames
    
    logger.info(f"Игроков с никнеймами: {players_with_nicknames}")
    logger.info(f"Игроков без никнеймов: {players_without_nicknames}")
    
    # Вычисляем процент игроков без никнеймов
    if total_players > 0:
        percentage_without_nicknames = (players_without_nicknames / total_players) * 100
        logger.info(f"Процент игроков без никнеймов: {percentage_without_nicknames:.2f}%")
    
    return {
        "total_players": total_players,
        "total_nicknames": total_nicknames,
        "players_with_nicknames": players_with_nicknames,
        "players_without_nicknames": players_without_nicknames
    }

def check_database_tables(db: Session) -> None:
    """
    Проверяет наличие и структуру таблиц в базе данных
    """
    # Проверяем таблицу players
    try:
        result = db.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'players'
        """))
        columns = result.fetchall()
        logger.info(f"Таблица 'players' содержит {len(columns)} колонок:")
        for column in columns:
            logger.info(f"  - {column[0]}: {column[1]}")
    except Exception as e:
        logger.error(f"Ошибка при проверке таблицы 'players': {str(e)}")
    
    # Проверяем таблицу player_nicknames
    try:
        result = db.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'player_nicknames'
        """))
        columns = result.fetchall()
        logger.info(f"Таблица 'player_nicknames' содержит {len(columns)} колонок:")
        for column in columns:
            logger.info(f"  - {column[0]}: {column[1]}")
    except Exception as e:
        logger.error(f"Ошибка при проверке таблицы 'player_nicknames': {str(e)}")

def check_example_players(db: Session, limit: int = 5) -> None:
    """
    Проверяет примеры игроков и их никнеймы
    """
    # Получаем несколько игроков с никнеймами
    players_with_nicknames = db.query(models.Player) \
        .join(models.PlayerNickname) \
        .distinct(models.Player.id) \
        .limit(limit) \
        .all()
    
    if players_with_nicknames:
        logger.info(f"Найдено {len(players_with_nicknames)} игроков с никнеймами:")
        for player in players_with_nicknames:
            nicknames = db.query(models.PlayerNickname) \
                .filter(models.PlayerNickname.player_id == player.id) \
                .all()
            logger.info(f"Игрок: {player.full_name} (ID: {player.id})")
            logger.info(f"  Никнеймы ({len(nicknames)}):")
            for nickname in nicknames:
                logger.info(f"    - {nickname.nickname} (Рум: {nickname.room}, Дисциплина: {nickname.discipline})")
    else:
        logger.warning("Не найдено игроков с никнеймами")
    
    # Получаем несколько игроков без никнеймов
    players_without_nicknames_query = db.query(models.Player) \
        .outerjoin(models.PlayerNickname) \
        .filter(models.PlayerNickname.id == None) \
        .limit(limit)
    
    players_without_nicknames = players_without_nicknames_query.all()
    
    if players_without_nicknames:
        logger.info(f"Найдено {len(players_without_nicknames)} игроков без никнеймов:")
        for player in players_without_nicknames:
            # Проверяем наличие никнеймов в поле additional_info
            additional_info = player.additional_info
            if additional_info and 'nickname' in str(additional_info).lower():
                logger.info(f"Игрок: {player.full_name} (ID: {player.id}) - имеет информацию о никнеймах в additional_info: {additional_info}")
            else:
                logger.info(f"Игрок: {player.full_name} (ID: {player.id}) - не имеет никнеймов")
    else:
        logger.warning("Не найдено игроков без никнеймов")

def main():
    # Создаем сессию базы данных
    db = SessionLocal()
    try:
        logger.info("Начинаем проверку игроков и их никнеймов")
        
        # Проверяем структуру таблиц
        check_database_tables(db)
        
        # Проверяем статистику никнеймов
        stats = check_player_nicknames(db)
        
        # Если есть игроки, проверяем примеры
        if stats["total_players"] > 0:
            check_example_players(db)
        
        logger.info("Проверка завершена")
    finally:
        db.close()

if __name__ == "__main__":
    main() 