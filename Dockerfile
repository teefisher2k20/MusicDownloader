# Multi-stage Dockerfile for UMDM+

# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build || echo "No build step yet"

# Stage 2: Python dependencies
FROM python:3.11-slim AS python-builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 3: Final production image
FROM python:3.11-slim
LABEL maintainer="UMDM+ Team"
LABEL description="Universal Media Downloader, Converter, and Manager Plus"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /downloads && \
    chown -R appuser:appuser /app /downloads

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=python-builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application files
COPY --chown=appuser:appuser . .
COPY --from=frontend-builder --chown=appuser:appuser /app/node_modules ./node_modules

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Switch to app user
USER appuser

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    NODE_ENV=production \
    PORT=3000

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Start application
CMD ["node", "server.js"]
