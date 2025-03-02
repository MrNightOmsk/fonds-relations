import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from backend.main import app
from backend.models import Person

@pytest.fixture
async def test_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def test_db(test_client):
    # Здесь можно добавить код для создания тестовой базы данных
    yield
    # Здесь можно добавить код для очистки тестовой базы данных

@pytest.mark.asyncio
async def test_create_person(test_client, test_db):
    response = await test_client.post(
        "/api/v1/persons",
        json={
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "ivan@example.com",
            "phone": "+7 (999) 999-99-99"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Иван"
    assert data["last_name"] == "Иванов"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_persons(test_client, test_db):
    response = await test_client.get("/api/v1/persons")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_person(test_client, test_db):
    # Сначала создаем персону
    create_response = await test_client.post(
        "/api/v1/persons",
        json={
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "ivan@example.com",
            "phone": "+7 (999) 999-99-99"
        }
    )
    person_id = create_response.json()["id"]

    # Затем получаем её
    response = await test_client.get(f"/api/v1/persons/{person_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == person_id

@pytest.mark.asyncio
async def test_update_person(test_client, test_db):
    # Сначала создаем персону
    create_response = await test_client.post(
        "/api/v1/persons",
        json={
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "ivan@example.com",
            "phone": "+7 (999) 999-99-99"
        }
    )
    person_id = create_response.json()["id"]

    # Затем обновляем её
    response = await test_client.put(
        f"/api/v1/persons/{person_id}",
        json={
            "first_name": "Петр",
            "last_name": "Петров",
            "middle_name": "Петрович",
            "email": "petr@example.com",
            "phone": "+7 (888) 888-88-88"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Петр"
    assert data["last_name"] == "Петров"

@pytest.mark.asyncio
async def test_delete_person(test_client, test_db):
    # Сначала создаем персону
    create_response = await test_client.post(
        "/api/v1/persons",
        json={
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "ivan@example.com",
            "phone": "+7 (999) 999-99-99"
        }
    )
    person_id = create_response.json()["id"]

    # Затем удаляем её
    response = await test_client.delete(f"/api/v1/persons/{person_id}")
    assert response.status_code == 204

    # Проверяем, что персона действительно удалена
    get_response = await test_client.get(f"/api/v1/persons/{person_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_validation_error(test_client, test_db):
    response = await test_client.post(
        "/api/v1/persons",
        json={
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "invalid-email",  # Неверный формат email
            "phone": "+7 (999) 999-99-99"
        }
    )
    assert response.status_code == 422  # Ошибка валидации 