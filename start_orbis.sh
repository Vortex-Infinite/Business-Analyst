#!/bin/bash

# ORBIS Business Analytics System Launcher for Unix-like systems (Linux/macOS)
# This script provides cross-platform compatibility for starting the system

set -e  # Exit on any error

echo "Starting ORBIS Business Analytics System..."
echo

# Change to script directory
cd "$(dirname "$0")"

VENV_PY="venv/bin/python"

# Check if virtual environment exists
if [ ! -f "$VENV_PY" ]; then
    echo "[INFO] Virtual environment not found at $VENV_PY"
    echo "Creating virtual environment..."
    python3 -m venv venv || python -m venv venv
fi

if [ ! -f "$VENV_PY" ]; then
    echo "[ERROR] Failed to create virtual environment. Please ensure Python is installed."
    exit 1
fi

# Ensure UTF-8 mode for Python IO
export PYTHONUTF8=1

# Install requirements if Django is missing
if ! "$VENV_PY" -c "import django" >/dev/null 2>&1; then
    echo "Installing dependencies..."
    "$VENV_PY" -m pip install --upgrade pip
    "$VENV_PY" -m pip install -r requirements.txt
fi

# Run database migrations
echo "Running database migrations..."
if ! "$VENV_PY" manage.py migrate; then
    echo "[WARN] Migrations reported errors. Continuing..."
fi

# Start the transaction system
echo "Starting ORBIS system..."
"$VENV_PY" start_transaction_system.py
