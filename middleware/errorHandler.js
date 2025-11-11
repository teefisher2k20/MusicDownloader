/**
 * Error Handling Middleware
 * Centralized error handling for the application
 */

const { MESSAGES } = require('../config/constants');

/**
 * 404 Not Found handler
 */
const notFoundHandler = (req, res) => {
  res.status(404).json({ 
    error: MESSAGES.NOT_FOUND,
    path: req.originalUrl,
    method: req.method
  });
};

/**
 * Global error handler
 * Must have 4 parameters for Express to recognize it as error middleware
 */
const errorHandler = (err, req, res, next) => {
  // Log error for debugging
  console.error('Error:', {
    message: err.message,
    stack: err.stack,
    url: req.originalUrl,
    method: req.method
  });
  
  // Determine status code
  const statusCode = err.statusCode || res.statusCode || 500;
  
  // Send error response
  res.status(statusCode).json({
    error: err.message || MESSAGES.INTERNAL_ERROR,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

module.exports = {
  notFoundHandler,
  errorHandler
};
