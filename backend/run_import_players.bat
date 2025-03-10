@echo off
echo Installing required dependencies...
pip install requests
if %errorlevel% neq 0 (
    echo Failed to install required packages
    pause
    exit /b %errorlevel%
)
echo Dependencies installed successfully

echo Starting import of players from output.json...
python scripts/import_players_api.py
echo Import process finished. Check log file for details.
pause 