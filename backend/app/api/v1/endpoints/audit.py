from typing import Any, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.AuditLog])
def read_audit_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve audit logs.
    """
    logs = crud.audit.get_multi(db, skip=skip, limit=limit)
    return logs


@router.post("/", response_model=schemas.AuditLog)
def create_audit_log(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int,
    details: dict = None,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new audit log.
    """
    log = crud.audit.create_log(
        db=db,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )
    return log


@router.get("/by-user/{user_id}", response_model=List[schemas.AuditLog])
def read_user_audit_logs(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get audit logs by user ID.
    """
    logs = crud.audit.get_by_user(db=db, user_id=user_id, skip=skip, limit=limit)
    return logs


@router.get("/by-entity/{entity_type}/{entity_id}", response_model=List[schemas.AuditLog])
def read_entity_audit_logs(
    *,
    db: Session = Depends(deps.get_db),
    entity_type: str,
    entity_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get audit logs by entity type and ID.
    """
    logs = crud.audit.get_by_entity(
        db=db,
        entity_type=entity_type,
        entity_id=entity_id,
        skip=skip,
        limit=limit
    )
    return logs


@router.get("/by-action/{action}", response_model=List[schemas.AuditLog])
def read_action_audit_logs(
    *,
    db: Session = Depends(deps.get_db),
    action: str,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get audit logs by action.
    """
    logs = crud.audit.get_by_action(db=db, action=action, skip=skip, limit=limit)
    return logs


@router.get("/by-date-range/", response_model=List[schemas.AuditLog])
def read_date_range_audit_logs(
    *,
    db: Session = Depends(deps.get_db),
    start_date: datetime,
    end_date: datetime,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get audit logs by date range.
    """
    logs = crud.audit.get_by_date_range(
        db=db,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    return logs 