from typing import List, Optional, Any, Dict, Union
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate


class CRUDRoom(CRUDBase[Room, RoomCreate, RoomUpdate]):
    """
    CRUD for room operations.
    """
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Room]:
        """
        Get room by name.
        """
        return db.query(self.model).filter(self.model.name == name).first()
    
    def create(self, db: Session, *, obj_in: RoomCreate) -> Room:
        """
        Create new room.
        """
        db_obj = Room(
            name=obj_in.name,
            description=obj_in.description,
            logo_url=obj_in.logo_url,
            website=obj_in.website,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: Room, obj_in: Union[RoomUpdate, Dict[str, Any]]
    ) -> Room:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def get_multi_by_active(
        self, db: Session, *, skip: int = 0, limit: int = 100, active_only: bool = True
    ) -> List[Room]:
        query = db.query(self.model)
        if active_only:
            query = query.filter(self.model.is_active == True)
        return query.offset(skip).limit(limit).all()


room = CRUDRoom(Room) 