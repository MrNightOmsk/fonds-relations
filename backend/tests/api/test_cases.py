import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

pytestmark = pytest.mark.asyncio

async def test_create_case(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест создания кейса"""
    # Сначала создаем игрока
    player_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Test Player",
            "birth_date": "1990-01-01"
        }
    )
    player_id = player_response.json()["id"]

    # Создаем кейс
    response = await async_client.post(
        "/api/v1/cases/",
        headers=admin_token_headers,
        json={
            "player_id": player_id,
            "title": "Test Case",
            "description": "Test Case Description",
            "status": "open"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Case"
    assert data["player_id"] == player_id
    assert data["status"] == "open"
    assert "id" in data

async def test_create_case_invalid_data(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест создания кейса с некорректными данными"""
    random_uuid = str(uuid.uuid4())
    invalid_data_cases = [
        {
            "player_id": str(uuid.uuid4()),  # Несуществующий игрок
            "title": "Test Case",
            "description": "Description",
            "status": "open"
        },
        {
            "player_id": random_uuid,
            "title": "",  # Пустой заголовок
            "description": "Description",
            "status": "open"
        },
        {
            "player_id": random_uuid,
            "title": "Test Case",
            "description": "Description",
            "status": "invalid_status"  # Неверный статус
        }
    ]

    for invalid_data in invalid_data_cases:
        response = await async_client.post(
            "/api/v1/cases/",
            headers=admin_token_headers,
            json=invalid_data
        )
        assert response.status_code in [404, 422]

async def test_get_case(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест получения информации о кейсе"""
    # Создаем игрока и кейс
    player_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Test Player",
            "birth_date": "1990-01-01"
        }
    )
    player_id = player_response.json()["id"]

    case_response = await async_client.post(
        "/api/v1/cases/",
        headers=admin_token_headers,
        json={
            "player_id": player_id,
            "title": "Test Case",
            "description": "Description",
            "status": "open"
        }
    )
    case_id = case_response.json()["id"]

    # Получаем информацию о кейсе
    response = await async_client.get(
        f"/api/v1/cases/{case_id}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == case_id
    assert data["title"] == "Test Case"
    assert data["player_id"] == player_id

async def test_get_nonexistent_case(async_client: AsyncClient, admin_token_headers: dict):
    """Тест получения информации о несуществующем кейсе"""
    response = await async_client.get(
        f"/api/v1/cases/{uuid.uuid4()}",
        headers=admin_token_headers
    )
    assert response.status_code == 404

async def test_update_case(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест обновления информации о кейсе"""
    # Создаем игрока
    player_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Test Player for Case Update",
            "birth_date": "1990-01-01",
            "contact_info": {
                "phone": "+1234567890",
                "email": "player_case_update@example.com"
            }
        }
    )
    assert player_response.status_code == 201
    player_id = player_response.json()["id"]
    
    # Создаем кейс для обновления
    case_response = await async_client.post(
        "/api/v1/cases/",
        headers=admin_token_headers,
        json={
            "title": "Test Case for Update",
            "description": "Original description",
            "player_id": player_id,
            "status": "open"
        }
    )
    assert case_response.status_code == 201
    case_id = case_response.json()["id"]
    
    # Обновляем кейс
    update_response = await async_client.put(
        f"/api/v1/cases/{case_id}",
        headers=admin_token_headers,
        json={
            "title": "Updated Test Case",
            "description": "Updated description"
        }
    )
    assert update_response.status_code == 200
    updated_case = update_response.json()
    assert updated_case["title"] == "Updated Test Case"
    assert updated_case["description"] == "Updated description"
    assert updated_case["player_id"] == player_id

