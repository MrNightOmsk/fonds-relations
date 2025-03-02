import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_create_fund(async_client: AsyncClient, admin_token_headers: dict):
    """Тест создания фонда"""
    response = await async_client.post(
        "/api/v1/funds/",
        headers=admin_token_headers,
        json={
            "name": "New Test Fund",
            "description": "New Test Fund Description"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Test Fund"
    assert data["description"] == "New Test Fund Description"
    assert "id" in data

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
    assert data["id"] == test_fund["id"]
    assert data["name"] == test_fund["name"]

async def test_get_nonexistent_fund(async_client: AsyncClient, admin_token_headers: dict):
    """Тест получения информации о несуществующем фонде"""
    response = await async_client.get(
        "/api/v1/funds/99999",
        headers=admin_token_headers
    )
    assert response.status_code == 404

async def test_update_fund(
    async_client: AsyncClient, admin_token_headers: dict, test_fund: dict
):
    """Тест обновления информации о фонде"""
    response = await async_client.put(
        f"/api/v1/funds/{test_fund['id']}",
        headers=admin_token_headers,
        json={
            "name": "Updated Fund Name",
            "description": "Updated Fund Description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Fund Name"
    assert data["description"] == "Updated Fund Description"

async def test_update_fund_not_found(async_client: AsyncClient, admin_token_headers: dict):
    """Тест обновления несуществующего фонда"""
    response = await async_client.put(
        "/api/v1/funds/99999",
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
    fund_id = create_response.json()["id"]

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
    async_client: AsyncClient, admin_token_headers: dict, test_fund: dict
):
    """Тест удаления фонда с привязанными пользователями"""
    response = await async_client.delete(
        f"/api/v1/funds/{test_fund['id']}",
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
    """Тест ограничений доступа для менеджера"""
    headers = {"Authorization": f"Bearer {test_manager['token']}"}
    
    # Менеджер не должен иметь доступ к созданию фондов
    response = await async_client.post(
        "/api/v1/funds/",
        headers=headers,
        json={
            "name": "New Fund",
            "description": "Description"
        }
    )
    assert response.status_code == 403
    
    # Менеджер не должен иметь доступ к удалению фондов
    response = await async_client.delete(
        f"/api/v1/funds/{test_manager['fund_id']}",
        headers=headers
    )
    assert response.status_code == 403 