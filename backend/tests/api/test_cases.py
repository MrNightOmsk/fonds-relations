import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

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
    invalid_data_cases = [
        {
            "player_id": 99999,  # Несуществующий игрок
            "title": "Test Case",
            "description": "Description",
            "status": "open"
        },
        {
            "player_id": 1,
            "title": "",  # Пустой заголовок
            "description": "Description",
            "status": "open"
        },
        {
            "player_id": 1,
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
        "/api/v1/cases/99999",
        headers=admin_token_headers
    )
    assert response.status_code == 404

async def test_update_case(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест обновления информации о кейсе"""
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

    # Обновляем информацию
    response = await async_client.put(
        f"/api/v1/cases/{case_id}",
        headers=admin_token_headers,
        json={
            "title": "Updated Case Title",
            "description": "Updated Description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Case Title"
    assert data["description"] == "Updated Description"

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
    await async_client.put(
        f"/api/v1/cases/{case_id}/close",
        headers=admin_token_headers
    )

    # Пытаемся обновить закрытый кейс
    response = await async_client.put(
        f"/api/v1/cases/{case_id}",
        headers=admin_token_headers,
        json={
            "title": "Updated Title"
        }
    )
    assert response.status_code == 400
    assert "closed" in response.json()["detail"].lower()

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
    """Тест изоляции кейсов между фондами"""
    # Создаем игрока и кейс от имени админа
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

    # Пытаемся получить доступ к кейсу от имени менеджера другого фонда
    manager_headers = {"Authorization": f"Bearer {test_manager['token']}"}
    response = await async_client.get(
        f"/api/v1/cases/{case_id}",
        headers=manager_headers
    )
    assert response.status_code == 404  # Кейс не должен быть виден другому фонду 