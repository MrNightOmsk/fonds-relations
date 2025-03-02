import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

pytestmark = pytest.mark.asyncio

async def test_create_player(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест создания игрока"""
    response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Test Player",
            "birth_date": "1990-01-01",
            "contact_info": {
                "phone": "+1234567890",
                "email": "player@example.com"
            },
            "additional_info": {
                "nickname": "Player1",
                "notes": "Some notes"
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Test Player"
    assert data["birth_date"] == "1990-01-01"
    assert data["contact_info"]["phone"] == "+1234567890"
    assert "id" in data

async def test_create_player_invalid_data(async_client: AsyncClient, admin_token_headers: dict):
    """Тест создания игрока с некорректными данными"""
    invalid_data_cases = [
        {
            "full_name": "",  # Пустое имя
            "birth_date": "1990-01-01"
        },
        {
            "full_name": "Test Player",
            "birth_date": "invalid-date"  # Неверный формат даты
        },
        {
            "full_name": "Test Player",
            "birth_date": "2025-01-01"  # Дата в будущем
        }
    ]

    for invalid_data in invalid_data_cases:
        response = await async_client.post(
            "/api/v1/players/",
            headers=admin_token_headers,
            json=invalid_data
        )
        assert response.status_code == 422

async def test_get_player(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест получения информации об игроке"""
    # Сначала создаем игрока
    create_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Test Player",
            "birth_date": "1990-01-01"
        }
    )
    player_id = create_response.json()["id"]

    # Получаем информацию о созданном игроке
    response = await async_client.get(
        f"/api/v1/players/{player_id}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == player_id
    assert data["full_name"] == "Test Player"

async def test_get_nonexistent_player(async_client: AsyncClient, admin_token_headers: dict):
    """Тест получения информации о несуществующем игроке"""
    response = await async_client.get(
        "/api/v1/players/99999",
        headers=admin_token_headers
    )
    assert response.status_code == 404

async def test_update_player(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест обновления информации об игроке"""
    # Создаем игрока
    create_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Test Player",
            "birth_date": "1990-01-01"
        }
    )
    player_id = create_response.json()["id"]

    # Обновляем информацию
    response = await async_client.put(
        f"/api/v1/players/{player_id}",
        headers=admin_token_headers,
        json={
            "full_name": "Updated Player Name",
            "contact_info": {
                "phone": "+9876543210"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Player Name"
    assert data["contact_info"]["phone"] == "+9876543210"

async def test_delete_player(
    async_client: AsyncClient, admin_token_headers: dict
):
    """Тест удаления игрока"""
    # Создаем игрока
    create_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Player To Delete",
            "birth_date": "1990-01-01"
        }
    )
    player_id = create_response.json()["id"]

    # Удаляем игрока
    response = await async_client.delete(
        f"/api/v1/players/{player_id}",
        headers=admin_token_headers
    )
    assert response.status_code == 204

    # Проверяем, что игрок действительно удален
    get_response = await async_client.get(
        f"/api/v1/players/{player_id}",
        headers=admin_token_headers
    )
    assert get_response.status_code == 404

async def test_list_players(async_client: AsyncClient, admin_token_headers: dict):
    """Тест получения списка игроков"""
    response = await async_client.get(
        "/api/v1/players/",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

async def test_list_players_pagination(async_client: AsyncClient, admin_token_headers: dict):
    """Тест пагинации списка игроков"""
    response = await async_client.get(
        "/api/v1/players/?skip=0&limit=1",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 1

async def test_search_players(async_client: AsyncClient, admin_token_headers: dict):
    """Тест поиска игроков"""
    # Создаем игрока для поиска
    await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Unique Player Name",
            "birth_date": "1990-01-01"
        }
    )

    # Поиск по имени
    response = await async_client.get(
        "/api/v1/players/?search=Unique Player",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(player["full_name"] == "Unique Player Name" for player in data)

async def test_player_fund_isolation(
    async_client: AsyncClient, test_manager: dict, admin_token_headers: dict
):
    """Тест изоляции данных между фондами"""
    # Создаем игрока от имени админа
    admin_player = await async_client.post(
        "/api/v1/players/",
        headers=admin_token_headers,
        json={
            "full_name": "Admin's Player",
            "birth_date": "1990-01-01"
        }
    )
    admin_player_id = admin_player.json()["id"]

    # Пытаемся получить доступ к игроку от имени менеджера другого фонда
    manager_headers = {"Authorization": f"Bearer {test_manager['token']}"}
    response = await async_client.get(
        f"/api/v1/players/{admin_player_id}",
        headers=manager_headers
    )
    assert response.status_code == 404  # Игрок не должен быть виден другому фонду

async def test_player_contact_info_validation(async_client: AsyncClient, admin_token_headers: dict):
    """Тест валидации контактной информации игрока"""
    invalid_contact_info_cases = [
        {
            "phone": "not-a-phone",  # Неверный формат телефона
            "email": "valid@example.com"
        },
        {
            "phone": "+1234567890",
            "email": "not-an-email"  # Неверный формат email
        }
    ]

    for contact_info in invalid_contact_info_cases:
        response = await async_client.post(
            "/api/v1/players/",
            headers=admin_token_headers,
            json={
                "full_name": "Test Player",
                "birth_date": "1990-01-01",
                "contact_info": contact_info
            }
        )
        assert response.status_code == 422 