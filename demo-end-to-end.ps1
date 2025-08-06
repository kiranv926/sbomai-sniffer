# SBOMAI End-to-End Pipeline Demonstration
# This script demonstrates the complete SBOMAI pipeline:
# 1. Go Parser scanning a repository
# 2. Python AI Engine analysis
# 3. Infrastructure integration (PostgreSQL, Kafka)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SBOMAI END-TO-END PIPELINE DEMONSTRATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check infrastructure status
Write-Host "Step 1: Checking Infrastructure Status..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "Step 2: Scanning Apache Kafka Repository..." -ForegroundColor Yellow

# Navigate to Go parser directory
Set-Location "..\sbomai-parser-go"

# Scan the Kafka repository
.\sbomai-parser.exe scan kafka-repo -o kafka-demo-sbom.json

Write-Host ""
Write-Host "Step 3: Running AI Analysis..." -ForegroundColor Yellow

# Copy SBOM to Python engine
Copy-Item kafka-demo-sbom.json ..\sbomai-engine\

# Navigate to Python engine and run analysis
Set-Location "..\sbomai-engine"
python integrate_go_parser.py kafka-demo-sbom.json

Write-Host ""
Write-Host "Step 4: Infrastructure Integration Demo..." -ForegroundColor Yellow

# Show how the data would be stored in PostgreSQL
Write-Host "PostgreSQL Database: localhost:5432" -ForegroundColor Green
Write-Host "pgAdmin UI: http://localhost:8082 (admin@sbomai.com / admin)" -ForegroundColor Green
Write-Host "Kafka UI: http://localhost:8080" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5: Sample Data Structure..." -ForegroundColor Yellow

# Show sample of the generated SBOM
Write-Host "SBOM Components Found:" -ForegroundColor Green
$sbomContent = Get-Content kafka-demo-sbom.json | ConvertFrom-Json
Write-Host "Total Components: $($sbomContent.components.Count)" -ForegroundColor Green
Write-Host "SBOM Format: $($sbomContent.bomFormat)" -ForegroundColor Green
Write-Host "SBOM Version: $($sbomContent.specVersion)" -ForegroundColor Green

Write-Host ""
Write-Host "Sample Components:" -ForegroundColor Green
$sbomContent.components | Select-Object -First 5 | ForEach-Object {
    Write-Host "  - $($_.name)@$($_.version) ($($_.type))" -ForegroundColor White
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "DEMONSTRATION COMPLETED SUCCESSFULLY!" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Access pgAdmin at http://localhost:8082 to view database" -ForegroundColor White
Write-Host "2. Access Kafka UI at http://localhost:8080 to view messages" -ForegroundColor White
Write-Host "3. Review the analysis report: sbomai_analysis_report.json" -ForegroundColor White
Write-Host "4. Integrate with Java orchestrator (sbomai-core) for full automation" -ForegroundColor White
Write-Host "" 