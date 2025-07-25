@echo off
REM SBOMAI Monitoring Stack Startup Script for Windows
REM This script starts the complete monitoring stack with Grafana, Prometheus, and Loki

echo 🚀 Starting SBOMAI Monitoring Stack...
echo ======================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not available. Please install Docker Desktop and try again.
    pause
    exit /b 1
)

REM Create log directory if it doesn't exist
if not exist logs mkdir logs

echo 📦 Starting monitoring services...
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check service status
echo 🔍 Checking service status...
docker-compose ps

echo.
echo ✅ Monitoring stack is starting up!
echo.
echo 📊 Access URLs:
echo    Grafana:     http://localhost:3000 (admin/sbomai2024)
echo    Prometheus:  http://localhost:9090
echo    Loki:        http://localhost:3100
echo.
echo 📈 Available Dashboards:
echo    - SBOMAI Overview Dashboard (auto-loaded)
echo    - System Health Dashboard
echo    - Vulnerability Analysis Dashboard
echo.
echo 🔧 Useful Commands:
echo    View logs:     docker-compose logs -f [service]
echo    Stop stack:    docker-compose down
echo    Restart:       docker-compose restart [service]
echo    Status:        docker-compose ps
echo.
echo 📋 Next Steps:
echo    1. Open Grafana at http://localhost:3000
echo    2. Login with admin/sbomai2024
echo    3. Navigate to Dashboards to see SBOMAI metrics
echo    4. Start your SBOMAI services to see metrics flowing
echo.
echo 🎯 To see metrics, ensure your SBOMAI services are running and exposing metrics on:
echo    - Core:     http://localhost:8080/actuator/prometheus
echo    - Parser:   http://localhost:8081/actuator/prometheus
echo    - VulnScan: http://localhost:8082/actuator/prometheus
echo    - Policy:   http://localhost:8083/actuator/prometheus
echo.

REM Check if services are responding
echo 🔍 Testing service connectivity...

REM Test Prometheus
curl -s http://localhost:9090/api/v1/status/config >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Prometheus is responding
) else (
    echo ⚠️  Prometheus is starting up (may take a moment)
)

REM Test Grafana
curl -s http://localhost:3000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Grafana is responding
) else (
    echo ⚠️  Grafana is starting up (may take a moment)
)

REM Test Loki
curl -s http://localhost:3100/ready >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Loki is responding
) else (
    echo ⚠️  Loki is starting up (may take a moment)
)

echo.
echo 🎉 Monitoring stack startup complete!
echo    Check the URLs above to access the dashboards.
echo.
pause 