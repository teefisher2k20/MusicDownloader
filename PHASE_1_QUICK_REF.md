# Phase 1 Quick Reference Card

## 🎯 Goal: Database Setup & Backend Foundation

---

## ⚡ Quick Start (Choose One)

### Option A: Docker (Recommended - Fastest!)
```powershell
# Start all services (PostgreSQL, Redis, MinIO, etc.)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app

# Stop all services
docker-compose down
```

**Pros**: Everything configured automatically, isolated environment  
**Cons**: Requires Docker Desktop installed

---

### Option B: Automated Script
```powershell
# Run the setup assistant
.\setup-phase1.ps1

# Follow the prompts to install:
# - PostgreSQL 17
# - Redis
# - npm packages
# - Create directories
```

**Pros**: Guided installation, explains each step  
**Cons**: Requires manual password setup

---

### Option C: Manual Installation
```powershell
# 1. Install PostgreSQL
winget install PostgreSQL.PostgreSQL.17

# 2. Install Redis
winget install Redis.Redis

# 3. Install npm packages
npm install pg pg-hstore sequelize redis jsonwebtoken bcryptjs joi

# 4. Create database
psql -U postgres
CREATE DATABASE umdm_plus;
CREATE USER umdm_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE umdm_plus TO umdm_user;
\q

# 5. Run schema
psql -U postgres -d umdm_plus -f database/schema.sql

# 6. Configure .env
cp .env.example .env
# Edit .env with your passwords
```

**Pros**: Full control, understand each component  
**Cons**: Most time-consuming

---

## 📁 Files Created for Phase 1

| File | Purpose | Lines |
|------|---------|-------|
| `PHASE_1_IMPLEMENTATION.md` | Complete step-by-step guide | 500+ |
| `setup-phase1.ps1` | Automated setup script | 100+ |
| `database/schema.sql` | PostgreSQL database schema | 300+ |
| `database/` | Directory for DB files | - |

---

## 🗄️ Database Schema Overview

### Tables Created (9 total)

1. **users** - User accounts (username, email, password, role)
2. **downloads** - Download history and status tracking
3. **queue** - Download queue management
4. **settings** - User preferences (JSON storage)
5. **sessions** - JWT refresh tokens
6. **playlists** - Batch download tracking
7. **conversions** - Format conversion tasks
8. **activity_log** - Audit trail
9. **schema_version** - Database versioning

### Key Features
- 20+ indexes for fast queries
- 2 views: `active_downloads`, `user_stats`
- Auto-updating timestamps (triggers)
- Foreign key constraints with CASCADE
- Default admin user (username: admin, password: admin123)

---

## 🔧 Essential Commands

### PostgreSQL
```powershell
# Connect to database
psql -U postgres -d umdm_plus

# List tables
\dt

# Describe table structure
\d users

# Query users
SELECT * FROM users;

# Check database size
\l+

# Exit
\q
```

### Redis
```powershell
# Start Redis (if not running as service)
redis-server

# Connect to Redis
redis-cli

# Test connection
ping
# Should return: PONG

# View all keys
keys *

# Exit
exit
```

### Docker
```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart app

# Connect to PostgreSQL in Docker
docker exec -it umdm-db psql -U umdm_user -d umdm_plus

# Connect to Redis in Docker
docker exec -it umdm-redis redis-cli
```

---

## 🔐 Environment Variables (.env)

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=umdm_plus
DB_USER=umdm_user
DB_PASSWORD=your_secure_password_here

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your_super_secret_key_change_in_production
JWT_EXPIRES_IN=1h
JWT_REFRESH_EXPIRES_IN=7d

# Application
NODE_ENV=development
PORT=3000
```

⚠️ **Never commit .env to git!**

---

## ✅ Phase 1 Checklist

### Setup
- [ ] PostgreSQL installed and running
- [ ] Redis installed and running
- [ ] Database `umdm_plus` created
- [ ] Schema applied successfully
- [ ] .env file configured
- [ ] npm packages installed

### Verification
- [ ] Can connect to PostgreSQL (`psql -U postgres`)
- [ ] Can query tables (`SELECT * FROM users;`)
- [ ] Can connect to Redis (`redis-cli ping`)
- [ ] All 9 tables exist (`\dt` in psql)
- [ ] Default admin user exists

### Development
- [ ] Create auth endpoints (register, login, refresh)
- [ ] Create download endpoints
- [ ] Implement queue system
- [ ] Add authentication middleware
- [ ] Write integration tests

---

## 🐛 Common Issues & Solutions

### PostgreSQL won't start
```powershell
# Check service status
Get-Service postgresql*

# Start service
Start-Service postgresql-x64-17

# Check if port 5432 is in use
netstat -ano | findstr :5432
```

### Redis won't start
```powershell
# Check service
Get-Service redis*

# Start manually
redis-server

# Or start as Windows service
net start redis
```

### Can't connect to database
```powershell
# Test connection
psql -U postgres -h localhost -d umdm_plus

# If fails, check:
# 1. PostgreSQL service running?
# 2. Correct password?
# 3. User has permissions?
# 4. Database exists?
```

### Docker issues
```powershell
# Check Docker is running
docker ps

# Restart Docker Desktop if needed

# Clean up and restart
docker-compose down
docker-compose up -d --build
```

---

## 📚 Documentation Reference

| Topic | File | Section |
|-------|------|---------|
| Detailed setup | `PHASE_1_IMPLEMENTATION.md` | All |
| Database schema | `database/schema.sql` | - |
| API endpoints | `API.md` | Phase 1 |
| Project roadmap | `docs/PROJECT_ROADMAP.md` | Phase 1 |
| General setup | `SETUP.md` | Database |

---

## 🚀 What's Next After Phase 1?

Once database is set up and basic API works:

1. **Phase 2**: Integrate yt-dlp for real downloads (Weeks 7-12)
2. **Phase 3**: FFmpeg for conversion (Weeks 13-18)
3. **Phase 4**: AI integration (Weeks 19-24)

---

## 💡 Pro Tips

1. **Use Docker for development** - Fastest way to get started
2. **Keep .env secure** - Never commit passwords to git
3. **Test database first** - Verify connection before coding
4. **Use pgAdmin** - Install GUI for easier database management
5. **Enable query logging** - Set `logging: true` in Sequelize config during development

---

## 🆘 Need Help?

1. Read `PHASE_1_IMPLEMENTATION.md` for detailed explanations
2. Check `PROJECT_STATUS.md` for current implementation status
3. Review `API.md` for endpoint specifications
4. See `TROUBLESHOOTING.md` (if exists) for common issues

---

**Current Phase**: 1 of 10  
**Estimated Time**: 2-4 weeks solo development  
**Status**: 🟡 Ready to Begin

---

*Last Updated: 2025-11-10*
