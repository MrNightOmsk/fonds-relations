from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Fund])
def read_funds(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve funds."""
    funds = crud.fund.get_multi(db, skip=skip, limit=limit)
    return funds

@router.post("/", response_model=schemas.Fund)
def create_fund(
    *,
    db: Session = Depends(deps.get_db),
    fund_in: schemas.FundCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new fund."""
    fund = crud.fund.create_with_owner(
        db=db, obj_in=fund_in, owner_id=current_user.id
    )
    return fund

@router.get("/{id}", response_model=schemas.Fund)
def read_fund(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get fund by ID."""
    fund = crud.fund.get(db=db, id=id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund 