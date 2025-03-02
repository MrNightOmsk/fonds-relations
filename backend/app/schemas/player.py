from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


# Contact schemas
class PlayerContactBase(BaseModel):
    contact_type: str
    contact_value: str
    is_verified: bool = False


class PlayerContactCreate(PlayerContactBase):
    pass


class PlayerContactUpdate(PlayerContactBase):
    pass


class PlayerContact(PlayerContactBase):
    id: UUID
    player_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Location schemas
class PlayerLocationBase(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    is_verified: bool = False


class PlayerLocationCreate(PlayerLocationBase):
    pass


class PlayerLocationUpdate(PlayerLocationBase):
    pass


class PlayerLocation(PlayerLocationBase):
    id: UUID
    player_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Nickname schemas
class PlayerNicknameBase(BaseModel):
    room: str
    nickname: str
    discipline: Optional[str] = None
    is_active: bool = True


class PlayerNicknameCreate(PlayerNicknameBase):
    pass


class PlayerNicknameUpdate(PlayerNicknameBase):
    pass


class PlayerNickname(PlayerNicknameBase):
    id: UUID
    player_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Player schemas
class PlayerBase(BaseModel):
    full_name: str


class PlayerCreate(PlayerBase):
    contacts: Optional[List[PlayerContactCreate]] = None
    locations: Optional[List[PlayerLocationCreate]] = None
    nicknames: Optional[List[PlayerNicknameCreate]] = None


class PlayerUpdate(PlayerBase):
    contacts: Optional[List[PlayerContactUpdate]] = None
    locations: Optional[List[PlayerLocationUpdate]] = None
    nicknames: Optional[List[PlayerNicknameUpdate]] = None


class Player(PlayerBase):
    id: UUID
    created_by_id: UUID
    created_at: datetime
    updated_at: datetime
    contacts: List[PlayerContact] = []
    locations: List[PlayerLocation] = []
    nicknames: List[PlayerNickname] = []

    class Config:
        from_attributes = True


# Search result schema
class PlayerSearchResult(BaseModel):
    id: UUID
    full_name: str
    nicknames: List[PlayerNickname]
    cases_count: int
    latest_case_date: Optional[datetime]

    class Config:
        from_attributes = True 