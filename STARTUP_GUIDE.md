# ORBIS System Startup Guide

## ✅ **Fixed Batch Files - Now Working!**

### `start_orbis.bat` - Main System Launcher ✅ WORKING
**Full system startup with automatic database detection and fallback**

**Features:**
- ✅ Automatic PostgreSQL/SQLite database detection
- ✅ Virtual environment setup and dependency installation  
- ✅ Database migrations
- ✅ Sample data generation (if needed)
- ✅ Transaction generator + Django server startup
- ✅ Real-time transaction processing with anomaly detection

**Usage:**
```cmd
start_orbis.bat
```

### `start_simple.bat` - Quick Django Only ✅ WORKING
**Lightweight Django server startup (no transaction generator)**

**Features:**
- ✅ Instant Django server startup
- ✅ No background processes
- ✅ Perfect for testing/debugging

**Usage:**
```cmd
start_simple.bat
```

### `start_django_only.bat` - Alternative Simple Server
**Backup simple server launcher**

## ✅ **System Status: FULLY OPERATIONAL**

**Verified Working:**
- ✅ Virtual environment detection/creation
- ✅ Django dependency installation
- ✅ PostgreSQL database connection
- ✅ Database migrations
- ✅ Sample data exists (transactions, accounts, users)
- ✅ Transaction generator running
- ✅ Anomaly detection active
- ✅ Django server accessible at http://127.0.0.1:8000
- ✅ Dynamic user names in menu bar

## Database Configuration

### PostgreSQL (Primary)
- **Database:** `orbis`
- **User:** `orbis_admin`
- **Password:** `pass`
- **Host:** `localhost`
- **Port:** `5432`

### SQLite (Automatic Fallback)
- **File:** `db.sqlite3`
- **Auto-created** if PostgreSQL unavailable

## System Requirements

### Required
- Python 3.8+ installed and in PATH
- Virtual environment support

### Optional (for full features)
- PostgreSQL 12+ server running
- `psycopg2` package (auto-installed)

## Startup Process

1. **Environment Check**
   - Validates Python installation
   - Creates/activates virtual environment
   - Installs required dependencies

2. **Database Detection**
   - Tests PostgreSQL connection
   - Falls back to SQLite if needed
   - Backs up original settings

3. **Database Setup**
   - Runs migrations
   - Generates sample data if empty

4. **System Launch**
   - Starts transaction generator (background)
   - Launches Django development server
   - Opens on http://127.0.0.1:8000

## Troubleshooting

### PostgreSQL Issues
- Ensure PostgreSQL service is running
- Verify database 'orbis' exists
- Check user credentials (orbis_admin/pass)
- System automatically falls back to SQLite

### General Issues
- Run `start_django_only.bat` for basic testing
- Check console output for specific errors
- Ensure Python is in system PATH

### Log Messages
- `[INFO]` - Normal operation status
- `[SUCCESS]` - Operation completed successfully  
- `[WARN]` - Non-critical issues, system continues
- `[ERROR]` - Critical issues that stop execution

## Access Points

- **Main Application:** http://127.0.0.1:8000
- **Admin Panel:** http://127.0.0.1:8000/admin
- **Employee Login:** http://127.0.0.1:8000/employee_login

## Test Credentials

**Test User:**
- Username: `john_analyst`
- Password: `testpass123`  
- Email: `john.analyst@orbis.com`
- Name: `John Smith`
