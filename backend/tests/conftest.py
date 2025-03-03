import asyncio
import os
from typing import AsyncGenerator, Dict, Generator
import uuid

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from sqlalchemy.sql import select

from app.core.config import settings
from app.core.security import create_access_token
from app.db.base import Base
from app.main import app

# Импортируем все модели, чтобы они были доступны для Base.metadata
from app.models import User, Fund, Player, Case, CaseEvidence, PlayerContact, PlayerLocation, PlayerNickname

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
        # Сначала удаляем все таблицы, если они существуют
        await conn.run_sync(Base.metadata.drop_all)
        # Затем создаем таблицы заново, обеспечивая правильный порядок создания
        # Сначала создаем таблицу funds
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS funds (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(255) NOT NULL UNIQUE, 
                description TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """))
        
        # Затем создаем таблицу users
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) NOT NULL UNIQUE,
                hashed_password VARCHAR(255) NOT NULL,
                full_name VARCHAR(255),
                fund_id UUID NOT NULL REFERENCES funds(id),
                role VARCHAR(50) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """))
        
        # Создаем таблицу players
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS players (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                full_name VARCHAR(255) NOT NULL,
                birth_date DATE,
                contact_info JSONB,
                additional_info JSONB,
                created_by_user_id UUID NOT NULL REFERENCES users(id),
                created_by_fund_id UUID NOT NULL REFERENCES funds(id),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """))
        
        # Создаем таблицу player_contacts
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS player_contacts (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                player_id UUID NOT NULL REFERENCES players(id),
                type VARCHAR(50) NOT NULL,
                value VARCHAR(255) NOT NULL,
                description TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """))
        
        # Создаем таблицу player_locations
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS player_locations (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                player_id UUID NOT NULL REFERENCES players(id),
                country VARCHAR(100),
                city VARCHAR(100),
                address TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """))
        
        # Создаем таблицу player_nicknames
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS player_nicknames (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                player_id UUID NOT NULL REFERENCES players(id),
                nickname VARCHAR(100) NOT NULL,
                source VARCHAR(100),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """))
        
        # Создаем таблицу cases
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS cases (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                player_id UUID NOT NULL REFERENCES players(id),
                title VARCHAR(255) NOT NULL,
                description TEXT,
                status VARCHAR(50) NOT NULL,
                created_by_user_id UUID NOT NULL REFERENCES users(id),
                created_by_fund_id UUID NOT NULL REFERENCES funds(id),
                closed_at TIMESTAMP WITH TIME ZONE,
                closed_by_user_id UUID REFERENCES users(id),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """))
        
        # Создаем таблицу case_evidences
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS case_evidences (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                case_id UUID NOT NULL REFERENCES cases(id),
                type VARCHAR(50) NOT NULL,
                file_path VARCHAR(255) NOT NULL,
                uploaded_by_id UUID REFERENCES users(id),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """))
        
        # Создаем таблицу auditlog
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS auditlog (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                entity_type VARCHAR(50) NOT NULL,
                entity_id UUID NOT NULL,
                action VARCHAR(50) NOT NULL,
                changes JSONB,
                performed_by_id UUID REFERENCES users(id),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """))
        
        # Создаем таблицу notification_subscriptions
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS notification_subscriptions (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL REFERENCES users(id),
                type VARCHAR(50) NOT NULL,
                settings JSONB,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """))
        
        # Создаем остальные таблицы через SQLAlchemy
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
    # Используем базовый URL с правильным префиксом API для тестов
    base_url = "http://test"
    async with AsyncClient(app=app, base_url=base_url) as ac:
        yield ac

@pytest.fixture(scope="session")
async def test_fund(db: AsyncSession) -> Dict:
    """Создает тестовый фонд"""
    fund_name = f"Test Fund {uuid.uuid4()}"
    fund = Fund(
        name=fund_name,
        description="Test Fund Description"
    )
    db.add(fund)
    await db.commit()
    await db.refresh(fund)
    return {"id": str(fund.id), "name": fund.name}

@pytest.fixture(scope="session")
async def test_admin(db: AsyncSession, test_fund: dict):
    """Создает тестового админа"""
    # Проверяем существует ли уже пользователь с таким email
    existing_admin = await db.execute(
        select(User).where(User.email == "admin@example.com")
    )
    existing_admin = existing_admin.scalars().first()
    
    if existing_admin:
        admin = existing_admin
    else:
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
        subject=admin.id,
        extra_data={"fund_id": str(admin.fund_id), "role": admin.role}
    )
    
    return {
        "id": admin.id,
        "email": admin.email,
        "token": access_token,
        "fund_id": admin.fund_id
    }

@pytest.fixture(scope="session")
async def test_manager(db: AsyncSession, test_fund: dict):
    """Создает тестового менеджера"""
    # Проверяем существует ли уже пользователь с таким email
    existing_manager = await db.execute(
        select(User).where(User.email == "manager@example.com")
    )
    existing_manager = existing_manager.scalars().first()
    
    if existing_manager:
        manager = existing_manager
    else:
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
        subject=manager.id,
        extra_data={"fund_id": str(manager.fund_id), "role": manager.role}
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