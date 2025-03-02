from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from app.db.types import GUID

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) 