from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.schemas.player import Player


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


# Базовые схемы для дел
class CaseBase(BaseModel):
    title: str
    description: str
    status: str
    priority: Optional[str] = None
    player_id: int


class CaseCreate(CaseBase):
    pass


class CaseUpdate(CaseBase):
    pass


class Case(CaseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    evidences: List[CaseEvidence] = []

    class Config:
        from_attributes = True


# Расширенная схема дела с информацией об игроке
class CaseWithPlayer(Case):
    player: Player

    class Config:
        from_attributes = True 