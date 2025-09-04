@echo off
echo ============================================
echo    ORBIS System Status Check
echo ============================================
echo.

cd /d "%~dp0"
set VENV_PY=venv\Scripts\python.exe

REM Check Python and Virtual Environment
echo [CHECK] Python Virtual Environment...
if exist "%VENV_PY%" (
    echo   ✅ Virtual environment found
    "%VENV_PY%" --version
) else (
    echo   ❌ Virtual environment not found
    goto :end
)

REM Check Django Installation
echo.
echo [CHECK] Django Installation...
"%VENV_PY%" -c "import django; print(f'   ✅ Django {django.get_version()} installed')" 2>NUL
if errorlevel 1 (
    echo   ❌ Django not installed
)

REM Check PostgreSQL Connection
echo.
echo [CHECK] PostgreSQL Database...
"%VENV_PY%" -c "
import psycopg2
try:
    conn = psycopg2.connect(host='localhost', database='orbis', user='orbis_admin', password='pass', port='5432')
    conn.close()
    print('   ✅ PostgreSQL connection successful')
except Exception as e:
    print('   ❌ PostgreSQL connection failed:', str(e))
    print('   💡 System will use SQLite fallback')
" 2>NUL

REM Check SQLite Database
echo.
echo [CHECK] SQLite Database...
if exist "db.sqlite3" (
    echo   ✅ SQLite database file exists
    "%VENV_PY%" -c "
import sqlite3
try:
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
    tables = cursor.fetchall()
    print(f'   📊 {len(tables)} tables found')
    conn.close()
except Exception as e:
    print('   ❌ SQLite database error:', str(e))
"
) else (
    echo   💡 SQLite database not found (will be created on first run)
)

REM Check Application Data
echo.
echo [CHECK] Application Data...
"%VENV_PY%" -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Transaction, Account, UserProfile
from django.contrib.auth.models import User

try:
    transaction_count = Transaction.objects.count()
    account_count = Account.objects.count()  
    user_count = User.objects.count()
    
    print(f'   📈 {transaction_count} transactions')
    print(f'   🏦 {account_count} accounts') 
    print(f'   👥 {user_count} users')
    
    if user_count > 0:
        print('   ✅ User data available')
    else:
        print('   💡 No users found - create test user on first run')
        
except Exception as e:
    print('   ❌ Cannot access application data:', str(e))
" 2>NUL

echo.
echo ============================================
echo [INFO] System Status Check Complete
echo [INFO] Run start_orbis.bat to launch system  
echo ============================================

:end
pause
