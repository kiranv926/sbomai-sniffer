#!/usr/bin/env pwsh

# SBOMAI Testing Script
# This script automates the testing process for the SBOMAI project

param(
    [switch]$StartServices,
    [switch]$TestCLI,
    [switch]$TestAPI,
    [switch]$TestMetrics,
    [switch]$GenerateReports,
    [switch]$All
)

Write-Host " SBOMAI Testing Script" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Function to check if Docker is running
function Test-Docker {
    try {
        docker version | Out-Null
        return $true
    }
    catch {
        Write-Host " Docker is not running. Please start Docker Desktop." -ForegroundColor Red
        return $false
    }
}

# Function to check if services are running
function Test-Services {
    Write-Host " Checking service status..." -ForegroundColor Yellow
    
    $services = @("sbomai-core", "sbomai-parser", "sbomai-vulnscan", "sbomai-policy", "sbomai-cli", "grafana", "prometheus")
    $running = 0
    
    foreach ($service in $services) {
        $status = docker ps --filter "name=$service" --format "{{.Status}}"
        if ($status) {
            Write-Host " $service is running" -ForegroundColor Green
            $running++
        } else {
            Write-Host " $service is not running" -ForegroundColor Red
        }
    }
    
    return $running -eq $services.Count
}

# Function to start services
function Start-SBOMAIServices {
    Write-Host " Starting SBOMAI services..." -ForegroundColor Yellow
    
    if (-not (Test-Docker)) {
        return $false
    }
    
    try {
        docker-compose up -d
        Write-Host " Waiting for services to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        
        if (Test-Services) {
            Write-Host " All services started successfully!" -ForegroundColor Green
            return $true
        } else {
            Write-Host " Some services may not be fully started. Check logs with: docker-compose logs" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host " Failed to start services: $_" -ForegroundColor Red
        return $false
    }
}

# Function to test CLI
function Test-CLI {
    Write-Host " Testing CLI functionality..." -ForegroundColor Yellow
    
    try {
        # Test help command
        Write-Host "Testing help command..." -ForegroundColor Cyan
        docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar --help
        
        # Test analyze command with SPDX sample
        Write-Host "Testing SPDX analysis..." -ForegroundColor Cyan
        docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json --format SPDX --output TEXT
        
        # Test analyze command with CycloneDX sample
        Write-Host "Testing CycloneDX analysis..." -ForegroundColor Cyan
        docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/cyclonedx-sample.json --format CYCLONEDX --output JSON
        
        Write-Host " CLI tests completed successfully!" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host " CLI test failed: $_" -ForegroundColor Red
        return $false
    }
}

# Function to test API endpoints
function Test-API {
    Write-Host " Testing API endpoints..." -ForegroundColor Yellow
    
    $endpoints = @(
        @{Service="Core"; URL="http://localhost:8080/actuator/health"},
        @{Service="Parser"; URL="http://localhost:8081/actuator/health"},
        @{Service="VulnScan"; URL="http://localhost:8082/actuator/health"},
        @{Service="Policy"; URL="http://localhost:8083/actuator/health"}
    )
    
    $success = 0
    
    foreach ($endpoint in $endpoints) {
        try {
            $response = Invoke-RestMethod -Uri $endpoint.URL -Method Get -TimeoutSec 10
            Write-Host " $($endpoint.Service) API is healthy" -ForegroundColor Green
            $success++
        }
        catch {
            Write-Host " $($endpoint.Service) API is not responding" -ForegroundColor Red
        }
    }
    
    if ($success -eq $endpoints.Count) {
        Write-Host " All API endpoints are healthy!" -ForegroundColor Green
        return $true
    } else {
        Write-Host " Some API endpoints are not responding" -ForegroundColor Yellow
        return $false
    }
}

# Function to test metrics
function Test-Metrics {
    Write-Host " Testing metrics collection..." -ForegroundColor Yellow
    
    try {
        # Test Prometheus metrics endpoint
        Write-Host "Testing Prometheus metrics..." -ForegroundColor Cyan
        $metrics = Invoke-RestMethod -Uri "http://localhost:8080/actuator/prometheus" -Method Get
        if ($metrics -match "sbomai") {
            Write-Host " SBOMAI metrics are being collected" -ForegroundColor Green
        } else {
            Write-Host " No SBOMAI metrics found" -ForegroundColor Yellow
        }
        
        # Test Grafana accessibility
        Write-Host "Testing Grafana accessibility..." -ForegroundColor Cyan
        $grafana = Invoke-RestMethod -Uri "http://localhost:3000/api/health" -Method Get
        Write-Host " Grafana is accessible" -ForegroundColor Green
        
        Write-Host " Metrics tests completed!" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host " Metrics test failed: $_" -ForegroundColor Red
        return $false
    }
}

# Function to generate reports
function Generate-Reports {
    Write-Host " Generating test reports..." -ForegroundColor Yellow
    
    try {
        # Create reports directory if it doesn't exist
        if (-not (Test-Path "reports")) {
            New-Item -ItemType Directory -Path "reports" | Out-Null
        }
        
        # Generate JSON report
        Write-Host "Generating JSON report..." -ForegroundColor Cyan
        docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json --output JSON > reports/test-report-spdx.json
        
        # Generate HTML report
        Write-Host "Generating HTML report..." -ForegroundColor Cyan
        docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/cyclonedx-sample.json --output HTML > reports/test-report-cyclonedx.html
        
        # Export Prometheus metrics
        Write-Host "Exporting Prometheus metrics..." -ForegroundColor Cyan
        Invoke-RestMethod -Uri "http://localhost:9090/api/v1/export" -Method Get > reports/metrics-export.json
        
        Write-Host " Reports generated in reports/ directory!" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host " Report generation failed: $_" -ForegroundColor Red
        return $false
    }
}

# Function to display access information
function Show-AccessInfo {
    Write-Host "`n Access Information" -ForegroundColor Green
    Write-Host "===================" -ForegroundColor Green
    Write-Host "Grafana Dashboard: http://localhost:3000 (admin/sbomai2024)" -ForegroundColor Cyan
    Write-Host "Prometheus: http://localhost:9090" -ForegroundColor Cyan
    Write-Host "Loki: http://localhost:3100" -ForegroundColor Cyan
    Write-Host "Alertmanager: http://localhost:9093" -ForegroundColor Cyan
    Write-Host "Core API: http://localhost:8080" -ForegroundColor Cyan
    Write-Host "Parser API: http://localhost:8081" -ForegroundColor Cyan
    Write-Host "VulnScan API: http://localhost:8082" -ForegroundColor Cyan
    Write-Host "Policy API: http://localhost:8083" -ForegroundColor Cyan
}

# Main execution logic
if ($All -or $StartServices) {
    if (Start-SBOMAIServices) {
        Show-AccessInfo
    } else {
        Write-Host " Failed to start services. Check Docker and try again." -ForegroundColor Red
        exit 1
    }
}

if ($All -or $TestCLI) {
    if (-not (Test-Services)) {
        Write-Host " Services are not running. Use -StartServices first." -ForegroundColor Red
        exit 1
    }
    Test-CLI
}

if ($All -or $TestAPI) {
    if (-not (Test-Services)) {
        Write-Host " Services are not running. Use -StartServices first." -ForegroundColor Red
        exit 1
    }
    Test-API
}

if ($All -or $TestMetrics) {
    if (-not (Test-Services)) {
        Write-Host " Services are not running. Use -StartServices first." -ForegroundColor Red
        exit 1
    }
    Test-Metrics
}

if ($All -or $GenerateReports) {
    if (-not (Test-Services)) {
        Write-Host " Services are not running. Use -StartServices first." -ForegroundColor Red
        exit 1
    }
    Generate-Reports
}

if (-not ($StartServices -or $TestCLI -or $TestAPI -or $TestMetrics -or $GenerateReports -or $All)) {
    Write-Host "Usage: .\test-sbomai.ps1 [options]" -ForegroundColor Yellow
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -StartServices    Start all SBOMAI services" -ForegroundColor Cyan
    Write-Host "  -TestCLI          Test CLI functionality" -ForegroundColor Cyan
    Write-Host "  -TestAPI          Test API endpoints" -ForegroundColor Cyan
    Write-Host "  -TestMetrics      Test metrics collection" -ForegroundColor Cyan
    Write-Host "  -GenerateReports  Generate test reports" -ForegroundColor Cyan
    Write-Host "  -All              Run all tests" -ForegroundColor Cyan
    Write-Host "`nExample: .\test-sbomai.ps1 -All" -ForegroundColor Green
}

Write-Host "`n Testing completed!" -ForegroundColor Green 