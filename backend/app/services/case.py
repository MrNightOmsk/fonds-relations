from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.case import Case, CaseEvidence
from app.schemas.case import CaseCreate, CaseUpdate
from app.services import audit, notification


def get(db: Session, case_id: UUID) -> Optional[Case]:
    return (
        db.query(Case)
        .options(joinedload(Case.evidences))
        .filter(Case.id == case_id)
        .first()
    )


def get_multi(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    player_id: Optional[UUID] = None,
    reported_by_id: Optional[UUID] = None,
) -> List[Case]:
    query = db.query(Case).options(joinedload(Case.evidences))
    
    if player_id:
        query = query.filter(Case.player_id == player_id)
    
    if reported_by_id:
        query = query.filter(Case.reported_by_id == reported_by_id)
    
    return query.offset(skip).limit(limit).all()


def create(db: Session, obj_in: CaseCreate, reported_by_id: UUID) -> Case:
    db_obj = Case(
        player_id=obj_in.player_id,
        reported_by_id=reported_by_id,
        type=obj_in.type,
        description=obj_in.description,
        amount=obj_in.amount,
        status=obj_in.status,
    )
    
    if obj_in.evidences:
        db_obj.evidences = [
            CaseEvidence(**{
                **evidence.model_dump(),
                "uploaded_by_id": reported_by_id
            })
            for evidence in obj_in.evidences
        ]
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    # Log the creation
    audit.log_action(
        db,
        entity_type="case",
        entity_id=db_obj.id,
        action="create",
        changes=obj_in.model_dump(),
        performed_by_id=reported_by_id,
    )
    
    # Send notifications
    notification.send_new_case_notification(db, db_obj)
    
    return db_obj


def update(
    db: Session, db_obj: Case, obj_in: CaseUpdate, updated_by_id: UUID
) -> Case:
    update_data = obj_in.model_dump(exclude_unset=True)
    old_data = {
        "type": db_obj.type,
        "description": db_obj.description,
        "amount": str(db_obj.amount) if db_obj.amount else None,
        "status": db_obj.status,
        "evidences": [e.model_dump() for e in db_obj.evidences],
    }
    
    # Update main fields
    for field in ["type", "description", "amount", "status"]:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    # Update evidences
    if "evidences" in update_data:
        db_obj.evidences = [
            CaseEvidence(**{
                **evidence.model_dump(),
                "uploaded_by_id": updated_by_id
            })
            for evidence in update_data["evidences"]
        ]
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    # Log the update
    audit.log_action(
        db,
        entity_type="case",
        entity_id=db_obj.id,
        action="update",
        changes={"old": old_data, "new": update_data},
        performed_by_id=updated_by_id,
    )
    
    # Send notifications if status changed
    if "status" in update_data and update_data["status"] != old_data["status"]:
        notification.send_case_status_notification(db, db_obj)
    
    return db_obj 