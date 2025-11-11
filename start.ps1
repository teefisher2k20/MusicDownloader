# UMDM+ Quick Start Script for PowerShell
# Run this to start the application

Write-Host "`n====================================" -ForegroundColor Cyan
Write-Host "   UMDM+ Quick Start" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>$null
    $npmVersion = npm --version 2>$null
    
    Write-Host "[INFO] Node.js: " -NoNewline -ForegroundColor Green
    Write-Host $nodeVersion
    Write-Host "[INFO] npm: " -NoNewline -ForegroundColor Green
    Write-Host $npmVersion
    Write-Host ""
} catch {
    Write-Host "[ERROR] Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if dependencies are installed
if (-not (Test-Path "node_modules")) {
    Write-Host "[INFO] Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host ""
}

Write-Host "[INFO] Starting application..." -ForegroundColor Green
Write-Host ""
Write-Host "Opening in browser: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
npm run serve
