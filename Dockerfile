FROM python:3.12-slim

WORKDIR /app

# System deps for psycopg, asyncpg, and subprocess render
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Non-root user for security
RUN useradd -m -u 1001 appuser && \
    mkdir -p /artifacts /tmp/renders && \
    chown -R appuser:appuser /app /artifacts /tmp/renders

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
