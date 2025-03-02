from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.schemas.player import Player


# Общие атрибуты
class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    player_id: int
    status: str = "open"  # open, closed


# Свойства для создания
class CaseCreate(CaseBase):
    pass


# Свойства для обновления
class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


# Свойства для чтения
class Case(CaseBase):
    id: int
    created_by_user_id: int
    created_by_fund_id: int
    closed_at: Optional[datetime] = None
    closed_by_user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Расширенная информация о кейсе
class CaseDetail(Case):
    player_name: str
    fund_name: str
    created_by_user_name: str
    closed_by_user_name: Optional[str] = None


# Базовые схемы для доказательств
class CaseEvidenceBase(BaseModel):
    type: str
    description: str
    url: Optional[str] = None


class CaseEvidenceCreate(CaseEvidenceBase):
    pass


class CaseEvidenceUpdate(CaseEvidenceBase):
    pass


class CaseEvidence(CaseEvidenceBase):
    id: int
    case_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Расширенная схема дела с информацией об игроке
class CaseWithPlayer(Case):
    player: Player

    class Config:
        from_attributes = True 