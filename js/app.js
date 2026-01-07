/**
 * UMDM+ - Universal Media Downloader, Converter, and Manager Plus
 * Main Application JavaScript
 * Version: 1.0.0
 * Refactored for improved maintainability and readability
 */

import { AppState, loadSettings, saveSettings, applyTheme, toggleTheme } from './state.js';
import { showNotification, showClipboardNotification, dismissNotification } from './notifications.js';
import { 
  generateId, 
  extractTitleFromUrl, 
  formatFileSize, 
  formatTime, 
  validateUrl, 
  detectVideoSource 
} from './utils.js';

// ============================================
// CONSTANTS
// ============================================
const API_BASE_URL = '/api';
const CLIPBOARD_CHECK_INTERVAL = 2000;
const DOWNLOAD_PROGRESS_INTERVAL = 500;

// ============================================
// DOM ELEMENTS
// ============================================
const DOM = {
  // Inputs
  urlInput: document.getElementById('urlInput'),
  pasteBtn: document.getElementById('pasteBtn'),
  downloadBtn: document.getElementById('downloadBtn'),
    
  // Selects
  qualitySelect: document.getElementById('qualitySelect'),
  formatSelect: document.getElementById('formatSelect'),
  audioQualitySelect: document.getElementById('audioQualitySelect'),
    
  // Checkboxes
  subtitlesCheck: document.getElementById('subtitlesCheck'),
  thumbnailCheck: document.getElementById('thumbnailCheck'),
  metadataCheck: document.getElementById('metadataCheck'),
  removeAdsCheck: document.getElementById('removeAdsCheck'),
  trimCheck: document.getElementById('trimCheck'),
    
  // Sections
  downloadOptions: document.getElementById('downloadOptions'),
  advancedOptions: document.getElementById('advancedOptions'),
  trimInputs: document.getElementById('trimInputs'),
  queueList: document.getElementById('queueList'),
    
  // Buttons
  themeToggle: document.getElementById('themeToggle'),
  settingsBtn: document.getElementById('settingsBtn'),
  advancedToggle: document.getElementById('advancedToggle'),
  clearCompletedBtn: document.getElementById('clearCompletedBtn'),
  pauseAllBtn: document.getElementById('pauseAllBtn'),
    
  // Tabs
  toolTabs: document.querySelectorAll('.tool-tab'),
  queueTabs: document.querySelectorAll('.queue-tab')
};

// ============================================
// INITIALIZATION
// ============================================
function init() {
  // Load saved settings
  loadSettings();
  
  // Apply theme
  applyTheme(AppState.settings.theme);
  
  // Setup event listeners
  setupEventListeners();
  
  // Initialize clipboard monitor
  if (AppState.settings.clipboardMonitor) {
    initClipboardMonitor();
  }
  
  console.log('UMDM+ Application Initialized');
}

// ============================================
// EVENT LISTENERS
// ============================================
function setupEventListeners() {
  // URL Input
  DOM.urlInput?.addEventListener('input', handleUrlInput);
  DOM.urlInput?.addEventListener('paste', handleUrlPaste);
    
  // Buttons
  DOM.pasteBtn?.addEventListener('click', handlePasteClick);
  DOM.downloadBtn?.addEventListener('click', handleDownload);
  DOM.themeToggle?.addEventListener('click', handleThemeToggle);
  DOM.settingsBtn?.addEventListener('click', openSettings);
  DOM.advancedToggle?.addEventListener('click', toggleAdvancedOptions);
  DOM.clearCompletedBtn?.addEventListener('click', clearCompleted);
  DOM.pauseAllBtn?.addEventListener('click', pauseAll);
    
  // Checkboxes
  DOM.trimCheck?.addEventListener('change', handleTrimToggle);
    
  // Tool Tabs
  DOM.toolTabs.forEach(tab => {
    tab.addEventListener('click', () => handleToolTab(tab));
  });
    
  // Queue Tabs
  DOM.queueTabs.forEach(tab => {
    tab.addEventListener('click', () => handleQueueTab(tab));
  });
    
  // Navigation Links
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
            
      const target = link.getAttribute('href');
      document.querySelector(target)?.scrollIntoView({ behavior: 'smooth' });
    });
  });
}

