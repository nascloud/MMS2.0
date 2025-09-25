# Multi-stage build

# Builder stage
FROM python:3.10-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY mihomo_sync/ ./mihomo_sync/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Final stage
FROM python:3.10-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser/app

# Copy installed packages from builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/mihomo_sync/ ./mihomo_sync/
COPY --from=builder /app/pyproject.toml ./pyproject.toml

# Copy main entry point
COPY main.py ./main.py

# Copy config directory for reference
COPY config/ ./config/

# Change ownership to non-root user
RUN chown -R appuser:appuser /home/appuser/app

# Switch to non-root user
USER appuser

# Expose volume for configuration
VOLUME ["/home/appuser/app/config"]

# Default command
CMD ["python", "main.py"]