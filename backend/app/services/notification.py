from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.case import Case
from app.models.notification import NotificationSubscription
from app.schemas.notification import NotificationMessage
from app.utils.email import send_email


def get_subscriptions(
    db: Session,
    user_id: Optional[UUID] = None,
    type: Optional[str] = None,
    is_active: bool = True,
) -> List[NotificationSubscription]:
    """Get notification subscriptions."""
    query = db.query(NotificationSubscription)
    
    if user_id:
        query = query.filter(NotificationSubscription.user_id == user_id)
    
    if type:
        query = query.filter(NotificationSubscription.type == type)
    
    if is_active is not None:
        query = query.filter(NotificationSubscription.is_active == is_active)
    
    return query.all()


def send_new_case_notification(db: Session, case: Case) -> None:
    """Send notification about a new case."""
    # Get all active email subscriptions
    subscriptions = get_subscriptions(db, type="email", is_active=True)
    
    if not subscriptions:
        return
    
    # Prepare notification message
    message = NotificationMessage(
        type="new_case",
        title=f"Новый случай нарушения: {case.type}",
        message=(
            f"Добавлен новый случай нарушения для игрока {case.player.full_name}.\n"
            f"Тип: {case.type}\n"
            f"Описание: {case.description}\n"
            f"Сумма: {case.amount if case.amount else 'Не указана'}"
        ),
        data={
            "case_id": str(case.id),
            "player_id": str(case.player_id),
            "type": case.type,
        },
    )
    
    # Send email notifications
    for subscription in subscriptions:
        if subscription.settings.get("new_cases", True):
            send_email(
                email_to=subscription.user.email,
                subject=message.title,
                template_str="new_case.html",
                template_data={
                    "case": case,
                    "player": case.player,
                    "reported_by": case.reported_by,
                },
            )


def send_case_status_notification(db: Session, case: Case) -> None:
    """Send notification about case status change."""
    # Get all active email subscriptions
    subscriptions = get_subscriptions(db, type="email", is_active=True)
    
    if not subscriptions:
        return
    
    # Prepare notification message
    message = NotificationMessage(
        type="case_status_update",
        title=f"Обновление статуса дела: {case.type}",
        message=(
            f"Статус дела для игрока {case.player.full_name} был изменен на {case.status}.\n"
            f"Тип: {case.type}\n"
            f"Описание: {case.description}"
        ),
        data={
            "case_id": str(case.id),
            "player_id": str(case.player_id),
            "status": case.status,
        },
    )
    
    # Send email notifications
    for subscription in subscriptions:
        if subscription.settings.get("case_updates", True):
            send_email(
                email_to=subscription.user.email,
                subject=message.title,
                template_str="case_status_update.html",
                template_data={
                    "case": case,
                    "player": case.player,
                },
            ) 