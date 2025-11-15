# NATO PMP Analyzer - Docker Image
# Multi-stage build for optimized image size

# Stage 1: Base Python image
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Build dependencies
FROM base as builder

# Create and set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 3: Final runtime image
FROM base as runtime

# Create non-root user for security
RUN useradd -m -u 1000 streamlit && \
    mkdir -p /app && \
    chown -R streamlit:streamlit /app

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/streamlit/.local

# Copy application code
COPY --chown=streamlit:streamlit . .

# Create necessary directories
RUN mkdir -p /app/chroma_db && \
    mkdir -p /app/.streamlit && \
    chown -R streamlit:streamlit /app

# Switch to non-root user
USER streamlit

# Add local Python packages to PATH
ENV PATH=/home/streamlit/.local/bin:$PATH

# Expose Streamlit default port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