// ============================================
// URL INPUT HANDLERS
// ============================================
function handleUrlInput(e) {
  const url = e.target.value.trim();
  
  if (url.length > 0) {
    const isValid = validateUrl(url);
    if (isValid) {
      detectSourceAndShowOptions(url);
      DOM.downloadBtn.disabled = false;
    } else {
      DOM.downloadBtn.disabled = true;
    }
  } else {
    hideDownloadOptions();
  }
}

function handleUrlPaste() {
  setTimeout(() => {
    const url = DOM.urlInput.value.trim();
    if (url) {
      validateUrl(url);
    }
  }, 100);
}

async function handlePasteClick() {
  try {
    const text = await navigator.clipboard.readText();
    DOM.urlInput.value = text;
    const isValid = validateUrl(text);
    if (isValid) {
      detectSourceAndShowOptions(text);
      DOM.downloadBtn.disabled = false;
    }
    showNotification('URL pasted from clipboard', 'success');
  } catch (err) {
    showNotification('Failed to read clipboard', 'error');
    console.error('Clipboard read error:', err);
  }
}

function detectSourceAndShowOptions(url) {
  const source = detectVideoSource(url);
  if (source) {
    showDownloadOptions();
    fetchVideoMetadata(url);
  }
}

function showDownloadOptions() {
  DOM.downloadOptions.style.display = 'block';
  DOM.downloadOptions.classList.add('animate-slide-in');
}

function hideDownloadOptions() {
  DOM.downloadOptions.style.display = 'none';
}

// ============================================
// VIDEO METADATA FETCHING
// ============================================
async function fetchVideoMetadata(url) {
  try {
    // This would connect to backend API
    // For demo purposes, we'll simulate the response
    console.log('Fetching metadata for:', url);
        
    // Simulate API call
    showNotification('Analyzing video...', 'info');
        
    // In production, this would be:
    // const response = await fetch('/api/v1/metadata', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ url })
    // });
    // const data = await response.json();
        
  } catch (error) {
    console.error('Error fetching metadata:', error);
    showNotification('Failed to fetch video information', 'error');
  }
}

// ============================================
// DOWNLOAD HANDLER
// ============================================
async function handleDownload() {
  const url = DOM.urlInput.value.trim();
    
  if (!url) {
    showNotification('Please enter a valid URL', 'error');
    return;
  }
    
  // Gather download options
  const downloadConfig = {
    url: url,
    quality: DOM.qualitySelect.value,
    format: DOM.formatSelect.value,
    audioQuality: DOM.audioQualitySelect.value,
    subtitles: DOM.subtitlesCheck.checked,
    thumbnail: DOM.thumbnailCheck?.checked,
    metadata: DOM.metadataCheck?.checked,
    removeAds: DOM.removeAdsCheck?.checked,
    trim: DOM.trimCheck?.checked ? {
      start: document.getElementById('trimStart')?.value,
      end: document.getElementById('trimEnd')?.value
    } : null
  };
    
  // Add to queue
  addToQueue(downloadConfig);
    
  // Clear input
  DOM.urlInput.value = '';
  hideDownloadOptions();
    
  // Start download
  startDownload(downloadConfig);
}

function addToQueue(config) {
  const download = {
    id: generateId(),
    url: config.url,
    title: extractTitleFromUrl(config.url),
    status: 'pending',
    progress: 0,
    quality: config.quality,
    format: config.format,
    addedAt: new Date(),
    config: config
  };
    
  AppState.downloads.push(download);
  AppState.queue.push(download);
    
  updateQueueDisplay();
  showNotification('Added to download queue', 'success');
}

async function startDownload(config) {
  console.log('Starting download:', config);
    
  try {
    // This would connect to backend API
    // const response = await fetch('/api/v1/download', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(config)
    // });
        
    // Simulate download progress
    simulateDownloadProgress(config);
        
  } catch (error) {
    console.error('Download error:', error);
    showNotification('Download failed', 'error');
  }
}

