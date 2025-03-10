@echo off
echo Installing required dependencies...
pip install requests
if %errorlevel% neq 0 (
    echo Failed to install required packages
    pause
    exit /b %errorlevel%
)
echo Dependencies installed successfully

echo Starting import of funds from output.json...
python scripts/import_funds_api.py
echo Import process finished. Check log file for details.
pause 