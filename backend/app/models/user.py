from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, Column, String, DateTime

from app.models.base import Base
from app.db.types import GUID

class User(Base):
    __tablename__ = "users"

    id = Column(GUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) 