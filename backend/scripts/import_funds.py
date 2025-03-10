#!/usr/bin/env python
import json
import os
import sys
from typing import Set, Dict, Any, List
import uuid
from sqlalchemy.orm import Session

# Добавляем корневую директорию в путь, чтобы импортировать модули приложения
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import crud, models, schemas
from app.api import deps
from app.db.session import SessionLocal

def read_output_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает файл output.json и возвращает его содержимое
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_fund_ids(data: List[Dict[str, Any]]) -> Set[str]:
    """
    Извлекает уникальные ID фондов из поля "author" в данных
    """
    fund_ids = set()
    for item in data:
        if "author" in item and item["author"]:
            fund_ids.add(item["author"])
    return fund_ids

def create_funds(fund_ids: Set[str], db: Session) -> Dict[str, uuid.UUID]:
    """
    Создает фонды в базе данных с именами, равными их ID из output.json
    Возвращает словарь соответствий {original_id: new_uuid}
    """
    fund_mapping = {}
    
    for fund_id in fund_ids:
        # Создаем объект FundCreate
        fund_create = schemas.FundCreate(
            name=fund_id,
            description=f"Фонд, импортированный из output.json (ID: {fund_id})"
        )
        
        # Проверяем, существует ли уже фонд с таким именем
        existing_fund = crud.fund.get_by_name(db=db, name=fund_id)
        if existing_fund:
            print(f"Фонд с именем {fund_id} уже существует, пропускаем")
            fund_mapping[fund_id] = existing_fund.id
            continue
        
        # Создаем новый фонд
        new_fund = crud.fund.create(db=db, obj_in=fund_create)
        print(f"Создан новый фонд: {fund_id} (UUID: {new_fund.id})")
        fund_mapping[fund_id] = new_fund.id
    
    return fund_mapping

def main():
    # Пути к файлу output.json (проверяем несколько вариантов)
    possible_paths = [
        "../output.json",
        "../../output.json",
        "/app/output.json",
        "/output.json",
        "./output.json"
    ]
    
    found = False
    for output_path in possible_paths:
        abs_path = os.path.abspath(output_path)
        print(f"Проверка пути: {abs_path}")
        if os.path.exists(abs_path):
            found = True
            break
    
    if not found:
        print(f"Файл output.json не найден по проверенным путям")
        return
    
    print(f"Чтение файла {abs_path}...")
    data = read_output_json(abs_path)
    print(f"Файл успешно прочитан. Найдено {len(data)} записей.")
    
    # Извлекаем ID фондов
    fund_ids = extract_fund_ids(data)
    print(f"Найдено {len(fund_ids)} уникальных ID фондов.")
    
    # Создаем сессию базы данных
    db = SessionLocal()
    try:
        # Создаем фонды
        fund_mapping = create_funds(fund_ids, db)
        print(f"Обработано {len(fund_mapping)} фондов.")
        
        # Можно сохранить маппинг в файл для дальнейшего использования
        mapping_file = "fund_mapping.json"
        with open(mapping_file, 'w', encoding='utf-8') as f:
            # Преобразуем UUID в строки для сериализации
            serializable_mapping = {k: str(v) for k, v in fund_mapping.items()}
            json.dump(serializable_mapping, f, indent=2, ensure_ascii=False)
        print(f"Соответствие ID фондов сохранено в файл {mapping_file}")
        
    finally:
        db.close()

if __name__ == "__main__":
    main() 