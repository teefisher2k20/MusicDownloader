# Phase 1 Implementation Guide
## Database Setup and Backend Foundation (Weeks 1-6)

---

## 📋 Overview

This guide walks you through Phase 1 of the UMDM+ development roadmap, focusing on setting up the database infrastructure and implementing core backend functionality.

**Timeline**: 6 weeks  
**Status**: 🟡 Ready to Start  
**Prerequisites**: ✅ All completed (Node.js, Python, project structure, documentation)

---

## 🎯 Phase 1 Goals

1. **PostgreSQL Database Setup** - Install and configure production database
2. **Redis Cache Setup** - Install queue management system
3. **Database Schema Design** - Create tables for users, downloads, queue, settings
4. **ORM Integration** - Connect backend to database (Sequelize or Prisma)
5. **Authentication System** - Implement JWT-based user authentication
6. **Core API Endpoints** - Replace mock endpoints with real implementations
7. **Environment Configuration** - Set up secure credential management

---

## 🗄️ Step 1: PostgreSQL Installation

### Install PostgreSQL 17 (Latest Stable)

```powershell
# Install PostgreSQL via winget
winget install PostgreSQL.PostgreSQL.17

# Verify installation (restart terminal first)
postgres --version
psql --version
```

### Initial Configuration

After installation:

1. **Default Settings**:
   - Port: `5432`
   - Username: `postgres`
   - Password: Set during installation (REMEMBER THIS!)

2. **Add to PATH** (if needed):
   ```powershell
   $pgPath = "C:\Program Files\PostgreSQL\17\bin"
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$pgPath", "User")
   ```

3. **Test Connection**:
   ```powershell
   # Connect to PostgreSQL
   psql -U postgres
   
   # In psql prompt:
   \l          # List databases
   \q          # Quit
   ```

---

## 🗃️ Step 2: Create UMDM+ Database

### Method 1: Using psql Command Line

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE umdm_plus;

-- Create application user
CREATE USER umdm_user WITH PASSWORD 'your_secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE umdm_plus TO umdm_user;

-- Connect to new database
\c umdm_plus

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO umdm_user;
```

### Method 2: Using PowerShell Script

```powershell
# Run this from your project directory
$env:PGPASSWORD = "your_postgres_password"
psql -U postgres -c "CREATE DATABASE umdm_plus;"
psql -U postgres -c "CREATE USER umdm_user WITH PASSWORD 'your_secure_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE umdm_plus TO umdm_user;"
```

---

## 📊 Step 3: Database Schema Design

### Core Tables Structure

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    role VARCHAR(20) DEFAULT 'user'
);

-- Downloads table
CREATE TABLE downloads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    title VARCHAR(500),
    platform VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    quality VARCHAR(20),
    format VARCHAR(20),
    file_size BIGINT,
    file_path TEXT,
    download_speed FLOAT,
    progress INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    metadata JSONB
);

-- Queue table
CREATE TABLE queue (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    download_id INTEGER REFERENCES downloads(id) ON DELETE CASCADE,
    priority INTEGER DEFAULT 0,
    position INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'waiting',
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    UNIQUE(user_id, position)
);

-- Settings table
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    key VARCHAR(100) NOT NULL,
    value JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, key)
);

-- Sessions table (for JWT refresh tokens)
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    refresh_token VARCHAR(500) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_downloads_user_id ON downloads(user_id);
CREATE INDEX idx_downloads_status ON downloads(status);
CREATE INDEX idx_downloads_created_at ON downloads(created_at DESC);
CREATE INDEX idx_queue_user_id ON queue(user_id);
CREATE INDEX idx_queue_status ON queue(status);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_refresh_token ON sessions(refresh_token);
```

**Save this as**: `database/schema.sql`

---

## 🔧 Step 4: Install Node.js Database Packages

```powershell
# Install PostgreSQL client and ORM
npm install pg pg-hstore sequelize

# Or use Prisma (alternative, recommended for modern projects)
npm install @prisma/client
npm install --save-dev prisma

# Install authentication packages
npm install jsonwebtoken bcryptjs
npm install --save-dev @types/jsonwebtoken @types/bcryptjs

# Install validation
npm install joi

# Install Redis client
npm install redis
```

---

## 🔴 Step 5: Redis Installation

### Install Redis for Windows

```powershell
# Install Redis via winget
winget install Redis.Redis

# Or install Memurai (Redis-compatible for Windows)
winget install Memurai.Memurai

# Verify installation
redis-cli --version
```

### Test Redis Connection

```powershell
# Start Redis server (if not running as service)
redis-server

# In another terminal, test connection
redis-cli
> ping
PONG
> exit
```

---

## 🔐 Step 6: Environment Configuration

### Create `.env` File

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=umdm_plus
DB_USER=umdm_user
DB_PASSWORD=your_secure_password_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_change_this_in_production
JWT_REFRESH_SECRET=your_super_secret_refresh_key_change_this
JWT_EXPIRES_IN=1h
JWT_REFRESH_EXPIRES_IN=7d

# Application Configuration
NODE_ENV=development
PORT=3000
CORS_ORIGIN=http://localhost:3000

# External Services (for future phases)
YTDLP_PATH=/path/to/yt-dlp
FFMPEG_PATH=/path/to/ffmpeg

# Security
BCRYPT_ROUNDS=10
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_TIME=900000

# File Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5368709120
```

**⚠️ SECURITY NOTE**: Never commit `.env` to git! It's already in `.gitignore`.

---

## 💾 Step 7: Database Connection Setup

### Option A: Using Sequelize

Create `database/connection.js`:

```javascript
const { Sequelize } = require('sequelize');
require('dotenv').config();

