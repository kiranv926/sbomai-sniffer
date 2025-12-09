# Use multi-stage build for smaller final image
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 sbomai
USER sbomai

# Set working directory
WORKDIR /app

# Copy application code
COPY protos/ /app/protos/
COPY src/ /app/src/
COPY main.py /app/

# Generate gRPC code
RUN python -m grpc_tools.protoc \
    --python_out=./src \
    --grpc_python_out=./src \
    --proto_path=./protos \
    ./protos/sbomai_ai.proto

# Create cache directory
RUN mkdir -p /app/.cache && chown sbomai:sbomai /app/.cache

# Expose ports
# gRPC
EXPOSE 50051
# Metrics
EXPOSE 9090

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:9090/health || exit 1

# Run the gRPC service
CMD ["python", "-m", "sbomai_ai.service"] 