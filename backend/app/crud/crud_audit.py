from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.audit import AuditLog
from app.schemas.audit import AuditLogCreate, AuditLogUpdate


class CRUDAudit(CRUDBase[AuditLog, AuditLogCreate, AuditLogUpdate]):
    def create_log(
        self,
        db: Session,
        *,
        user_id: int,
        action: str,
        entity_type: str,
        entity_id: int,
        details: Optional[dict] = None
    ) -> AuditLog:
        db_obj = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            timestamp=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[AuditLog]:
        return (
            db.query(self.model)
            .filter(AuditLog.user_id == user_id)
            .order_by(AuditLog.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_entity(
        self,
        db: Session,
        *,
        entity_type: str,
        entity_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        return (
            db.query(self.model)
            .filter(
                AuditLog.entity_type == entity_type,
                AuditLog.entity_id == entity_id
            )
            .order_by(AuditLog.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_action(
        self, db: Session, *, action: str, skip: int = 0, limit: int = 100
    ) -> List[AuditLog]:
        return (
            db.query(self.model)
            .filter(AuditLog.action == action)
            .order_by(AuditLog.timestamp.desc())
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
    ) -> List[AuditLog]:
        return (
            db.query(self.model)
            .filter(AuditLog.timestamp >= start_date)
            .filter(AuditLog.timestamp <= end_date)
            .order_by(AuditLog.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


audit = CRUDAudit(AuditLog) 