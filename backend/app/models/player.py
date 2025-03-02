from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .case import Case  # noqa: F401


class PlayerContact(Base):
    __tablename__ = "player_contacts"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    type = Column(String, index=True)
    value = Column(String)
    description = Column(String, nullable=True)

    player = relationship("Player", back_populates="contacts")


class PlayerLocation(Base):
    __tablename__ = "player_locations"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    country = Column(String, index=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)

    player = relationship("Player", back_populates="locations")


class PlayerNickname(Base):
    __tablename__ = "player_nicknames"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    nickname = Column(String, index=True)
    platform = Column(String, nullable=True)

    player = relationship("Player", back_populates="nicknames")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=True)
    contact_info = Column(JSON, nullable=True)  # телефон, email, другие контакты
    additional_info = Column(JSON, nullable=True)  # дополнительная информация
    
    created_by_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_by_user = relationship("User", back_populates="created_players")
    
    created_by_fund_id = Column(Integer, ForeignKey("fund.id"), nullable=False)
    created_by_fund = relationship("Fund")
    
    # Связи с другими таблицами
    cases = relationship("Case", back_populates="player")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    contacts = relationship("PlayerContact", back_populates="player")
    locations = relationship("PlayerLocation", back_populates="player")
    nicknames = relationship("PlayerNickname", back_populates="player") 