from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.arbitrage import crud_arbitrage_case
from app.schemas.arbitrage import (
    ArbitrageCase,
    ArbitrageCaseCreate,
    ArbitrageCaseUpdate,
    ArbitrageCaseSearch
)
from app.schemas.auth import User

router = APIRouter()

@router.post("/", response_model=ArbitrageCase)
def create_arbitrage_case(
    *,
    db: Session = Depends(get_db),
    case_in: ArbitrageCaseCreate,
    current_user: User = Depends(get_current_user)
) -> ArbitrageCase:
    """
    Создать новый арбитражный случай.
    """
    case = crud_arbitrage_case.create_with_relations(
        db=db, obj_in=case_in, author_id=current_user.id
    )
    return case

@router.get("/", response_model=List[ArbitrageCase])
def search_arbitrage_cases(
    *,
    db: Session = Depends(get_db),
    query: Optional[str] = None,
    types: Optional[List[str]] = Query(None),
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    amount_from: Optional[float] = None,
    amount_to: Optional[float] = None,
    rooms: Optional[List[UUID]] = Query(None),
    disciplines: Optional[List[UUID]] = Query(None),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
) -> List[ArbitrageCase]:
    """
    Поиск арбитражных случаев с фильтрацией.
    """
    search_params = ArbitrageCaseSearch(
        query=query or "",
        types=types,
        date_from=date_from,
        date_to=date_to,
        amount_from=amount_from,
        amount_to=amount_to,
        rooms=rooms,
        disciplines=disciplines
    )
    cases = crud_arbitrage_case.search(
        db=db, search=search_params, skip=skip, limit=limit
    )
    return cases

@router.get("/{case_id}", response_model=ArbitrageCase)
def get_arbitrage_case(
    case_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ArbitrageCase:
    """
    Получить арбитражный случай по ID.
    """
    case = crud_arbitrage_case.get(db=db, id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Арбитражный случай не найден")
    return case

@router.put("/{case_id}", response_model=ArbitrageCase)
def update_arbitrage_case(
    *,
    db: Session = Depends(get_db),
    case_id: UUID,
    case_in: ArbitrageCaseUpdate,
    current_user: User = Depends(get_current_user)
) -> ArbitrageCase:
    """
    Обновить арбитражный случай.
    """
    case = crud_arbitrage_case.get(db=db, id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Арбитражный случай не найден")
    case = crud_arbitrage_case.update(db=db, db_obj=case, obj_in=case_in)
    return case

@router.delete("/{case_id}", response_model=ArbitrageCase)
def delete_arbitrage_case(
    *,
    db: Session = Depends(get_db),
    case_id: UUID,
    current_user: User = Depends(get_current_user)
) -> ArbitrageCase:
    """
    Удалить арбитражный случай.
    """
    case = crud_arbitrage_case.get(db=db, id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Арбитражный случай не найден")
    case = crud_arbitrage_case.remove(db=db, id=case_id)
    return case 