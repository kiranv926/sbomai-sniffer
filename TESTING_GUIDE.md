# SBOMAI Testing & Reporting Guide

This guide provides comprehensive instructions for testing the SBOMAI project, analyzing repositories, and generating detailed reports with metrics.

## 🎯 Overview

SBOMAI is a modular Java project for AI-powered SBOM analysis with the following capabilities:
- **SBOM Parsing**: Parse SPDX, CycloneDX, and SWID formats
- **Vulnerability Scanning**: Scan against NVD, OSS Index, OSV databases
- **AI Analysis**: Predictive risk scoring using ML/LLM models
- **Policy Enforcement**: Custom rules for CVSS thresholds and license compliance
- **Real-time Monitoring**: Grafana dashboards with Prometheus metrics
- **CLI Interface**: Command-line tool for local and remote analysis

## 🚀 Quick Start

### 1. Start the Complete SBOMAI Stack

```bash
# Using the provided PowerShell script (Windows)
.\start-sbomai.ps1

# Or manually with Docker Compose
docker-compose up -d
```

This starts:
- **Java Services**: sbomai-parser, sbomai-vulnscan, sbomai-policy, sbomai-core, sbomai-cli
- **Monitoring Stack**: Grafana, Prometheus, Loki, Alertmanager, Redis, Nginx
- **System Monitoring**: Node Exporter, cAdvisor

### 2. Verify Services are Running

```bash
# Check all containers
docker-compose ps

# Check specific service logs
docker-compose logs sbomai-core
docker-compose logs grafana
```

### 3. Access Monitoring Dashboards

- **Grafana**: http://localhost:3000 (admin/sbomai2024)
- **Prometheus**: http://localhost:9090
- **Loki**: http://localhost:3100
- **Alertmanager**: http://localhost:9093

## 📋 Testing Scenarios

### Scenario 1: Analyze Sample SBOM Files

The project includes sample SBOM files for testing:

```bash
# Analyze SPDX sample
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json --format SPDX --output JSON

# Analyze CycloneDX sample
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/cyclonedx-sample.json --format CYCLONEDX --output HTML
```

### Scenario 2: Test Individual Services

#### Test Parser Service
```bash
# Check parser health
curl http://localhost:8081/actuator/health

# Parse SBOM via REST API
curl -X POST http://localhost:8081/api/v1/parse \
  -H "Content-Type: application/json" \
  -d @sample-sboms/spdx-sample.json
```

#### Test Vulnerability Scanner
```bash
# Check scanner health
curl http://localhost:8082/actuator/health

# Scan components for vulnerabilities
curl -X POST http://localhost:8082/api/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"components":[{"name":"log4j-core","version":"2.17.1"}]}'
```

#### Test Policy Service
```bash
# Check policy service health
curl http://localhost:8083/actuator/health

# Check policy violations
curl -X POST http://localhost:8083/api/v1/enforce \
  -H "Content-Type: application/json" \
  -d @sample-sboms/cyclonedx-sample.json
```

#### Test Core Service
```bash
# Check core service health
curl http://localhost:8080/actuator/health

# Full analysis via core service
curl -X POST http://localhost:8080/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d @sample-sboms/spdx-sample.json
```

### Scenario 3: CLI Testing

#### Local Analysis
```bash
# Analyze with local processing
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json --verbose
```

#### Remote Analysis
```bash
# Analyze using remote core service
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/cyclonedx-sample.json --remote --url http://sbomai-core:8080
```

#### Different Output Formats
```bash
# JSON output
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json --output JSON

# HTML report
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/cyclonedx-sample.json --output HTML

# Text output
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json --output TEXT
```

### Scenario 4: Performance Testing

#### Load Testing
```bash
# Run multiple analyses concurrently
for i in {1..10}; do
  docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json &
done
wait
```

#### Monitor Performance Metrics
1. Open Grafana: http://localhost:3000
2. Navigate to "SBOMAI Overview" dashboard
3. Monitor:
   - SBOM Files Parsed per Minute
   - CVEs Found per Minute
   - 95th Percentile Scan Duration
   - Success Rate

## 📊 Metrics and Monitoring

### Key Metrics to Monitor

#### SBOM Parsing Metrics
- **Files parsed per minute**: `sbomai_parser_files_parsed_total`
- **Parse time per file**: `sbomai_parser_parse_duration_seconds`
- **Parser errors**: `sbomai_parser_errors_total`
- **Format distribution**: SPDX vs CycloneDX vs SWID

#### Vulnerability Scanning Metrics
- **Total CVEs found**: `sbomai_vulnscan_cves_found_total`
- **CVEs by severity**: Critical, High, Medium, Low
- **Scan duration per package**: `sbomai_vulnscan_scan_duration_seconds`
- **CVE source breakdown**: NVD, OSS Index, OSV

#### AI Analysis Metrics
- **Risk score predictions**: `sbomai_ai_risk_score_predictions_total`
- **Model confidence intervals**: `sbomai_ai_confidence_score`
- **Prediction accuracy**: `sbomai_ai_prediction_accuracy`

