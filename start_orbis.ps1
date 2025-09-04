# ORBIS Business Analytics System - PowerShell Launcher
# Enhanced Windows launcher with modern PowerShell features

param(
    [switch]$Verbose,
    [switch]$SkipMigrations
)

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "ORBIS Business Analytics System - PowerShell Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

try {
    # Change to script directory
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $ScriptDir
    Write-Host "[INFO] Working directory: $((Get-Location).Path)" -ForegroundColor Green
    
    # Define virtual environment paths
    $VenvPath = Join-Path $ScriptDir "venv"
    $VenvPython = Join-Path $VenvPath "Scripts\python.exe"
    
    # Check if virtual environment exists
    if (-not (Test-Path $VenvPython)) {
        Write-Host "[INFO] Virtual environment not found at $VenvPython" -ForegroundColor Yellow
        Write-Host "[INFO] Creating virtual environment..." -ForegroundColor Yellow
        
        # Try different Python commands
        $PythonCommands = @("python", "py", "python3")
        $VenvCreated = $false
        
        foreach ($PythonCmd in $PythonCommands) {
            try {
                & $PythonCmd -m venv venv
                $VenvCreated = $true
                Write-Host "[SUCCESS] Virtual environment created using $PythonCmd" -ForegroundColor Green
                break
            }
            catch {
                if ($Verbose) {
                    Write-Host "[DEBUG] Failed to create venv with $PythonCmd" -ForegroundColor Gray
                }
                continue
            }
        }
        
        if (-not $VenvCreated) {
            throw "Failed to create virtual environment. Please ensure Python 3.7+ is installed."
        }
    }
    
    # Verify virtual environment was created
    if (-not (Test-Path $VenvPython)) {
        throw "Virtual environment creation failed. Python executable not found at $VenvPython"
    }
    
    Write-Host "[INFO] Using Python: $VenvPython" -ForegroundColor Green
    
    # Set environment variables
    $env:PYTHONUTF8 = "1"
    
    # Check and install dependencies
    Write-Host "[INFO] Checking dependencies..." -ForegroundColor Yellow
    
    try {
        & $VenvPython -c "import django" 2>$null
        Write-Host "[INFO] Dependencies already installed" -ForegroundColor Green
    }
    catch {
        Write-Host "[INFO] Installing dependencies..." -ForegroundColor Yellow
        
        # Upgrade pip
        & $VenvPython -m pip install --upgrade pip
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to upgrade pip"
        }
        
        # Install requirements
        & $VenvPython -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install requirements"
        }
        
        Write-Host "[SUCCESS] Dependencies installed" -ForegroundColor Green
    }
    
    # Run database migrations
    if (-not $SkipMigrations) {
        Write-Host "[INFO] Running database migrations..." -ForegroundColor Yellow
        
        try {
            & $VenvPython manage.py migrate
            Write-Host "[SUCCESS] Migrations completed" -ForegroundColor Green
        }
        catch {
            Write-Host "[WARN] Migrations reported errors. Continuing..." -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "[INFO] Skipping migrations (SkipMigrations flag set)" -ForegroundColor Gray
    }
    
    # Start the system
    Write-Host "[INFO] Starting ORBIS Business Analytics System..." -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    & $VenvPython start_transaction_system.py
    
}
catch {
    Write-Host ""
    Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "1. Ensure Python 3.7+ is installed from https://python.org/downloads/" -ForegroundColor Yellow
    Write-Host "2. Make sure Python is added to PATH during installation" -ForegroundColor Yellow
    Write-Host "3. Try running as Administrator if permission issues occur" -ForegroundColor Yellow
    Write-Host "4. Check that requirements.txt exists in the current directory" -ForegroundColor Yellow
    
    exit 1
}
finally {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "ORBIS System Launcher Finished" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    if (-not $env:CI) {  # Don't pause in CI environments
        Read-Host "Press Enter to exit"
    }
}
