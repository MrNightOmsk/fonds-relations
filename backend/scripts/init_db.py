import asyncio
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.elasticsearch import es_client, ARBITRAGE_INDEX_MAPPING
from app.core.config import settings
from app.models.arbitrage import PokerRoom, Discipline
from app.crud.user import crud_user
from app.schemas.auth import UserCreate

# Список покерных румов для инициализации
INITIAL_ROOMS = [
    "PokerStars",
    "GGPoker",
    "PartyPoker",
    "888poker",
    "Winamax",
    "iPoker",
]

# Список дисциплин для инициализации
INITIAL_DISCIPLINES = [
    "No Limit Hold'em",
    "Pot Limit Omaha",
    "Mixed Games",
    "Short Deck",
    "Tournaments",
    "Spin & Go",
]

def init_db(db: Session) -> None:
    """Инициализация базы данных начальными данными"""
    # Создаем покерные румы
    for room_name in INITIAL_ROOMS:
        if not db.query(PokerRoom).filter(PokerRoom.name == room_name).first():
            room = PokerRoom(name=room_name)
            db.add(room)
    
    # Создаем дисциплины
    for discipline_name in INITIAL_DISCIPLINES:
        if not db.query(Discipline).filter(Discipline.name == discipline_name).first():
            discipline = Discipline(name=discipline_name)
            db.add(discipline)
    
    # Создаем суперпользователя, если его нет
    superuser = UserCreate(
        email="admin@fondsrelations.com",
        password="admin123",  # В продакшене заменить на безопасный пароль
        full_name="Admin",
        organization="FondsRelations"
    )
    user = crud_user.get_by_email(db, email=superuser.email)
    if not user:
        user = crud_user.create(db, obj_in=superuser)
        user.is_superuser = True
        db.add(user)
    
    db.commit()

async def init_elasticsearch() -> None:
    """Инициализация индексов Elasticsearch"""
    index_name = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_arbitrage"
    
    # Удаляем индекс, если он существует
    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)
    
    # Создаем индекс с нужным маппингом
    es_client.indices.create(
        index=index_name,
        body=ARBITRAGE_INDEX_MAPPING
    )

def main() -> None:
    """Основная функция инициализации"""
    print("Инициализация базы данных...")
    db = SessionLocal()
    try:
        init_db(db)
        print("База данных успешно инициализирована")
    finally:
        db.close()
    
    print("Инициализация Elasticsearch...")
    asyncio.run(init_elasticsearch())
    print("Elasticsearch успешно инициализирован")

if __name__ == "__main__":
    main() 