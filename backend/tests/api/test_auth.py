import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_login_success(async_client: AsyncClient, test_admin: dict):
    """Тест успешного входа в систему"""
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": test_admin["email"],
            "password": "secret"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_wrong_password(async_client: AsyncClient, test_admin: dict):
    """Тест входа с неверным паролем"""
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": test_admin["email"],
            "password": "wrong_password"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

async def test_login_nonexistent_user(async_client: AsyncClient):
    """Тест входа с несуществующим пользователем"""
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "password"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

async def test_login_inactive_user(async_client: AsyncClient, db: AsyncSession, test_admin: dict):
    """Тест входа с неактивным пользователем"""
    # Деактивируем пользователя
    async with db as session:
        query = "UPDATE users SET is_active = false WHERE email = :email"
        await session.execute(query, {"email": test_admin["email"]})
        await session.commit()

    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": test_admin["email"],
            "password": "secret"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Inactive user"

    # Возвращаем пользователя в активное состояние
    async with db as session:
        query = "UPDATE users SET is_active = true WHERE email = :email"
        await session.execute(query, {"email": test_admin["email"]})
        await session.commit()

async def test_login_invalid_email_format(async_client: AsyncClient):
    """Тест входа с неверным форматом email"""
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": "not_an_email",
            "password": "password"
        }
    )
    assert response.status_code == 422  # Validation error

async def test_login_empty_password(async_client: AsyncClient, test_admin: dict):
    """Тест входа с пустым паролем"""
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": test_admin["email"],
            "password": ""
        }
    )
    assert response.status_code == 422  # Validation error 