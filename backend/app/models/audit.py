import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AuditLog(Base):
    __tablename__ = "auditlog"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(50), nullable=False)  # player, case, etc.
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String(50), nullable=False)  # create, update, delete
    changes = Column(JSON)
    performed_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    performed_by = relationship("User", back_populates="audit_logs")


class NotificationSubscription(Base):
    __tablename__ = "notification_subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(String(50), nullable=False)  # email, telegram, etc.
    settings = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="notification_subscriptions") 