#!/usr/bin/env python3
import uuid

def test_uuid(value):
    try:
        uuid_obj = uuid.UUID(value)
        print(f"'{value}' - валидный UUID: {uuid_obj}")
        return True
    except ValueError as e:
        print(f"'{value}' - невалидный UUID. Ошибка: {e}")
        return False

# Тестируем разные значения
values_to_test = ['1', '00000000-0000-0000-0000-000000000001', 'case1', 'invalid-uuid']
for val in values_to_test:
    test_uuid(val) 