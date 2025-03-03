from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


# Общие атрибуты
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    fund_id: Optional[UUID] = None
    role: Optional[str] = None
    is_active: Optional[bool] = True


# Свойства для создания
class UserCreate(UserBase):
    email: EmailStr
    password: str
    fund_id: UUID
    role: str


# Свойства для обновления
class UserUpdate(UserBase):
    password: Optional[str] = None


# Свойства для чтения
class UserInDBBase(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str 