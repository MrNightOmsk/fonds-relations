from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, constr

from .base import BaseSchema, TimestampedSchema

class UserBase(BaseSchema):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    organization: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str
    full_name: str
    organization: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: str
    
    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: int 