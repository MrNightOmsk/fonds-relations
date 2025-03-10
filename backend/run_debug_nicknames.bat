@echo off
echo Запускаем диагностику никнеймов игроков...

REM Установка необходимых зависимостей
pip install requests

REM Запуск скрипта диагностики
python scripts/debug_player_nicknames.py

echo Диагностика завершена. Проверьте файл debug_player_nicknames.log для получения полной информации.
pause 