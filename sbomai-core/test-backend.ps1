# Test Backend API Endpoints
Write-Host "Testing SBOMAI Core Backend API..." -ForegroundColor Green

# Wait for backend to start
Write-Host "Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Test health endpoint
Write-Host "`n1. Testing health endpoint..." -ForegroundColor Cyan
try {
    $healthResponse = Invoke-WebRequest -Uri "http://localhost:8081/actuator/health" -Method GET -TimeoutSec 10
    Write-Host "Health endpoint: ✅ SUCCESS" -ForegroundColor Green
    Write-Host "Response: $($healthResponse.Content)" -ForegroundColor Gray
} catch {
    Write-Host "Health endpoint: ❌ FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

# Test AI model health endpoint
Write-Host "`n2. Testing AI model health endpoint..." -ForegroundColor Cyan
try {
    $aiHealthResponse = Invoke-WebRequest -Uri "http://localhost:8081/api/v1/ai/enhanced/model-health" -Method GET -TimeoutSec 10
    Write-Host "AI Model Health endpoint: ✅ SUCCESS" -ForegroundColor Green
    Write-Host "Response: $($aiHealthResponse.Content)" -ForegroundColor Gray
} catch {
    Write-Host "AI Model Health endpoint: ❌ FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

# Test AI model status endpoint
Write-Host "`n3. Testing AI model status endpoint..." -ForegroundColor Cyan
try {
    $aiStatusResponse = Invoke-WebRequest -Uri "http://localhost:8081/api/v1/ai/enhanced/model-status" -Method GET -TimeoutSec 10
    Write-Host "AI Model Status endpoint: ✅ SUCCESS" -ForegroundColor Green
    Write-Host "Response: $($aiStatusResponse.Content)" -ForegroundColor Gray
} catch {
    Write-Host "AI Model Status endpoint: ❌ FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

# Test dashboard insights endpoint
Write-Host "`n4. Testing dashboard insights endpoint..." -ForegroundColor Cyan
try {
    $insightsResponse = Invoke-WebRequest -Uri "http://localhost:8081/api/v1/ai/enhanced/dashboard-insights" -Method GET -TimeoutSec 10
    Write-Host "Dashboard Insights endpoint: ✅ SUCCESS" -ForegroundColor Green
    Write-Host "Response: $($insightsResponse.Content)" -ForegroundColor Gray
} catch {
    Write-Host "Dashboard Insights endpoint: ❌ FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

# Test security insights endpoint
Write-Host "`n5. Testing security insights endpoint..." -ForegroundColor Cyan
try {
    $securityResponse = Invoke-WebRequest -Uri "http://localhost:8081/api/v1/ai/enhanced/security-insights" -Method GET -TimeoutSec 10
    Write-Host "Security Insights endpoint: ✅ SUCCESS" -ForegroundColor Green
    Write-Host "Response: $($securityResponse.Content)" -ForegroundColor Gray
} catch {
    Write-Host "Security Insights endpoint: ❌ FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

# Test portfolio recommendations endpoint
Write-Host "`n6. Testing portfolio recommendations endpoint..." -ForegroundColor Cyan
try {
    $recommendationsResponse = Invoke-WebRequest -Uri "http://localhost:8081/api/v1/ai/enhanced/recommendations/portfolio" -Method GET -TimeoutSec 10
    Write-Host "Portfolio Recommendations endpoint: ✅ SUCCESS" -ForegroundColor Green
    Write-Host "Response: $($recommendationsResponse.Content)" -ForegroundColor Gray
} catch {
    Write-Host "Portfolio Recommendations endpoint: ❌ FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nBackend API testing completed!" -ForegroundColor Green 