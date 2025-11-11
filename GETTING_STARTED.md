# 🚀 Development Environment Setup - Step by Step

This guide will walk you through setting up your development environment from scratch.

## ✅ Current Status

You already have:

- ✅ Python 3.12.10 installed
- ✅ uv package manager installed
- ✅ markitdown tool working
- ✅ Complete UMDM+ application code

## 📦 What You Need to Install

### 1. Node.js (Required)

**Download & Install:**

1. Go to <https://nodejs.org/>
2. Download the **LTS version** (currently v20.x or v18.x)
3. Run the installer
4. **Important:** Check "Add to PATH" during installation
5. Restart your terminal after installation

**Verify Installation:**

```powershell
node --version  # Should show v18.x or v20.x
npm --version   # Should show v9.x or v10.x
```

### 2. Git (Recommended)

**Download & Install:**

1. Go to <https://git-scm.com/download/win>
2. Download and run the installer
3. Use default settings

**Verify:**

```powershell
git --version
```

### 3. PostgreSQL (For Backend)

**Download & Install:**

```powershell
# Using winget (easiest)
winget install PostgreSQL.PostgreSQL

# Or download from: <https://www.postgresql.org/download/windows/>
```

**Verify:**

```powershell
psql --version
```

### 4. Redis (For Queue System)

**Download & Install:**

```powershell
# Using winget
winget install Redis.Redis

# Or use WSL2 for native Redis
# Or download from: https://github.com/microsoftarchive/redis/releases
```

**Verify:**

```powershell
redis-cli --version
```

### 5. FFmpeg (For Media Processing)

**Download & Install:**

```powershell
# Using winget
winget install Gyan.FFmpeg

# Or download from: https://ffmpeg.org/download.html
```

**Verify:**

```powershell
ffmpeg -version
```

## 🔧 Initial Setup Steps

### Step 1: Install Node.js Dependencies

```powershell
cd c:\Users\teefi\OneDrive\Desktop\MusicDownloader
npm install
```

This will install all JavaScript dependencies listed in `package.json`.

### Step 2: Install Python Dependencies

```powershell
# You already have Python, now install requirements
pip install -r requirements.txt
```

### Step 3: Configure Environment

```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env with your settings
notepad .env
```

**Minimum configuration:**

```env
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost:5432/umdm_plus
REDIS_URL=redis://localhost:6379
JWT_SECRET=your_random_secret_here_change_this
```

### Step 4: Set Up Database

```powershell
# Start PostgreSQL service
Start-Service postgresql-x64-14  # Or your version

# Create database
psql -U postgres -c "CREATE DATABASE umdm_plus;"
psql -U postgres -c "CREATE USER umdm_user WITH PASSWORD 'your_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE umdm_plus TO umdm_user;"
```

### Step 5: Start Development Server

**Option A: Just the frontend (current working version):**

```powershell
# Serve static files
npm run serve
# Opens at http://localhost:8000
```

**Option B: Full backend (once dependencies installed):**

```powershell
# Start with auto-reload
npm run dev
# Opens at http://localhost:3000
```

## 🧪 Testing Setup

### Run Tests

```powershell
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Watch mode (auto-rerun on changes)
npm run test:watch
```

### Linting and Formatting

```powershell
# Check code style
npm run lint

# Auto-fix issues
npm run lint:fix

# Format code
npm run format
```

## 🐳 Docker Setup (Alternative)

If you prefer Docker instead of local installation:

### Install Docker Desktop

1. Download from <https://www.docker.com/products/docker-desktop/>
2. Install and restart
3. Enable WSL2 integration (if using WSL)

### Run with Docker Compose

```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

This starts:

- UMDM+ app on port 3000
- PostgreSQL on port 5432
- Redis on port 6379
- MinIO (S3) on ports 9000-9001

## 📁 Project Structure Overview

```text
MusicDownloader/
├── index.html              # Main web application
├── server.js               # Backend API server
├── package.json            # Node.js dependencies
├── requirements.txt        # Python dependencies
├── 
├── css/styles.css          # Styling
├── js/app.js               # Frontend logic
├── 
├── tests/                  # Test files
│   ├── setup.js
│   └── app.test.js
├── 
├── .eslintrc.json          # Linting config
├── .prettierrc.json        # Code formatting
├── jest.config.js          # Test configuration
├── 
├── Dockerfile              # Docker image
├── docker-compose.yml      # Docker services
├── .dockerignore           # Docker ignore rules
├── 
└── .github/workflows/      # CI/CD pipelines
    └── ci.yml
```

## 🎯 Development Workflow

### 1. Create a Feature Branch

```powershell
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit files in your code editor (VS Code recommended)

### 3. Test Your Changes

```powershell
npm run lint      # Check code style
npm test          # Run tests
npm run dev       # Test locally
```

