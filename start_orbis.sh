#!/bin/bash

# ORBIS Business Analytics System - Linux Startup Script
echo "============================================"
echo "    ORBIS Business Analytics System"
echo "============================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_PY="venv/bin/python"

# Check if venv exists
if [ ! -f "$VENV_PY" ]; then
  echo "[ERROR] Virtual environment not found at $VENV_PY"
  echo "[INFO] Creating virtual environment..."
  python3 -m venv venv
  if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment. Please ensure Python 3 is installed."
    exit 1
  fi
  
  echo "[SUCCESS] Virtual environment created"
  echo "[INFO] Installing dependencies..."
  "$VENV_PY" -m pip install --upgrade pip
  "$VENV_PY" -m pip install -r requirements.txt
  if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
  fi
  echo "[SUCCESS] Dependencies installed"
fi

if [ ! -f "$VENV_PY" ]; then
  echo "[ERROR] Virtual environment setup failed."
  exit 1
fi

echo "[SUCCESS] Virtual environment ready"

# Ensure UTF-8 mode for Python IO
export PYTHONUTF8=1

# Test database connection
echo "[INFO] Testing database connection..."
"$VENV_PY" manage.py check --database default >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "[WARN] Database connection issues detected"
  echo "[INFO] Switching to SQLite fallback..."
  
  # Create SQLite settings backup
  if [ -f "backend/settings.py" ]; then
    cp "backend/settings.py" "backend/settings_postgresql_backup.py" 2>/dev/null
    echo "[INFO] PostgreSQL settings backed up"
  fi
  
  # Create simple SQLite settings
  cat > "backend/settings.py" << 'EOF'
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
EOF
  
  echo "[SUCCESS] SQLite configuration applied"
else
  echo "[SUCCESS] Database connection verified"
fi

# Run migrations
echo "[INFO] Running database migrations..."
"$VENV_PY" manage.py migrate
if [ $? -ne 0 ]; then
  echo "[ERROR] Database migrations failed"
  exit 1
else
  echo "[SUCCESS] Database migrations completed"
fi

# Check for sample data
echo "[INFO] Checking for sample data..."
"$VENV_PY" manage.py shell -c "from core.models import Transaction; print('Sample data exists' if Transaction.objects.count() > 0 else 'No sample data')" 2>/dev/null
if [ $? -ne 0 ]; then
  echo "[INFO] Generating sample data..."
  "$VENV_PY" manage.py run_transaction_generator --count 20 2>/dev/null
fi

# Start the system
echo "[INFO] Starting ORBIS system..."
echo "[INFO] Server will be available at: http://127.0.0.1:8000"
echo "[INFO] Press Ctrl+C to stop"
echo "============================================"
echo ""

"$VENV_PY" start_transaction_system.py

echo ""
echo "[INFO] ORBIS System stopped"
