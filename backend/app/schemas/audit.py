from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel


# Audit log schemas
class AuditLogBase(BaseModel):
    entity_type: str
    entity_id: UUID
    action: str
    changes: Optional[Dict[str, Any]] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLog(AuditLogBase):
    id: UUID
    performed_by_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Notification subscription schemas
class NotificationSubscriptionBase(BaseModel):
    type: str
    settings: Dict[str, Any]
    is_active: bool = True


class NotificationSubscriptionCreate(NotificationSubscriptionBase):
    pass


class NotificationSubscriptionUpdate(NotificationSubscriptionBase):
    pass


class NotificationSubscription(NotificationSubscriptionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Notification message schema
class NotificationMessage(BaseModel):
    type: str
    title: str
    message: str
    data: Optional[Dict[str, Any]] = None 