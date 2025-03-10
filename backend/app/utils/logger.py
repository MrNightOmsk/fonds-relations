import logging
from typing import Optional

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Создаем логгер для приложения
logger = logging.getLogger("app")

def setup_logger(log_level: Optional[str] = None) -> logging.Logger:
    """
    Настройка и получение логгера для приложения.
    
    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Настроенный логгер
    """
    if log_level:
        numeric_level = getattr(logging, log_level.upper(), None)
        if isinstance(numeric_level, int):
            logger.setLevel(numeric_level)
    
    return logger

# Установка уровня логирования для запросов
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

# Экспортируем логгер для использования в других модулях
__all__ = ["logger", "setup_logger"] 