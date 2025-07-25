#!/bin/bash

# SBOMAI Monitoring Stack Startup Script
# This script starts the complete monitoring stack with Grafana, Prometheus, and Loki

set -e

echo "🚀 Starting SBOMAI Monitoring Stack..."
echo "======================================"

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

# Create log directory if it doesn't exist
mkdir -p logs

echo "📦 Starting monitoring services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Monitoring stack is starting up!"
echo ""
echo "📊 Access URLs:"
echo "   Grafana:     http://localhost:3000 (admin/sbomai2024)"
echo "   Prometheus:  http://localhost:9090"
echo "   Loki:        http://localhost:3100"
echo ""
echo "📈 Available Dashboards:"
echo "   - SBOMAI Overview Dashboard (auto-loaded)"
echo "   - System Health Dashboard"
echo "   - Vulnerability Analysis Dashboard"
echo ""
echo "🔧 Useful Commands:"
echo "   View logs:     docker-compose logs -f [service]"
echo "   Stop stack:    docker-compose down"
echo "   Restart:       docker-compose restart [service]"
echo "   Status:        docker-compose ps"
echo ""
echo "📋 Next Steps:"
echo "   1. Open Grafana at http://localhost:3000"
echo "   2. Login with admin/sbomai2024"
echo "   3. Navigate to Dashboards to see SBOMAI metrics"
echo "   4. Start your SBOMAI services to see metrics flowing"
echo ""
echo "🎯 To see metrics, ensure your SBOMAI services are running and exposing metrics on:"
echo "   - Core:     http://localhost:8080/actuator/prometheus"
echo "   - Parser:   http://localhost:8081/actuator/prometheus"
echo "   - VulnScan: http://localhost:8082/actuator/prometheus"
echo "   - Policy:   http://localhost:8083/actuator/prometheus"
echo ""

# Check if services are responding
echo "🔍 Testing service connectivity..."

# Test Prometheus
if curl -s http://localhost:9090/api/v1/status/config > /dev/null; then
    echo "✅ Prometheus is responding"
else
    echo "⚠️  Prometheus is starting up (may take a moment)"
fi

# Test Grafana
if curl -s http://localhost:3000/api/health > /dev/null; then
    echo "✅ Grafana is responding"
else
    echo "⚠️  Grafana is starting up (may take a moment)"
fi

# Test Loki
if curl -s http://localhost:3100/ready > /dev/null; then
    echo "✅ Loki is responding"
else
    echo "⚠️  Loki is starting up (may take a moment)"
fi

echo ""
echo "🎉 Monitoring stack startup complete!"
echo "   Check the URLs above to access the dashboards." 