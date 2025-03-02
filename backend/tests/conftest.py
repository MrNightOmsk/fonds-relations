import pytest
from typing import Dict, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.session import get_db
from app.main import app
from app.models.base import Base
from app.crud.user import crud_user
from app.schemas.auth import UserCreate

# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db() -> Generator:
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db) -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def superuser_token_headers(client: TestClient, db) -> Dict[str, str]:
    """
    Возвращает заголовки авторизации для суперпользователя
    """
    user_in = UserCreate(
        email="admin@example.com",
        password="admin123",
        full_name="Admin",
        organization="Test Org"
    )
    user = crud_user.create(db, obj_in=user_in)
    user.is_superuser = True
    db.add(user)
    db.commit()

    data = {"username": user_in.email, "password": user_in.password}
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=data)
    response = r.json()
    auth_token = response["access_token"]
    return {"Authorization": f"Bearer {auth_token}"} 