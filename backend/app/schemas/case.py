from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


# Evidence schemas
class CaseEvidenceBase(BaseModel):
    type: str
    file_path: str


class CaseEvidenceCreate(CaseEvidenceBase):
    pass


class CaseEvidenceUpdate(CaseEvidenceBase):
    pass


class CaseEvidence(CaseEvidenceBase):
    id: UUID
    case_id: UUID
    uploaded_by_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Case schemas
class CaseBase(BaseModel):
    type: str
    description: str
    amount: Optional[Decimal] = None
    status: str = "open"


class CaseCreate(CaseBase):
    player_id: UUID
    evidences: Optional[List[CaseEvidenceCreate]] = None


class CaseUpdate(CaseBase):
    evidences: Optional[List[CaseEvidenceUpdate]] = None


class Case(CaseBase):
    id: UUID
    player_id: UUID
    reported_by_id: UUID
    created_at: datetime
    updated_at: datetime
    evidences: List[CaseEvidence] = []

    class Config:
        from_attributes = True


# Case with player info
class CaseWithPlayer(Case):
    player_full_name: str
    player_nicknames: List[str]

    class Config:
        from_attributes = True 