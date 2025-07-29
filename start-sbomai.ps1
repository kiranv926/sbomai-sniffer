#!/usr/bin/env pwsh

<#
.SYNOPSIS
    Start the complete SBOMAI stack with monitoring

.DESCRIPTION
    This script starts all SBOMAI microservices and monitoring components
    using Docker Compose. It includes health checks and status reporting.

.PARAMETER Build
    Force rebuild of all containers

.PARAMETER Clean
    Clean up existing containers and volumes before starting

.PARAMETER Logs
    Show logs after starting services

.EXAMPLE
    .\start-sbomai.ps1
    .\start-sbomai.ps1 -Build
    .\start-sbomai.ps1 -Clean -Logs
#>

param(
    [switch]$Build,
    [switch]$Clean,
    [switch]$Logs
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
$Cyan = "Cyan"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Test-Docker {
    try {
        docker --version | Out-Null
        docker-compose --version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Test-Environment {
    Write-ColorOutput "🔍 Checking environment..." $Cyan
    
    if (-not (Test-Docker)) {
        Write-ColorOutput "❌ Docker and Docker Compose are required but not installed." $Red
        Write-ColorOutput "Please install Docker Desktop from https://www.docker.com/products/docker-desktop" $Yellow
        exit 1
    }
    
    Write-ColorOutput "✅ Docker and Docker Compose are available" $Green
    
    # Check if .env file exists
    if (-not (Test-Path ".env")) {
        Write-ColorOutput "⚠️  .env file not found. Creating template..." $Yellow
        @"
# SBOMAI Environment Configuration
OPENAI_API_KEY=your-openai-api-key-here
NVD_API_KEY=your-nvd-api-key-here

# Optional: Customize ports
CORE_PORT=8080
PARSER_PORT=8081
VULNSCAN_PORT=8082
POLICY_PORT=8083
GRAFANA_PORT=3000
PROMETHEUS_PORT=9090
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-ColorOutput "📝 Created .env template. Please update with your API keys." $Yellow
    }
}

function Start-Services {
    param(
        [switch]$Build,
        [switch]$Clean
    )
    
    Write-ColorOutput "🚀 Starting SBOMAI services..." $Cyan
    
    $composeArgs = @("up", "-d")
    
    if ($Build) {
        $composeArgs += "--build"
        Write-ColorOutput "🔨 Building containers..." $Yellow
    }
    
    if ($Clean) {
        Write-ColorOutput "🧹 Cleaning up existing containers..." $Yellow
        docker-compose down -v
        docker system prune -f
    }
    
    try {
        docker-compose $composeArgs
        Write-ColorOutput "✅ Services started successfully" $Green
    }
    catch {
        Write-ColorOutput "❌ Failed to start services: $($_.Exception.Message)" $Red
        exit 1
    }
}

function Wait-ForServices {
    Write-ColorOutput "⏳ Waiting for services to be ready..." $Cyan
    
    $services = @(
        @{Name="Core API"; Url="http://localhost:8080/actuator/health"},
        @{Name="Parser API"; Url="http://localhost:8081/actuator/health"},
        @{Name="VulnScan API"; Url="http://localhost:8082/actuator/health"},
        @{Name="Policy API"; Url="http://localhost:8083/actuator/health"},
        @{Name="Prometheus"; Url="http://localhost:9090/-/healthy"},
        @{Name="Grafana"; Url="http://localhost:3000/api/health"}
    )
    
    $maxAttempts = 30
    $attempt = 0
    
    foreach ($service in $services) {
        $attempt = 0
        Write-ColorOutput "🔍 Checking $($service.Name)..." $Cyan
        
        do {
            $attempt++
            try {
                $response = Invoke-WebRequest -Uri $service.Url -TimeoutSec 5 -UseBasicParsing
                if ($response.StatusCode -eq 200) {
                    Write-ColorOutput "✅ $($service.Name) is ready" $Green
                    break
                }
            }
            catch {
                if ($attempt -eq $maxAttempts) {
                    Write-ColorOutput "❌ $($service.Name) failed to start after $maxAttempts attempts" $Red
                }
                else {
                    Write-ColorOutput "⏳ Waiting for $($service.Name)... (attempt $attempt/$maxAttempts)" $Yellow
                    Start-Sleep -Seconds 2
                }
            }
        } while ($attempt -lt $maxAttempts)
    }
}

function Show-Status {
    Write-ColorOutput "📊 Service Status:" $Cyan
    docker-compose ps
    
    Write-ColorOutput "`n🌐 Access URLs:" $Cyan
    Write-ColorOutput "   Core API:        http://localhost:8080" $Green
    Write-ColorOutput "   Parser API:      http://localhost:8081" $Green
    Write-ColorOutput "   VulnScan API:    http://localhost:8082" $Green
    Write-ColorOutput "   Policy API:      http://localhost:8083" $Green
    Write-ColorOutput "   Grafana:         http://localhost:3000 (admin/sbomai2024)" $Green
    Write-ColorOutput "   Prometheus:      http://localhost:9090" $Green
    Write-ColorOutput "   Alertmanager:    http://localhost:9093" $Green
    Write-ColorOutput "   Loki:            http://localhost:3100" $Green
    
    Write-ColorOutput "`n📁 Directories:" $Cyan
    Write-ColorOutput "   SBOMs:           ./sboms" $Green
    Write-ColorOutput "   Reports:         ./reports" $Green
    Write-ColorOutput "   Logs:            ./logs" $Green
}

function Show-Logs {
    Write-ColorOutput "📋 Recent logs (last 20 lines):" $Cyan
    docker-compose logs --tail=20
}

# Main execution
try {
    Write-ColorOutput "🔍 SBOMAI - AI-Powered SBOM Analysis Tool" $Cyan
    Write-ColorOutput "=============================================" $Cyan
    
    Test-Environment
    Start-Services -Build:$Build -Clean:$Clean
    Wait-ForServices
    Show-Status
    
    if ($Logs) {
        Show-Logs
    }
    
    Write-ColorOutput "`n🎉 SBOMAI stack is ready!" $Green
    Write-ColorOutput "Run '.\test-sbomai.ps1' to test the system" $Yellow
}
catch {
    Write-ColorOutput "❌ Error: $($_.Exception.Message)" $Red
    exit 1
}