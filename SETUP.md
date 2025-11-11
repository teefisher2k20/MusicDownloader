# UMDM+ Setup Guide

Complete setup instructions for developers and contributors.

## 📋 Prerequisites

### Required Software

1. **Node.js 18+**
   - Download: <https://nodejs.org/>
   - Verify: `node --version`

2. **Python 3.11+**
   - Download: <https://www.python.org/>
   - Verify: `python --version`

3. **Git**
   - Download: <https://git-scm.com/>
   - Verify: `git --version`

4. **FFmpeg** (for media processing)
   - Download: <https://ffmpeg.org/download.html>
   - Verify: `ffmpeg -version`

5. **PostgreSQL 14+** (for production)
   - Download: <https://www.postgresql.org/download/>
   - Verify: `psql --version`

6. **Redis** (for queue management)
   - Download: <https://redis.io/download>
   - Verify: `redis-cli --version`

### Optional (for AI features)

- **CUDA Toolkit** (NVIDIA GPU acceleration)
- **PyTorch** (for AI models)
- **Whisper AI** (for transcription)

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/umdm-plus.git
cd umdm-plus
```

### 2. Install Dependencies

**Node.js packages:**

```bash
npm install
```

**Python packages:**

```bash
pip install -r requirements.txt
```

Or with virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env  # or use your preferred editor
```

**Minimum required variables:**

```env
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost:5432/umdm_plus
REDIS_URL=redis://localhost:6379
JWT_SECRET=your_random_secret_here
```

### 4. Database Setup

```bash
# Create database
createdb umdm_plus

# Run migrations (once implemented)
npm run migrate

# Seed data (optional)
npm run seed
```

### 5. Start Development Server

#### Option A: Frontend only (current state)

```bash
npm run serve
# Opens at http://localhost:8000
```

#### Option B: Full stack (with backend)

```bash
npm run dev
# Opens at http://localhost:3000
```

## 🛠️ Development Setup

### IDE Setup (VS Code Recommended)

1. **Install Extensions:**
   - ESLint
   - Prettier
   - GitLens
   - Thunder Client (API testing)
   - Live Server

2. **VS Code Settings:**

   ```json
   {
     "editor.formatOnSave": true,
     "editor.defaultFormatter": "esbenp.prettier-vscode",
     "eslint.autoFixOnSave": true
   }
   ```

### Code Style

**Install linters:**

```bash
npm install -g eslint prettier
```

**Run linting:**

```bash
npm run lint
npm run lint:fix
```

**Format code:**

```bash
npm run format
```

## 🗄️ Database Setup (Detailed)

### PostgreSQL

1. **Install PostgreSQL:**

   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS (Homebrew)
   brew install postgresql
   
   # Windows
   # Download installer from postgresql.org
   ```

2. **Create User and Database:**

   ```sql
   -- Connect to PostgreSQL
   psql postgres
   
   -- Create user
   CREATE USER umdm_user WITH PASSWORD 'your_password';
   
   -- Create database
   CREATE DATABASE umdm_plus OWNER umdm_user;
   
   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE umdm_plus TO umdm_user;
   ```

3. **Update .env:**

   ```env
   DATABASE_URL=postgresql://umdm_user:your_password@localhost:5432/umdm_plus
   ```

### Redis

1. **Install Redis:**

   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server
   
   # macOS (Homebrew)
   brew install redis
   
   # Windows (WSL or download)
   # https://redis.io/docs/getting-started/installation/install-redis-on-windows/
   ```

2. **Start Redis:**

   ```bash
   redis-server
   ```

3. **Verify:**

   ```bash
   redis-cli ping
   # Should return: PONG
   ```

## 🎬 Media Tools Setup

### FFmpeg Installation

#### Ubuntu/Debian

```bash
sudo apt-get install ffmpeg
```

#### macOS

```bash
brew install ffmpeg
```

#### Windows

