from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.schemas.audit import AuditLogCreate


def log_action(
    db: Session,
    entity_type: str,
    entity_id: UUID,
    action: str,
    changes: Dict[str, Any],
    performed_by_id: UUID,
) -> AuditLog:
    """
    Log an action in the audit log.
    
    Args:
        db: Database session
        entity_type: Type of entity (player, case, etc.)
        entity_id: ID of the entity
        action: Type of action (create, update, delete)
        changes: Dictionary containing the changes
        performed_by_id: ID of the user who performed the action
    """
    db_obj = AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        changes=changes,
        performed_by_id=performed_by_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_entity_history(
    db: Session,
    entity_type: str,
    entity_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> List[AuditLog]:
    """
    Get the history of changes for a specific entity.
    
    Args:
        db: Database session
        entity_type: Type of entity (player, case, etc.)
        entity_id: ID of the entity
        skip: Number of records to skip
        limit: Maximum number of records to return
    """
    return (
        db.query(AuditLog)
        .filter(AuditLog.entity_type == entity_type, AuditLog.entity_id == entity_id)
        .order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_user_actions(
    db: Session,
    performed_by_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> List[AuditLog]:
    """
    Get all actions performed by a specific user.
    
    Args:
        db: Database session
        performed_by_id: ID of the user
        skip: Number of records to skip
        limit: Maximum number of records to return
    """
    return (
        db.query(AuditLog)
        .filter(AuditLog.performed_by_id == performed_by_id)
        .order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    ) 