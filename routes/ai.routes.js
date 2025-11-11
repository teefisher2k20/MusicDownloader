/**
 * AI Routes
 * AI-powered feature endpoints (Phase 4+)
 */

const express = require('express');
const router = express.Router();
const { MESSAGES } = require('../config/constants');

/**
 * AI Summarization endpoint
 * POST /api/ai/summarize
 */
router.post('/summarize', (req, res) => {
  res.json({ message: MESSAGES.AI_SUMMARIZATION });
});

/**
 * AI Transcription endpoint
 * POST /api/ai/transcribe
 */
router.post('/transcribe', (req, res) => {
  res.json({ message: MESSAGES.AI_TRANSCRIPTION });
});

/**
 * AI Upscaling endpoint
 * POST /api/ai/upscale
 */
router.post('/upscale', (req, res) => {
  res.json({ message: MESSAGES.AI_UPSCALING });
});

module.exports = router;
