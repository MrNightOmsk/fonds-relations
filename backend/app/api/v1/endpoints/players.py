from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Player])
def read_players(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve players."""
    players = crud.player.get_multi(db, skip=skip, limit=limit)
    return players

@router.post("/", response_model=schemas.Player)
def create_player(
    *,
    db: Session = Depends(deps.get_db),
    player_in: schemas.PlayerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new player."""
    player = crud.player.create_with_fund(
        db=db, obj_in=player_in, fund_id=current_user.fund_id
    )
    return player

@router.get("/{id}", response_model=schemas.Player)
def read_player(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get player by ID."""
    player = crud.player.get(db=db, id=id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/search/", response_model=List[schemas.Player])
def search_players(
    *,
    db: Session = Depends(deps.get_db),
    query: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Search players by name or nickname."""
    players = crud.player.search(db=db, query=query)
    return players 