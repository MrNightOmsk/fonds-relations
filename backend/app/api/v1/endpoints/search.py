from typing import Any, List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from app.api import deps
from app.models import User
from app.models.player import Player
from app.services.search import search_service
from app.schemas.player import PlayerSearchResult
from app import crud
from app.utils.logger import logger

router = APIRouter()


class UnifiedSearchResult(BaseModel):
    players: List[PlayerSearchResult] = []
    cases: List[Any] = []
    total_players: int = 0
    total_cases: int = 0


@router.get("/unified", response_model=UnifiedSearchResult)
async def unified_search(
    *,
    query: str = Query(..., description="Поисковый запрос"),
    room: Optional[str] = Query(None, description="Фильтр по покерной комнате"),
    discipline: Optional[str] = Query(None, description="Фильтр по дисциплине"),
    skip: int = Query(0, description="Количество результатов для пропуска"),
    limit: int = Query(10, description="Максимальное количество результатов"),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Унифицированный поиск по игрокам, кейсам и другим сущностям.
    """
    try:
        # Проверяем длину запроса
        query = query.strip()
        if len(query) < 2:
            logger.warning(f"Слишком короткий поисковый запрос: '{query}'")
            return UnifiedSearchResult(
                players=[],
                total_players=0,
                cases=[],
                total_cases=0
            )
            
        # Поиск игроков
        logger.info(f"Выполняется поиск для запроса: '{query}'")
        players = await search_service.search_players(
            query=query,
            room=room,
            discipline=discipline,
            skip=skip,
            limit=limit
        )
        
        logger.info(f"Найдено {len(players)} игроков по запросу '{query}'")
        
        # В будущем здесь можно добавить поиск по другим сущностям
        
        return UnifiedSearchResult(
            players=players,
            total_players=len(players),  # В будущем можно получать общее количество из ES
            cases=[],  # Пока заглушка для кейсов
            total_cases=0
        )
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Ошибка при поиске: {error_msg}")
        
        # Если это ошибка с Elasticsearch, возвращаем более информативное сообщение
        if "ConnectionError" in error_msg:
            raise HTTPException(
                status_code=503,
                detail=f"Поисковый сервис временно недоступен. Пожалуйста, повторите запрос позже."
            )
        
        # Если это ошибка с индексом "no such index" - предлагаем инициализировать индекс
        if "index_not_found_exception" in error_msg.lower():
            logger.warning("Поисковый индекс не найден. Возвращаем пустой результат.")
            return UnifiedSearchResult(
                players=[],
                total_players=0,
                cases=[],
                total_cases=0
            )
            
        # Если это ошибка с маппингом или типами полей
        if "illegal_argument_exception" in error_msg.lower() or "search_phase_execution_exception" in error_msg.lower():
            # Вернуть пустой результат вместо ошибки, чтобы не блокировать работу приложения
            logger.warning(f"Проблема со структурой индекса: {error_msg}. Возвращаем пустой результат.")
            return UnifiedSearchResult(
                players=[],
                total_players=0,
                cases=[],
                total_cases=0
            )
            
        # Для всех остальных ошибок
        logger.warning(f"Непредвиденная ошибка поиска: {error_msg}. Возвращаем пустой результат.")
        return UnifiedSearchResult(
            players=[],
            total_players=0,
            cases=[],
            total_cases=0
        )


@router.post("/init", status_code=200)
async def initialize_search_index(
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Инициализирует индекс Elasticsearch. Требуются права администратора.
    """
    try:
        await search_service.create_index()
        return {"status": "success", "message": "Индекс успешно создан"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка инициализации индекса: {str(e)}")


@router.delete("/delete-index", status_code=200)
async def delete_search_index(
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Удаляет индекс Elasticsearch. Требуются права администратора.
    Внимание: эта операция приведет к потере всех данных поискового индекса!
    """
    try:
        # Проверяем существование индекса перед удалением
        if await search_service.es.indices.exists(index=search_service.index_name):
            await search_service.es.indices.delete(index=search_service.index_name)
            logger.info(f"Индекс {search_service.index_name} успешно удален")
            return {"status": "success", "message": f"Индекс {search_service.index_name} успешно удален"}
        else:
            logger.info(f"Индекс {search_service.index_name} не существует")
            return {"status": "warning", "message": f"Индекс {search_service.index_name} не существует"}
    except Exception as e:
        logger.error(f"Ошибка при удалении индекса: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка удаления индекса: {str(e)}")


@router.post("/index-players", status_code=200)
async def index_all_players(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Количество игроков для пропуска"),
    limit: int = Query(100, description="Максимальное количество игроков для индексации"),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Индексирует игроков в Elasticsearch. Требуются права администратора.
    """
    try:
        # Получаем игроков из базы данных
        players = crud.player.get_multi(db, skip=skip, limit=limit)
        
        # Индексируем каждого игрока
        indexed_count = 0
        for player in players:
            await search_service.index_player(player)
            indexed_count += 1
        
        return {
            "status": "success", 
            "message": f"Успешно проиндексировано {indexed_count} игроков",
            "indexed_count": indexed_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка индексации игроков: {str(e)}")


@router.post("/index-all-players", status_code=200)
async def index_all_players_batched(
    *,
    db: Session = Depends(deps.get_db),
    batch_size: int = Query(100, description="Размер партии игроков для индексации"),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Индексирует всех игроков в Elasticsearch в нескольких партиях. Требуются права администратора.
    """
    try:
        # Получаем общее количество игроков
        total_players = db.query(Player).count()
        
        # Индексируем игроков партиями
        total_indexed = 0
        failed_count = 0
        
        for offset in range(0, total_players, batch_size):
            try:
                # Получаем текущую партию игроков
                players = (
                    db.query(Player)
                    .options(
                        # Загружаем связанные данные для предотвращения множества запросов
                        joinedload(Player.contacts),
                        joinedload(Player.locations),
                        joinedload(Player.nicknames),
                        joinedload(Player.cases),
                        joinedload(Player.created_by_fund)
                    )
                    .offset(offset)
                    .limit(batch_size)
                    .all()
                )
                
                # Индексируем каждого игрока в партии
                batch_indexed = 0
                for player in players:
                    try:
                        await search_service.index_player(player)
                        batch_indexed += 1
                    except Exception as player_error:
                        # Логируем ошибку, но продолжаем для других игроков
                        logger.error(f"Ошибка при индексации игрока {player.id}: {str(player_error)}")
                        failed_count += 1
                
                total_indexed += batch_indexed
                logger.info(f"Партия {offset//batch_size + 1}: проиндексировано {batch_indexed} игроков")
                
            except Exception as batch_error:
                # Логируем ошибку партии, но продолжаем для следующих партий
                logger.error(f"Ошибка при индексации партии, начиная с {offset}: {str(batch_error)}")
        
        # Формируем сообщение о результатах
        message = f"Всего проиндексировано {total_indexed} игроков из {total_players}"
        if failed_count > 0:
            message += f" (не удалось проиндексировать {failed_count} игроков)"
        
        return {
            "status": "success", 
            "message": message,
            "indexed_count": total_indexed,
            "total_count": total_players,
            "failed_count": failed_count
        }
    except Exception as e:
        logger.error(f"Общая ошибка индексации: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка индексации игроков: {str(e)}")


@router.post("/index-player/{player_id}", status_code=200)
async def index_player(
    *,
    db: Session = Depends(deps.get_db),
    player_id: UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Индексирует отдельного игрока в Elasticsearch.
    """
    try:
        # Получаем игрока из базы данных
        player = crud.player.get(db, id=player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Игрок не найден")
        
        # Проверка прав доступа - только админ может индексировать игроков других фондов
        if current_user.role != "admin" and player.created_by_fund_id != current_user.fund_id:
            raise HTTPException(status_code=403, detail="Недостаточно прав")
        
        # Индексируем игрока
        await search_service.index_player(player)
        
        return {
            "status": "success", 
            "message": f"Игрок {player.full_name} успешно проиндексирован",
            "player_id": str(player.id)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка индексации игрока: {str(e)}") 