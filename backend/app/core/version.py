from datetime import datetime
from typing import Dict

API_VERSION = "1.0.0"
LAST_UPDATE = datetime(2024, 3, 19).strftime("%Y-%m-%d")

RELEASE_NOTES: Dict[str, str] = {
    "1.0.0": "Первый релиз API с базовой функциональностью",
    # При добавлении новых версий, добавляйте их сюда
    # "1.1.0": "Добавлена новая функциональность X",
    # "1.2.0": "Улучшена производительность Y",
} 