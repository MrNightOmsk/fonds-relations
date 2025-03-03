async def test_player_fund_isolation(
    async_client: AsyncClient, test_manager: dict, admin_token_headers: dict, db: Session
):
    """Тест изоляции игроков между фондами - пользователь одного фонда не должен видеть игроков из другого фонда"""
    import uuid
    from app import crud, schemas
    
    # Создаем отдельный фонд для админа для этого теста
    admin_fund_id = str(uuid.uuid4())
    admin_fund = crud.fund.create(
        db=db,
        obj_in=schemas.FundCreate(
            name="Admin Test Fund",
            description="Separate fund for admin test",
            contact_info={"phone": "+1234567890", "email": "admin_test_fund@example.com"}
        ),
        fund_id=admin_fund_id
    )
    
    # Создаем админа с этим фондом
    admin_user = crud.user.create_with_role(
        db=db, 
        obj_in=schemas.UserCreate(
            email="admin_test_players@example.com",
            password="admin",
            full_name="Test Admin For Players Isolation",
            role="admin",
            fund_id=admin_fund_id
        )
    )
    
    # Создаем токен для этого админа
    from app.core.security import create_access_token
    from app.core.config import settings
    from datetime import timedelta
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": admin_user.email, "role": admin_user.role, "fund_id": str(admin_user.fund_id)},
        expires_delta=access_token_expires
    )
    admin_test_headers = {"Authorization": f"Bearer {token}"}
    
    # Получаем заголовки для менеджера
    manager_token_headers = {"Authorization": f"Bearer {test_manager['token']}"}

    # Создаём игрока от имени админа с отдельным фондом
    create_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_test_headers,
        json={
            "full_name": "Admin's Player",
            "birth_date": "1990-01-01",
            "contact_info": {
                "phone": "+1234567890",
                "email": "admin_player@example.com"
            }
        }
    )
    assert create_response.status_code == 201
    player_id = create_response.json()["id"]

    # Менеджер пытается получить игрока, созданного администратором с другим фондом
    # Должен получить 404, так как игрок принадлежит другому фонду
    response = await async_client.get(
        f"/api/v1/players/{player_id}",
        headers=manager_token_headers
    )
    assert response.status_code == 404 