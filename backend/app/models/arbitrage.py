from sqlalchemy import Column, String, ForeignKey, Numeric, Boolean, Text, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel, Base
from app.db.types import GUID

class ArbitrageCase(BaseModel):
    __tablename__ = 'arbitrage_cases'
    
    author_id = Column(GUID, nullable=False)
    status = Column(String(50), nullable=False, default='active')
    
    # Relationships
    person = relationship("Person", back_populates="case", uselist=False)
    nicknames = relationship("Nickname", back_populates="case")
    contacts = relationship("Contact", back_populates="case")
    address = relationship("Address", back_populates="case", uselist=False)
    incidents = relationship("Incident", back_populates="case")

class Person(BaseModel):
    __tablename__ = 'persons'
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    middle_name = Column(String(100))
    case_id = Column(GUID, ForeignKey('arbitrage_cases.id'))
    
    # Relationships
    case = relationship("ArbitrageCase", back_populates="person")

class PokerRoom(BaseModel):
    __tablename__ = 'poker_rooms'
    
    name = Column(String(100), nullable=False, unique=True)

class Discipline(BaseModel):
    __tablename__ = 'disciplines'
    
    name = Column(String(50), nullable=False, unique=True)

class Nickname(BaseModel):
    __tablename__ = 'nicknames'
    
    case_id = Column(GUID, ForeignKey('arbitrage_cases.id'))
    room_id = Column(GUID, ForeignKey('poker_rooms.id'))
    discipline_id = Column(GUID, ForeignKey('disciplines.id'))
    nickname = Column(String(100), nullable=False)
    
    # Relationships
    case = relationship("ArbitrageCase", back_populates="nicknames")
    room = relationship("PokerRoom")
    discipline = relationship("Discipline")

class Contact(BaseModel):
    __tablename__ = 'contacts'
    
    case_id = Column(GUID, ForeignKey('arbitrage_cases.id'))
    type = Column(String(50), nullable=False)
    value = Column(Text, nullable=False)
    verified = Column(Boolean, default=False)
    
    # Relationships
    case = relationship("ArbitrageCase", back_populates="contacts")

class Address(BaseModel):
    __tablename__ = 'addresses'
    
    case_id = Column(GUID, ForeignKey('arbitrage_cases.id'))
    country = Column(String(100))
    region = Column(String(100))
    city = Column(String(100))
    street = Column(String(200))
    building = Column(String(50))
    apartment = Column(String(50))
    postal_code = Column(String(20))
    
    # Relationships
    case = relationship("ArbitrageCase", back_populates="address")

class Incident(BaseModel):
    __tablename__ = 'incidents'
    
    case_id = Column(GUID, ForeignKey('arbitrage_cases.id'))
    type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Numeric(15, 2))
    currency = Column(String(3), default='USD')
    
    # Relationships
    case = relationship("ArbitrageCase", back_populates="incidents")
    evidence = relationship("Evidence", back_populates="incident")

class Evidence(BaseModel):
    __tablename__ = 'evidence'
    
    incident_id = Column(GUID, ForeignKey('incidents.id'))
    type = Column(String(50), nullable=False)
    url = Column(Text, nullable=False)
    description = Column(Text)
    
    # Relationships
    incident = relationship("Incident", back_populates="evidence") 