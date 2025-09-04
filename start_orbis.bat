@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
title ORBIS Business Analytics System
echo ============================================================
echo ORBIS Business Analytics System - Windows Launcher
echo ============================================================
echo.

REM Change to script directory
cd /d "%~dp0"
echo [INFO] Working directory: %CD%

set VENV_PY=venv\Scripts\python.exe

REM Check venv exists
if not exist "%VENV_PY%" (
  echo [INFO] Virtual environment not found at %VENV_PY%
  echo Creating virtual environment...
  
  REM Try different Python commands
  python -m venv venv 2>NUL
  if errorlevel 1 (
    py -m venv venv 2>NUL
    if errorlevel 1 (
      python3 -m venv venv 2>NUL
    )
  )
)

if not exist "%VENV_PY%" (
  echo [ERROR] Failed to create virtual environment.
  echo Please ensure Python 3.7+ is installed and accessible via:
  echo - python
  echo - py
  echo - python3
  echo.
  echo You can download Python from: https://python.org/downloads/
  goto :end
)

echo [INFO] Using Python: %VENV_PY%

REM Ensure UTF-8 mode for Python IO
set PYTHONUTF8=1

REM Install requirements if Django is missing
echo [INFO] Checking dependencies...
"%VENV_PY%" -c "import django" 1>NUL 2>&1
if errorlevel 1 (
  echo [INFO] Installing dependencies...
  "%VENV_PY%" -m pip install --upgrade pip
  if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip
    goto :end
  )
  
  "%VENV_PY%" -m pip install -r requirements.txt
  if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    goto :end
  )
  echo [SUCCESS] Dependencies installed
) else (
  echo [INFO] Dependencies already installed
)

REM Run database migrations
echo [INFO] Running database migrations...
"%VENV_PY%" manage.py migrate
if errorlevel 1 (
  echo [WARN] Migrations reported errors. Continuing...
) else (
  echo [SUCCESS] Migrations completed
)

REM Start the transaction system
echo [INFO] Starting ORBIS Business Analytics System...
echo ============================================================
"%VENV_PY%" start_transaction_system.py

:end
echo.
echo ============================================================
echo ORBIS System Launcher Finished
echo ============================================================
pause

