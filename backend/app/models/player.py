from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, String, ForeignKey, Date, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base_class import Base

if TYPE_CHECKING:
    from .case import Case  # noqa: F401


class PlayerContact(Base):
    __tablename__ = "player_contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"))
    type = Column(String(50), nullable=False)  # phone, email, etc.
    value = Column(String(255), nullable=False)
    description = Column(String(255))

    player = relationship("Player", back_populates="contacts")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PlayerLocation(Base):
    __tablename__ = "player_locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"))
    country = Column(String(255))
    city = Column(String(255))
    address = Column(String(255))

    player = relationship("Player", back_populates="locations")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PlayerNickname(Base):
    __tablename__ = "player_nicknames"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"))
    nickname = Column(String(255), nullable=False)
    source = Column(String(255))  # где был использован никнейм

    player = relationship("Player", back_populates="nicknames")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Player(Base):
    __tablename__ = "players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    birth_date = Column(Date)
    contact_info = Column(JSON)
    additional_info = Column(JSON)
    
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_by_user = relationship("User", back_populates="created_players", foreign_keys="Player.created_by_user_id")
    
    created_by_fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=False)
    created_by_fund = relationship("Fund")
    
    # Связи с другими таблицами
    cases = relationship("Case", back_populates="player")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    contacts = relationship("PlayerContact", back_populates="player", cascade="all, delete-orphan")
    locations = relationship("PlayerLocation", back_populates="player", cascade="all, delete-orphan")
    nicknames = relationship("PlayerNickname", back_populates="player", cascade="all, delete-orphan") 