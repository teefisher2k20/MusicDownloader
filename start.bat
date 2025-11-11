@echo off
REM UMDM+ Quick Start Script
REM Run this to start the application

echo.
echo ====================================
echo    UMDM+ Quick Start
echo ====================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    echo.
    pause
    exit /b 1
)

REM Display versions
echo [INFO] Checking environment...
node --version
npm --version
echo.

REM Check if dependencies are installed
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
)

echo [INFO] Starting application...
echo.
echo Opening in browser: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

REM Start the server
call npm run serve

pause
