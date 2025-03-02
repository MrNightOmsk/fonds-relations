from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.case import Case
from app.schemas.case import CaseCreate, CaseUpdate


class CRUDCase(CRUDBase[Case, CaseCreate, CaseUpdate]):
    def create_with_player(
        self, db: Session, *, obj_in: CaseCreate, player_id: int
    ) -> Case:
        obj_in_data = obj_in.dict()
        obj_in_data["player_id"] = player_id
        obj_in_data["created_at"] = datetime.utcnow()
        db_obj = Case(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_player(
        self, db: Session, *, player_id: int, skip: int = 0, limit: int = 100
    ) -> List[Case]:
        return (
            db.query(self.model)
            .filter(Case.player_id == player_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Case]:
        return (
            db.query(self.model)
            .filter(Case.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[Case]:
        return (
            db.query(self.model)
            .filter(Case.created_at >= start_date)
            .filter(Case.created_at <= end_date)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_status(
        self,
        db: Session,
        *,
        db_obj: Case,
        status: str,
        notes: Optional[str] = None
    ) -> Case:
        db_obj.status = status
        if notes:
            db_obj.notes = notes
        db_obj.updated_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


case = CRUDCase(Case) 