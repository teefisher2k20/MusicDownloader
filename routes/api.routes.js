/**
 * API Routes
 * Health and system status endpoints
 */

const express = require('express');
const router = express.Router();

/**
 * Health check endpoint
 * GET /api/health
 */
router.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

/**
 * Get supported sites
 * GET /api/sites
 */
router.get('/sites', (req, res) => {
  const { SUPPORTED_SITES } = require('../config/constants');
  res.json(SUPPORTED_SITES);
});

module.exports = router;
