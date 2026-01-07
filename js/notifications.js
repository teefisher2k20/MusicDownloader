/**
 * Notification Manager
 * Handles all application notifications
 */

// Track active notifications to prevent duplicates
const activeNotifications = new Set();

/**
 * Show notification to user
 * @param {string} message - Notification message
 * @param {string} type - Notification type (info, success, error, warning)
 */
function showNotification(message, type = 'info') {
  // Prevent duplicate notifications
  const notificationKey = `${type}:${message}`;
  if (activeNotifications.has(notificationKey)) {
    return;
  }
  
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  activeNotifications.add(notificationKey);
  
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => {
      notification.remove();
      activeNotifications.delete(notificationKey);
    }, 300);
  }, 3000);
}

/**
 * Show clipboard notification with action buttons
 * @param {string} url - The URL detected in clipboard
 */
function showClipboardNotification(url) {
  // Remove any existing clipboard notifications first
  document.querySelectorAll('.clipboard-notification').forEach(n => n.remove());
  
  const notification = document.createElement('div');
  notification.className = 'clipboard-notification';
  
  // Create elements safely to prevent XSS
  const message = document.createElement('p');
  message.textContent = 'URL detected in clipboard';
  
  const addButton = document.createElement('button');
  addButton.textContent = 'Add to Download';
  addButton.onclick = () => window.useClipboardUrl(url);
  
  const dismissButton = document.createElement('button');
  dismissButton.textContent = 'Dismiss';
  dismissButton.onclick = function () { window.dismissNotification(this); };
  
  notification.appendChild(message);
  notification.appendChild(addButton);
  notification.appendChild(dismissButton);
  
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
