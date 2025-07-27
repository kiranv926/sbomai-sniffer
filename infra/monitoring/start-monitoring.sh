#!/bin/bash

# SBOMAI Monitoring Stack Startup Script
# This script starts the complete monitoring stack for SBOMAI

set -e

echo "🚀 Starting SBOMAI Monitoring Stack..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data/prometheus
mkdir -p data/grafana
mkdir -p data/loki
mkdir -p data/alertmanager
mkdir -p data/redis

# Set environment variables for OAuth (optional)
if [ -z "$GITHUB_CLIENT_ID" ]; then
    echo "⚠️  GITHUB_CLIENT_ID not set. OAuth will be disabled."
    export GITHUB_CLIENT_ID=""
    export GITHUB_CLIENT_SECRET=""
    export GITHUB_TEAM_IDS=""
    export GITHUB_ORGS=""
fi

# Start the monitoring stack
echo "🔧 Starting monitoring services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check Prometheus
if curl -s http://localhost:9090/-/healthy > /dev/null; then
    echo "✅ Prometheus is healthy"
else
    echo "❌ Prometheus is not responding"
fi

# Check Grafana
if curl -s http://localhost:3000/api/health > /dev/null; then
    echo "✅ Grafana is healthy"
else
    echo "❌ Grafana is not responding"
fi

# Check Loki
if curl -s http://localhost:3100/ready > /dev/null; then
    echo "✅ Loki is healthy"
else
    echo "❌ Loki is not responding"
fi

# Check Alertmanager
if curl -s http://localhost:9093/-/healthy > /dev/null; then
    echo "✅ Alertmanager is healthy"
else
    echo "❌ Alertmanager is not responding"
fi

echo ""
echo "🎉 SBOMAI Monitoring Stack is ready!"
echo ""
echo "📊 Access URLs:"
echo "   Grafana:      http://localhost:3000 (admin/sbomai2024)"
echo "   Prometheus:   http://localhost:9090"
echo "   Alertmanager: http://localhost:9093"
echo "   Loki:         http://localhost:3100"
echo ""
echo "📋 Useful Commands:"
echo "   View logs:    docker-compose logs -f"
echo "   Stop stack:   docker-compose down"
echo "   Restart:      docker-compose restart"
echo ""
echo "🔧 Next Steps:"
echo "   1. Open Grafana at http://localhost:3000"
echo "   2. Login with admin/sbomai2024"
echo "   3. The SBOMAI dashboards should be automatically loaded"
echo "   4. Configure your SBOMAI services to expose metrics on /actuator/prometheus"
echo ""
echo "📈 To start SBOMAI services with metrics:"
echo "   cd .. && mvn spring-boot:run -pl sbomai-core"
echo "" 