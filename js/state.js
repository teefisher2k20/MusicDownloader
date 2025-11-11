/** * State Management * Application state and settings */ /** * Application State */ const AppState =
  {
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
/** * Load settings from localStorage */ function loadSettings() {
  const savedSettings = localStorage.getItem('umdm_settings');
  if (savedSettings) {
    AppState.settings = { ...AppState.settings, ...JSON.parse(savedSettings) };
  }
}
/** * Save settings to localStorage */ function saveSettings() {
  localStorage.setItem('umdm_settings', JSON.stringify(AppState.settings));
}
/** * Apply theme * @param {string} theme - Theme name ('light' or 'dark') */ function applyTheme(
  theme
) {
  document.body.className = theme === 'dark' ? 'dark-theme' : 'light-theme';
  AppState.settings.theme = theme;
  saveSettings();
}
/** * Toggle theme */ function toggleTheme() {
  const newTheme = AppState.settings.theme === 'light' ? 'dark' : 'light';
  applyTheme(newTheme);
  return newTheme;
}
export { AppState, loadSettings, saveSettings, applyTheme, toggleTheme };
