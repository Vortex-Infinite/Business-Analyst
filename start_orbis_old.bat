@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
echo ============================================
echo    ORBIS Business Analytics System
echo ============================================
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
  echo [INFO] Installing dependencies...
  "%VENV_PY%" -m pip install --upgrade pip
  "%VENV_PY%" -m pip install -r requirements.txt
)

REM Check PostgreSQL connection
echo [INFO] Checking database configuration...
echo [INFO] Attempting to connect to PostgreSQL database...

"%VENV_PY%" -c "
import psycopg2
from decouple import config
try:
    conn = psycopg2.connect(
        host=config('DB_HOST', default='localhost'),
        database=config('DB_NAME'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        port=config('DB_PORT', default='5432')
    )
    conn.close()
    print('[SUCCESS] PostgreSQL connection established')
    exit(0)
except Exception as e:
    print('[ERROR] PostgreSQL connection failed:', str(e))
    exit(1)
" 2>NUL

if errorlevel 1 (
  echo [WARN] PostgreSQL not available or not configured properly
  echo [INFO] Switching to SQLite backup database...
  
  REM Create backup settings file for SQLite
  echo Creating SQLite backup configuration...
  "%VENV_PY%" -c "
import os
settings_content = '''
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.user_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# SQLite Database Configuration (Backup)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/employee_login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

SESSION_COOKIE_AGE = 1800
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
'''

# Backup original settings
import shutil
if os.path.exists('backend/settings.py'):
    shutil.copy('backend/settings.py', 'backend/settings_postgresql.py')
    print('[INFO] PostgreSQL settings backed up to settings_postgresql.py')

# Write SQLite settings
with open('backend/settings.py', 'w') as f:
    f.write(settings_content)
    
print('[INFO] SQLite configuration applied')
"
  
  echo [INFO] Database switched to SQLite mode
) else (
  echo [SUCCESS] PostgreSQL database connection verified
  echo [INFO] Using PostgreSQL database 'orbis'
)

REM Run database migrations
echo [INFO] Running database migrations...
"%VENV_PY%" manage.py migrate
if errorlevel 1 (
  echo [ERROR] Database migrations failed!
  echo [INFO] Please check your database configuration
  goto :end
) else (
  echo [SUCCESS] Database migrations completed
)

REM Check if sample data exists
echo [INFO] Checking for sample data...
"%VENV_PY%" -c "
from core.models import Transaction, Account, UserProfile
from django.contrib.auth.models import User
import django
django.setup()

transaction_count = Transaction.objects.count()
account_count = Account.objects.count()
user_count = User.objects.count()

print(f'[INFO] Found {transaction_count} transactions, {account_count} accounts, {user_count} users')

if transaction_count == 0:
    print('[INFO] No sample data found - will generate initial data')
    exit(1)
else:
    print('[INFO] Sample data available')
    exit(0)
"

if errorlevel 1 (
  echo [INFO] Generating initial sample data...
  "%VENV_PY%" manage.py run_transaction_generator --count 50
  if errorlevel 1 (
    echo [WARN] Sample data generation had issues, continuing...
  ) else (
    echo [SUCCESS] Initial sample data generated
  )
)

REM Start the transaction system
echo [INFO] Starting ORBIS Transaction System...
echo [INFO] - Transaction Generator: Background Mode
echo [INFO] - Django Server: http://127.0.0.1:8000
echo [INFO] - Press Ctrl+C to stop the system
echo.
echo ============================================
echo   System Ready - Access via Browser
echo   URL: http://127.0.0.1:8000
echo ============================================
echo.

REM Start the transaction system (runs Django server + generator)
"%VENV_PY%" start_transaction_system.py

:end
echo.
echo [INFO] ORBIS System stopped
pause

