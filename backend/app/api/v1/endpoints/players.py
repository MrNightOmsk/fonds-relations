from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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


@router.post("/", response_model=schemas.Player)
def create_player(
    *,
    db: Session = Depends(deps.get_db),
    player_in: schemas.PlayerCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new player.
    """
    player = crud.player.create_with_details(db=db, obj_in=player_in)
    return player


@router.put("/{player_id}", response_model=schemas.Player)
def update_player(
    *,
    db: Session = Depends(deps.get_db),
    player_id: int,
    player_in: schemas.PlayerUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a player.
    """
    player = crud.player.get(db=db, id=player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player = crud.player.update_with_details(db=db, db_obj=player, obj_in=player_in)
    return player


@router.get("/{player_id}", response_model=schemas.Player)
def read_player(
    *,
    db: Session = Depends(deps.get_db),
    player_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get player by ID.
    """
    player = crud.player.get(db=db, id=player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.delete("/{player_id}", response_model=schemas.Player)
def delete_player(
    *,
    db: Session = Depends(deps.get_db),
    player_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a player.
    """
    player = crud.player.get(db=db, id=player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player = crud.player.remove(db=db, id=player_id)
    return player


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