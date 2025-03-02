from datetime import datetime
from typing import Dict

API_VERSION = "0.1.0"
LAST_UPDATE = datetime.now().strftime("%Y-%m-%d")

RELEASE_NOTES: Dict[str, str] = {
    "0.1.0": "Начальная версия API с базовой функциональностью: аутентификация, управление пользователями, работа с делами",
    # При добавлении новых версий, добавляйте их сюда
    # "0.1.1": "Исправление ошибок в ...",
    # "0.2.0": "Добавлена новая функциональность ...",
} 