from typing import List, Optional, Union, Dict, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerUpdate


class CRUDPlayer(CRUDBase[Player, PlayerCreate, PlayerUpdate]):
    def create_with_fund(
        self, db: Session, *, obj_in: PlayerCreate, fund_id: int
    ) -> Player:
        obj_in_data = obj_in.model_dump()
        db_obj = Player(**obj_in_data, fund_id=fund_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_fund(
        self, db: Session, *, fund_id: int, skip: int = 0, limit: int = 100
    ) -> List[Player]:
        return (
            db.query(self.model)
            .filter(Player.fund_id == fund_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Player]:
        return (
            db.query(self.model)
            .filter(
                (Player.name.ilike(f"%{query}%")) |
                (Player.nickname.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


player = CRUDPlayer(Player) 