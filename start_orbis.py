#!/usr/bin/env python3
"""
ORBIS Business Analytics System - Universal Launcher
This Python script provides cross-platform compatibility for all operating systems
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

def get_platform_info():
    """Get platform-specific information"""
    system = platform.system().lower()
    is_windows = system == 'windows'
    is_mac = system == 'darwin'
    is_linux = system == 'linux'
    
    return {
        'system': system,
        'is_windows': is_windows,
        'is_mac': is_mac,
        'is_linux': is_linux,
        'python_exe': 'python.exe' if is_windows else 'python3'
    }

def get_venv_python(platform_info):
    """Get the virtual environment Python executable path"""
    if platform_info['is_windows']:
        return Path('venv') / 'Scripts' / 'python.exe'
    else:
        return Path('venv') / 'bin' / 'python'

def create_virtual_environment(platform_info):
    """Create virtual environment if it doesn't exist"""
    venv_path = Path('venv')
    venv_python = get_venv_python(platform_info)
    
    if not venv_python.exists():
        print(f"[INFO] Virtual environment not found at {venv_python}")
        print("Creating virtual environment...")
        
        try:
            # Try different Python commands based on platform
            python_commands = []
            if platform_info['is_windows']:
                python_commands = ['python', 'py', 'python3']
            else:
                python_commands = ['python3', 'python']
            
            for python_cmd in python_commands:
                try:
                    subprocess.run([python_cmd, '-m', 'venv', 'venv'], check=True)
                    print(f"[SUCCESS] Virtual environment created using {python_cmd}")
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            else:
                raise Exception("Failed to create virtual environment with any Python command")
                
        except Exception as e:
            print(f"[ERROR] Failed to create virtual environment: {e}")
            print("Please ensure Python is installed and accessible from PATH")
            return False
    
    return venv_python.exists()

def install_dependencies(venv_python):
    """Install required dependencies"""
    try:
        # Check if Django is installed
        result = subprocess.run([str(venv_python), '-c', 'import django'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("Installing dependencies...")
            subprocess.run([str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
            subprocess.run([str(venv_python), '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
            print("[SUCCESS] Dependencies installed")
        else:
            print("[INFO] Dependencies already installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install dependencies: {e}")
        return False

def run_migrations(venv_python):
    """Run database migrations"""
    try:
        print("Running database migrations...")
        result = subprocess.run([str(venv_python), 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("[WARN] Migrations reported errors. Continuing...")
            print(f"Migration output: {result.stderr}")
        else:
            print("[SUCCESS] Migrations completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[WARN] Migration error: {e}. Continuing...")
        return True

def start_system(venv_python):
    """Start the ORBIS system"""
    try:
        print("Starting ORBIS Business Analytics System...")
        print("=" * 50)
        
        # Set environment variables
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        
        # Start the transaction system
        subprocess.run([str(venv_python), 'start_transaction_system.py'], 
                      env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to start system: {e}")
        return False
    except KeyboardInterrupt:
        print("\n[INFO] System stopped by user")
        return True

def main():
    """Main launcher function"""
    print("ORBIS Business Analytics System - Universal Launcher")
    print("=" * 60)
    
    # Get platform information
    platform_info = get_platform_info()
    print(f"[INFO] Detected system: {platform_info['system'].title()}")
    
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    print(f"[INFO] Working directory: {script_dir}")
    
    # Create virtual environment if needed
    if not create_virtual_environment(platform_info):
        print("[ERROR] Failed to set up virtual environment")
        return 1
    
    # Get virtual environment Python path
    venv_python = get_venv_python(platform_info)
    print(f"[INFO] Using Python: {venv_python}")
    
    # Install dependencies
    if not install_dependencies(venv_python):
        print("[ERROR] Failed to install dependencies")
        return 1
    
    # Run migrations
    run_migrations(venv_python)
    
    # Start the system
    start_system(venv_python)
    
    return 0

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"[FATAL ERROR] Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
