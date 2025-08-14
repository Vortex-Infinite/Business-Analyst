#!/usr/bin/env python
"""
Transaction System Startup Script
This script automatically starts the transaction generator when Django runs
"""

import os
import sys
import django
import threading
import time
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def run_transaction_generator():
    """Run the transaction generator in daemon mode"""
    try:
        from django.core.management import call_command
        print("Starting transaction generator in background...")
        call_command('run_transaction_generator', '--daemon')
    except Exception as e:
        print(f"Error starting transaction generator: {e}")

def start_django_server():
    """Start the Django development server"""
    try:
        print("Starting Django development server...")
        execute_from_command_line(['manage.py', 'runserver'])
    except Exception as e:
        print(f"Error starting Django server: {e}")

if __name__ == "__main__":
    print("Starting ORBIS Transaction System...")
    
    # Start transaction generator in a separate thread
    transaction_thread = threading.Thread(target=run_transaction_generator, daemon=True)
    transaction_thread.start()
    
    # Give the transaction generator a moment to initialize
    time.sleep(2)
    
    # Start Django server
    start_django_server()

