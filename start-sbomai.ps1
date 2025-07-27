# SBOMAI Startup Script
# This script starts all SBOMAI services using Docker Compose

Write-Host " Starting SBOMAI - AI-Powered SBOM Analysis Tool" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check if Docker is running
Write-Host " Checking Docker status..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host " Docker is running" -ForegroundColor Green
} catch {
    Write-Host " Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

# Check if docker-compose is available
Write-Host " Checking docker-compose..." -ForegroundColor Yellow
try {
    docker-compose --version | Out-Null
    Write-Host " docker-compose is available" -ForegroundColor Green
} catch {
    Write-Host " docker-compose is not available. Please install Docker Compose and try again." -ForegroundColor Red
    exit 1
}

# Create necessary directories
Write-Host " Creating necessary directories..." -ForegroundColor Yellow
if (!(Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
    Write-Host " Created reports directory" -ForegroundColor Green
}

# Start all services
Write-Host " Starting all SBOMAI services..." -ForegroundColor Yellow
docker-compose up -d

# Wait for services to start
Write-Host " Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service status
Write-Host " Checking service status..." -ForegroundColor Yellow
docker-compose ps

# Display access information
Write-Host ""
Write-Host " SBOMAI is now running!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host " Grafana Dashboard: http://localhost:3000" -ForegroundColor Cyan
Write-Host "   Username: admin" -ForegroundColor Cyan
Write-Host "   Password: sbomai2024" -ForegroundColor Cyan
Write-Host ""
Write-Host " Prometheus: http://localhost:9090" -ForegroundColor Cyan
Write-Host " Loki (Logs): http://localhost:3100" -ForegroundColor Cyan
Write-Host " Alertmanager: http://localhost:9093" -ForegroundColor Cyan
Write-Host " Nginx: http://localhost:80" -ForegroundColor Cyan
Write-Host ""
Write-Host " SBOMAI Services:" -ForegroundColor Cyan
Write-Host "   Core API: http://localhost:8080" -ForegroundColor Cyan
Write-Host "   Parser: http://localhost:8081" -ForegroundColor Cyan
Write-Host "   Vulnerability Scanner: http://localhost:8082" -ForegroundColor Cyan
Write-Host "   Policy Engine: http://localhost:8083" -ForegroundColor Cyan
Write-Host "   AI/ML Models Microservice: gRPC localhost:50051, Metrics http://localhost:9091" -ForegroundColor Cyan
Write-Host ""
Write-Host " Useful Commands:" -ForegroundColor Yellow
Write-Host "   View logs: docker-compose logs -f [service-name]" -ForegroundColor White
Write-Host "   Stop all: docker-compose down" -ForegroundColor White
Write-Host "   Restart: docker-compose restart [service-name]" -ForegroundColor White
Write-Host "   Status: docker-compose ps" -ForegroundColor White
Write-Host "   docker-compose exec sbomai-cli java -jar target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze --file /app/sboms/spdx-sample.json --output /app/reports/report.json" -ForegroundColor White