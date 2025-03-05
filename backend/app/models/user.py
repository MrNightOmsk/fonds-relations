from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=False)
    fund = relationship("Fund", backref="users")
    
    role = Column(String(50), nullable=False)  # admin, manager
    is_active = Column(Boolean, default=True)
    
    # Связи с другими таблицами
    created_players = relationship("Player", back_populates="created_by_user", foreign_keys="Player.created_by_user_id")
    created_cases = relationship("Case", back_populates="created_by_user", foreign_keys="Case.created_by_user_id")
    closed_cases = relationship("Case", back_populates="closed_by_user", foreign_keys="Case.closed_by_user_id")
    audit_logs = relationship("AuditLog", back_populates="performed_by", foreign_keys="AuditLog.performed_by_id")
    notification_subscriptions = relationship("NotificationSubscription", back_populates="user", foreign_keys="NotificationSubscription.user_id")
    uploaded_evidences = relationship("CaseEvidence", back_populates="uploaded_by", foreign_keys="CaseEvidence.uploaded_by_id")
    
    # Новые связи для комментариев к кейсам
    case_comments = relationship("CaseComment", back_populates="created_by", foreign_keys="CaseComment.created_by_id")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 