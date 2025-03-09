from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, String, ForeignKey, Date, DateTime, JSON, Float, Text
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
    type = Column(String(50), nullable=False)  # phone, email, skype, vk, facebook, instagram, etc.
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
    room = Column(String(255))      # покерная комната (Red Star, Coin, WPN, Pokerdom, Pokerok, etc.)
    discipline = Column(String(255)) # дисциплина (MTT, Cash, etc.)

    player = relationship("Player", back_populates="nicknames")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PlayerPaymentMethod(Base):
    __tablename__ = "player_payment_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"))
    type = Column(String(50), nullable=False)  # webmoney, skrill, neteller, ecopayz, etc.
    value = Column(String(255), nullable=False)
    description = Column(String(255))

    player = relationship("Player", back_populates="payment_methods")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PlayerSocialMedia(Base):
    __tablename__ = "player_social_media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"))
    type = Column(String(50), nullable=False)  # vk, facebook, instagram, blog, forum, gipsyteam, pokerstrategy
    value = Column(String(255), nullable=False)
    description = Column(String(255))

    player = relationship("Player", back_populates="social_media")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Player(Base):
    __tablename__ = "players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Разделяем ФИО на отдельные поля
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    middle_name = Column(String(255), nullable=True)
    full_name = Column(String(255))  # Сохраняем для совместимости с предыдущей версией
    
    birth_date = Column(Date, nullable=True)
    contact_info = Column(JSON, nullable=True)    # Оставляем для совместимости
    additional_info = Column(JSON, nullable=True)  # Для хранения дополнительной информации
    health_notes = Column(String(1000), nullable=True)
    
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_by_user = relationship("User", back_populates="created_players")
    
    created_by_fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=False)
    created_by_fund = relationship("Fund")
    
    # Связи с другими таблицами
    cases = relationship("Case", back_populates="player", cascade="all, delete-orphan")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    contacts = relationship("PlayerContact", back_populates="player", cascade="all, delete-orphan")
    locations = relationship("PlayerLocation", back_populates="player", cascade="all, delete-orphan")
    nicknames = relationship("PlayerNickname", back_populates="player", cascade="all, delete-orphan")
    payment_methods = relationship("PlayerPaymentMethod", back_populates="player", cascade="all, delete-orphan")
    social_media = relationship("PlayerSocialMedia", back_populates="player", cascade="all, delete-orphan") 