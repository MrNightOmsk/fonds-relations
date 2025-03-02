import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Player(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    
    # Relationships
    created_by = relationship("User", back_populates="players")
    contacts = relationship("PlayerContact", back_populates="player", cascade="all, delete-orphan")
    locations = relationship("PlayerLocation", back_populates="player", cascade="all, delete-orphan")
    nicknames = relationship("PlayerNickname", back_populates="player", cascade="all, delete-orphan")
    cases = relationship("Case", back_populates="player", cascade="all, delete-orphan")


class PlayerContact(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("player.id"))
    contact_type = Column(String(50), nullable=False)
    contact_value = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="contacts")


class PlayerLocation(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("player.id"))
    country = Column(String(100))
    city = Column(String(100))
    address = Column(String)
    postal_code = Column(String(20))
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="locations")


class PlayerNickname(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("player.id"))
    room = Column(String(100), nullable=False)
    nickname = Column(String(100), nullable=False)
    discipline = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="nicknames") 