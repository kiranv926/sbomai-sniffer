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

# SBOMAI Service Startup Script
# This script starts all SBOMAI services in the correct order

# Stop on first error
$ErrorActionPreference = "Stop"

# Function to check if a service is healthy
function Test-ServiceHealth {
    param (
        [string]$ServiceName,
        [string]$Url,
        [int]$MaxAttempts = 30,
        [int]$DelaySeconds = 2
    )
    
    Write-Host "Checking health of $ServiceName..."
    $attempts = 0
    
    while ($attempts -lt $MaxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri $Url -Method GET -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ $ServiceName is healthy"
                return $true
            }
        }
        catch {
            $attempts++
            if ($attempts -eq $MaxAttempts) {
                Write-Host "❌ $ServiceName health check failed after $MaxAttempts attempts"
                return $false
            }
            Write-Host "⏳ Waiting for $ServiceName to become healthy (attempt $attempts/$MaxAttempts)..."
            Start-Sleep -Seconds $DelaySeconds
        }
    }
    return $false
}

# Function to check if Docker is running
function Test-DockerRunning {
    try {
        $dockerInfo = docker info 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

# Check if Docker is running
if (-not (Test-DockerRunning)) {
    Write-Host "❌ Docker is not running. Please start Docker and try again."
    exit 1
}

# Check if .env file exists
if (-not (Test-Path .env)) {
    Write-Host "❌ .env file not found. Please create one from .env.example"
    exit 1
}

# Create required directories
$directories = @(
    "logs",
    "monitoring/prometheus",
    "monitoring/grafana/provisioning/datasources",
    "monitoring/grafana/provisioning/dashboards",
    "monitoring/grafana/dashboards",
    "monitoring/loki",
    "monitoring/promtail"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "📁 Created directory: $dir"
    }
}

# Build all Java services
Write-Host "🔨 Building Java services..."
try {
    mvn clean install -DskipTests
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Maven build failed"
        exit 1
    }
}
catch {
    Write-Host "❌ Maven build failed: $_"
    exit 1
}

# Build AI/ML Engine
Write-Host "🔨 Building AI/ML Engine..."
Set-Location sbomai-engine
try {
    python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Python dependencies installation failed"
        exit 1
    }
    
    # Generate gRPC code
    python -m grpc_tools.protoc `
        --python_out=./src `
        --grpc_python_out=./src `
        --proto_path=./protos `
        ./protos/sbomai_ai.proto
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ gRPC code generation failed"
        exit 1
    }
}
catch {
    Write-Host "❌ AI Engine build failed: $_"
    exit 1
}
Set-Location ..

# Start services with Docker Compose
Write-Host "🚀 Starting services..."
try {
    docker-compose up -d
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Docker Compose failed"
        exit 1
    }
}
catch {
    Write-Host "❌ Docker Compose failed: $_"
    exit 1
}

# Check service health
$services = @{
    "API Gateway" = "http://localhost:8080/actuator/health"
    "Core Service" = "http://localhost:8081/actuator/health"
    "Storage Service" = "http://localhost:8082/actuator/health"
    "Integrations Service" = "http://localhost:8083/actuator/health"
    "Engine Metrics" = "http://localhost:9090/health"
    "Prometheus" = "http://localhost:9091/-/healthy"
    "Grafana" = "http://localhost:3000/api/health"
    "Loki" = "http://localhost:3100/ready"
    "MinIO" = "http://localhost:9000/minio/health/live"
}

$allHealthy = $true
foreach ($service in $services.GetEnumerator()) {
    if (-not (Test-ServiceHealth -ServiceName $service.Key -Url $service.Value)) {
        $allHealthy = $false
    }
}

if ($allHealthy) {
    Write-Host "`n✨ All services are running and healthy!"
    Write-Host "`n📊 Service URLs:"
    Write-Host "- API Gateway: http://localhost:8080"
    Write-Host "- Grafana: http://localhost:3000 (admin/sbomai2024)"
    Write-Host "- Prometheus: http://localhost:9091"
    Write-Host "- MinIO Console: http://localhost:9001"
}
else {
    Write-Host "`n⚠️ Some services failed health checks. Please check the logs:"
    Write-Host "docker-compose logs -f"
}

# Optional: Open browser tabs
$openBrowser = Read-Host "`nWould you like to open service URLs in your browser? (y/n)"
if ($openBrowser -eq "y") {
    Start-Process "http://localhost:8080"
    Start-Process "http://localhost:3000"
    Start-Process "http://localhost:9091"
    Start-Process "http://localhost:9001"
}