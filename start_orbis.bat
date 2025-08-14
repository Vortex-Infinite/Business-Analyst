@echo off
echo Starting ORBIS Business Analytics System...
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Start the transaction system
python start_transaction_system.py

pause

