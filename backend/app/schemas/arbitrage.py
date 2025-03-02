from typing import List, Optional
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl, constr
from datetime import datetime

from .base import BaseSchema, TimestampedSchema

# Схемы для создания
class PersonCreate(BaseSchema):
    first_name: str
    last_name: Optional[str] = None
    middle_name: Optional[str] = None

class AddressCreate(BaseSchema):
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    building: Optional[str] = None
    apartment: Optional[str] = None
    postal_code: Optional[str] = None

class NicknameCreate(BaseSchema):
    room_id: UUID
    discipline_id: UUID
    nickname: str

class ContactCreate(BaseSchema):
    type: str  # email, phone, skype, etc.
    value: str
    verified: bool = False

class EvidenceCreate(BaseSchema):
    type: str
    url: HttpUrl
    description: Optional[str] = None

class IncidentCreate(BaseSchema):
    type: str
    description: str
    amount: Optional[Decimal] = None
    currency: str = "USD"
    evidence: Optional[List[EvidenceCreate]] = None

class ArbitrageCaseCreate(BaseSchema):
    person: PersonCreate
    nicknames: List[NicknameCreate]
    contacts: List[ContactCreate]
    address: Optional[AddressCreate] = None
    incidents: List[IncidentCreate]

# Схемы для чтения
class Person(TimestampedSchema, PersonCreate):
    case_id: UUID

class Address(TimestampedSchema, AddressCreate):
    case_id: UUID

class Nickname(TimestampedSchema, NicknameCreate):
    case_id: UUID

class Contact(TimestampedSchema, ContactCreate):
    case_id: UUID

class Evidence(TimestampedSchema, EvidenceCreate):
    incident_id: UUID

class Incident(TimestampedSchema, IncidentCreate):
    case_id: UUID
    evidence: List[Evidence] = []

class ArbitrageCase(TimestampedSchema):
    author_id: UUID
    status: str
    person: Person
    nicknames: List[Nickname] = []
    contacts: List[Contact] = []
    address: Optional[Address] = None
    incidents: List[Incident] = []

# Схемы для обновления
class PersonUpdate(PersonCreate):
    pass

class AddressUpdate(AddressCreate):
    pass

class NicknameUpdate(BaseSchema):
    room_id: Optional[UUID] = None
    discipline_id: Optional[UUID] = None
    nickname: Optional[str] = None

class ContactUpdate(BaseSchema):
    type: Optional[str] = None
    value: Optional[str] = None
    verified: Optional[bool] = None

class EvidenceUpdate(BaseSchema):
    type: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None

class IncidentUpdate(BaseSchema):
    type: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    currency: Optional[str] = None

class ArbitrageCaseUpdate(BaseSchema):
    status: Optional[str] = None
    person: Optional[PersonUpdate] = None
    address: Optional[AddressUpdate] = None

# Схемы для поиска
class ArbitrageCaseSearch(BaseSchema):
    query: str
    types: Optional[List[str]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    amount_from: Optional[Decimal] = None
    amount_to: Optional[Decimal] = None
    rooms: Optional[List[UUID]] = None
    disciplines: Optional[List[UUID]] = None 