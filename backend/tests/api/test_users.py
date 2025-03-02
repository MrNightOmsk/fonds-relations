import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_create_user(
    async_client: AsyncClient, admin_token_headers: dict, test_fund: dict
):
    """Тест создания пользователя"""
    response = await async_client.post(
        "/api/v1/users/",
        headers=admin_token_headers,
        json={
            "email": "newuser@example.com",
            "password": "newpassword123",
            "full_name": "New User",
            "fund_id": test_fund["id"],
            "role": "manager"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert data["fund_id"] == test_fund["id"]
    assert data["role"] == "manager"
    assert "id" in data
    assert "password" not in data

async def test_create_user_duplicate_email(
    async_client: AsyncClient, admin_token_headers: dict, test_fund: dict, test_admin: dict
):
    """Тест создания пользователя с существующим email"""
    response = await async_client.post(
        "/api/v1/users/",
        headers=admin_token_headers,
        json={
            "email": test_admin["email"],
            "password": "password123",
            "full_name": "Another User",
            "fund_id": test_fund["id"],
            "role": "manager"
        }
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()

async def test_create_user_invalid_data(async_client: AsyncClient, admin_token_headers: dict):
    """Тест создания пользователя с некорректными данными"""
    invalid_data_cases = [
        {
            "email": "not_an_email",  # Неверный формат email
            "password": "password123",
            "full_name": "Test User",
            "fund_id": 1,
            "role": "manager"
        },
        {
            "email": "user@example.com",
            "password": "short",  # Слишком короткий пароль
            "full_name": "Test User",
            "fund_id": 1,
            "role": "manager"
        },
        {
            "email": "user@example.com",
            "password": "password123",
            "full_name": "Test User",
            "fund_id": 1,
            "role": "invalid_role"  # Неверная роль
        }
    ]

    for invalid_data in invalid_data_cases:
        response = await async_client.post(
            "/api/v1/users/",
            headers=admin_token_headers,
            json=invalid_data
        )
        assert response.status_code == 422

async def test_get_user(
    async_client: AsyncClient, admin_token_headers: dict, test_admin: dict
):
    """Тест получения информации о пользователе"""
    response = await async_client.get(
        f"/api/v1/users/{test_admin['id']}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_admin["id"]
    assert data["email"] == test_admin["email"]
    assert "password" not in data

async def test_get_nonexistent_user(async_client: AsyncClient, admin_token_headers: dict):
    """Тест получения информации о несуществующем пользователе"""
    response = await async_client.get(
        "/api/v1/users/99999",
        headers=admin_token_headers
    )
    assert response.status_code == 404

async def test_update_user(
    async_client: AsyncClient, admin_token_headers: dict, test_manager: dict
):
    """Тест обновления информации о пользователе"""
    response = await async_client.put(
        f"/api/v1/users/{test_manager['id']}",
        headers=admin_token_headers,
        json={
            "full_name": "Updated Manager Name",
            "password": "newpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Manager Name"
    assert "password" not in data

async def test_update_user_email_exists(
    async_client: AsyncClient, admin_token_headers: dict, test_manager: dict, test_admin: dict
):
    """Тест обновления email пользователя на уже существующий"""
    response = await async_client.put(
        f"/api/v1/users/{test_manager['id']}",
        headers=admin_token_headers,
        json={
            "email": test_admin["email"]
        }
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()

async def test_delete_user(
    async_client: AsyncClient, admin_token_headers: dict, db: AsyncSession
):
    """Тест удаления пользователя"""
    # Создаем пользователя для удаления
    create_response = await async_client.post(
        "/api/v1/users/",
        headers=admin_token_headers,
        json={
            "email": "todelete@example.com",
            "password": "password123",
            "full_name": "To Delete",
            "fund_id": 1,
            "role": "manager"
        }
    )
    user_id = create_response.json()["id"]

    # Удаляем пользователя
    response = await async_client.delete(
        f"/api/v1/users/{user_id}",
        headers=admin_token_headers
    )
    assert response.status_code == 204

    # Проверяем, что пользователь действительно удален
    get_response = await async_client.get(
        f"/api/v1/users/{user_id}",
        headers=admin_token_headers
    )
    assert get_response.status_code == 404

async def test_list_users(async_client: AsyncClient, admin_token_headers: dict):
    """Тест получения списка пользователей"""
    response = await async_client.get(
        "/api/v1/users/",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for user in data:
        assert "password" not in user

async def test_list_users_pagination(async_client: AsyncClient, admin_token_headers: dict):
    """Тест пагинации списка пользователей"""
    response = await async_client.get(
        "/api/v1/users/?skip=0&limit=1",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 1

async def test_manager_user_restrictions(
    async_client: AsyncClient, test_manager: dict
):
    """Тест ограничений доступа для менеджера при работе с пользователями"""
    headers = {"Authorization": f"Bearer {test_manager['token']}"}
    
    # Менеджер не должен иметь доступ к созданию пользователей
    response = await async_client.post(
        "/api/v1/users/",
        headers=headers,
        json={
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User",
            "fund_id": test_manager["fund_id"],
            "role": "manager"
        }
    )
    assert response.status_code == 403

    # Менеджер не должен иметь доступ к удалению пользователей
    response = await async_client.delete(
        f"/api/v1/users/{test_manager['id']}",
        headers=headers
    )
    assert response.status_code == 403

async def test_user_fund_access(
    async_client: AsyncClient, test_manager: dict, test_admin: dict
):
    """Тест доступа пользователя только к данным своего фонда"""
    headers = {"Authorization": f"Bearer {test_manager['token']}"}
    
    # Менеджер должен видеть пользователей своего фонда
    response = await async_client.get(
        "/api/v1/users/",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    for user in data:
        assert user["fund_id"] == test_manager["fund_id"] 