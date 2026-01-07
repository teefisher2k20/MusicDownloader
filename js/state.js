/**
 * State Management
 * Application state and settings
 */

/**
 * Application State
 */
const AppState = {
  downloads: [],
  queue: [],
  settings: {
    theme: 'light',
    defaultQuality: '1080p',
    defaultFormat: 'mp4',
    smartMode: true,
    clipboardMonitor: true,
    autoSubtitles: true
  },
  currentTab: 'active'
};

/**
 * Load settings from localStorage
 */
function loadSettings() {
  try {
    const savedSettings = localStorage.getItem('umdm_settings');
    if (savedSettings) {
      const parsed = JSON.parse(savedSettings);
      // Validate that parsed settings have expected structure
      if (parsed && typeof parsed === 'object') {
        // Merge with defaults to ensure all required properties exist
        AppState.settings = { ...AppState.settings, ...parsed };
      }
    }
  } catch (error) {
    // Handle corrupted localStorage data gracefully
    console.error('Failed to load settings:', error);
    // Only remove if it's a parse error (corrupted data)
    if (error instanceof SyntaxError) {
      console.warn('Removing corrupted settings data');
      localStorage.removeItem('umdm_settings');
    }
    // For other errors (like SecurityError), keep the data
  }
}

/**
 * Save settings to localStorage
 */
function saveSettings() {
  try {
    localStorage.setItem('umdm_settings', JSON.stringify(AppState.settings));
  } catch (error) {
    // Handle localStorage quota exceeded or other errors
    console.error('Failed to save settings:', error);
  }
}

/**
 * Apply theme
 * @param {string} theme - Theme name ('light' or 'dark')
 */
function applyTheme(theme) {
  document.body.className = theme === 'dark' ? 'dark-theme' : 'light-theme';
  AppState.settings.theme = theme;
  saveSettings();
}

/**
 * Toggle theme
 */
function toggleTheme() {
  const newTheme = AppState.settings.theme === 'light' ? 'dark' : 'light';
  applyTheme(newTheme);
  return newTheme;
}

export { AppState, loadSettings, saveSettings, applyTheme, toggleTheme };
