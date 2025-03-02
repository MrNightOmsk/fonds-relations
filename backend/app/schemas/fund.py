from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Общие атрибуты
class FundBase(BaseModel):
    name: str
    description: Optional[str] = None


# Свойства для создания
class FundCreate(FundBase):
    pass


# Свойства для обновления
class FundUpdate(FundBase):
    pass


# Свойства для чтения
class Fund(FundBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 