from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.case import Case, CaseEvidence, CaseComment
from app.schemas.case import CaseCreate, CaseUpdate


class CRUDCase(CRUDBase[Case, CaseCreate, CaseUpdate]):
    def create_with_player(
        self, db: Session, *, obj_in: CaseCreate, player_id: UUID, user_id: UUID, fund_id: UUID
    ) -> Case:
        obj_in_data = obj_in.model_dump()
        obj_in_data["player_id"] = player_id
        obj_in_data["created_by_user_id"] = user_id
        obj_in_data["created_by_fund_id"] = fund_id
        obj_in_data["created_at"] = datetime.utcnow()
        obj_in_data["updated_at"] = datetime.utcnow()
        db_obj = Case(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_comment(
        self, db: Session, *, case_id: UUID, comment_text: str, user_id: UUID
    ) -> CaseComment:
        db_obj = CaseComment(
            case_id=case_id,
            comment=comment_text,
            created_by_id=user_id,
            created_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_evidence(
        self, db: Session, *, case_id: UUID, evidence_type: str, file_path: str, 
        description: Optional[str], user_id: UUID
    ) -> CaseEvidence:
        db_obj = CaseEvidence(
            case_id=case_id,
            type=evidence_type,
            file_path=file_path,
            description=description,
            uploaded_by_id=user_id,
            created_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_player(
        self, db: Session, *, player_id: UUID, skip: int = 0, limit: int = 100
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

    def get_comments(
        self, db: Session, *, case_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[CaseComment]:
        return (
            db.query(CaseComment)
            .filter(CaseComment.case_id == case_id)
            .order_by(CaseComment.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_evidences(
        self, db: Session, *, case_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[CaseEvidence]:
        return (
            db.query(CaseEvidence)
            .filter(CaseEvidence.case_id == case_id)
            .order_by(CaseEvidence.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


case = CRUDCase(Case) 