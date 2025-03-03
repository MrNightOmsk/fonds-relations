async def test_case_fund_isolation(
    async_client: AsyncClient, test_manager: dict, admin_token_headers: dict, db: Session
):
    """Тест изоляции кейсов между фондами - пользователь одного фонда не должен видеть кейсы из другого фонда"""
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
            email="admin_test@example.com",
            password="admin",
            full_name="Test Admin For Fund Isolation",
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

    # Админ создает игрока и кейс с отдельным фондом
    player_response = await async_client.post(
        "/api/v1/players/",
        headers=admin_test_headers,
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
        headers=admin_test_headers,
        json={
            "title": "Admin Case",
            "description": "Case created by admin",
            "player_id": player_id,
            "status": "open"
        }
    )
    assert case_response.status_code == 201
    case_id = case_response.json()["id"]

    # Теперь у нас точно разные фонды, проверяем
    # Менеджер пытается получить доступ к кейсу, созданному администратором с другим фондом
    # Должен получить 404, так как кейс принадлежит другому фонду
    get_response = await async_client.get(
        f"/api/v1/cases/{case_id}",
        headers=manager_token_headers
    )
    assert get_response.status_code == 404 