async def test_close_case(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест закрытия кейса"""
    # Создаем игрока и кейс
    player_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Test Player",
            "birth_date": "1990-01-01"
        }
    )
    player_id = player_response.json()["id"]

    case_response = await async_client.post(
        "/api/v1/cases/",
        headers=admin_token_headers,
        json={
            "player_id": player_id,
            "title": "Test Case",
            "description": "Description",
            "status": "open"
        }
    )
    case_id = case_response.json()["id"]

    # Закрываем кейс
    response = await async_client.put(
        f"/api/v1/cases/{case_id}/close",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "closed"
    assert data["closed_at"] is not None
    assert data["closed_by_user_id"] is not None

async def test_update_closed_case(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест попытки обновления закрытого кейса"""
    # Создаем игрока
    player_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Test Player for Closed Case",
            "birth_date": "1990-01-01",
            "contact_info": {
                "phone": "+1234567890",
                "email": "player_closed_case@example.com"
            }
        }
    )
    assert player_response.status_code == 201
    player_id = player_response.json()["id"]
    
    # Создаем кейс
    case_response = await async_client.post(
        "/api/v1/cases/",
        headers=admin_token_headers,
        json={
            "title": "Test Closed Case",
            "description": "Description for closed case",
            "player_id": player_id,
            "status": "open"
        }
    )
    assert case_response.status_code == 201
    case_id = case_response.json()["id"]
    
    # Закрываем кейс
    close_response = await async_client.put(
        f"/api/v1/cases/{case_id}/close",
        headers=admin_token_headers
    )
    assert close_response.status_code == 200
    
    # Пытаемся обновить закрытый кейс
    update_response = await async_client.put(
        f"/api/v1/cases/{case_id}",
        headers=admin_token_headers,
        json={
            "title": "Updated Closed Case",
            "description": "This update should be rejected"
        }
    )
    assert update_response.status_code == 400
    assert "closed" in update_response.json()["detail"].lower()

async def test_list_cases(async_client: AsyncClient, admin_token_headers: dict):
    """Тест получения списка кейсов"""
    response = await async_client.get(
        "/api/v1/cases/",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

async def test_list_cases_pagination(async_client: AsyncClient, admin_token_headers: dict):
    """Тест пагинации списка кейсов"""
    response = await async_client.get(
        "/api/v1/cases/?skip=0&limit=1",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 1

async def test_list_cases_by_player(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест получения списка кейсов конкретного игрока"""
    # Создаем игрока и кейсы
    player_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Test Player",
            "birth_date": "1990-01-01"
        }
    )
    player_id = player_response.json()["id"]

    # Создаем несколько кейсов для игрока
    for i in range(3):
        await async_client.post(
            "/api/v1/cases/",
            headers=admin_token_headers,
            json={
                "player_id": player_id,
                "title": f"Test Case {i}",
                "description": "Description",
                "status": "open"
            }
        )

    # Получаем кейсы игрока
    response = await async_client.get(
        f"/api/v1/cases/?player_id={player_id}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    for case in data:
        assert case["player_id"] == player_id

async def test_case_fund_isolation(
    async_client: AsyncClient, test_manager: dict, admin_token_headers: dict
):
    """Тест изоляции кейсов между фондами - пользователь одного фонда не должен видеть кейсы из другого фонда"""
    # Получаем заголовки для менеджера
    manager_token_headers = {"Authorization": f"Bearer {test_manager['token']}"}
    
    # Админ создает игрока и кейс
    player_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Admin Player for Case Isolation",
            "birth_date": "1990-01-01",
            "contact_info": {
                "phone": "+1234567890",
                "email": "admin_case_isolation@example.com"
            }
        }
    )
    assert player_response.status_code == 201
    player_id = player_response.json()["id"]
    
    case_response = await async_client.post(
        "/api/v1/cases/",
        headers=admin_token_headers,
        json={
            "title": "Admin Case",
            "description": "Case created by admin",
            "player_id": player_id,
            "status": "open"
        }
    )
    assert case_response.status_code == 201
    case_id = case_response.json()["id"]
    
    # Менеджер пытается получить доступ к кейсу, созданному администратором
    # Должен получить 404, так как кейс принадлежит другому фонду
    get_response = await async_client.get(
        f"/api/v1/cases/{case_id}",
        headers=manager_token_headers
    )
    assert get_response.status_code == 404
    assert "not found" in get_response.json()["detail"].lower() 