"""
Скрипт для индексации игроков в Elasticsearch.
Запускать из корневой директории проекта:
python -m backend.index_players
"""

import asyncio
import logging
from typing import List

from sqlalchemy.orm import Session, joinedload

from app.db.session import SessionLocal
from app.models.player import Player
from app.services.search import search_service

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Количество игроков для индексации за один раз
BATCH_SIZE = 100


async def index_players(players: List[Player]) -> int:
    """Индексирует список игроков в Elasticsearch."""
    indexed_count = 0
    for player in players:
        try:
            await search_service.index_player(player)
            indexed_count += 1
            if indexed_count % 10 == 0:
                logger.info(f"Проиндексировано {indexed_count} игроков")
        except Exception as e:
            logger.error(f"Ошибка при индексации игрока {player.id}: {str(e)}")
    return indexed_count


async def main():
    """Основная функция для индексации всех игроков."""
    # Создаем индекс, если он не существует
    logger.info("Создание индекса...")
    await search_service.create_index()
    logger.info("Индекс создан")

    # Получаем общее количество игроков
    db = SessionLocal()
    try:
        total_players = db.query(Player).count()
        logger.info(f"Всего игроков: {total_players}")

        # Индексируем игроков пакетами
        offset = 0
        total_indexed = 0

        while offset < total_players:
            logger.info(f"Индексация игроков {offset}-{offset + BATCH_SIZE}...")
            players = (
                db.query(Player)
                .options(
                    # Загружаем связанные данные
                    joinedload(Player.contacts),
                    joinedload(Player.locations),
                    joinedload(Player.nicknames),
                    joinedload(Player.cases)
                )
                .offset(offset)
                .limit(BATCH_SIZE)
                .all()
            )
            
            indexed = await index_players(players)
            total_indexed += indexed
            
            offset += BATCH_SIZE
            logger.info(f"Проиндексировано {indexed} игроков в текущем пакете")
            logger.info(f"Всего проиндексировано: {total_indexed}")
    
    finally:
        db.close()
        await search_service.close()
    
    logger.info(f"Индексация завершена. Всего проиндексировано: {total_indexed} игроков")


if __name__ == "__main__":
    asyncio.run(main()) 