from typing import Any, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Case])
def read_cases(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve cases.
    """
    cases = crud.case.get_multi(db, skip=skip, limit=limit)
    return cases


@router.post("/", response_model=schemas.Case)
def create_case(
    *,
    db: Session = Depends(deps.get_db),
    case_in: schemas.CaseCreate,
    player_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new case.
    """
    player = crud.player.get(db=db, id=player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    case = crud.case.create_with_player(db=db, obj_in=case_in, player_id=player_id)
    return case


@router.put("/{case_id}", response_model=schemas.Case)
def update_case(
    *,
    db: Session = Depends(deps.get_db),
    case_id: int,
    case_in: schemas.CaseUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a case.
    """
    case = crud.case.get(db=db, id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    case = crud.case.update(db=db, db_obj=case, obj_in=case_in)
    return case


@router.get("/{case_id}", response_model=schemas.Case)
def read_case(
    *,
    db: Session = Depends(deps.get_db),
    case_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get case by ID.
    """
    case = crud.case.get(db=db, id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.delete("/{case_id}", response_model=schemas.Case)
def delete_case(
    *,
    db: Session = Depends(deps.get_db),
    case_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a case.
    """
    case = crud.case.get(db=db, id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    case = crud.case.remove(db=db, id=case_id)
    return case


@router.get("/by-player/{player_id}", response_model=List[schemas.Case])
def read_cases_by_player(
    *,
    db: Session = Depends(deps.get_db),
    player_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cases by player ID.
    """
    cases = crud.case.get_multi_by_player(
        db=db, player_id=player_id, skip=skip, limit=limit
    )
    return cases


@router.get("/by-status/{status}", response_model=List[schemas.Case])
def read_cases_by_status(
    *,
    db: Session = Depends(deps.get_db),
    status: str,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cases by status.
    """
    cases = crud.case.get_by_status(db=db, status=status, skip=skip, limit=limit)
    return cases


@router.put("/{case_id}/status", response_model=schemas.Case)
def update_case_status(
    *,
    db: Session = Depends(deps.get_db),
    case_id: int,
    status: str,
    notes: str = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update case status.
    """
    case = crud.case.get(db=db, id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    case = crud.case.update_status(db=db, db_obj=case, status=status, notes=notes)
    return case


@router.get("/by-date-range/", response_model=List[schemas.Case])
def read_cases_by_date_range(
    *,
    db: Session = Depends(deps.get_db),
    start_date: datetime,
    end_date: datetime,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get cases by date range.
    """
    cases = crud.case.get_by_date_range(
        db=db, start_date=start_date, end_date=end_date, skip=skip, limit=limit
    )
    return cases 