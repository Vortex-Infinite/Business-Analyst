# ORBIS Business Analytics System - Cross-Platform Launcher Guide

This guide explains how to run the ORBIS Business Analytics System on different operating systems using the appropriate launcher scripts.

## Available Launchers

### 1. Universal Python Launcher (Recommended for all systems)
**File:** `start_orbis.py`
- ✅ Works on Windows, macOS, and Linux
- ✅ Automatic platform detection
- ✅ Enhanced error handling and diagnostics
- ✅ No additional dependencies beyond Python

**Usage:**
```bash
# On any system with Python installed
python start_orbis.py
# or
python3 start_orbis.py
```

### 2. Windows Batch File
**File:** `start_orbis.bat`
- ✅ Windows only (all versions)
- ✅ Enhanced error handling
- ✅ Multiple Python command fallback

**Usage:**
```cmd
# Double-click the file or run from Command Prompt
start_orbis.bat
```

### 3. PowerShell Script (Modern Windows)
**File:** `start_orbis.ps1`
- ✅ Windows PowerShell 5.1+ and PowerShell Core
- ✅ Advanced features and verbose logging
- ✅ Optional parameters for customization

**Usage:**
```powershell
# Basic usage
.\start_orbis.ps1

# With verbose output
.\start_orbis.ps1 -Verbose

# Skip database migrations
.\start_orbis.ps1 -SkipMigrations
```

**Note:** You may need to enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Unix Shell Script (Linux/macOS)
**File:** `start_orbis.sh`
- ✅ Linux and macOS
- ✅ Bash-compatible shell required

**Usage:**
```bash
# Make executable (first time only)
chmod +x start_orbis.sh

# Run the script
./start_orbis.sh
```

## System Requirements

### All Systems
- Python 3.7 or higher
- Internet connection (for initial dependency installation)
- At least 1GB free disk space

### Windows
- Windows 7 or higher
- Python installed from python.org or Microsoft Store
- Command Prompt, PowerShell, or Windows Terminal

### macOS
- macOS 10.14 (Mojave) or higher
- Python 3 (install via Homebrew: `brew install python3`)
- Terminal application

### Linux
- Any modern Linux distribution
- Python 3.7+ (usually pre-installed)
- Bash shell

## Quick Start Guide

### Option 1: Universal Python Launcher (Recommended)
1. Ensure Python is installed and accessible
2. Navigate to the project directory
3. Run: `python start_orbis.py`

### Option 2: Platform-Specific Launchers
**Windows:**
- Double-click `start_orbis.bat`, or
- Run `.\start_orbis.ps1` in PowerShell

**Linux/macOS:**
- Run `./start_orbis.sh` in Terminal

## What the Launchers Do

1. **Environment Setup**
   - Create a Python virtual environment (if not exists)
   - Activate the virtual environment

2. **Dependency Management**
   - Check if required packages are installed
   - Install/upgrade packages from `requirements.txt`

3. **Database Setup**
   - Run Django migrations to set up the database
   - Handle migration errors gracefully

4. **System Launch**
   - Start the ORBIS transaction system
   - Launch the Django web server
   - Initialize background processes

## Troubleshooting

### Python Not Found
- **Windows:** Install Python from https://python.org/downloads/
- **macOS:** Install via Homebrew: `brew install python3`
- **Linux:** Install via package manager: `sudo apt install python3` (Ubuntu/Debian)

### Permission Denied (Linux/macOS)
```bash
chmod +x start_orbis.sh
```

### PowerShell Execution Policy (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Virtual Environment Issues
Delete the `venv` folder and run the launcher again:
```bash
# Linux/macOS
rm -rf venv

# Windows
rmdir /s venv
```

### Port Already in Use
If the default port is occupied, the system will try alternative ports automatically.

## Advanced Usage

### Environment Variables
Set these before running the launcher for customization:

```bash
# Custom port
export DJANGO_PORT=8080

# Debug mode
export DJANGO_DEBUG=True

# Custom database URL
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
```

### Development Mode
For development with auto-reload:
```bash
# Set environment variable
export DJANGO_DEBUG=True

# Then run any launcher
python start_orbis.py
```

## Support

If you encounter issues:

1. Check that Python 3.7+ is installed: `python --version`
2. Verify you're in the correct directory (should contain `manage.py`)
3. Ensure `requirements.txt` exists
4. Try deleting the `venv` folder and running again
5. Check the console output for specific error messages

For additional help, refer to the main project documentation or contact support.

---

**Recommended approach:** Use `start_orbis.py` as it provides the best cross-platform compatibility and error handling.
