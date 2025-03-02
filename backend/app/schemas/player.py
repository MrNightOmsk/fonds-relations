from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime, date


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
    id: int
    player_id: int

    class Config:
        from_attributes = True


# Базовые схемы для местоположения игрока
class PlayerLocationBase(BaseModel):
    country: str
    city: Optional[str] = None
    address: Optional[str] = None


class PlayerLocationCreate(PlayerLocationBase):
    pass


class PlayerLocationUpdate(PlayerLocationBase):
    pass


class PlayerLocation(PlayerLocationBase):
    id: int
    player_id: int

    class Config:
        from_attributes = True


# Базовые схемы для никнеймов игрока
class PlayerNicknameBase(BaseModel):
    nickname: str
    platform: Optional[str] = None


class PlayerNicknameCreate(PlayerNicknameBase):
    pass


class PlayerNicknameUpdate(PlayerNicknameBase):
    pass


class PlayerNickname(PlayerNicknameBase):
    id: int
    player_id: int

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
    pass


# Свойства для обновления
class PlayerUpdate(PlayerBase):
    full_name: Optional[str] = None


# Свойства для чтения
class Player(PlayerBase):
    id: int
    created_by_user_id: int
    created_by_fund_id: int
    created_at: datetime
    updated_at: datetime
    contacts: List[PlayerContact] = []
    locations: List[PlayerLocation] = []
    nicknames: List[PlayerNickname] = []

    class Config:
        orm_mode = True


# Расширенная информация об игроке
class PlayerDetail(Player):
    fund_name: str
    created_by_user_name: str
    cases_count: int
    open_cases_count: int


# Схема для результатов поиска игрока
class PlayerSearchResult(BaseModel):
    id: int
    full_name: str
    description: Optional[str] = None
    contacts: List[PlayerContact] = []
    locations: List[PlayerLocation] = []
    nicknames: List[PlayerNickname] = []

    class Config:
        from_attributes = True 