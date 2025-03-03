from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from app.schemas.player import Player


# Общие атрибуты
class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    player_id: UUID
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
    id: UUID
    created_by_user_id: UUID
    created_by_fund_id: UUID
    closed_at: Optional[datetime] = None
    closed_by_user_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Расширенная схема для чтения с дополнительными полями
class CaseExtended(Case):
    closed_by_user_name: Optional[str] = None


# Базовые схемы для доказательств
class CaseEvidenceBase(BaseModel):
    type: str
    description: str


class CaseEvidenceCreate(CaseEvidenceBase):
    pass


class CaseEvidenceUpdate(CaseEvidenceBase):
    pass


class CaseEvidence(CaseEvidenceBase):
    id: UUID
    case_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Расширенная схема дела с информацией об игроке
class CaseWithPlayer(Case):
    player: Player

    class Config:
        from_attributes = True 