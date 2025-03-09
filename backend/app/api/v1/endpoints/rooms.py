from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.Room])
def read_rooms(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve rooms.
    """
    rooms = crud.room.get_multi_by_active(
        db, skip=skip, limit=limit, active_only=active_only
    )
    return rooms


@router.post("/", response_model=schemas.Room)
def create_room(
    *,
    db: Session = Depends(deps.get_db),
    room_in: schemas.RoomCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new room.
    """
    room = crud.room.get_by_name(db, name=room_in.name)
    if room:
        raise HTTPException(
            status_code=400,
            detail="The room with this name already exists in the system.",
        )
    room = crud.room.create(db, obj_in=room_in)
    return room


@router.put("/{room_id}", response_model=schemas.Room)
def update_room(
    *,
    db: Session = Depends(deps.get_db),
    room_id: int,
    room_in: schemas.RoomUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a room.
    """
    room = crud.room.get(db, id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room = crud.room.update(db, db_obj=room, obj_in=room_in)
    return room


@router.get("/{room_id}", response_model=schemas.Room)
def read_room(
    *,
    db: Session = Depends(deps.get_db),
    room_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get room by ID.
    """
    room = crud.room.get(db, id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.delete("/{room_id}", response_model=schemas.Room)
def delete_room(
    *,
    db: Session = Depends(deps.get_db),
    room_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a room.
    """
    room = crud.room.get(db, id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room = crud.room.remove(db, id=room_id)
    return room


@router.get("/by-name/{room_name}", response_model=schemas.Room)
def read_room_by_name(
    *,
    db: Session = Depends(deps.get_db),
    room_name: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get room by name.
    """
    room = crud.room.get_by_name(db, name=room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room 