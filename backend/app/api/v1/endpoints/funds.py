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
    """
    Retrieve funds.
    """
    if current_user.role != "admin":
        # Если пользователь не админ, возвращаем только его фонд
        return [crud.fund.get(db=db, id=current_user.fund_id)]
    return crud.fund.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Fund)
def create_fund(
    *,
    db: Session = Depends(deps.get_db),
    fund_in: schemas.FundCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new fund.
    """
    fund = crud.fund.get_by_name(db=db, name=fund_in.name)
    if fund:
        raise HTTPException(
            status_code=400,
            detail="The fund with this name already exists in the system.",
        )
    fund = crud.fund.create(db=db, obj_in=fund_in)
    return fund


@router.get("/{fund_id}", response_model=schemas.Fund)
def read_fund(
    *,
    db: Session = Depends(deps.get_db),
    fund_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get fund by ID.
    """
    fund = crud.fund.get(db=db, id=fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    if current_user.role != "admin" and current_user.fund_id != fund_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return fund


@router.put("/{fund_id}", response_model=schemas.Fund)
def update_fund(
    *,
    db: Session = Depends(deps.get_db),
    fund_id: int,
    fund_in: schemas.FundUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update fund.
    """
    fund = crud.fund.get(db=db, id=fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    fund = crud.fund.update(db=db, db_obj=fund, obj_in=fund_in)
    return fund


@router.delete("/{fund_id}", response_model=schemas.Fund)
def delete_fund(
    *,
    db: Session = Depends(deps.get_db),
    fund_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete fund.
    """
    fund = crud.fund.get(db=db, id=fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    # Проверяем, есть ли пользователи в фонде
    if fund.users:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete fund with active users",
        )
    fund = crud.fund.remove(db=db, id=fund_id)
    return fund 