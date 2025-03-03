from typing import Any, List
import uuid
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    fund_id: UUID = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    if current_user.role == "admin":
        if fund_id:
            users = crud.user.get_multi_by_fund(db, fund_id=fund_id, skip=skip, limit=limit)
        else:
            users = crud.user.get_multi(db, skip=skip, limit=limit)
    else:
        # Менеджеры могут видеть только пользователей своего фонда
        users = crud.user.get_multi_by_fund(db, fund_id=current_user.fund_id, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User, status_code=201)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    # Проверка формата email
    if "@" not in user_in.email:
        raise HTTPException(
            status_code=422,
            detail="Invalid email format"
        )
    
    # Проверка длины пароля
    if len(user_in.password) < 8:
        raise HTTPException(
            status_code=422,
            detail="Password must be at least 8 characters long"
        )
    
    # Проверка допустимых ролей
    valid_roles = ["admin", "manager"]
    if user_in.role not in valid_roles:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
        )
    
    # Проверка существования фонда
    try:
        fund_id_uuid = uuid.UUID(str(user_in.fund_id))
        fund = crud.fund.get(db=db, id=fund_id_uuid)
        if not fund:
            raise HTTPException(
                status_code=404,
                detail="Fund not found"
            )
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid fund ID format"
        )
    
    # Проверка уникальности email
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists."
        )
    
    user = crud.user.create(db=db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User, status_code=201)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    try:
        user_id_uuid = UUID(str(user_id))
        user = crud.user.get(db, id=user_id_uuid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user == current_user:
            return user
        if not crud.user.is_superuser(current_user):
            raise HTTPException(
                status_code=400, detail="The user doesn't have enough privileges"
            )
        return user
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid user ID format")


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: uuid.UUID,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    try:
        user_id_uuid = uuid.UUID(str(user_id))
        user = crud.user.get(db, id=user_id_uuid)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
            
        # Проверка уникальности email, если он обновляется
        if user_in.email and user_in.email != user.email:
            existing_user = crud.user.get_by_email(db, email=user_in.email)
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="A user with this email already exists."
                )
                
        # Проверка существования фонда, если он обновляется
        if user_in.fund_id:
            try:
                fund_id_uuid = uuid.UUID(str(user_in.fund_id))
                fund = crud.fund.get(db=db, id=fund_id_uuid)
                if not fund:
                    raise HTTPException(
                        status_code=404,
                        detail="Fund not found"
                    )
            except ValueError:
                raise HTTPException(
                    status_code=422,
                    detail="Invalid fund ID format"
                )
                
        user = crud.user.update(db, db_obj=user, obj_in=user_in)
        return user
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid user ID format")


@router.delete("/{user_id}", status_code=204)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> None:
    """
    Delete a user.
    """
    try:
        user_id_uuid = UUID(str(user_id))
        user = crud.user.get(db, id=user_id_uuid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        crud.user.remove(db, id=user_id_uuid)
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid user ID format") 