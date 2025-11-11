# UMDM+ Phase 1 Setup Script
# Automates PostgreSQL and Redis installation

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   UMDM+ Phase 1 Setup Assistant" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Step 1: Check PostgreSQL
Write-Host "Step 1: Checking PostgreSQL..." -ForegroundColor Yellow
if (Test-Command "psql") {
    $pgVersion = psql --version
    Write-Host "✅ PostgreSQL already installed: $pgVersion" -ForegroundColor Green
} else {
    Write-Host "❌ PostgreSQL not found" -ForegroundColor Red
    Write-Host "Installing PostgreSQL 17..." -ForegroundColor Yellow
    
    $install = Read-Host "Install PostgreSQL now? (y/n)"
    if ($install -eq "y") {
        winget install PostgreSQL.PostgreSQL.17
        Write-Host "`n⚠️  IMPORTANT: After installation completes:" -ForegroundColor Yellow
        Write-Host "   1. REMEMBER the password you set for 'postgres' user" -ForegroundColor White
        Write-Host "   2. Restart this terminal" -ForegroundColor White
        Write-Host "   3. Run this script again`n" -ForegroundColor White
        exit
    }
}

# Step 2: Check Redis
Write-Host "`nStep 2: Checking Redis..." -ForegroundColor Yellow
if (Test-Command "redis-cli") {
    $redisVersion = redis-cli --version
    Write-Host "✅ Redis already installed: $redisVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Redis not found" -ForegroundColor Red
    Write-Host "Installing Redis..." -ForegroundColor Yellow
    
    $install = Read-Host "Install Redis now? (y/n)"
    if ($install -eq "y") {
        winget install Redis.Redis
        Write-Host "`n⚠️  After installation, restart terminal and run this script again`n" -ForegroundColor Yellow
        exit
    }
}

# Step 3: Install npm packages
Write-Host "`nStep 3: Installing database packages..." -ForegroundColor Yellow
Write-Host "This will install: pg, sequelize, redis, jsonwebtoken, bcryptjs, joi" -ForegroundColor Gray

$install = Read-Host "Install npm packages now? (y/n)"
if ($install -eq "y") {
    npm install pg pg-hstore sequelize redis jsonwebtoken bcryptjs joi
    npm install --save-dev @types/jsonwebtoken @types/bcryptjs
    Write-Host "✅ Packages installed successfully" -ForegroundColor Green
}

# Step 4: Create directories
Write-Host "`nStep 4: Creating project directories..." -ForegroundColor Yellow
$dirs = @("database", "auth", "middleware", "models", "routes", "uploads")
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "  Created: $dir/" -ForegroundColor Gray
    }
}
Write-Host "✅ Directories ready" -ForegroundColor Green

# Step 5: Create .env file
Write-Host "`nStep 5: Environment configuration..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Gray
    
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ .env file created from .env.example" -ForegroundColor Green
        Write-Host "⚠️  IMPORTANT: Edit .env and add your database password!" -ForegroundColor Yellow
    } else {
        Write-Host "❌ .env.example not found" -ForegroundColor Red
    }
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Step 6: Database setup instructions
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Next Steps" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "1. Create PostgreSQL database:" -ForegroundColor Yellow
Write-Host "   psql -U postgres" -ForegroundColor White
Write-Host "   CREATE DATABASE umdm_plus;" -ForegroundColor Gray
Write-Host "   CREATE USER umdm_user WITH PASSWORD 'your_password';" -ForegroundColor Gray
Write-Host "   GRANT ALL PRIVILEGES ON DATABASE umdm_plus TO umdm_user;" -ForegroundColor Gray
Write-Host "   \q`n" -ForegroundColor Gray

Write-Host "2. Update .env file with your database password`n" -ForegroundColor Yellow

Write-Host "3. Create database schema:" -ForegroundColor Yellow
Write-Host "   psql -U postgres -d umdm_plus -f database/schema.sql`n" -ForegroundColor White

Write-Host "4. Read the implementation guide:" -ForegroundColor Yellow
Write-Host "   PHASE_1_IMPLEMENTATION.md`n" -ForegroundColor White

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup assistant complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
