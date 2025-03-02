import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Case(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("player.id"))
    reported_by_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    type = Column(String(50), nullable=False)  # arbitrage, scam, etc.
    description = Column(Text, nullable=False)
    amount = Column(Numeric(10, 2))
    status = Column(String(50), nullable=False, default="open")  # open, closed, resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="cases")
    reported_by = relationship("User", back_populates="reported_cases")
    evidences = relationship("CaseEvidence", back_populates="case", cascade="all, delete-orphan")


class CaseEvidence(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("case.id"))
    type = Column(String(50), nullable=False)  # screenshot, log, document
    file_path = Column(String, nullable=False)
    uploaded_by_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    case = relationship("Case", back_populates="evidences")
    uploaded_by = relationship("User", back_populates="uploaded_evidences") 