from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID


# Базовые схемы для контактов игрока
class PlayerContactBase(BaseModel):
    type: str
    value: str
    description: Optional[str] = None


class PlayerContactCreate(PlayerContactBase):
    pass


class PlayerContactUpdate(PlayerContactBase):
    pass


class PlayerContact(PlayerContactBase):
    id: UUID
    player_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Базовые схемы для местоположения игрока
class PlayerLocationBase(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None


class PlayerLocationCreate(PlayerLocationBase):
    pass


class PlayerLocationUpdate(PlayerLocationBase):
    pass


class PlayerLocation(PlayerLocationBase):
    id: UUID
    player_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Базовые схемы для никнеймов игрока
class PlayerNicknameBase(BaseModel):
    nickname: str
    source: Optional[str] = None


class PlayerNicknameCreate(PlayerNicknameBase):
    pass


class PlayerNicknameUpdate(PlayerNicknameBase):
    pass


class PlayerNickname(PlayerNicknameBase):
    id: UUID
    player_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Общие атрибуты
class PlayerBase(BaseModel):
    full_name: str
    birth_date: Optional[date] = None
    contact_info: Optional[Dict[str, Any]] = None
    additional_info: Optional[Dict[str, Any]] = None


# Свойства для создания
class PlayerCreate(PlayerBase):
    created_by_user_id: Optional[UUID] = None
    created_by_fund_id: Optional[UUID] = None
    contacts: Optional[List[PlayerContactCreate]] = None
    locations: Optional[List[PlayerLocationCreate]] = None
    nicknames: Optional[List[PlayerNicknameCreate]] = None


# Свойства для обновления
class PlayerUpdate(PlayerBase):
    full_name: Optional[str] = None


# Свойства для чтения
class Player(PlayerBase):
    id: UUID
    created_by_user_id: UUID
    created_by_fund_id: UUID
    created_at: datetime
    updated_at: datetime
    contacts: List[PlayerContact] = []
    locations: List[PlayerLocation] = []
    nicknames: List[PlayerNickname] = []

    class Config:
        from_attributes = True


# Расширенная информация об игроке
class PlayerDetail(Player):
    fund_name: str
    created_by_user_name: str
    cases_count: int
    open_cases_count: int


# Схема для результатов поиска игрока
class PlayerSearchResult(BaseModel):
    id: UUID
    full_name: str
    description: Optional[str] = None
    contacts: List[PlayerContact] = []
    locations: List[PlayerLocation] = []
    nicknames: List[PlayerNickname] = []

    class Config:
        from_attributes = True 