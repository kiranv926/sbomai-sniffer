# Test Encoding Fix
Write-Host "Testing Encoding Fix..." -ForegroundColor Green

# Check if backend is running
Write-Host "`n1. Checking Backend Status..." -ForegroundColor Cyan
try {
    $healthResponse = Invoke-WebRequest -Uri "http://localhost:8081/actuator/health" -Method GET -TimeoutSec 5
    Write-Host "✅ Backend is running on port 8081" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend is not running on port 8081" -ForegroundColor Red
    Write-Host "   Please start the backend with: cd sbomai-core && mvn spring-boot:run" -ForegroundColor Yellow
}

# Check UI files for encoding issues
Write-Host "`n2. Checking UI Files for Encoding Issues..." -ForegroundColor Cyan

$uiFiles = @(
    "../sbomai-ui/src/api/client.ts",
    "../sbomai-ui/src/api/services/projects.ts",
    "../sbomai-ui/src/api/services/ai.ts",
    "../sbomai-ui/src/api/services/scans.ts",
    "../sbomai-ui/src/api/services/vulnerabilities.ts",
    "../sbomai-ui/src/hooks/useApi.ts"
)

$encodingIssues = 0

foreach ($file in $uiFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw -Encoding UTF8
        if ($content -match "") {
            Write-Host "❌ Encoding issue found in: $file" -ForegroundColor Red
            $encodingIssues++
        } else {
            Write-Host "✅ No encoding issues in: $file" -ForegroundColor Green
        }
    } else {
        Write-Host "⚠️  File not found: $file" -ForegroundColor Yellow
    }
}

if ($encodingIssues -eq 0) {
    Write-Host "`n✅ All encoding issues have been resolved!" -ForegroundColor Green
} else {
    Write-Host "`n❌ $encodingIssues encoding issues still remain" -ForegroundColor Red
}

# Test API endpoints
Write-Host "`n3. Testing API Endpoints..." -ForegroundColor Cyan

$endpoints = @(
    "http://localhost:8081/ai/enhanced/model-health",
    "http://localhost:8081/ai/enhanced/dashboard-insights",
    "http://localhost:8081/ai/enhanced/security-insights",
    "http://localhost:8081/ai/enhanced/recommendations/portfolio"
)

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri $endpoint -Method GET -TimeoutSec 5
        Write-Host "✅ $endpoint - SUCCESS" -ForegroundColor Green
    } catch {
        Write-Host "❌ $endpoint - FAILED" -ForegroundColor Red
    }
}

Write-Host "`n🎉 Encoding fix test completed!" -ForegroundColor Green
Write-Host "The UI should now compile without encoding errors." -ForegroundColor Yellow 