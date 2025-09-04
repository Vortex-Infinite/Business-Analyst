@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
echo ============================================
echo    ORBIS - Simple Django Server Start
echo ============================================
echo.

REM Change to script directory
cd /d "%~dp0"

set VENV_PY=venv\Scripts\python.exe

REM Check venv exists
if not exist "%VENV_PY%" (
  echo [ERROR] Virtual environment not found at %VENV_PY%
  echo Please run start_orbis.bat first to set up the environment
  goto :end
)

REM Ensure UTF-8 mode for Python IO
set PYTHONUTF8=1

echo [INFO] Starting Django development server only...
echo [INFO] Access the application at: http://127.0.0.1:8000
echo [INFO] Press Ctrl+Break to stop the server
echo.

REM Start only the Django server
"%VENV_PY%" manage.py runserver

:end
echo.
echo [INFO] Django server stopped
pause
