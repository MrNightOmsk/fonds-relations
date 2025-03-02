from typing import Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from app.core.config import settings
from app.crud.arbitrage import crud_arbitrage_case
from app.models.arbitrage import PokerRoom, Discipline

def create_test_room_and_discipline(db: Session):
    room = PokerRoom(id=uuid4(), name="Test Room")
    discipline = Discipline(id=uuid4(), name="Test Discipline")
    db.add(room)
    db.add(discipline)
    db.commit()
    db.refresh(room)
    db.refresh(discipline)
    return room, discipline

def test_create_arbitrage_case(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    db: Session
) -> None:
    room, discipline = create_test_room_and_discipline(db)
    
    data = {
        "person": {
            "first_name": "John",
            "last_name": "Doe",
            "middle_name": "Smith"
        },
        "nicknames": [
            {
                "room_id": str(room.id),
                "discipline_id": str(discipline.id),
                "nickname": "johndoe"
            }
        ],
        "contacts": [
            {
                "type": "email",
                "value": "john@example.com"
            }
        ],
        "address": {
            "country": "USA",
            "city": "New York"
        },
        "incidents": [
            {
                "type": "fraud",
                "description": "Test incident",
                "amount": 100.50,
                "currency": "USD"
            }
        ]
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/arbitrage/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["person"]["first_name"] == data["person"]["first_name"]
    assert len(content["nicknames"]) == 1
    assert content["nicknames"][0]["nickname"] == "johndoe"

def test_get_arbitrage_case(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    db: Session
) -> None:
    # Создаем тестовый случай
    room, discipline = create_test_room_and_discipline(db)
    data = {
        "person": {
            "first_name": "John",
            "last_name": "Doe"
        },
        "nicknames": [
            {
                "room_id": str(room.id),
                "discipline_id": str(discipline.id),
                "nickname": "johndoe"
            }
        ],
        "contacts": [
            {
                "type": "email",
                "value": "john@example.com"
            }
        ],
        "incidents": [
            {
                "type": "fraud",
                "description": "Test incident",
                "amount": 100.50,
                "currency": "USD"
            }
        ]
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/arbitrage/",
        headers=superuser_token_headers,
        json=data,
    )
    created_case = response.json()
    
    # Получаем созданный случай
    response = client.get(
        f"{settings.API_V1_STR}/arbitrage/{created_case['id']}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == created_case["id"]

def test_search_arbitrage_cases(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    db: Session
) -> None:
    # Создаем тестовый случай
    room, discipline = create_test_room_and_discipline(db)
    data = {
        "person": {
            "first_name": "John",
            "last_name": "Doe"
        },
        "nicknames": [
            {
                "room_id": str(room.id),
                "discipline_id": str(discipline.id),
                "nickname": "johndoe"
            }
        ],
        "contacts": [
            {
                "type": "email",
                "value": "john@example.com"
            }
        ],
        "incidents": [
            {
                "type": "fraud",
                "description": "Test incident",
                "amount": 100.50,
                "currency": "USD"
            }
        ]
    }
    
    client.post(
        f"{settings.API_V1_STR}/arbitrage/",
        headers=superuser_token_headers,
        json=data,
    )
    
    # Поиск по имени
    response = client.get(
        f"{settings.API_V1_STR}/arbitrage/?query=John",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["person"]["first_name"] == "John"

    # Поиск по никнейму
    response = client.get(
        f"{settings.API_V1_STR}/arbitrage/?query=johndoe",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["nicknames"][0]["nickname"] == "johndoe" 