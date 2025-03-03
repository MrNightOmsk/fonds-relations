from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        # Если имя таблицы явно задано в классе, используем его
        if hasattr(cls, '__tablename__'):
            return cls.__tablename__
        # Иначе используем имя класса в нижнем регистре
        return cls.__name__.lower() 