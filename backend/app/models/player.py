from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

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
    full_name = Column(String, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    contacts = relationship("PlayerContact", back_populates="player")
    locations = relationship("PlayerLocation", back_populates="player")
    nicknames = relationship("PlayerNickname", back_populates="player")
    cases = relationship("Case", back_populates="player") 