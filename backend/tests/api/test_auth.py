from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.auth import UserCreate

def test_create_user(client: TestClient, db: Session) -> None:
    data = {
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User",
        "organization": "Test Org"
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == data["email"]
    assert content["full_name"] == data["full_name"]
    assert "id" in content

def test_login(client: TestClient, db: Session) -> None:
    # Создаем пользователя
    user_data = {
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User",
        "organization": "Test Org"
    }
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data,
    )

    # Пробуем залогиниться
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"],
    }
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"

def test_login_incorrect_password(client: TestClient, db: Session) -> None:
    # Создаем пользователя
    user_data = {
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User",
        "organization": "Test Org"
    }
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data,
    )

    # Пробуем залогиниться с неверным паролем
    login_data = {
        "username": user_data["email"],
        "password": "wrong_password",
    }
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == 400

def test_get_current_user(client: TestClient, superuser_token_headers: dict) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == "admin@example.com"
    assert content["is_superuser"] is True 