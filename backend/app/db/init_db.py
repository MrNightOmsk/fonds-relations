from sqlalchemy.orm import Session
import uuid

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401


def init_db(db: Session) -> None:
    """
    Инициализирует базу данных начальными данными.
    
    Важно: Таблицы должны быть созданы заранее через миграции Alembic!
    """
    # Создаем первый фонд, если еще нет ни одного
    fund = crud.fund.get_multi(db, limit=1)
    if not fund:
        fund_id = str(uuid.uuid4())
        fund_in = schemas.FundCreate(
            name="Default Fund",
            description="Default fund created during initialization",
            contact_info={"email": "admin@example.com", "phone": "+1234567890"}
        )
        fund = crud.fund.create(db, obj_in=fund_in, fund_id=fund_id)
    else:
        fund = fund[0]
        fund_id = str(fund.id)

    # Создаем суперпользователя, если он не существует
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name="Initial Admin",
            fund_id=fund_id,  # Привязываем к созданному фонду
            role="admin",
            is_active=True
        )
        user = crud.user.create(db, obj_in=user_in)
        print(f"Superuser {user.email} created successfully") 