/**
 * Conversion Routes
 * Media conversion endpoints
 */

const express = require('express');
const router = express.Router();
const { CONVERSION_STATUS, MESSAGES } = require('../config/constants');

/**
 * Conversion endpoint
 * POST /api/convert
 */
router.post('/', (req, res) => {
  const { fileId, targetFormat } = req.body;
  
  if (!fileId || !targetFormat) {
    return res.status(400).json({ error: MESSAGES.MISSING_PARAMS });
  }
  
  res.json({
    id: `convert_${Date.now()}`,
    fileId,
    targetFormat,
    status: CONVERSION_STATUS.QUEUED,
    message: MESSAGES.CONVERSION_QUEUED
  });
});

module.exports = router;
