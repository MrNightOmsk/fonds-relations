#!/usr/bin/env python
import json
import random
import uuid
from datetime import datetime, timedelta
import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, text

# Импортируем модели и настройки базы данных
from app.models.fund import Fund
from app.models.user import User
from app.models.player import Player, PlayerContact, PlayerLocation, PlayerNickname, PlayerPaymentMethod
from app.models.case import Case
from app.core.security import get_password_hash

# Создаем соединение с базой данных
def get_db():
    engine_local = create_engine(os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db/app"))
    session = Session(autocommit=False, autoflush=False, bind=engine_local)
    try:
        yield session
    finally:
        session.close()

# Функция загрузки данных из output.json
def load_data_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"Ошибка при чтении файла: {str(e)}")
        return []

# Функция создания фондов
def create_funds(db: Session):
    funds = [
        {"name": "Фонд покерной взаимопомощи", "description": "Первый и самый крупный фонд взаимопомощи для покерных игроков"},
        {"name": "Poker Foundation", "description": "Международный фонд поддержки покерных игроков"},
        {"name": "RUN GOOD фонд", "description": "Фонд для поддержки игроков в сложных ситуациях"},
        {"name": "Честная игра", "description": "Фонд честной игры и борьбы с мошенничеством в покере"},
        {"name": "PokerHelp", "description": "Помощь покерным игрокам по всему миру"}
    ]
    
    created_funds = []
    for fund_data in funds:
        fund = Fund(
            id=uuid.uuid4(),
            name=fund_data["name"],
            description=fund_data["description"],
            created_at=datetime.now()
        )
        db.add(fund)
        created_funds.append(fund)
    
    db.commit()
    print(f"Создано {len(created_funds)} фондов")
    return created_funds

