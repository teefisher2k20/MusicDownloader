# 🚀 UMDM+ - Quick Reference Guide

## ⚡ Quick Start Commands

### Start the Application
```powershell
# Option 1: Open HTML file directly (works immediately)
start index.html

# Option 2: Use startup script (requires Node.js)
.\start.ps1

# Option 3: Manual server start
npm run serve
```

### Development Commands
```powershell
npm test              # Run all tests
npm run lint          # Check code quality
npm run format        # Format code with Prettier
npm run dev           # Start with hot reload (backend)
```

### Docker Commands
```powershell
docker-compose up -d     # Start all services
docker-compose down      # Stop all services
docker-compose logs -f   # View logs
```

## 📁 Important Files

### Documentation
- `PROJECT_STATUS.md` - ⭐ Complete project overview
- `GETTING_STARTED.md` - Beginner setup guide
- `README.md` - Project introduction
- `API.md` - REST API documentation
- `CONTRIBUTING.md` - How to contribute

### Configuration
- `.env.example` - Environment variables template
- `package.json` - Node.js dependencies
- `requirements.txt` - Python dependencies

### Application
- `index.html` - Main application
- `css/styles.css` - Styling
- `js/app.js` - Frontend logic
- `server.js` - Backend API

## 🛠️ Troubleshooting

### npm not found
```powershell
# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Or restart VS Code
```

### Port already in use
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

### Tests failing
```powershell
# Reinstall dependencies
Remove-Item node_modules -Recurse -Force
npm install
npm test
```

## 📊 Project Status

✅ **Working:**
- Python 3.12.10 + uv + markitdown
- Node.js v24.11.0 + npm 11.6.1
- 534 npm packages (0 vulnerabilities)
- 15 tests passing ✅
- Complete frontend application
- Testing framework configured
- Docker & CI/CD ready

🔄 **To Implement:**
- Backend API (PostgreSQL, Redis)
- Real download functionality (yt-dlp)
- Media conversion (FFmpeg)
- AI features (Whisper, upscaling)

## 🎯 Development Phases

**Phase 1** (Weeks 1-6): Foundation & Infrastructure
**Phase 2** (Weeks 7-12): Core Downloads
**Phase 3** (Weeks 13-18): Format Conversion
**Phase 4** (Weeks 19-24): AI Integration
**Phase 5** (Weeks 25-28): Advanced DRM
**Phase 6** (Weeks 29-32): Advanced Features
**Phase 7** (Weeks 33-36): Legal & Compliance
**Phase 8** (Weeks 37-40): Testing
**Phase 9** (Weeks 41-44): Beta Release
**Phase 10** (Weeks 45-48): Public Launch

See `PROJECT_ROADMAP.md` for details.

## 🌐 Supported Sites

**1,100+ websites** including:
- YouTube, TikTok, Instagram, Twitter/X
- Spotify, SoundCloud, Apple Music
- Twitch, Kick, DLive
- Coursera, Udemy, Khan Academy
- And 1,000+ more...

## 🔑 Key Features

### Current (Frontend):
- ✅ Responsive design
- ✅ Light/dark themes
- ✅ Download form with validation
- ✅ Queue management UI
- ✅ Settings panel
- ✅ AI tools interface

### Planned (Backend):
- 🔄 Real downloads (yt-dlp)
- 🔄 Format conversion (FFmpeg)
- 🔄 AI transcription (Whisper)
- 🔄 Video upscaling
- 🔄 DRM support

## 💡 Tips

1. **Always** refresh PATH in new terminals:
   ```powershell
   $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
   ```

2. **Use startup scripts** for convenience:
   - Windows: `start.bat`
   - PowerShell: `.\start.ps1`

3. **Read documentation** before coding:
   - Start with `PROJECT_STATUS.md`
   - Then `GETTING_STARTED.md`
   - Then `CONTRIBUTING.md`

4. **Test often**:
   ```powershell
   npm test
   ```

## 📞 Support

- **Documentation:** Check project root for guides
- **Issues:** Report bugs on GitHub
- **Questions:** Create GitHub Discussion
- **Email:** support@umdm.app

## 🎉 Quick Wins

### Want to see it work right now?
```powershell
start index.html
```

### Want to run tests?
```powershell
npm test
# Result: 15 tests passing ✅
```

### Want to start coding?
1. Open `js/app.js`
2. Make changes
3. Refresh browser
4. See results immediately!

---

**Last Updated:** November 10, 2025  
**Version:** 1.0.0-alpha  
**Status:** ✅ Ready for Development
