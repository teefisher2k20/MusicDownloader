/**
 * UMDM+ Server
 * Universal Media Downloader, Converter, and Manager Plus
 * Main server file with improved structure and error handling
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const path = require('path');
require('dotenv').config();

// Import constants and middleware
const { DEFAULT_PORT } = require('./config/constants');
const { notFoundHandler, errorHandler } = require('./middleware/errorHandler');

// Import routes
const apiRoutes = require('./routes/api.routes');
const downloadRoutes = require('./routes/download.routes');
const convertRoutes = require('./routes/convert.routes');
const aiRoutes = require('./routes/ai.routes');

const app = express();
const PORT = process.env.PORT || DEFAULT_PORT;

// Middleware
app.use(helmet({
  contentSecurityPolicy: false // Adjust for production
}));
app.use(cors());
app.use(compression());
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static(path.join(__dirname)));

// Mount API routes
app.use('/api', apiRoutes);
app.use('/api/download', downloadRoutes);
app.use('/api/convert', convertRoutes);
app.use('/api/ai', aiRoutes);

// Error handling (must be last)
app.use(notFoundHandler);
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════════════════╗
║                    UMDM+ Server                            ║
╚════════════════════════════════════════════════════════════╝

🚀 Server running on: http://localhost:${PORT}
📝 Environment: ${process.env.NODE_ENV || 'development'}
🕐 Started at: ${new Date().toLocaleString()}

📚 Documentation: http://localhost:${PORT}/README.md
🔗 API Health: http://localhost:${PORT}/api/health
🌐 Web App: http://localhost:${PORT}

Next Steps:
1. Install dependencies: npm install
2. Review PROJECT_ROADMAP.md for development phases
3. Set up .env file (see .env.example)
4. Start implementing Phase 1 features

Press Ctrl+C to stop the server
  `);
});

module.exports = app;
