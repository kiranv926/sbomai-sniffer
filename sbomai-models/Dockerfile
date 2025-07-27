# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app/src

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY protos/ ./protos/

# Generate gRPC code
RUN python -m grpc_tools.protoc \
    --python_out=./src \
    --grpc_python_out=./src \
    --proto_path=./protos \
    ./protos/sbomai_ai.proto

# Create non-root user
RUN useradd --create-home --shell /bin/bash sbomai && \
    chown -R sbomai:sbomai /app

# Switch to non-root user
USER sbomai

# Create necessary directories
RUN mkdir -p /app/data /app/cache /app/models /app/logs

# Expose gRPC port
EXPOSE 50051

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50051/health || exit 1

# Run the service
CMD ["python", "-m", "sbomai_ai.service"] 