const sequelize = new Sequelize(
  process.env.DB_NAME,
  process.env.DB_USER,
  process.env.DB_PASSWORD,
  {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    dialect: 'postgres',
    logging: process.env.NODE_ENV === 'development' ? console.log : false,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
);

// Test connection
async function testConnection() {
  try {
    await sequelize.authenticate();
    console.log('✅ Database connection established successfully.');
  } catch (error) {
    console.error('❌ Unable to connect to database:', error);
  }
}

module.exports = { sequelize, testConnection };
```

### Option B: Using Prisma (Recommended)

```powershell
# Initialize Prisma
npx prisma init

# This creates:
# - prisma/schema.prisma
# - .env (if not exists)
```

Edit `prisma/schema.prisma`:

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id           Int       @id @default(autoincrement())
  username     String    @unique @db.VarChar(50)
  email        String    @unique @db.VarChar(255)
  passwordHash String    @map("password_hash") @db.VarChar(255)
  createdAt    DateTime  @default(now()) @map("created_at")
  updatedAt    DateTime  @updatedAt @map("updated_at")
  lastLogin    DateTime? @map("last_login")
  isActive     Boolean   @default(true) @map("is_active")
  role         String    @default("user") @db.VarChar(20)
  
  downloads    Download[]
  queue        Queue[]
  settings     Setting[]
  sessions     Session[]
  
  @@map("users")
}

model Download {
  id              Int       @id @default(autoincrement())
  userId          Int       @map("user_id")
  url             String
  title           String?   @db.VarChar(500)
  platform        String?   @db.VarChar(50)
  status          String    @default("pending") @db.VarChar(20)
  quality         String?   @db.VarChar(20)
  format          String?   @db.VarChar(20)
  fileSize        BigInt?   @map("file_size")
  filePath        String?   @map("file_path")
  downloadSpeed   Float?    @map("download_speed")
  progress        Int       @default(0)
  errorMessage    String?   @map("error_message")
  createdAt       DateTime  @default(now()) @map("created_at")
  startedAt       DateTime? @map("started_at")
  completedAt     DateTime? @map("completed_at")
  metadata        Json?
  
  user            User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  queue           Queue[]
  
  @@index([userId])
  @@index([status])
  @@index([createdAt(sort: Desc)])
  @@map("downloads")
}

// Add other models (Queue, Setting, Session) similarly...
```

Generate Prisma client:

```powershell
npx prisma generate
npx prisma db push
```

---

## 🔑 Step 8: Authentication Implementation

### Create `auth/jwt.js`

```javascript
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

class AuthService {
  // Generate access token
  generateAccessToken(userId, username, role) {
    return jwt.sign(
      { userId, username, role },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN }
    );
  }

  // Generate refresh token
  generateRefreshToken(userId) {
    return jwt.sign(
      { userId },
      process.env.JWT_REFRESH_SECRET,
      { expiresIn: process.env.JWT_REFRESH_EXPIRES_IN }
    );
  }

  // Verify access token
  verifyAccessToken(token) {
    try {
      return jwt.verify(token, process.env.JWT_SECRET);
    } catch (error) {
      throw new Error('Invalid or expired token');
    }
  }

  // Hash password
  async hashPassword(password) {
    return bcrypt.hash(password, parseInt(process.env.BCRYPT_ROUNDS));
  }

  // Compare password
  async comparePassword(password, hash) {
    return bcrypt.compare(password, hash);
  }
}

module.exports = new AuthService();
```

### Create `middleware/auth.js`

```javascript
const authService = require('../auth/jwt');

function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.substring(7);

  try {
    const decoded = authService.verifyAccessToken(token);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

function authorize(...roles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    next();
  };
}

module.exports = { authenticate, authorize };
```

---

## 🚀 Step 9: Update server.js with Real Implementation

Update your `server.js` to include:

1. Database connection on startup
2. Real authentication endpoints (register, login, logout, refresh)
3. Protected routes using authentication middleware
4. Real download endpoint that stores to database
5. Queue management endpoints

See `server_phase1.js` (to be created) for full implementation.

---

## ✅ Step 10: Testing Checklist

### Manual Testing

- [ ] PostgreSQL installed and running
- [ ] Database `umdm_plus` created
- [ ] All tables created successfully
- [ ] Redis installed and running
- [ ] Environment variables configured
- [ ] Database connection successful
- [ ] Can register new user
- [ ] Can login and receive JWT token
- [ ] Protected routes require authentication
- [ ] Can create download record
- [ ] Can add to queue

### Automated Testing

```powershell
# Run existing tests
npm test

# Add new database tests (to be implemented)
npm test -- --testPathPattern=database
```

---

## 📚 Next Steps After Phase 1

Once Phase 1 is complete:

1. **Phase 2**: Integrate yt-dlp for actual video downloads
2. **Phase 3**: Implement FFmpeg for format conversion
3. **Phase 4**: Add WebSocket for real-time progress updates
4. **Phase 5**: Implement AI features (transcription, upscaling)

---

## 🆘 Troubleshooting

### PostgreSQL Connection Issues

```powershell
# Check if PostgreSQL service is running
Get-Service postgresql*

# Start service if stopped
Start-Service postgresql-x64-17
```

### Redis Connection Issues

```powershell
# Check if Redis service is running
Get-Service redis*

# Or start manually
redis-server
```

### Port Already in Use

```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

---

## 📖 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Sequelize Documentation](https://sequelize.org/)
- [Prisma Documentation](https://www.prisma.io/docs/)
- [JWT Best Practices](https://jwt.io/introduction)
- [Redis Documentation](https://redis.io/documentation)

---

**Status**: Ready to begin Phase 1 implementation  
**Estimated Time**: 2-4 weeks for solo developer  
**Next Action**: Install PostgreSQL and Redis

