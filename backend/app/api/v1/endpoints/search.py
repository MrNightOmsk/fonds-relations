from typing import Any, List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api import deps
from app.models import User
from app.services.search import search_service
from app.schemas.player import PlayerSearchResult
from app import crud

router = APIRouter()


class UnifiedSearchResult(BaseModel):
    players: List[PlayerSearchResult]
    total_players: int


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
        # Поиск игроков
        players = await search_service.search_players(
            query=query,
            room=room,
            discipline=discipline,
            skip=skip,
            limit=limit
        )
        
        # В будущем здесь можно добавить поиск по другим сущностям
        
        return UnifiedSearchResult(
            players=players,
            total_players=len(players)  # В будущем можно получать общее количество из ES
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")


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