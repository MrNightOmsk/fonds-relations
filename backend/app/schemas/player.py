from typing import Optional, List
from pydantic import BaseModel


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


# Базовые схемы для игрока
class PlayerBase(BaseModel):
    full_name: str
    description: Optional[str] = None
    is_active: bool = True


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    contacts: List[PlayerContact] = []
    locations: List[PlayerLocation] = []
    nicknames: List[PlayerNickname] = []

    class Config:
        from_attributes = True


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