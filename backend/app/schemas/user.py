from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Общие атрибуты
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    fund_id: int
    role: str  # admin, manager
    is_active: bool = True


# Свойства для создания
class UserCreate(UserBase):
    password: str


# Свойства для обновления
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


# Свойства для чтения
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Токен
class Token(BaseModel):
    access_token: str
    token_type: str


# Данные в токене
class TokenPayload(BaseModel):
    sub: int  # user_id
    fund_id: int
    role: str 