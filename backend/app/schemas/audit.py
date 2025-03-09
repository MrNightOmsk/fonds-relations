from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


# Audit log schemas
class AuditLogBase(BaseModel):
    action: str
    entity_type: str
    entity_id: int
    changes: Dict[str, Any]
    user_id: int


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogUpdate(AuditLogBase):
    pass


class AuditLog(AuditLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Notification subscription schemas
class NotificationSubscriptionBase(BaseModel):
    user_id: int
    entity_type: str
    entity_id: int
    enabled: bool = True


class NotificationSubscriptionCreate(NotificationSubscriptionBase):
    pass


class NotificationSubscriptionUpdate(NotificationSubscriptionBase):
    pass


class NotificationSubscription(NotificationSubscriptionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Notification message schema
class NotificationMessage(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    read: bool = False
    created_at: datetime

    class Config:
        orm_mode = True 