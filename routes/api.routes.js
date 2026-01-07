/**
 * API Routes
 * Health and system status endpoints
 */

const express = require('express');
const router = express.Router();
const { SUPPORTED_SITES } = require('../config/constants');

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
  res.json(SUPPORTED_SITES);
});

module.exports = router;