#### Policy Enforcement Metrics
- **Policy violations**: `sbomai_policy_violations_total`
- **Blocked builds**: `sbomai_policy_builds_blocked_total`
- **Rule hit count**: `sbomai_policy_rule_hits_total`

### Grafana Dashboard Queries

#### SBOM Parsing Rate
```promql
rate(sbomai_parser_files_parsed_total[5m])
```

#### CVE Severity Distribution
```promql
sum by (severity) (sbomai_vulnscan_cves_found_total)
```

#### Average Scan Duration
```promql
histogram_quantile(0.95, rate(sbomai_vulnscan_scan_duration_seconds_bucket[5m]))
```

#### Policy Violation Rate
```promql
rate(sbomai_policy_violations_total[5m])
```

## 📈 Report Generation

### 1. Automated Reports

Reports are automatically generated in the `reports/` directory:

```bash
# Check generated reports
ls -la reports/

# View latest report
cat reports/latest-analysis-report.json
```

### 2. Custom Report Formats

#### JSON Report
```bash
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json --output JSON > reports/custom-report.json
```

#### HTML Report
```bash
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/cyclonedx-sample.json --output HTML > reports/custom-report.html
```

### 3. Grafana Dashboard Export

Export dashboards as PDF or PNG:

1. Open Grafana: http://localhost:3000
2. Navigate to desired dashboard
3. Click "Share" button
4. Select "Export PDF" or "Export PNG"
5. Download the report

### 4. Prometheus Metrics Export

Export metrics for external analysis:

```bash
# Export current metrics
curl http://localhost:9090/api/v1/export > metrics-export.json

# Export metrics for specific time range
curl "http://localhost:9090/api/v1/export?start=2024-01-01T00:00:00Z&end=2024-01-02T00:00:00Z" > metrics-range.json
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Services Not Starting
```bash
# Check Docker logs
docker-compose logs sbomai-core
docker-compose logs sbomai-parser

# Check service health
curl http://localhost:8080/actuator/health
```

#### 2. Build Failures
```bash
# Clean and rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### 3. Metrics Not Appearing
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check metrics endpoint
curl http://localhost:8080/actuator/prometheus
```

#### 4. Dashboard Not Loading
```bash
# Check Grafana logs
docker-compose logs grafana

# Verify datasource configuration
curl http://localhost:3000/api/datasources
```

### Debug Commands

#### Check Service Status
```bash
# All services
docker-compose ps

# Specific service logs
docker-compose logs -f sbomai-core
```

#### Check Network Connectivity
```bash
# Test inter-service communication
docker exec -it sbomai-core curl http://sbomai-parser:8080/actuator/health
docker exec -it sbomai-core curl http://sbomai-vulnscan:8080/actuator/health
```

#### Check Metrics Endpoints
```bash
# Core service metrics
curl http://localhost:8080/actuator/prometheus | grep sbomai

# Parser service metrics
curl http://localhost:8081/actuator/prometheus | grep sbomai
```

## 🎯 Advanced Testing

### 1. Repository Analysis

To analyze a real repository:

```bash
# Clone a repository
git clone https://github.com/example/repo.git
cd repo

# Generate SBOM (if not present)
# For Maven projects
mvn dependency:tree -DoutputType=dot -DoutputFile=dependencies.dot

# For Node.js projects
npm audit --json > audit-report.json

# Analyze with SBOMAI
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /path/to/sbom.json
```

### 2. Continuous Integration Testing

Create a CI pipeline:

```yaml
# .github/workflows/sbomai-analysis.yml
name: SBOMAI Analysis
on: [push, pull_request]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Start SBOMAI
        run: docker-compose up -d
      - name: Wait for services
        run: sleep 30
      - name: Analyze SBOM
        run: |
          docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: sbomai-report
          path: reports/
```

### 3. Performance Benchmarking

```bash
# Benchmark parsing performance
time docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json

# Load test with multiple files
for file in /app/sboms/*.json; do
  echo "Analyzing $file"
  time docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze "$file"
done
```

## 📚 Additional Resources

- **Monitoring Setup**: See `MONITORING_SETUP.md`
- **API Documentation**: Check individual service endpoints
- **Sample SBOMs**: Located in `sample-sboms/` directory
- **Configuration**: Check `application.yml` files in each module

## 🎉 Success Criteria

A successful test run should show:

1. ✅ All services start without errors
2. ✅ Sample SBOM files are parsed successfully
3. ✅ Vulnerabilities are detected and categorized
4. ✅ Policy violations are identified
5. ✅ AI analysis provides risk scores
6. ✅ Metrics are collected in Prometheus
7. ✅ Dashboards display data in Grafana
8. ✅ Reports are generated in multiple formats
9. ✅ CLI commands execute successfully
10. ✅ All health endpoints return healthy status

This comprehensive testing approach ensures the SBOMAI system is working correctly and provides valuable insights into your software supply chain security. 