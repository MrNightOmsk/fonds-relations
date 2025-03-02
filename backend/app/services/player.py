from typing import List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.player import Player, PlayerContact, PlayerLocation, PlayerNickname
from app.models.case import Case
from app.schemas.player import PlayerCreate, PlayerUpdate
from app.services import audit


def get(db: Session, player_id: UUID) -> Optional[Player]:
    return (
        db.query(Player)
        .options(
            joinedload(Player.contacts),
            joinedload(Player.locations),
            joinedload(Player.nicknames),
        )
        .filter(Player.id == player_id)
        .first()
    )


def get_by_nickname(db: Session, room: str, nickname: str) -> Optional[Player]:
    return (
        db.query(Player)
        .join(Player.nicknames)
        .filter(
            PlayerNickname.room == room,
            PlayerNickname.nickname == nickname,
            PlayerNickname.is_active == True,
        )
        .first()
    )


def get_multi(
    db: Session, skip: int = 0, limit: int = 100, created_by_id: Optional[UUID] = None
) -> List[Player]:
    query = db.query(Player).options(
        joinedload(Player.contacts),
        joinedload(Player.locations),
        joinedload(Player.nicknames),
    )
    
    if created_by_id:
        query = query.filter(Player.created_by_id == created_by_id)
    
    return query.offset(skip).limit(limit).all()


def create(db: Session, obj_in: PlayerCreate, created_by_id: UUID) -> Player:
    db_obj = Player(
        full_name=obj_in.full_name,
        created_by_id=created_by_id,
    )
    
    if obj_in.contacts:
        db_obj.contacts = [
            PlayerContact(**contact.model_dump()) for contact in obj_in.contacts
        ]
    
    if obj_in.locations:
        db_obj.locations = [
            PlayerLocation(**location.model_dump()) for location in obj_in.locations
        ]
    
    if obj_in.nicknames:
        db_obj.nicknames = [
            PlayerNickname(**nickname.model_dump()) for nickname in obj_in.nicknames
        ]
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    # Log the creation
    audit.log_action(
        db,
        entity_type="player",
        entity_id=db_obj.id,
        action="create",
        changes=obj_in.model_dump(),
        performed_by_id=created_by_id,
    )
    
    return db_obj


def update(
    db: Session, db_obj: Player, obj_in: PlayerUpdate, updated_by_id: UUID
) -> Player:
    update_data = obj_in.model_dump(exclude_unset=True)
    old_data = {
        "full_name": db_obj.full_name,
        "contacts": [c.model_dump() for c in db_obj.contacts],
        "locations": [l.model_dump() for l in db_obj.locations],
        "nicknames": [n.model_dump() for n in db_obj.nicknames],
    }
    
    # Update main fields
    if "full_name" in update_data:
        db_obj.full_name = update_data["full_name"]
    
    # Update contacts
    if "contacts" in update_data:
        db_obj.contacts = [
            PlayerContact(**contact.model_dump()) for contact in update_data["contacts"]
        ]
    
    # Update locations
    if "locations" in update_data:
        db_obj.locations = [
            PlayerLocation(**location.model_dump()) for location in update_data["locations"]
        ]
    
    # Update nicknames
    if "nicknames" in update_data:
        db_obj.nicknames = [
            PlayerNickname(**nickname.model_dump()) for nickname in update_data["nicknames"]
        ]
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    # Log the update
    audit.log_action(
        db,
        entity_type="player",
        entity_id=db_obj.id,
        action="update",
        changes={"old": old_data, "new": update_data},
        performed_by_id=updated_by_id,
    )
    
    return db_obj


def get_cases_count(db: Session, player_id: UUID) -> int:
    return db.query(func.count(Case.id)).filter(Case.player_id == player_id).scalar()


def get_latest_case_date(db: Session, player_id: UUID) -> Optional[datetime]:
    return (
        db.query(func.max(Case.created_at))
        .filter(Case.player_id == player_id)
        .scalar()
    ) 