1. Download from <https://ffmpeg.org/download.html>
2. Extract to `C:\ffmpeg`
3. Add to PATH: `C:\ffmpeg\bin`

### yt-dlp Installation

```bash
# With pip
pip install yt-dlp

# Or download binary
# https://github.com/yt-dlp/yt-dlp/releases
```

**Verify:**

```bash
yt-dlp --version
```

## 🤖 AI Services Setup (Optional)

### Whisper AI (Transcription)

```bash
pip install openai-whisper
```

**Download model:**

```python
import whisper
model = whisper.load_model("base")
```

Models: `tiny`, `base`, `small`, `medium`, `large`

### Video Upscaling (Real-ESRGAN)

```bash
pip install realesrgan
```

**Requires:**

- CUDA toolkit for GPU acceleration
- At least 4GB VRAM

## 🧪 Testing Setup

### Install Test Dependencies

```bash
npm install --save-dev jest @testing-library/jest-dom
```

### Run Tests

```bash
# All tests
npm test

# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage
```

### Write Tests

Create files with `.test.js` or `.spec.js` extension:

```javascript
// app.test.js
const { validateUrl } = require('./js/app');

describe('URL Validation', () => {
  test('validates YouTube URLs', () => {
    expect(validateUrl('https://youtube.com/watch?v=test')).toBe(true);
  });
});
```

## 🐳 Docker Setup (Alternative)

### Using Docker Compose

```yaml
# docker-compose.yml (create this)
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/umdm_plus
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:14
    environment:
      POSTGRES_USER: umdm_user
      POSTGRES_PASSWORD: your_password
      POSTGRES_DB: umdm_plus
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**Run:**

```bash
docker-compose up -d
```

## 📝 Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following style guide
- Add tests for new features
- Update documentation

### 3. Test Locally

```bash
npm run lint
npm test
npm run dev
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add new feature"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
# Create Pull Request on GitHub
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process or change PORT in .env
```

#### 2. Database Connection Error

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Check connection string in .env
```

#### 3. Module Not Found

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 4. Python Package Errors

```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall with --force-reinstall
pip install --force-reinstall -r requirements.txt
```

#### 5. FFmpeg Not Found

```bash
# Verify installation
which ffmpeg

# Add to PATH if needed
export PATH="/path/to/ffmpeg/bin:$PATH"
```

## 📚 Additional Resources

### Documentation

- [Project Specification](UMDM_PLUS_SPECIFICATION.md)
- [Development Roadmap](docs/PROJECT_ROADMAP.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Quick Start](QUICK_START.md)

### External Resources

- [Node.js Docs](<https://nodejs.org/docs/>)
- [Express.js Guide](<https://expressjs.com/en/guide/>)
- [PostgreSQL Manual](<https://www.postgresql.org/docs/>)
- [Redis Documentation](<https://redis.io/docs/>)
- [FFmpeg Documentation](<https://ffmpeg.org/documentation.html>)

## 🆘 Getting Help

- **GitHub Issues:** Report bugs or request features
- **GitHub Discussions:** Ask questions, share ideas
- **Discord:** Join our community (invite link)
- **Email:** <support@umdm.app>

## ✅ Setup Checklist

- [ ] Node.js installed (v18+)
- [ ] Python installed (v3.11+)
- [ ] Git installed
- [ ] Repository cloned
- [ ] Dependencies installed (`npm install`)
- [ ] Environment variables configured (`.env`)
- [ ] PostgreSQL installed and running
- [ ] Redis installed and running
- [ ] Database created
- [ ] FFmpeg installed
- [ ] yt-dlp installed
- [ ] Tests passing (`npm test`)
- [ ] Development server running (`npm run dev`)
- [ ] Application accessible in browser

## 🎉 You're Ready

Once all steps are complete, you're ready to contribute to UMDM+!

Start by:

1. Reading the [Contributing Guide](CONTRIBUTING.md)
2. Finding a "good first issue" on GitHub
3. Joining our community discussions

Happy coding! 🚀
