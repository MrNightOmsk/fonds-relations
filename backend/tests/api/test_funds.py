import pytest
from uuid import UUID
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

pytestmark = pytest.mark.asyncio

async def test_create_fund(async_client: AsyncClient, admin_token_headers: dict):
    """Тест создания фонда"""
    fund_name = f"Test Fund {uuid.uuid4()}"
    response = await async_client.post(
        "/api/v1/funds/",
        headers=admin_token_headers,
        json={
            "name": fund_name,
            "description": "Test Fund Description"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == fund_name
    assert data["description"] == "Test Fund Description"
    assert UUID(data["id"])

async def test_create_fund_duplicate_name(
    async_client: AsyncClient, admin_token_headers: dict, test_fund: dict
):
    """Тест создания фонда с дублирующимся именем"""
    response = await async_client.post(
        "/api/v1/funds/",
        headers=admin_token_headers,
        json={
            "name": test_fund["name"],
            "description": "Another description"
        }
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()

async def test_create_fund_invalid_data(async_client: AsyncClient, admin_token_headers: dict):
    """Тест создания фонда с некорректными данными"""
    response = await async_client.post(
        "/api/v1/funds/",
        headers=admin_token_headers,
        json={
            "name": "",  # Пустое имя
            "description": "Description"
        }
    )
    assert response.status_code == 422

async def test_get_fund(
    async_client: AsyncClient, admin_token_headers: dict, test_fund: dict
):
    """Тест получения информации о фонде"""
    response = await async_client.get(
        f"/api/v1/funds/{test_fund['id']}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert UUID(data["id"]) == UUID(test_fund["id"])
    assert data["name"] == test_fund["name"]

async def test_get_nonexistent_fund(async_client: AsyncClient, admin_token_headers: dict):
    """Тест получения информации о несуществующем фонде"""
    nonexistent_uuid = str(uuid.uuid4())
    response = await async_client.get(
        f"/api/v1/funds/{nonexistent_uuid}",
        headers=admin_token_headers
    )
    assert response.status_code == 404

async def test_update_fund(
    async_client: AsyncClient, admin_token_headers: dict, test_fund: dict
):
    """Тест обновления информации о фонде"""
    unique_name = f"Updated Fund Name {uuid.uuid4()}"
    
    response = await async_client.put(
        f"/api/v1/funds/{test_fund['id']}",
        headers=admin_token_headers,
        json={
            "name": unique_name,
            "description": "Updated Fund Description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == unique_name
    assert data["description"] == "Updated Fund Description"
    assert UUID(data["id"]) == UUID(test_fund["id"])

async def test_update_fund_not_found(async_client: AsyncClient, admin_token_headers: dict):
    """Тест обновления несуществующего фонда"""
    nonexistent_uuid = str(uuid.uuid4())
    response = await async_client.put(
        f"/api/v1/funds/{nonexistent_uuid}",
        headers=admin_token_headers,
        json={
            "name": "Updated Fund Name",
            "description": "Updated Fund Description"
        }
    )
    assert response.status_code == 404

async def test_delete_fund(
    async_client: AsyncClient, admin_token_headers: dict, db: AsyncSession
):
    """Тест удаления фонда"""
    # Создаем фонд для удаления
    create_response = await async_client.post(
        "/api/v1/funds/",
        headers=admin_token_headers,
        json={
            "name": "Fund To Delete",
            "description": "This fund will be deleted"
        }
    )
    assert create_response.status_code == 201
    response_data = create_response.json()
    assert "id" in response_data, f"Ответ не содержит id фонда: {response_data}"
    fund_id = response_data["id"]

    # Удаляем фонд
    response = await async_client.delete(
        f"/api/v1/funds/{fund_id}",
        headers=admin_token_headers
    )
    assert response.status_code == 204

    # Проверяем, что фонд действительно удален
    get_response = await async_client.get(
        f"/api/v1/funds/{fund_id}",
        headers=admin_token_headers
    )
    assert get_response.status_code == 404

async def test_delete_fund_with_users(
    async_client: AsyncClient, admin_token_headers: dict, test_fund: dict, db: AsyncSession
):
    """Тест удаления фонда с пользователями"""
    fund_id = test_fund["id"]
    
    # Создаем пользователя, привязанного к фонду
    user_data = {
        "email": f"test_user_{uuid.uuid4()}@example.com",
        "password": "password123",
        "full_name": "Test User",
        "fund_id": fund_id,
        "role": "manager"
    }
    create_user_response = await async_client.post(
        "/api/v1/users/",
        headers=admin_token_headers,
        json=user_data
    )
    assert create_user_response.status_code == 201
    
    # Проверяем, что пользователь действительно создан и привязан к фонду
    users_response = await async_client.get(
        f"/api/v1/users/?fund_id={fund_id}",
        headers=admin_token_headers
    )
    assert users_response.status_code == 200
    users = users_response.json()
    assert len(users) > 0, "Не найдены пользователи, привязанные к фонду"
    
    # Пытаемся удалить фонд с пользователями
    response = await async_client.delete(
        f"/api/v1/funds/{fund_id}",
        headers=admin_token_headers
    )
    assert response.status_code == 400
    assert "users" in response.json()["detail"].lower()

async def test_list_funds(async_client: AsyncClient, admin_token_headers: dict):
    """Тест получения списка фондов"""
    response = await async_client.get(
        "/api/v1/funds/",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Проверяем, что все id являются валидными UUID
    for fund in data:
        assert UUID(fund["id"])

async def test_list_funds_pagination(async_client: AsyncClient, admin_token_headers: dict):
    """Тест пагинации списка фондов"""
    response = await async_client.get(
        "/api/v1/funds/?skip=0&limit=1",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 1

async def test_unauthorized_access(async_client: AsyncClient):
    """Тест доступа без авторизации"""
    endpoints = [
        ("GET", "/api/v1/funds/"),
        ("POST", "/api/v1/funds/"),
        ("GET", "/api/v1/funds/1"),
        ("PUT", "/api/v1/funds/1"),
        ("DELETE", "/api/v1/funds/1"),
    ]
    
    for method, endpoint in endpoints:
        response = await async_client.request(method, endpoint)
        assert response.status_code == 401
        assert "not authenticated" in response.json()["detail"].lower()

async def test_manager_access_restrictions(
    async_client: AsyncClient, test_manager: dict
):
    """Тест ограничений доступа для роли менеджера при работе с фондами"""
    manager_headers = {"Authorization": f"Bearer {test_manager['token']}"}
    
    # Менеджер не должен иметь доступ к созданию фондов
    create_response = await async_client.post(
        "/api/v1/funds/",
        headers=manager_headers,
        json={
            "name": "Manager's Fund",
            "description": "This should not be allowed"
        }
    )
    assert create_response.status_code == 403
    
    # Менеджер не должен иметь доступ к удалению фондов
    delete_response = await async_client.delete(
        f"/api/v1/funds/{test_manager['fund_id']}",
        headers=manager_headers
    )
    assert delete_response.status_code == 403 