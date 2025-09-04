# Database Setup Guide for ORBIS Business Analytics System

## Quick Answer: **NO, PostgreSQL is NOT mandatory!**

The ORBIS system has been designed with **automatic database detection and fallback**. Here's what you need to know:

## 🎯 How Database Selection Works

When you start ORBIS, the system automatically:

1. **Checks for PostgreSQL** on localhost:5432
2. **If PostgreSQL is found** → Uses PostgreSQL database
3. **If PostgreSQL is NOT found** → Automatically switches to SQLite
4. **No manual configuration needed!**

## 📊 Database Options Comparison

| Feature | SQLite (Default) | PostgreSQL (Optional) |
|---------|------------------|----------------------|
| **Setup Required** | ❌ None | ✅ Installation needed |
| **Cross-Platform** | ✅ All systems | ✅ All systems |
| **File Size** | 📦 Small | 📦 Variable |
| **Performance** | ⚡ Good for small-medium | ⚡ Excellent for large |
| **Multi-User** | ⚠️ Limited | ✅ Full support |
| **Backup** | 📄 Copy db.sqlite3 file | 🔧 pg_dump commands |

## 🚀 Recommended Setup by Use Case

### For Development & Small Teams (Recommended)
```bash
# Just run the system - SQLite will be used automatically!
python start_orbis.py
```
- ✅ **Zero configuration**
- ✅ **Works immediately**
- ✅ **Perfect for testing and development**

### For Production & Large Teams (Optional)
If you want PostgreSQL for better performance:

#### Windows:
```bash
# Install PostgreSQL
# Download from: https://www.postgresql.org/download/windows/
# Or use chocolatey: choco install postgresql

# Create database
psql -U postgres
CREATE DATABASE orbis;
CREATE USER orbis_admin WITH PASSWORD 'pass';
GRANT ALL PRIVILEGES ON DATABASE orbis TO orbis_admin;
```

#### macOS:
```bash
# Install PostgreSQL
brew install postgresql
brew services start postgresql

# Create database
createdb orbis
psql orbis -c "CREATE USER orbis_admin WITH PASSWORD 'pass';"
psql orbis -c "GRANT ALL PRIVILEGES ON DATABASE orbis TO orbis_admin;"
```

#### Linux (Ubuntu/Debian):
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE orbis;
CREATE USER orbis_admin WITH PASSWORD 'pass';
GRANT ALL PRIVILEGES ON DATABASE orbis TO orbis_admin;
```

## 🔄 Switching Between Databases

The system automatically detects which database to use. To force a specific database:

### Force SQLite (if PostgreSQL is installed but you want to use SQLite):
1. Stop PostgreSQL service temporarily
2. Run the ORBIS system
3. It will automatically use SQLite

### Force PostgreSQL:
1. Ensure PostgreSQL is running on port 5432
2. Run the ORBIS system
3. It will automatically detect and use PostgreSQL

## 📁 Data Location

### SQLite Database:
- **Location**: `db.sqlite3` file in the project root
- **Backup**: Simply copy the `db.sqlite3` file
- **Transfer**: Copy the file to move data between systems

### PostgreSQL Database:
- **Location**: PostgreSQL server data directory
- **Backup**: Use `pg_dump orbis > backup.sql`
- **Transfer**: Use `pg_restore` or SQL import

## 🔧 Troubleshooting

### "No module named 'psycopg2'" error:
```bash
# This is normal if PostgreSQL isn't installed
# The system will automatically switch to SQLite
# No action needed!
```

### Want to install PostgreSQL support later:
```bash
# Install PostgreSQL support
pip install psycopg2-binary

# Or use the full requirements
pip install -r requirements.txt
```

### Want to use only SQLite (minimal installation):
```bash
# Use minimal requirements (without PostgreSQL)
pip install -r requirements-minimal.txt
```

## 🎯 Summary

**For 99% of users**: Just run `python start_orbis.py` and let the system use SQLite automatically. No database setup required!

**For production environments**: Install PostgreSQL if you need multi-user access and better performance for large datasets.

The beauty of this system is that **it works immediately on any computer** without requiring any database server installation!
