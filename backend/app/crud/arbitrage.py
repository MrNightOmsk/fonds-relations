from typing import List, Optional, Union, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.arbitrage import (
    ArbitrageCase, Person, Nickname, Contact, Address, 
    Incident, Evidence, PokerRoom, Discipline
)
from app.schemas.arbitrage import (
    ArbitrageCaseCreate, ArbitrageCaseUpdate, ArbitrageCaseSearch
)

class CRUDArbitrageCase(CRUDBase[ArbitrageCase, ArbitrageCaseCreate, ArbitrageCaseUpdate]):
    def create_with_relations(
        self, db: Session, *, obj_in: ArbitrageCaseCreate, author_id: UUID
    ) -> ArbitrageCase:
        # Создаем основной кейс
        db_obj = ArbitrageCase(author_id=author_id)
        db.add(db_obj)
        db.flush()  # Получаем id без коммита

        # Создаем связанные данные
        person_data = obj_in.person.model_dump()
        person = Person(**person_data, case_id=db_obj.id)
        db.add(person)

        if obj_in.address:
            address_data = obj_in.address.model_dump()
            address = Address(**address_data, case_id=db_obj.id)
            db.add(address)

        for nickname_in in obj_in.nicknames:
            nickname_data = nickname_in.model_dump()
            nickname = Nickname(**nickname_data, case_id=db_obj.id)
            db.add(nickname)

        for contact_in in obj_in.contacts:
            contact_data = contact_in.model_dump()
            contact = Contact(**contact_data, case_id=db_obj.id)
            db.add(contact)

        for incident_in in obj_in.incidents:
            incident_data = incident_in.model_dump(exclude={'evidence'})
            incident = Incident(**incident_data, case_id=db_obj.id)
            db.add(incident)
            db.flush()  # Получаем id инцидента

            if incident_in.evidence:
                for evidence_in in incident_in.evidence:
                    evidence_data = evidence_in.model_dump()
                    evidence = Evidence(**evidence_data, incident_id=incident.id)
                    db.add(evidence)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def search(
        self,
        db: Session,
        *,
        search: ArbitrageCaseSearch,
        skip: int = 0,
        limit: int = 20
    ) -> List[ArbitrageCase]:
        query = db.query(ArbitrageCase)

        # Поиск по всем связанным полям
        if search.query:
            query = query.join(Person).join(Nickname).join(Contact).outerjoin(Address)
            query = query.filter(
                or_(
                    Person.first_name.ilike(f"%{search.query}%"),
                    Person.last_name.ilike(f"%{search.query}%"),
                    Person.middle_name.ilike(f"%{search.query}%"),
                    Nickname.nickname.ilike(f"%{search.query}%"),
                    Contact.value.ilike(f"%{search.query}%"),
                    Address.country.ilike(f"%{search.query}%"),
                    Address.city.ilike(f"%{search.query}%"),
                )
            )

        # Фильтры по датам
        if search.date_from:
            query = query.filter(ArbitrageCase.created_at >= search.date_from)
        if search.date_to:
            query = query.filter(ArbitrageCase.created_at <= search.date_to)

        # Фильтры по сумме
        if search.amount_from or search.amount_to:
            query = query.join(Incident)
            if search.amount_from:
                query = query.filter(Incident.amount >= search.amount_from)
            if search.amount_to:
                query = query.filter(Incident.amount <= search.amount_to)

        # Фильтры по румам и дисциплинам
        if search.rooms or search.disciplines:
            query = query.join(Nickname)
            if search.rooms:
                query = query.filter(Nickname.room_id.in_(search.rooms))
            if search.disciplines:
                query = query.filter(Nickname.discipline_id.in_(search.disciplines))

        return query.offset(skip).limit(limit).all()

crud_arbitrage_case = CRUDArbitrageCase(ArbitrageCase) 