from typing import Any, List, Dict
from uuid import UUID
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


class FundsList(BaseModel):
    funds: List[schemas.Fund]


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
    try:
        result = []
        if current_user.role != "admin":
            # Если пользователь не админ, возвращаем только его фонд
            if current_user.fund_id:
                fund = crud.fund.get(db=db, id=current_user.fund_id)
                if fund:
                    result = [fund]
        else:
            funds = crud.fund.get_multi(db, skip=skip, limit=limit)
            # Проверяем, что все элементы в списке являются объектами Fund
            result = [f for f in funds if f is not None]
        
        # Преобразуем SQLAlchemy объекты в словари для успешной сериализации
        from fastapi.encoders import jsonable_encoder
        return jsonable_encoder(result)
    except Exception as e:
        print(f"Error in read_funds: {str(e)}")
        return []


@router.post("/", response_model=schemas.Fund, status_code=201)
def create_fund(
    *,
    db: Session = Depends(deps.get_db),
    fund_in: schemas.FundCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new fund.
    """
    # Проверка на пустое имя
    if not fund_in.name or fund_in.name.strip() == "":
        raise HTTPException(
            status_code=422,
            detail="Fund name cannot be empty"
        )
        
    # Проверка на существование фонда с таким именем
    fund = crud.fund.get_by_name(db=db, name=fund_in.name)
    if fund:
        raise HTTPException(
            status_code=400,
            detail="Fund with this name already exists."
        )
        
    fund = crud.fund.create(db=db, obj_in=fund_in)
    return fund


@router.get("/{fund_id}", response_model=schemas.Fund)
def read_fund(
    *,
    db: Session = Depends(deps.get_db),
    fund_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get fund by ID.
    """
    try:
        fund_id_uuid = UUID(str(fund_id))
        fund = crud.fund.get(db=db, id=fund_id_uuid)
        if not fund:
            raise HTTPException(status_code=404, detail="Fund not found")
        if current_user.role != "admin" and current_user.fund_id != fund_id_uuid:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return fund
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid fund ID format")


@router.put("/{fund_id}", response_model=schemas.Fund)
def update_fund(
    *,
    db: Session = Depends(deps.get_db),
    fund_id: UUID,
    fund_in: schemas.FundUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update fund.
    """
    try:
        fund_id_uuid = UUID(str(fund_id))
        fund = crud.fund.get(db=db, id=fund_id_uuid)
        if not fund:
            raise HTTPException(status_code=404, detail="Fund not found")
        fund = crud.fund.update(db=db, db_obj=fund, obj_in=fund_in)
        return fund
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid fund ID format")


@router.delete("/{fund_id}", status_code=204)
def delete_fund(
    *,
    db: Session = Depends(deps.get_db),
    fund_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> None:
    """
    Delete a fund.
    """
    try:
        fund_id_uuid = UUID(str(fund_id))
        fund = crud.fund.get(db=db, id=fund_id_uuid)
        if not fund:
            raise HTTPException(status_code=404, detail="Fund not found")
        
        # Проверяем, есть ли пользователи, привязанные к фонду
        users = crud.user.get_multi_by_fund(db=db, fund_id=fund_id_uuid)
        if users:
            raise HTTPException(
                status_code=400, 
                detail="Cannot delete fund with associated users. Remove all users from the fund first."
            )
            
        crud.fund.remove(db=db, id=fund_id_uuid)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid fund ID format")


@router.get("/by-player/{player_id}", response_model=List[schemas.Fund])
def read_funds_by_player(
    *,
    db: Session = Depends(deps.get_db),
    player_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve funds associated with a specific player.
    """
    try:
        # Проверяем, что player_id имеет формат UUID
        player_uuid = uuid.UUID(player_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid player ID format: {player_id}. Must be a valid UUID."
        )
    
    # Проверяем, существует ли игрок
    player = db.query(models.Player).filter(models.Player.id == player_uuid).first()
    if not player:
        raise HTTPException(
            status_code=404,
            detail=f"Player with ID {player_id} not found"
        )
    
    try:
        # Получаем все кейсы, связанные с игроком
        cases = db.query(models.Case).filter(models.Case.player_id == player_uuid).all()
        
        # Собираем уникальные ID фондов из кейсов
        fund_ids = set()
        for case in cases:
            # Используем created_by_fund_id вместо fund_id
            fund_ids.add(case.created_by_fund_id)
        
        # Если нет фондов, возвращаем пустой список
        if not fund_ids:
            return []
        
        # Получаем фонды по собранным ID
        funds = db.query(models.Fund).filter(models.Fund.id.in_(fund_ids)).all()
        
        # Если пользователь не админ, возвращаем только его фонд
        if current_user.role != "admin":
            funds = [fund for fund in funds if fund.id == current_user.fund_id]
        
        return funds
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) 