from app.models.user import User
from app.models.player import Player, PlayerContact, PlayerLocation, PlayerNickname
from app.models.case import Case, CaseEvidence
from app.models.audit import AuditLog, NotificationSubscription

# Update User model relationships
User.players = relationship("Player", back_populates="created_by")
User.reported_cases = relationship("Case", back_populates="reported_by")
User.uploaded_evidences = relationship("CaseEvidence", back_populates="uploaded_by")
User.audit_logs = relationship("AuditLog", back_populates="performed_by")
User.notification_subscriptions = relationship("NotificationSubscription", back_populates="user") 