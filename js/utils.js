/**
 * Utility Functions
 * Reusable helper functions
 */

/**
 * Generate unique ID
 * @returns {string} Unique identifier
 */
function generateId() {
  return '_' + Math.random().toString(36).slice(2, 11) + Date.now().toString(36);
}

/**
 * Extract title from URL
 * @param {string} url - The URL to extract title from
 * @returns {string} Extracted title or default
 */
function extractTitleFromUrl(url) {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname.replace('www.', '') + ' video';
  } catch {
    return 'Downloaded video';
  }
}

/**
 * Format file size
 * @param {number} bytes - Size in bytes
 * @returns {string} Formatted size string
 */
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Format time from seconds
 * @param {number} seconds - Time in seconds
 * @returns {string} Formatted time string (HH:MM:SS or MM:SS)
 */
function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  
  if (h > 0) {
    return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  }
  return `${m}:${s.toString().padStart(2, '0')}`;
}

/**
 * Validate URL
 * @param {string} url - URL to validate
 * @returns {boolean} True if valid URL
 */
function validateUrl(url) {
  const urlPattern = /^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)/;
  return urlPattern.test(url);
}

/**
 * Detect video source from URL
 * @param {string} url - URL to analyze
 * @returns {string} Source name or 'generic'
 */
function detectVideoSource(url) {
  const sources = {
    youtube: /youtube\.com|youtu\.be/,
    tiktok: /tiktok\.com/,
    instagram: /instagram\.com/,
    facebook: /facebook\.com|fb\.watch/,
    twitter: /twitter\.com|x\.com/,
    vimeo: /vimeo\.com/,
    dailymotion: /dailymotion\.com/,
    twitch: /twitch\.tv/
  };
  
  for (const [name, pattern] of Object.entries(sources)) {
    if (pattern.test(url)) {
      return name;
    }
  }
  
  return 'generic';
}

export {
  generateId,
  extractTitleFromUrl,
  formatFileSize,
  formatTime,
  validateUrl,
  detectVideoSource
};
