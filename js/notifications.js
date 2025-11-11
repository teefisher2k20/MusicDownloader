/**
 * Notification Manager
 * Handles all application notifications
 */

/**
 * Show notification to user
 * @param {string} message - Notification message
 * @param {string} type - Notification type (info, success, error, warning)
 */
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

/**
 * Show clipboard notification with action buttons
 * @param {string} url - The URL detected in clipboard
 */
function showClipboardNotification(url) {
  const notification = document.createElement('div');
  notification.className = 'clipboard-notification';
  notification.innerHTML = `
    <p>URL detected in clipboard</p>
    <button onclick="window.useClipboardUrl('${url}')">Add to Download</button>
    <button onclick="window.dismissNotification(this)">Dismiss</button>
  `;
  document.body.appendChild(notification);
  
  setTimeout(() => notification.remove(), 10000);
}

/**
 * Dismiss notification
 * @param {HTMLElement} btn - The button element that triggered dismissal
 */
function dismissNotification(btn) {
  btn.closest('.clipboard-notification')?.remove();
}

export {
  showNotification,
  showClipboardNotification,
  dismissNotification
};
