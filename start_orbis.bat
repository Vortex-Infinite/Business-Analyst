@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
echo Starting ORBIS Business Analytics System...
echo.

REM Change to script directory
cd /d "%~dp0"

set VENV_PY=venv\Scripts\python.exe

REM Check venv exists
if not exist "%VENV_PY%" (
  echo [ERROR] Virtual environment not found at %VENV_PY%
  echo Creating virtual environment...
  python -m venv venv
)

if not exist "%VENV_PY%" (
  echo [ERROR] Failed to create virtual environment. Please ensure Python is installed and in PATH.
  goto :end
)

REM Ensure UTF-8 mode for Python IO
set PYTHONUTF8=1

REM Install requirements if Django is missing
"%VENV_PY%" -c "import django" 1>NUL 2>&1
if errorlevel 1 (
  echo Installing dependencies...
  "%VENV_PY%" -m pip install --upgrade pip
  "%VENV_PY%" -m pip install -r requirements.txt
)

REM Run database migrations (PostgreSQL must be running)
echo Running database migrations...
"%VENV_PY%" manage.py migrate
if errorlevel 1 (
  echo [WARN] Migrations reported errors. Continuing...
)

REM Start the transaction system (runs Django server + generator)
"%VENV_PY%" start_transaction_system.py

:end
pause

