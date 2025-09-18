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
  echo [INFO] Creating virtual environment...
  python -m venv venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment. Please ensure Python is installed.
    goto :end
  )
)

if not exist "%VENV_PY%" (
  echo [ERROR] Virtual environment setup failed.
  goto :end
)

echo [SUCCESS] Virtual environment ready

REM Ensure UTF-8 mode for Python IO
set PYTHONUTF8=1

REM Check if Django is installed
echo [INFO] Checking Django installation...
"%VENV_PY%" -c "import django" >NUL 2>&1
if errorlevel 1 (
  echo [INFO] Installing dependencies...
  "%VENV_PY%" -m pip install --upgrade pip
  "%VENV_PY%" -m pip install -r requirements.txt
  if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    goto :end
  )
  echo [SUCCESS] Dependencies installed
) else (
  echo [SUCCESS] Django already installed
)

REM Test database connection
echo [INFO] Testing database connection...
"%VENV_PY%" manage.py check --database default >NUL 2>&1
if errorlevel 1 (
  echo [WARN] Database connection issues detected
  echo [INFO] Switching to SQLite fallback...
  
  REM Create SQLite settings backup
  if exist "backend\settings.py" (
    copy "backend\settings.py" "backend\settings_postgresql_backup.py" >NUL 2>&1
    echo [INFO] PostgreSQL settings backed up
  )
  
  REM Create simple SQLite settings
  (
    echo from pathlib import Path
    echo import os
    echo.
    echo BASE_DIR = Path^(__file__^).resolve^(^).parent.parent
    echo SECRET_KEY = 'django-insecure-your-secret-key-here'
    echo DEBUG = True
    echo ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    echo.
    echo INSTALLED_APPS = [
    echo     'django.contrib.admin',
    echo     'django.contrib.auth',
    echo     'django.contrib.contenttypes',
    echo     'django.contrib.sessions',
    echo     'django.contrib.messages',
    echo     'django.contrib.staticfiles',
    echo     'core.apps.CoreConfig',
    echo ]
    echo.
    echo MIDDLEWARE = [
    echo     'django.middleware.security.SecurityMiddleware',
    echo     'django.contrib.sessions.middleware.SessionMiddleware',
    echo     'django.middleware.common.CommonMiddleware',
    echo     'django.middleware.csrf.CsrfViewMiddleware',
    echo     'django.contrib.auth.middleware.AuthenticationMiddleware',
    echo     'django.contrib.messages.middleware.MessageMiddleware',
    echo     'django.middleware.clickjacking.XFrameOptionsMiddleware',
    echo ]
    echo.
    echo ROOT_URLCONF = 'backend.urls'
    echo.
    echo TEMPLATES = [
    echo     {
    echo         'BACKEND': 'django.template.backends.django.DjangoTemplates',
    echo         'DIRS': [os.path.join^(BASE_DIR, 'core/templates'^)],
    echo         'APP_DIRS': True,
    echo         'OPTIONS': {
    echo             'context_processors': [
    echo                 'django.template.context_processors.debug',
    echo                 'django.template.context_processors.request',
    echo                 'django.contrib.auth.context_processors.auth',
    echo                 'django.contrib.messages.context_processors.messages',
    echo                 'core.context_processors.user_context',
    echo             ],
    echo         },
    echo     },
    echo ]
    echo.
    echo WSGI_APPLICATION = 'backend.wsgi.application'
    echo.
    echo DATABASES = {
    echo     'default': {
    echo         'ENGINE': 'django.db.backends.sqlite3',
    echo         'NAME': BASE_DIR / 'db.sqlite3',
    echo     }
    echo }
    echo.
    echo LANGUAGE_CODE = 'en-us'
    echo TIME_ZONE = 'UTC'
    echo USE_I18N = True
    echo USE_TZ = True
    echo STATIC_URL = 'static/'
    echo STATICFILES_DIRS = [os.path.join^(BASE_DIR, 'core/static'^)]
    echo STATIC_ROOT = os.path.join^(BASE_DIR, 'staticfiles'^)
    echo DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    echo LOGIN_URL = '/employee_login/'
    echo LOGIN_REDIRECT_URL = '/dashboard/'
    echo LOGOUT_REDIRECT_URL = '/'
    echo SESSION_COOKIE_AGE = 1800
    echo SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    echo SESSION_SAVE_EVERY_REQUEST = True
  ) > "backend\settings.py"
  
  echo [SUCCESS] SQLite configuration applied
) else (
  echo [SUCCESS] Database connection verified
)

REM Run migrations
echo [INFO] Running database migrations...
"%VENV_PY%" manage.py migrate
if errorlevel 1 (
  echo [ERROR] Database migrations failed
  goto :end
) else (
  echo [SUCCESS] Database migrations completed
)

REM Check for sample data
echo [INFO] Checking for sample data...
"%VENV_PY%" manage.py shell -c "from core.models import Transaction; print('Sample data exists' if Transaction.objects.count() > 0 else 'No sample data')" 2>NUL
if errorlevel 1 (
  echo [INFO] Generating sample data...
  "%VENV_PY%" manage.py run_transaction_generator --count 20 2>NUL
)

REM Start the system
echo [INFO] Starting ORBIS system...
echo [INFO] Server will be available at: http://127.0.0.1:8000
echo [INFO] Press Ctrl+Break to stop
echo ============================================
echo.

"%VENV_PY%" start_transaction_system.py

:end
echo.
echo [INFO] ORBIS System stopped
pause