### 4. Commit Changes

```powershell
git add .
git commit -m "feat: describe your changes"
```

### 5. Push and Create PR

```powershell
git push origin feature/your-feature-name
# Create Pull Request on GitHub
```

## 🛠️ Troubleshooting

### NPM Not Found

**Problem:** `npm : The term 'npm' is not recognized`

**Solution:**

1. Install Node.js from nodejs.org
2. Restart your terminal/PowerShell
3. Verify with `node --version`

### Python Not Found

**Problem:** `python : The term 'python' is not recognized`

**Solution:**

You already fixed this! But if it happens again:

1. Check Python is in PATH
2. Restart terminal
3. Use `python --version` to verify

### Port Already in Use

**Problem:** `Error: listen EADDRINUSE: address already in use :::3000`

**Solution:**

```powershell
# Find process using port
netstat -ano | findstr :3000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in .env
```

### Module Not Found Issue

**Problem:** `Cannot find module 'express'`

**Solution:**

```powershell
# Delete and reinstall
Remove-Item node_modules -Recurse -Force
Remove-Item package-lock.json -Force
npm install
```

### FFmpeg Not Found

**Problem:** `ffmpeg: command not found`

**Solution:**

1. Install FFmpeg via winget or manually
2. Add to PATH environment variable
3. Restart terminal

## 📚 Next Steps After Setup

### 1. Explore the Application

- Open <http://localhost:8000> in browser
- Try the theme toggle
- Test URL validation
- Explore all tabs and features

### 2. Read Documentation

- `README.md` - Project overview
- `QUICK_START.md` - User guide
- `API.md` - API documentation
- `UMDM_PLUS_SPECIFICATION.md` - Full specifications

### 3. Start Development

- Read `CONTRIBUTING.md` for guidelines
- Check `PROJECT_ROADMAP.md` for Phase 1 tasks
- Find "good first issue" tasks
- Set up your IDE (VS Code recommended)

### 4. Join Community

- Create GitHub account (if needed)
- Star the repository
- Watch for updates
- Join discussions

## 🎓 Learning Resources

### Essential Reading

- [Node.js Getting Started](https://nodejs.org/en/docs/guides/getting-started-guide/)
- [Express.js Guide](https://expressjs.com/en/starter/installing.html)
- [JavaScript MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Python Docs](https://docs.python.org/3/)

### Tools

- [VS Code](https://code.visualstudio.com/) - Recommended IDE
- [Postman](https://www.postman.com/) - API testing
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)

## ✅ Setup Checklist

Use this checklist to track your progress:

**Software Installation:**

- [ ] Node.js installed (v18+)
- [ ] npm working (`npm --version`)
- [ ] Python installed (v3.11+) ✅ (You have 3.12.10)
- [ ] pip working ✅
- [ ] Git installed
- [ ] PostgreSQL installed
- [ ] Redis installed
- [ ] FFmpeg installed

**Project Setup:**

- [ ] Repository cloned/downloaded ✅
- [ ] npm dependencies installed (`npm install`)
- [ ] Python packages installed (`pip install -r requirements.txt`)
- [ ] .env file configured
- [ ] Database created
- [ ] Redis running

**Development Environment:**

- [ ] VS Code installed (optional but recommended)
- [ ] VS Code extensions installed
- [ ] Tests passing (`npm test`)
- [ ] Linter working (`npm run lint`)
- [ ] Application running locally

**Documentation Read:**

- [ ] README.md
- [ ] SETUP.md (this file)
- [ ] CONTRIBUTING.md
- [ ] API.md
- [ ] UMDM_PLUS_SPECIFICATION.md

## 🎉 You're Ready When

You can successfully:

1. ✅ Run `npm --version` and see a version number
2. ✅ Run `python --version` and see 3.11+
3. ✅ Run `npm install` without errors
4. ✅ Run `npm run serve` and see the app at `http://localhost:8000`
5. ✅ Run `npm test` and see tests pass
6. ✅ Open the application in your browser and interact with it

## 🆘 Need Help?

**If you're stuck:**

1. Check this guide again carefully
2. Read the error messages
3. Search the error in documentation
4. Check GitHub Issues
5. Ask in GitHub Discussions
6. Email: <support@umdm.app>

**Common Questions:**

- **"Do I need Docker?"** - No, it's optional. Local installation works fine.
- **"Can I skip PostgreSQL?"** - For frontend development, yes. For backend, no.
- **"What if I'm new to programming?"** - Start with the frontend, learn JavaScript first.
- **"How long does setup take?"** - About 30-60 minutes with all installations.

---

**Pro Tip:** Install everything in this order for smoothest experience:

1. Node.js → 2. Git → 3. VS Code → 4. npm install → 5. Try the app!

Good luck! 🚀
