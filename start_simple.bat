@echo off
echo ============================================
echo    ORBIS - Quick Django Server Start
echo ============================================
echo.

cd /d "%~dp0"
set VENV_PY=venv\Scripts\python.exe

if not exist "%VENV_PY%" (
    echo [ERROR] Virtual environment not found!
    echo [INFO] Run start_orbis.bat first to set up the system
    pause
    exit /b 1
)

echo [INFO] Starting Django server only...
echo [INFO] Access at: http://0.0.0.0:8000
echo [INFO] Press Ctrl+Break to stop
echo.

"%VENV_PY%" manage.py runserver 0.0.0.0:8000

echo.
echo [INFO] Server stopped
pause
