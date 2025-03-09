from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from app.schemas.player import Player
from app.schemas.fund import Fund


# Общие атрибуты
class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    player_id: UUID
    status: str  # open, closed, in_progress
    arbitrage_type: Optional[str] = None
    arbitrage_amount: Optional[float] = 0.0  # Не может быть отрицательной, по умолчанию 0
    arbitrage_currency: str = "USD"  # По умолчанию USD, обязательное поле


# Свойства для создания
class CaseCreate(CaseBase):
    created_by_fund_id: UUID  # Обязательное поле - ID фонда


# Свойства для обновления
class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    arbitrage_type: Optional[str] = None
    arbitrage_amount: Optional[float] = None
    arbitrage_currency: Optional[str] = None


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
        orm_mode = True


# Расширенная схема для чтения с дополнительными полями
class CaseExtended(Case):
    player: Optional[Player] = None
    fund: Optional[Fund] = None
    closed_by_user_name: Optional[str] = None
    
    class Config:
        orm_mode = True


# Базовые схемы для доказательств
class CaseEvidenceBase(BaseModel):
    type: str
    description: Optional[str] = None


class CaseEvidenceCreate(CaseEvidenceBase):
    pass


class CaseEvidenceUpdate(CaseEvidenceBase):
    pass


class CaseEvidence(CaseEvidenceBase):
    id: UUID
    case_id: UUID
    file_path: str
    uploaded_by_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


# Базовые схемы для комментариев
class CaseCommentBase(BaseModel):
    comment: str


class CaseCommentCreate(CaseCommentBase):
    case_id: UUID


class CaseCommentUpdate(CaseCommentBase):
    pass


class CaseComment(CaseCommentBase):
    id: UUID
    case_id: UUID
    created_by_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


# Расширенная схема дела с информацией об игроке
class CaseWithPlayer(Case):
    player: Player
    comments: List[CaseComment] = []
    evidences: List[CaseEvidence] = []

    class Config:
        orm_mode = True 