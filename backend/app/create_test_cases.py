#!/usr/bin/env python3
import uuid
from datetime import datetime, timedelta
import random

from sqlalchemy.orm import Session

from db.session import SessionLocal
from models.user import User
from models.player import Player
from models.case import Case
from crud.crud_player import player as crud_player

def create_test_cases_for_fund():
    """
    Создает тестовые кейсы для фонда текущего менеджера.
    Все кейсы будут принадлежать указанному фонду и будут видны пользователю.
    """
    db = SessionLocal()
    try:
        # Найдем пользователя с ролью manager
        user = db.query(User).filter(User.role == 'manager').first()
        if not user:
            print("Пользователь с ролью manager не найден!")
            return
        
        # Получаем ID фонда
        fund_id = user.fund_id
        print(f"Создаем кейсы для фонда с ID: {fund_id}")
        
        # Получаем список игроков для кейсов
        players = db.query(Player).limit(10).all()
        if not players:
            print("Игроки не найдены!")
            return
        
        # Создаем 5 тестовых кейсов
        created_cases = []
        for i in range(5):
            player = random.choice(players)
            
            status = random.choice(['open', 'in_progress', 'closed'])
            closed_at = None
            closed_by_user_id = None
            
            if status == 'closed':
                closed_at = datetime.now() - timedelta(days=random.randint(1, 30))
                closed_by_user_id = user.id
            
            case = Case(
                id=uuid.uuid4(),
                title=f"Тестовый кейс {i+1} - {player.full_name}",
                description=f"Описание тестового кейса {i+1} для игрока {player.full_name}",
                status=status,
                player_id=player.id,
                created_by_user_id=user.id,
                created_by_fund_id=fund_id,
                closed_at=closed_at,
                closed_by_user_id=closed_by_user_id,
                created_at=datetime.now() - timedelta(days=random.randint(0, 60)),
                arbitrage_type="Test",
                arbitrage_amount=random.randint(100, 10000),
                arbitrage_currency="USD"
            )
            
            db.add(case)
            created_cases.append(case)
        
        db.commit()
        
        # Выводим информацию о созданных кейсах
        print(f"Создано {len(created_cases)} тестовых кейсов:")
        for case in created_cases:
            print(f"  - ID: {case.id}, Название: {case.title}, Статус: {case.status}")
        
    except Exception as e:
        print(f"Ошибка при создании тестовых кейсов: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_cases_for_fund() 