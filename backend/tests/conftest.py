import asyncio
import os
from typing import AsyncGenerator, Dict, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.security import create_access_token
from app.db.base import Base
from app.main import app
from app.models import User, Fund

# Используем настройки из конфигурации
SQLALCHEMY_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI).replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=NullPool,
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def db() -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def test_fund(db: AsyncSession) -> Dict:
    """Создает тестовый фонд"""
    fund = Fund(
        name="Test Fund",
        description="Test Fund Description"
    )
    db.add(fund)
    await db.commit()
    await db.refresh(fund)
    return {"id": fund.id, "name": fund.name}

@pytest.fixture(scope="session")
async def test_admin(db: AsyncSession, test_fund: Dict) -> Dict:
    """Создает тестового админа"""
    admin = User(
        email="admin@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        full_name="Test Admin",
        fund_id=test_fund["id"],
        role="admin",
        is_active=True
    )
    db.add(admin)
    await db.commit()
    await db.refresh(admin)
    
    access_token = create_access_token(
        data={"sub": admin.email, "fund_id": str(admin.fund_id)}
    )
    
    return {
        "id": admin.id,
        "email": admin.email,
        "token": access_token,
        "fund_id": admin.fund_id
    }

@pytest.fixture(scope="session")
async def test_manager(db: AsyncSession, test_fund: Dict) -> Dict:
    """Создает тестового менеджера"""
    manager = User(
        email="manager@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        full_name="Test Manager",
        fund_id=test_fund["id"],
        role="manager",
        is_active=True
    )
    db.add(manager)
    await db.commit()
    await db.refresh(manager)
    
    access_token = create_access_token(
        data={"sub": manager.email, "fund_id": str(manager.fund_id)}
    )
    
    return {
        "id": manager.id,
        "email": manager.email,
        "token": access_token,
        "fund_id": manager.fund_id
    }

@pytest.fixture(scope="session")
def admin_token_headers(test_admin: Dict) -> Dict[str, str]:
    return {"Authorization": f"Bearer {test_admin['token']}"} 