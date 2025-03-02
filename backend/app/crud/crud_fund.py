from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.fund import Fund
from app.schemas.fund import FundCreate, FundUpdate


class CRUDFund(CRUDBase[Fund, FundCreate, FundUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Fund]:
        return db.query(Fund).filter(Fund.name == name).first()

    def get_multi_by_ids(self, db: Session, *, ids: List[int], skip: int = 0, limit: int = 100) -> List[Fund]:
        return db.query(Fund).filter(Fund.id.in_(ids)).offset(skip).limit(limit).all()


fund = CRUDFund(Fund) 