# Функция создания пользователей
def create_users(db: Session, funds):
    users = []
    admin_user = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        hashed_password=get_password_hash("admin"),
        full_name="Администратор Системы",
        fund_id=funds[0].id,
        role="admin",
        is_active=True,
        created_at=datetime.now()
    )
    db.add(admin_user)
    users.append(admin_user)
    
    # Создаем 5 пользователей с разными ролями для разных фондов
    for i in range(5):
        user = User(
            id=uuid.uuid4(),
            email=f"user{i+1}@example.com",
            hashed_password=get_password_hash(f"password{i+1}"),
            full_name=f"Пользователь {i+1}",
            fund_id=funds[i % len(funds)].id,
            role="manager" if i > 0 else "admin",
            is_active=True,
            created_at=datetime.now()
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    print(f"Создано {len(users)} пользователей")
    return users

# Функция создания игроков и сопутствующих данных
def create_players(db: Session, players_data, funds, users, limit=100):
    count = 0
    created_players = []
    
    # Ограничиваем количество игроков
    players_data = players_data[:limit]
    
    for player_data in players_data:
        # Извлекаем ФИО
        full_name = ""
        first_name = ""
        last_name = ""
        middle_name = ""
        
        if player_data.get("FIO") and len(player_data["FIO"]) > 0:
            fio_parts = player_data["FIO"][0].get("firstname", "").split(" ")
            if len(fio_parts) >= 1:
                last_name = fio_parts[0]
            if len(fio_parts) >= 2:
                first_name = fio_parts[1]
            if len(fio_parts) >= 3:
                middle_name = fio_parts[2]
            full_name = player_data["FIO"][0].get("firstname", "")
        
        # Если имени нет, генерируем случайное
        if not first_name:
            first_name = f"Игрок {count+1}"
            full_name = first_name
        
        # Выбираем случайный фонд и пользователя для создания игрока
        fund = random.choice(funds)
        user = random.choice(users)
        
        # Создаем игрока
        player = Player(
            id=uuid.uuid4(),
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            full_name=full_name,
            birth_date=None,  # Можно добавить случайную дату рождения
            created_by_user_id=user.id,
            created_by_fund_id=fund.id,
            created_at=datetime.now() - timedelta(days=random.randint(1, 365))
        )
        db.add(player)
        
        # Добавляем контакты
        if player_data.get("phone"):
            for phone in player_data["phone"]:
                contact = PlayerContact(
                    id=uuid.uuid4(),
                    player_id=player.id,
                    type="phone",
                    value=phone,
                    created_at=player.created_at
                )
                db.add(contact)
        
        if player_data.get("mail"):
            for mail in player_data["mail"]:
                contact = PlayerContact(
                    id=uuid.uuid4(),
                    player_id=player.id,
                    type="email",
                    value=mail,
                    created_at=player.created_at
                )
                db.add(contact)
        
        # Добавляем местоположение
        if player_data.get("location") and len(player_data["location"]) > 0:
            location_data = player_data["location"][0]
            # Разбираем адрес на части (в данных все в поле country)
            address_parts = location_data.get("country", "").split(", ")
            country = address_parts[0] if len(address_parts) > 0 else ""
            city = address_parts[1] if len(address_parts) > 1 else ""
            address = ", ".join(address_parts[2:]) if len(address_parts) > 2 else ""
            
            location = PlayerLocation(
                id=uuid.uuid4(),
                player_id=player.id,
                country=country,
                city=city,
                address=address,
                created_at=player.created_at
            )
            db.add(location)
        
        # Добавляем никнеймы в покерных румах
        nickname_count = 0
        if player_data.get("nickname"):
            for nickname_data in player_data["nickname"]:
                try:
                    # Ограничиваем длину полей до 100 символов
                    nickname_value = nickname_data.get("value", "")
                    room_value = nickname_data.get("room", "")
                    discipline_value = nickname_data.get("discipline", "")
                    
                    # Обрезаем значения, если они превышают допустимую длину
                    if len(room_value) > 100:
                        room_value = room_value[:100]
                    if len(nickname_value) > 100:
                        nickname_value = nickname_value[:100]
                    
                    nickname = PlayerNickname(
                        id=uuid.uuid4(),
                        player_id=player.id,
                        nickname=nickname_value,
                        room=room_value,
                        discipline=discipline_value,
                        created_at=player.created_at
                    )
                    
                    # Добавляем и сразу сохраняем каждый никнейм
                    db.add(nickname)
                    db.flush()
                except Exception as e:
                    print(f"Ошибка при добавлении никнейма {nickname_value} в руме {room_value}: {str(e)}")
                    # Продолжаем выполнение со следующим никнеймом
                
                # Периодически выполняем коммит для сохранения данных
                nickname_count += 1
                if nickname_count >= 10:
                    try:
                        db.commit()
                        nickname_count = 0
                    except Exception as e:
                        db.rollback()
                        print(f"Ошибка при сохранении пакета никнеймов: {str(e)}")
        
        # Добавляем платежные методы
        payment_methods = ["skrill", "neteller", "webmoney", "ecopayz"]
        for method in payment_methods:
            if player_data.get(method) and len(player_data[method]) > 0:
                for value in player_data[method]:
                    payment = PlayerPaymentMethod(
                        id=uuid.uuid4(),
                        player_id=player.id,
                        type=method,
                        value=value,
                        created_at=player.created_at
                    )
                    db.add(payment)
        
        created_players.append(player)
        count += 1
    
    # Сохраняем последние изменения
    try:
        db.commit()
        print(f"Создано {len(created_players)} игроков")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при сохранении последних изменений: {str(e)}")
    
    return created_players

# Функция создания кейсов
def create_cases(db: Session, players_data, players, users, funds, limit=100):
    count = 0
    created_cases = []
    
    # Обрабатываем все записи batch по 50 штук вместо всех сразу
    # Это поможет избежать ошибок с длинными запросами к базе данных
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ошибка при сохранении данных игроков: {str(e)}")
    
    # Ограничиваем количество кейсов
    players_data = players_data[:limit]
    
    for idx, player_data in enumerate(players_data):
        if idx >= len(players):
            break
            
        player = players[idx]
        
        # Проверяем наличие кейсов у игрока
        if player_data.get("case") and len(player_data["case"]) > 0:
            for case_data in player_data["case"]:
                # Выбираем случайного пользователя и фонд для создания кейса
                user = random.choice(users)
                fund = random.choice(funds)
                
                # Определяем статус кейса
                status = random.choice(["open", "closed", "in_progress"])
                closed_at = None
                closed_by_user_id = None
                
                if status == "closed":
                    closed_at = datetime.now() - timedelta(days=random.randint(1, 30))
                    closed_by_user_id = random.choice(users).id
                
                # Обрабатываем значение суммы, удаляя символы валюты
                amount = case_data.get("amount", "0")
                float_amount = None
                
                if amount:
                    try:
                        # Удаляем все нецифровые символы, кроме точки и запятой
                        amount = ''.join(c for c in amount if c.isdigit() or c in '.,')
                        
                        # Обрабатываем случай, когда есть несколько точек или запятых
                        # Оставляем только первую
                        dot_pos = amount.find('.')
                        comma_pos = amount.find(',')
                        
                        if dot_pos >= 0 and comma_pos >= 0:
                            # Если есть и точка, и запятая, оставляем только одну из них
                            if dot_pos < comma_pos:
                                amount = amount.replace(',', '')
                            else:
                                amount = amount.replace('.', '').replace(',', '.')
                        elif comma_pos >= 0:
                            # Если есть только запятая, заменяем ее на точку
                            amount = amount.replace(',', '.')
                        
                        # Проверяем, что в строке осталась только одна точка
                        dots = amount.count('.')
                        if dots > 1:
                            # Оставляем только первую точку
                            first_dot = amount.find('.')
                            amount = amount[:first_dot+1] + amount[first_dot+1:].replace('.', '')
                        
                        # Преобразуем в число
                        if amount:
                            float_amount = float(amount)
                    except ValueError as e:
                        print(f"Не удалось преобразовать сумму '{case_data.get('amount')}' в число: {e}")
                
                # Создаем кейс
                case = Case(
                    id=uuid.uuid4(),
                    player_id=player.id,
                    title=f"Проблема с игроком {player.full_name}",
                    description=case_data.get("descr", "Описание отсутствует"),
                    status=status,
                    arbitrage_type=case_data.get("arbitrage", ""),
                    arbitrage_amount=float_amount,
                    arbitrage_currency="USD",
                    created_by_user_id=user.id,
                    created_by_fund_id=fund.id,
                    closed_at=closed_at,
                    closed_by_user_id=closed_by_user_id,
                    created_at=player.created_at + timedelta(days=random.randint(1, 30))
                )
                db.add(case)
                created_cases.append(case)
                count += 1
                
                # Ограничиваем общее количество кейсов
                if count >= limit:
                    break
        
        # Ограничиваем общее количество кейсов
        if count >= limit:
            break
    
    db.commit()
    print(f"Создано {len(created_cases)} кейсов")
    return created_cases

# Основная функция генерации тестовых данных
def generate_test_data():
    # Загружаем данные из файла
    data_path = "/app/output.json"
    players_data = load_data_from_file(data_path)
    
    if not players_data:
        print("Не удалось загрузить данные из файла")
        return
    
    print(f"Загружено {len(players_data)} записей из файла")
    
    # Создаем сессию базы данных
    db = next(get_db())
    
    try:
        # Очищаем существующие данные (опционально)
        print("Очистка существующих данных...")
        db.execute(text("DELETE FROM case_comments"))
        db.execute(text("DELETE FROM case_evidences"))
        db.execute(text("DELETE FROM cases"))
        db.execute(text("DELETE FROM player_nicknames"))
        db.execute(text("DELETE FROM player_payment_methods"))
        db.execute(text("DELETE FROM player_locations"))
        db.execute(text("DELETE FROM player_contacts"))
        db.execute(text("DELETE FROM player_social_media"))
        db.execute(text("DELETE FROM players"))
        db.execute(text("DELETE FROM users"))
        db.execute(text("DELETE FROM funds"))
        db.commit()
        
        # Генерируем тестовые данные
        print("Генерация тестовых данных...")
        funds = create_funds(db)
        users = create_users(db, funds)
        players = create_players(db, players_data, funds, users, limit=100)
        cases = create_cases(db, players_data, players, users, funds, limit=100)
        
        print("Тестовые данные успешно созданы!")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при генерации тестовых данных: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_test_data() 