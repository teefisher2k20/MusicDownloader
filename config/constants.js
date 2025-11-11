/**
 * Application Constants
 * Centralized configuration and magic numbers
 */

module.exports = {
  // Server Configuration
  DEFAULT_PORT: 3000,
  
  // Supported Sites
  SUPPORTED_SITES: {
    total: 1100,
    categories: {
      video: ['YouTube', 'TikTok', 'Instagram', 'Twitter/X', 'Facebook'],
      music: ['Spotify', 'SoundCloud', 'Apple Music', 'Bandcamp'],
      streaming: ['Twitch', 'Kick', 'DLive'],
      educational: ['Coursera', 'Udemy', 'Khan Academy'],
      social: ['Reddit', 'Pinterest', 'Tumblr']
    }
  },
  
  // Download Status
  DOWNLOAD_STATUS: {
    QUEUED: 'queued',
    DOWNLOADING: 'downloading',
    COMPLETED: 'completed',
    FAILED: 'failed',
    PAUSED: 'paused'
  },
  
  // Conversion Status
  CONVERSION_STATUS: {
    QUEUED: 'queued',
    CONVERTING: 'converting',
    COMPLETED: 'completed',
    FAILED: 'failed'
  },
  
  // Estimated Times
  ESTIMATED_DOWNLOAD_TIME: '2-5 minutes',
  
  // Mock Progress
  MOCK_PROGRESS: {
    PERCENTAGE: 45,
    CURRENT_STEP: 'Extracting video stream',
    ETA: '2 minutes'
  },
  
  // API Messages
  MESSAGES: {
    AI_SUMMARIZATION: 'AI summarization coming in Phase 4',
    AI_TRANSCRIPTION: 'AI transcription coming in Phase 4',
    AI_UPSCALING: 'AI upscaling coming in Phase 6',
    DOWNLOAD_QUEUED: 'Download queued successfully',
    CONVERSION_QUEUED: 'Conversion queued successfully',
    NOT_FOUND: 'Endpoint not found',
    INTERNAL_ERROR: 'Internal server error',
    MISSING_URL: 'URL is required',
    MISSING_PARAMS: 'Required parameters missing'
  }
};
