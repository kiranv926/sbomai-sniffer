#!/usr/bin/env pwsh

# SBOMAI Repository Analysis Script
# This script analyzes a repository and generates comprehensive SBOM reports

param(
    [Parameter(Mandatory=$true)]
    [string]$RepositoryUrl,
    
    [string]$Branch = "main",
    [string]$OutputDir = "repo-analysis",
    [switch]$GenerateSBOM,
    [switch]$AnalyzeVulnerabilities,
    [switch]$GenerateReport,
    [switch]$All
)

Write-Host "🔍 SBOMAI Repository Analysis" -ForegroundColor Green
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

# Function to check if SBOMAI services are running
function Test-SBOMAIServices {
    $services = @("sbomai-core", "sbomai-parser", "sbomai-vulnscan", "sbomai-policy")
    $running = 0
    
    foreach ($service in $services) {
        $status = docker ps --filter "name=$service" --format "{{.Status}}"
        if ($status) {
            $running++
        }
    }
    
    return $running -eq $services.Count
}

# Function to clone repository
function Clone-Repository {
    param([string]$Url, [string]$Branch, [string]$OutputDir)
    
    Write-Host " Cloning repository: $Url" -ForegroundColor Yellow
    
    try {
        # Create output directory
        if (Test-Path $OutputDir) {
            Remove-Item -Recurse -Force $OutputDir
        }
        New-Item -ItemType Directory -Path $OutputDir | Out-Null
        
        # Clone repository
        git clone -b $Branch $Url $OutputDir
        
        if (Test-Path "$OutputDir/.git") {
            Write-Host " Repository cloned successfully to $OutputDir" -ForegroundColor Green
            return $true
        } else {
            Write-Host " Failed to clone repository" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host " Error cloning repository: $_" -ForegroundColor Red
        return $false
    }
}

# Function to detect project type and generate SBOM
function Generate-SBOM {
    param([string]$RepoPath)
    
    Write-Host " Detecting project type and generating SBOM..." -ForegroundColor Yellow
    
    $sbomFiles = @()
    
    # Check for Maven project
    if (Test-Path "$RepoPath/pom.xml") {
        Write-Host " Detected Maven project" -ForegroundColor Cyan
        try {
            Push-Location $RepoPath
            mvn dependency:tree -DoutputType=dot -DoutputFile=dependencies.dot
            mvn dependency:tree -DoutputType=json -DoutputFile=dependencies.json
            
            # Convert to CycloneDX format
            if (Get-Command "cyclonedx-maven-plugin" -ErrorAction SilentlyContinue) {
                mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom
                if (Test-Path "target/bom.xml") {
                    $sbomFiles += "target/bom.xml"
                }
            }
            
            Pop-Location
        }
        catch {
            Write-Host " Maven SBOM generation failed: $_" -ForegroundColor Yellow
        }
    }
    
    # Check for Node.js project
    if (Test-Path "$RepoPath/package.json") {
        Write-Host " Detected Node.js project" -ForegroundColor Cyan
        try {
            Push-Location $RepoPath
            npm install
            
            # Generate audit report
            npm audit --json > audit-report.json
            
            # Try to generate SBOM with cyclonedx-npm
            if (Get-Command "cyclonedx-npm" -ErrorAction SilentlyContinue) {
                cyclonedx-npm --output-format json --output-file bom.json
                if (Test-Path "bom.json") {
                    $sbomFiles += "bom.json"
                }
            }
            
            Pop-Location
        }
        catch {
            Write-Host " Node.js SBOM generation failed: $_" -ForegroundColor Yellow
        }
    }
    
    # Check for Python project
    if (Test-Path "$RepoPath/requirements.txt" -or Test-Path "$RepoPath/pyproject.toml") {
        Write-Host " Detected Python project" -ForegroundColor Cyan
        try {
            Push-Location $RepoPath
            
            # Generate requirements with pip
            pip freeze > requirements-freeze.txt
            
            # Try to generate SBOM with cyclonedx-python
            if (Get-Command "cyclonedx-py" -ErrorAction SilentlyContinue) {
                cyclonedx-py --output-format json --output-file bom.json
                if (Test-Path "bom.json") {
                    $sbomFiles += "bom.json"
                }
            }
            
            Pop-Location
        }
        catch {
            Write-Host " Python SBOM generation failed: $_" -ForegroundColor Yellow
        }
    }
    
    # Check for Go project
    if (Test-Path "$RepoPath/go.mod") {
        Write-Host " Detected Go project" -ForegroundColor Cyan
        try {
            Push-Location $RepoPath
            
            # Generate go.mod.lock
            go mod download
            go mod tidy
            
            # Try to generate SBOM with cyclonedx-gomod
            if (Get-Command "cyclonedx-gomod" -ErrorAction SilentlyContinue) {
                cyclonedx-gomod mod --output-format json --output-file bom.json
                if (Test-Path "bom.json") {
                    $sbomFiles += "bom.json"
                }
            }
            
            Pop-Location
        }
        catch {
            Write-Host " Go SBOM generation failed: $_" -ForegroundColor Yellow
        }
    }
    
    return $sbomFiles
}

# Function to analyze SBOM with SBOMAI
function Analyze-SBOM {
    param([string]$RepoPath, [string]$OutputDir)
    
    Write-Host "🔍 Analyzing SBOM files with SBOMAI..." -ForegroundColor Yellow
    
    $sbomFiles = Get-ChildItem -Path $RepoPath -Recurse -Include "*.json", "*.xml", "bom.xml", "dependencies.json" | Where-Object { $_.Name -match "bom|dependencies|audit" }
    
    if ($sbomFiles.Count -eq 0) {
        Write-Host " No SBOM files found. Creating a basic dependency list..." -ForegroundColor Yellow
        
        # Create a basic SBOM from detected dependencies
        $basicSbom = @{
            bomFormat = "CycloneDX"
            specVersion = "1.4"
            version = 1
            metadata = @{
                timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
                tools = @(@{
                    vendor = "SBOMAI"
                    name = "SBOMAI-Generator"
                    version = "1.0.0"
                })
                component = @{
                    type = "application"
                    name = (Split-Path $RepoPath -Leaf)
                    version = "1.0.0"
                }
            }
            components = @()
        }
        
        # Add detected dependencies
        if (Test-Path "$RepoPath/requirements-freeze.txt") {
            Get-Content "$RepoPath/requirements-freeze.txt" | ForEach-Object {
                if ($_ -match "^([^=]+)==(.+)$") {
                    $basicSbom.components += @{
                        type = "library"
                        name = $matches[1]
                        version = $matches[2]
                        purl = "pkg:pypi/$($matches[1])@$($matches[2])"
                    }
                }
            }
        }
        
        $basicSbomPath = "$OutputDir/basic-sbom.json"
        $basicSbom | ConvertTo-Json -Depth 10 | Out-File $basicSbomPath
        $sbomFiles = @($basicSbomPath)
    }
    
    $analysisResults = @()
    
    foreach ($sbomFile in $sbomFiles) {
        Write-Host "Analyzing: $($sbomFile.Name)" -ForegroundColor Cyan
        
        try {
            # Copy SBOM file to container
            docker cp $sbomFile.FullName sbomai-cli:/app/sboms/
            
            # Analyze with SBOMAI
            $containerPath = "/app/sboms/$($sbomFile.Name)"
            $result = docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze $containerPath --output JSON --verbose
            
            # Save analysis result
            $resultFile = "$OutputDir/analysis-$($sbomFile.BaseName).json"
            $result | Out-File $resultFile
            
            $analysisResults += @{
                File = $sbomFile.Name
                Result = $resultFile
                Status = "Success"
            }
            
            Write-Host " Analysis completed for $($sbomFile.Name)" -ForegroundColor Green
        }
        catch {
            Write-Host " Analysis failed for $($sbomFile.Name): $_" -ForegroundColor Red
            $analysisResults += @{
                File = $sbomFile.Name
                Result = $null
                Status = "Failed"
                Error = $_.Exception.Message
            }
        }
    }
    
    return $analysisResults
}

# Function to generate comprehensive report
function Generate-ComprehensiveReport {
    param([string]$OutputDir, [array]$AnalysisResults, [string]$RepoPath)
    
    Write-Host " Generating comprehensive report..." -ForegroundColor Yellow
    
    $report = @{
        repository = @{
            url = $RepositoryUrl
            branch = $Branch
            name = (Split-Path $RepoPath -Leaf)
            analyzedAt = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
        }
        analysis = @{
            totalFiles = $AnalysisResults.Count
            successful = ($AnalysisResults | Where-Object { $_.Status -eq "Success" }).Count
            failed = ($AnalysisResults | Where-Object { $_.Status -eq "Failed" }).Count
            results = $AnalysisResults
        }
        summary = @{
            vulnerabilities = @{
                critical = 0
                high = 0
                medium = 0
                low = 0
            }
            policyViolations = 0
            recommendations = @()
        }
    }
    
    # Aggregate results from all analyses
    foreach ($result in $AnalysisResults) {
        if ($result.Status -eq "Success" -and $result.Result) {
            try {
                $analysisData = Get-Content $result.Result | ConvertFrom-Json
                
                # Aggregate vulnerability counts
                if ($analysisData.vulnerabilities) {
                    foreach ($vuln in $analysisData.vulnerabilities) {
                        switch ($vuln.severity.ToLower()) {
                            "critical" { $report.summary.vulnerabilities.critical++ }
                            "high" { $report.summary.vulnerabilities.high++ }
                            "medium" { $report.summary.vulnerabilities.medium++ }
                            "low" { $report.summary.vulnerabilities.low++ }
                        }
                    }
                }
                
                # Aggregate policy violations
                if ($analysisData.policyViolations) {
                    $report.summary.policyViolations += $analysisData.policyViolations.Count
                }
                
                # Add recommendations
                if ($analysisData.recommendations) {
                    $report.summary.recommendations += $analysisData.recommendations
                }
            }
            catch {
                Write-Host " Error processing analysis result: $_" -ForegroundColor Yellow
            }
        }
    }
    
    # Generate HTML report
    $htmlReport = @"
<!DOCTYPE html>
<html>
<head>
    <title>SBOMAI Analysis Report - $($report.repository.name)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background: #f5f5f5; padding: 20px; border-radius: 5px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric { background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }
        .critical { color: #d32f2f; }
        .high { color: #f57c00; }
        .medium { color: #fbc02d; }
        .low { color: #388e3c; }
        .vulnerabilities { margin: 20px 0; }
        .recommendations { background: #e3f2fd; padding: 20px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 SBOMAI Analysis Report</h1>
        <p><strong>Repository:</strong> $($report.repository.name)</p>
        <p><strong>URL:</strong> $($report.repository.url)</p>
        <p><strong>Analyzed:</strong> $($report.repository.analyzedAt)</p>
    </div>
    
    <div class="summary">
        <div class="metric">
            <h3>Total Files</h3>
            <h2>$($report.analysis.totalFiles)</h2>
        </div>
        <div class="metric">
            <h3>Successful</h3>
            <h2>$($report.analysis.successful)</h2>
        </div>
        <div class="metric">
            <h3>Failed</h3>
            <h2>$($report.analysis.failed)</h2>
        </div>
    </div>
    
    <div class="vulnerabilities">
        <h2>Vulnerability Summary</h2>
        <div class="summary">
            <div class="metric critical">
                <h3>Critical</h3>
                <h2>$($report.summary.vulnerabilities.critical)</h2>
            </div>
            <div class="metric high">
                <h3>High</h3>
                <h2>$($report.summary.vulnerabilities.high)</h2>
            </div>
            <div class="metric medium">
                <h3>Medium</h3>
                <h2>$($report.summary.vulnerabilities.medium)</h2>
            </div>
            <div class="metric low">
                <h3>Low</h3>
                <h2>$($report.summary.vulnerabilities.low)</h2>
            </div>
        </div>
    </div>
    
    <div class="recommendations">
        <h2>Recommendations</h2>
        <ul>
"@
    
    foreach ($rec in $report.summary.recommendations) {
        $htmlReport += "<li>$rec</li>`n"
    }
    
    $htmlReport += @"
        </ul>
    </div>
    
    <div>
        <h2>Detailed Results</h2>
        <ul>
"@
    
    foreach ($result in $AnalysisResults) {
        $htmlReport += "<li><strong>$($result.File):</strong> $($result.Status)</li>`n"
    }
    
    $htmlReport += @"
        </ul>
    </div>
</body>
</html>
"@
    
    # Save reports
    $report | ConvertTo-Json -Depth 10 | Out-File "$OutputDir/comprehensive-report.json"
    $htmlReport | Out-File "$OutputDir/comprehensive-report.html"
    
    Write-Host " Comprehensive report generated:" -ForegroundColor Green
    Write-Host "   JSON: $OutputDir/comprehensive-report.json" -ForegroundColor Cyan
    Write-Host "   HTML: $OutputDir/comprehensive-report.html" -ForegroundColor Cyan
}

# Main execution
if (-not (Test-Docker)) {
    exit 1
}

if (-not (Test-SBOMAIServices)) {
    Write-Host " SBOMAI services are not running. Please start them first with: .\start-sbomai.ps1" -ForegroundColor Red
    exit 1
}

# Clone repository
$repoName = ($RepositoryUrl -split "/")[-1] -replace "\.git$", ""
$repoPath = "$OutputDir/$repoName"

if (-not (Clone-Repository -Url $RepositoryUrl -Branch $Branch -OutputDir $OutputDir)) {
    exit 1
}

$sbomFiles = @()

if ($All -or $GenerateSBOM) {
    $sbomFiles = Generate-SBOM -RepoPath $repoPath
}

$analysisResults = @()

if ($All -or $AnalyzeVulnerabilities) {
    $analysisResults = Analyze-SBOM -RepoPath $repoPath -OutputDir $OutputDir
}

if ($All -or $GenerateReport) {
    Generate-ComprehensiveReport -OutputDir $OutputDir -AnalysisResults $analysisResults -RepoPath $repoPath
}

Write-Host "`n Repository analysis completed!" -ForegroundColor Green
Write-Host " Results saved in: $OutputDir" -ForegroundColor Cyan 