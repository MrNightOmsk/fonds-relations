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
        orm_mode = True


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
        orm_mode = True


# Базовые схемы для никнеймов игрока
class PlayerNicknameBase(BaseModel):
    nickname: str
    room: Optional[str] = None
    discipline: Optional[str] = None


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
        orm_mode = True


# Базовые схемы для платежных методов игрока
class PlayerPaymentMethodBase(BaseModel):
    type: str
    value: str
    description: Optional[str] = None


class PlayerPaymentMethodCreate(PlayerPaymentMethodBase):
    pass


class PlayerPaymentMethodUpdate(PlayerPaymentMethodBase):
    pass


class PlayerPaymentMethod(PlayerPaymentMethodBase):
    id: UUID
    player_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Базовые схемы для социальных медиа игрока
class PlayerSocialMediaBase(BaseModel):
    type: str
    value: str
    description: Optional[str] = None


class PlayerSocialMediaCreate(PlayerSocialMediaBase):
    pass


class PlayerSocialMediaUpdate(PlayerSocialMediaBase):
    pass


class PlayerSocialMedia(PlayerSocialMediaBase):
    id: UUID
    player_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Общие атрибуты
class PlayerBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    contact_info: Optional[Dict[str, Any]] = None
    additional_info: Optional[Dict[str, Any]] = None
    health_notes: Optional[str] = None


# Свойства для создания
class PlayerCreate(PlayerBase):
    created_by_user_id: Optional[UUID] = None
    created_by_fund_id: Optional[UUID] = None
    contacts: Optional[List[PlayerContactCreate]] = None
    locations: Optional[List[PlayerLocationCreate]] = None
    nicknames: Optional[List[PlayerNicknameCreate]] = None
    payment_methods: Optional[List[PlayerPaymentMethodCreate]] = None
    social_media: Optional[List[PlayerSocialMediaCreate]] = None


# Свойства для обновления
class PlayerUpdate(PlayerBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
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
    payment_methods: List[PlayerPaymentMethod] = []
    social_media: List[PlayerSocialMedia] = []

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
    id: UUID
    full_name: str
    first_name: str
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    description: Optional[str] = None
    fund_name: Optional[str] = None
    cases_count: Optional[int] = 0
    latest_case_date: Optional[datetime] = None
    contacts: Optional[List[str]] = []
    locations: Optional[List[str]] = []
    nicknames: Optional[List[Dict[str, str]]] = []

    class Config:
        orm_mode = True 