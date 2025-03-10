@echo off
echo Installing required dependencies...
pip install requests
if %errorlevel% neq 0 (
    echo Failed to install required packages
    pause
    exit /b %errorlevel%
)
echo Dependencies installed successfully

echo Starting test of Player API...
python scripts/test_player_api.py
echo Test finished. Check log file for details.
pause 