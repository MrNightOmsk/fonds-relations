from typing import Any, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.Player])
def read_players(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve players.
    """
    players = crud.player.get_multi(db, skip=skip, limit=limit)
    return players


@router.post("/", response_model=schemas.Player, status_code=201)
def create_player(
    *,
    db: Session = Depends(deps.get_db),
    player_in: schemas.PlayerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new player.
    """
    # Проверка имени
    if not player_in.full_name or player_in.full_name.strip() == "":
        raise HTTPException(status_code=422, detail="Player name cannot be empty")
    
    # Проверка даты рождения
    if player_in.birth_date:
        from datetime import date
        today = date.today()
        if player_in.birth_date > today:
            raise HTTPException(status_code=422, detail="Birth date cannot be in the future")
    
    # Проверка валидности данных контактной информации
    if player_in.contact_info:
        if "phone" in player_in.contact_info and not is_valid_phone(player_in.contact_info["phone"]):
            raise HTTPException(status_code=422, detail="Invalid phone number format")
        if "email" in player_in.contact_info and not is_valid_email(player_in.contact_info["email"]):
            raise HTTPException(status_code=422, detail="Invalid email format")
    
    # Создание копии входных данных и добавление информации о пользователе/фонде
    player_in_data = jsonable_encoder(player_in)
    player_create = schemas.PlayerCreate(**player_in_data)
    player_create.created_by_user_id = current_user.id
    player_create.created_by_fund_id = current_user.fund_id
    
    player = crud.player.create_with_details(db=db, obj_in=player_create)
    return player

# Вспомогательные функции для валидации
def is_valid_phone(phone: str) -> bool:
    """Проверка формата телефонного номера"""
    import re
    pattern = r'^\+?[0-9]{10,15}$'
    return bool(re.match(pattern, phone))

def is_valid_email(email: str) -> bool:
    """Проверка формата email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


@router.put("/{player_id}", response_model=schemas.Player)
def update_player(
    *,
    db: Session = Depends(deps.get_db),
    player_id: uuid.UUID,
    player_in: schemas.PlayerUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a player.
    """
    try:
        player_id_uuid = uuid.UUID(str(player_id))
        player = crud.player.get(db=db, id=player_id_uuid)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        player = crud.player.update_with_details(db=db, db_obj=player, obj_in=player_in)
        return player
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid player ID format")


@router.get("/{player_id}", response_model=schemas.Player)
def read_player(
    *,
    db: Session = Depends(deps.get_db),
    player_id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get player by ID.
    """
    try:
        import logging
        logger = logging.getLogger("app")
        
        player_id_uuid = uuid.UUID(str(player_id))
        player = crud.player.get(db=db, id=player_id_uuid)
        if not player:
            logger.error(f"Player not found: {player_id}")
            raise HTTPException(status_code=404, detail="Player not found")
        
        # Логирование для отладки
        logger.info(f"Current user role: {current_user.role}, fund_id: {current_user.fund_id}")
        logger.info(f"Player created_by_fund_id: {player.created_by_fund_id}")
            
        # Проверяем принадлежность игрока к фонду пользователя
        if current_user.role != "admin" and player.created_by_fund_id != current_user.fund_id:
            logger.error(f"Access denied: current_user.fund_id={current_user.fund_id}, player.created_by_fund_id={player.created_by_fund_id}")
            raise HTTPException(status_code=404, detail="Player not found")
            
        return player
    except ValueError:
        logger.error(f"Invalid player ID format: {player_id}")
        raise HTTPException(status_code=422, detail="Invalid player ID format")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{player_id}", status_code=204)
def delete_player(
    *,
    db: Session = Depends(deps.get_db),
    player_id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> None:
    """
    Delete a player.
    """
    try:
        player_id_uuid = uuid.UUID(str(player_id))
        player = crud.player.get(db=db, id=player_id_uuid)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        crud.player.remove(db=db, id=player_id_uuid)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid player ID format")


@router.get("/by-nickname/{nickname}", response_model=schemas.Player)
def read_player_by_nickname(
    *,
    db: Session = Depends(deps.get_db),
    nickname: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get player by nickname.
    """
    player = crud.player.get_by_nickname(db=db, nickname=nickname)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/by-contact/{contact_type}/{contact_value}", response_model=schemas.Player)
def read_player_by_contact(
    *,
    db: Session = Depends(deps.get_db),
    contact_type: str,
    contact_value: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get player by contact information.
    """
    player = crud.player.get_by_contact(
        db=db, contact_type=contact_type, contact_value=contact_value
    )
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/by-location/{country}", response_model=List[schemas.Player])
def read_players_by_location(
    *,
    db: Session = Depends(deps.get_db),
    country: str,
    city: Optional[str] = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get players by location.
    """
    players = crud.player.get_by_location(db=db, country=country, city=city)
    return players 