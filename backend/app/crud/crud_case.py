from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.case import Case, CaseEvidence, CaseComment
from app.schemas.case import CaseCreate, CaseUpdate


class CRUDCase(CRUDBase[Case, CaseCreate, CaseUpdate]):
    def create_with_player(
        self, db: Session, *, obj_in: CaseCreate, player_id: UUID, user_id: UUID, fund_id: UUID
    ) -> Case:
        obj_in_data = obj_in.dict()
        
        # Устанавливаем необходимые поля
        obj_in_data["player_id"] = player_id
        obj_in_data["created_by_user_id"] = user_id
        obj_in_data["created_by_fund_id"] = fund_id
        
        # Устанавливаем значения по умолчанию, если они не были указаны
        if obj_in_data.get("status") is None:
            obj_in_data["status"] = "open"
        
        if obj_in_data.get("arbitrage_amount") is None:
            obj_in_data["arbitrage_amount"] = 0.0
        
        if obj_in_data.get("arbitrage_currency") is None:
            obj_in_data["arbitrage_currency"] = "USD"
            
        # Устанавливаем временные метки
        obj_in_data["created_at"] = datetime.utcnow()
        obj_in_data["updated_at"] = datetime.utcnow()
        
        db_obj = Case(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_comment(
        self, db: Session, *, case_id: UUID, comment_text: str, user_id: UUID
    ) -> CaseComment:
        db_obj = CaseComment(
            case_id=case_id,
            comment=comment_text,
            created_by_id=user_id,
            created_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_evidence(
        self, db: Session, *, case_id: UUID, evidence_type: str, file_path: str, 
        description: Optional[str], user_id: UUID
    ) -> CaseEvidence:
        db_obj = CaseEvidence(
            case_id=case_id,
            type=evidence_type,
            file_path=file_path,
            description=description,
            uploaded_by_id=user_id,
            created_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_player(
        self, db: Session, *, player_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Case]:
        return (
            db.query(self.model)
            .filter(Case.player_id == player_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Case]:
        return (
            db.query(self.model)
            .filter(Case.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[Case]:
        return (
            db.query(self.model)
            .filter(Case.created_at >= start_date)
            .filter(Case.created_at <= end_date)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_status(
        self,
        db: Session,
        *,
        db_obj: Case,
        status: str,
        notes: Optional[str] = None
    ) -> Case:
        db_obj.status = status
        if notes:
            db_obj.notes = notes
        db_obj.updated_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_comments(
        self, db: Session, *, case_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[CaseComment]:
        return (
            db.query(CaseComment)
            .filter(CaseComment.case_id == case_id)
            .order_by(CaseComment.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_evidences(
        self, db: Session, *, case_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[CaseEvidence]:
        return (
            db.query(CaseEvidence)
            .filter(CaseEvidence.case_id == case_id)
            .order_by(CaseEvidence.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_fund(
        self, db: Session, *, fund_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Case]:
        return (
            db.query(self.model)
            .filter(Case.created_by_fund_id == fund_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_filtered(
        self, 
        db: Session, 
        *, 
        filters: Dict[str, Any] = None,
        search: Optional[str] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> tuple[int, List[Case]]:
        """
        Получение кейсов с применением различных фильтров и поиска.
        
        Args:
            db: сессия базы данных
            filters: словарь фильтров в формате {имя_поля: значение}
            search: строка для поиска в заголовке и описании
            skip: смещение для пагинации
            limit: максимальное количество результатов
            
        Returns:
            tuple: (общее количество записей, список кейсов)
        """
        import logging
        logger = logging.getLogger("app")
        
        # Создаём базовый запрос
        query = db.query(self.model)
        
        # Применяем фильтры
        if filters:
            logger.info(f"Applying filters: {filters}")
            
            # Фильтр по ID игрока
            if "player_id" in filters:
                query = query.filter(Case.player_id == filters["player_id"])
            
            # Фильтр по статусу
            if "status" in filters:
                query = query.filter(Case.status == filters["status"])
            
            # Фильтр по ID типа кейса
            if "case_type_id" in filters:
                query = query.filter(Case.case_type_id == filters["case_type_id"])
            
            # Фильтр по дате начала
            if "created_at_start" in filters:
                query = query.filter(Case.created_at >= filters["created_at_start"])
            
            # Фильтр по дате окончания
            if "created_at_end" in filters:
                query = query.filter(Case.created_at <= filters["created_at_end"])
                
            # Фильтр по ID фонда
            if "fund_id" in filters:
                query = query.filter(Case.created_by_fund_id == filters["fund_id"])
                
            # Фильтр по ID пользователя, создавшего кейс
            if "user_id" in filters:
                query = query.filter(Case.created_by_user_id == filters["user_id"])
                
            # Фильтр по арбитражу (если указано True или False)
            if "is_arbitrage" in filters:
                query = query.filter(Case.is_arbitrage == filters["is_arbitrage"])
                
        # Применяем поиск по заголовку и описанию
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Case.title.ilike(search_term)) | 
                (Case.description.ilike(search_term))
            )
        
        # Получаем общее количество без учета пагинации
        total_count = query.count()
        
        # Применяем пагинацию и получаем результаты
        results = query.order_by(Case.created_at.desc()).offset(skip).limit(limit).all()
        
        logger.info(f"Total count: {total_count}, returned results: {len(results)}")
        
        return total_count, results


case = CRUDCase(Case) 