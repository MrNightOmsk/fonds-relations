import uuid
from datetime import datetime, timedelta
import random
from app.db.session import SessionLocal
from app.models.user import User
from app.models.player import Player
from app.models.case import Case

def create_test_case():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.role == 'manager').first()
        if not user:
            print("Пользователь с ролью manager не найден!")
            return
        
        fund_id = user.fund_id
        player = db.query(Player).first()
        if not player:
            print("Игроки не найдены!")
            return
        
        # Создаем тестовый кейс
        case = Case(
            id=uuid.uuid4(),
            title="Тестовый кейс",
            description="Описание тестового кейса",
            status="open",
            player_id=player.id,
            created_by_user_id=user.id,
            created_by_fund_id=fund_id,
            created_at=datetime.now(),
            arbitrage_type="Test",
            arbitrage_amount=1000,
            arbitrage_currency="USD"
        )
        
        db.add(case)
        db.commit()
        
        print(f"Создан тестовый кейс с ID: {case.id}")
        return case.id
    except Exception as e:
        print(f"Ошибка при создании тестового кейса: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_case() 