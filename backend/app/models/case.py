import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Case(Base):
    __tablename__ = "cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)
    player = relationship("Player", back_populates="cases")
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)  # open, closed
    
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_by_user = relationship("User", back_populates="created_cases", foreign_keys=[created_by_user_id])
    
    created_by_fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=False)
    created_by_fund = relationship("Fund")
    
    closed_at = Column(DateTime(timezone=True), nullable=True)
    closed_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    closed_by_user = relationship("User", back_populates="closed_cases", foreign_keys=[closed_by_user_id])
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Связь с доказательствами
    evidences = relationship("CaseEvidence", back_populates="case", cascade="all, delete-orphan")


class CaseEvidence(Base):
    __tablename__ = "case_evidences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"))
    type = Column(String(50), nullable=False)  # screenshot, log, document
    file_path = Column(String, nullable=False)
    uploaded_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    case = relationship("Case", back_populates="evidences")
    uploaded_by = relationship("User", back_populates="uploaded_evidences", foreign_keys=[uploaded_by_id]) 