function simulateDownloadProgress() {
  // This simulates download progress for demonstration
  const downloadId = AppState.downloads[AppState.downloads.length - 1].id;
  let progress = 0;
  
  const interval = setInterval(() => {
    progress += Math.random() * 15;
        
    if (progress >= 100) {
      progress = 100;
      clearInterval(interval);
      updateDownloadStatus(downloadId, 'completed', 100);
      showNotification('Download completed!', 'success');
    } else {
      updateDownloadStatus(downloadId, 'downloading', progress);
    }
        
    updateQueueDisplay();
  }, 500);
}

function updateDownloadStatus(id, status, progress) {
  const download = AppState.downloads.find(d => d.id === id);
  if (download) {
    download.status = status;
    download.progress = Math.round(progress);
  }
}

// ============================================
// QUEUE MANAGEMENT
// ============================================
function updateQueueDisplay() {
  // Single pass through downloads array to categorize
  const categorizedDownloads = AppState.downloads.reduce((acc, download) => {
    switch(download.status) {
    case 'downloading':
      acc.active.push(download);
      break;
    case 'pending':
      acc.pending.push(download);
      break;
    case 'completed':
      acc.completed.push(download);
      break;
    case 'failed':
      acc.failed.push(download);
      break;
    }
    return acc;
  }, { active: [], pending: [], completed: [], failed: [] });
    
  // Update tab counts
  DOM.queueTabs.forEach(tab => {
    const queueType = tab.dataset.queue;
    const count = categorizedDownloads[queueType]?.length || 0;
    tab.textContent = `${queueType.charAt(0).toUpperCase() + queueType.slice(1)} (${count})`;
  });
    
  // Render current tab
  renderQueueList(categorizedDownloads);
}

function renderQueueList(categorizedDownloads) {
  // Get downloads for current tab from pre-categorized downloads
  const downloads = categorizedDownloads[AppState.currentTab] || [];
    
  if (downloads.length === 0) {
    DOM.queueList.innerHTML = `
            <div class="empty-state">
                <svg width="64" height="64" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                <p>No ${AppState.currentTab} downloads</p>
                <span>Downloads will appear here</span>
            </div>
        `;
  } else {
    DOM.queueList.innerHTML = downloads.map(download => createDownloadItemHTML(download)).join('');
  }
}

function createDownloadItemHTML(download) {
  const statusIcon = getStatusIcon(download.status);
  const progressBar = download.status === 'downloading' ? 
    `<div class="progress-bar"><div class="progress-fill" style="width: ${download.progress}%"></div></div>` : '';
    
  return `
        <div class="download-item" data-id="${download.id}">
            <div class="download-icon">${statusIcon}</div>
            <div class="download-info">
                <div class="download-title">${download.title}</div>
                <div class="download-meta">${download.quality} • ${download.format.toUpperCase()}</div>
                ${progressBar}
            </div>
            <div class="download-actions">
                ${download.status === 'downloading' ? '<button class="btn-icon" onclick="pauseDownload(\'' + download.id + '\')">⏸</button>' : ''}
                ${download.status === 'completed' ? '<button class="btn-icon" onclick="openDownload(\'' + download.id + '\')">📥</button>' : ''}
                <button class="btn-icon" onclick="removeDownload('${download.id}')">🗑</button>
            </div>
        </div>
    `;
}

function getStatusIcon(status) {
  const icons = {
    pending: '⏳',
    downloading: '⬇️',
    completed: '✅',
    failed: '❌',
    paused: '⏸️'
  };
  return icons[status] || '❓';
}

function clearCompleted() {
  AppState.downloads = AppState.downloads.filter(d => d.status !== 'completed');
  updateQueueDisplay();
  showNotification('Completed downloads cleared', 'success');
}

function pauseAll() {
  AppState.downloads.forEach(d => {
    if (d.status === 'downloading') {
      d.status = 'paused';
    }
  });
  updateQueueDisplay();
  showNotification('All downloads paused', 'info');
}

// ============================================
// TAB HANDLERS
// ============================================
function handleToolTab(tab) {
  // Remove active from all tabs
  DOM.toolTabs.forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tool-content').forEach(c => c.classList.remove('active'));
    
  // Add active to clicked tab
  tab.classList.add('active');
  const tabId = tab.dataset.tab + '-tab';
  document.getElementById(tabId)?.classList.add('active');
}

function handleQueueTab(tab) {
  // Remove active from all tabs
  DOM.queueTabs.forEach(t => t.classList.remove('active'));
    
  // Add active to clicked tab
  tab.classList.add('active');
  AppState.currentTab = tab.dataset.queue;
    
  // Update display - this will categorize and render
  updateQueueDisplay();
}

// ============================================
// ADVANCED OPTIONS
// ============================================
function toggleAdvancedOptions() {
  const isVisible = DOM.advancedOptions.style.display === 'block';
  DOM.advancedOptions.style.display = isVisible ? 'none' : 'block';
  DOM.advancedToggle.textContent = isVisible ? '▼ Advanced Options' : '▲ Advanced Options';
}

function handleTrimToggle(e) {
  DOM.trimInputs.style.display = e.target.checked ? 'grid' : 'none';
}

// ============================================
// THEME TOGGLE
// ============================================
function handleThemeToggle() {
  const newTheme = toggleTheme();
  showNotification(`${newTheme.charAt(0).toUpperCase() + newTheme.slice(1)} theme activated`, 'info');
}

// ============================================
// CLIPBOARD MONITOR
// ============================================
function initClipboardMonitor() {
  let lastClipboard = '';
  let clipboardCheckTimeout;
  
  // Reduced polling frequency and added debouncing
  const checkClipboard = async () => {
    try {
      const text = await navigator.clipboard.readText();
      
      if (text !== lastClipboard && validateUrl(text)) {
        lastClipboard = text;
        showClipboardNotification(text);
      }
    } catch (err) {
      // Clipboard access denied or not available
      // Silently fail - this is expected when tab is not focused
    } finally {
      // Schedule next check with increased interval to reduce CPU usage
      clipboardCheckTimeout = setTimeout(checkClipboard, CLIPBOARD_CHECK_INTERVAL);
    }
  };
  
  // Start monitoring
  checkClipboard();
  
  // Clean up on page unload
  window.addEventListener('beforeunload', () => {
    if (clipboardCheckTimeout) {
      clearTimeout(clipboardCheckTimeout);
    }
  });
}

function useClipboardUrl(url) {
  DOM.urlInput.value = url;
  const isValid = validateUrl(url);
  if (isValid) {
    detectSourceAndShowOptions(url);
    DOM.downloadBtn.disabled = false;
  }
  document.querySelector('.clipboard-notification')?.remove();
}

// ============================================
// SETTINGS MODAL
// ============================================
function openSettings() {
  const modal = document.getElementById('settingsModal');
  modal?.classList.add('active');
  
  // Close modal when clicking outside
  modal?.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.remove('active');
    }
  });
  
  // Close button
  modal?.querySelector('.modal-close')?.addEventListener('click', () => {
    modal.classList.remove('active');
  });
}

// ============================================
// GLOBAL WINDOW FUNCTIONS (for inline onclick)
// ============================================
window.pauseDownload = function (id) {
  const download = AppState.downloads.find(d => d.id === id);
  if (download) {
    download.status = 'paused';
    updateQueueDisplay();
    showNotification('Download paused', 'info');
  }
};

// eslint-disable-next-line no-unused-vars
window.openDownload = function (id) {
  showNotification('Opening download...', 'info');
  // In production, this would open/download the file
};

window.removeDownload = function (id) {
  AppState.downloads = AppState.downloads.filter(d => d.id !== id);
  updateQueueDisplay();
  showNotification('Download removed', 'info');
};

window.useClipboardUrl = useClipboardUrl;
window.dismissNotification = dismissNotification;

// ============================================
// SERVICE WORKER REGISTRATION (PWA)
// ============================================
// SERVICE WORKER REGISTRATION
// ============================================
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(() => console.log('ServiceWorker registered'))
      .catch(err => console.log('ServiceWorker registration failed:', err));
  });
}

// ============================================
// INITIALIZE APP
// ============================================
document.addEventListener('DOMContentLoaded', init);

// Export for module usage
export { AppState, init, showNotification };
