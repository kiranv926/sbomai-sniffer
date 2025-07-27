# SBOMAI - AI-Powered SBOM Analysis Tool

SBOMAI is a modular Java project for AI-powered Software Bill of Materials (SBOM) analysis, providing comprehensive vulnerability scanning, policy enforcement, and predictive risk analysis.

## 🚀 Quick Start

### Prerequisites
- Java 21
- Docker & Docker Compose
- Maven 3.8+

### Start the Complete Stack

```bash
# Using PowerShell script (Windows)
.\start-sbomai.ps1

# Or manually
docker-compose up -d
```

### Access Services
- **Grafana Dashboard**: http://localhost:3000 (admin/sbomai2024)
- **Prometheus**: http://localhost:9090
- **Core API**: http://localhost:8080
- **Parser API**: http://localhost:8081
- **VulnScan API**: http://localhost:8082
- **Policy API**: http://localhost:8083

## 📋 Testing & Analysis

### Test the System

```bash
# Run comprehensive tests
.\test-sbomai.ps1 -All

# Or test individual components
.\test-sbomai.ps1 -StartServices
.\test-sbomai.ps1 -TestCLI
.\test-sbomai.ps1 -TestAPI
.\test-sbomai.ps1 -TestMetrics
.\test-sbomai.ps1 -GenerateReports
```

### Analyze Sample SBOMs

```bash
# Analyze SPDX sample
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/spdx-sample.json --format SPDX --output JSON

# Analyze CycloneDX sample
docker exec -it sbomai-cli java -jar sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /app/sboms/cyclonedx-sample.json --format CYCLONEDX --output HTML
```

### Analyze a Repository

```bash
# Analyze a GitHub repository
.\analyze-repo.ps1 -RepositoryUrl "https://github.com/example/repo.git" -All

# Generate SBOM and analyze vulnerabilities
.\analyze-repo.ps1 -RepositoryUrl "https://github.com/example/repo.git" -GenerateSBOM -AnalyzeVulnerabilities -GenerateReport
```

## 🏗️ Architecture

SBOMAI is built as a modular microservices architecture:

### Core Modules
- **sbomai-parser**: Parse SPDX, CycloneDX, and SWID formats
- **sbomai-vulnscan**: Scan against NVD, OSS Index, OSV databases
- **sbomai-policy**: Enforce custom rules and policies
- **sbomai-core**: Orchestrate analysis and AI predictions
- **sbomai-cli**: Command-line interface for analysis

### Monitoring Stack
- **Grafana**: Dashboards and visualization
- **Prometheus**: Metrics collection
- **Loki**: Centralized logging
- **Alertmanager**: Alerting and notifications

## 📊 Key Features

### SBOM Analysis
- Parse multiple SBOM formats (SPDX, CycloneDX, SWID)
- Unified internal representation
- Format validation and error handling

### Vulnerability Scanning
- Integration with NVD, OSS Index, OSV
- Real-time vulnerability database updates
- Severity classification and scoring

### AI-Powered Risk Analysis
- Predictive risk scoring using ML/LLM models
- Zero-day vulnerability prediction
- Confidence intervals and model accuracy tracking

### Policy Enforcement
- Custom CVSS thresholds
- License compliance checking
- Build blocking and approval workflows

### Real-time Monitoring
- Live metrics and dashboards
- Performance monitoring
- Alerting for critical issues

## 📈 Metrics & Reporting

### Available Metrics
- SBOM parsing throughput and errors
- Vulnerability detection rates by severity
- AI model performance and accuracy
- Policy violation tracking
- System health and performance

### Report Formats
- **JSON**: Machine-readable detailed reports
- **HTML**: Human-readable visual reports
- **TEXT**: Console-friendly output
- **Grafana**: Interactive dashboards

### Sample Queries
```promql
# SBOM parsing rate
rate(sbomai_parser_files_parsed_total[5m])

# CVE severity distribution
sum by (severity) (sbomai_vulnscan_cves_found_total)

# Policy violation rate
rate(sbomai_policy_violations_total[5m])
```

## 🔧 Configuration

### Environment Variables
```bash
# Core service configuration
SBOMAI_PARSER_URL=http://sbomai-parser:8080
SBOMAI_VULNSCAN_URL=http://sbomai-vulnscan:8080
SBOMAI_POLICY_URL=http://sbomai-policy:8080

# AI model configuration
OPENAI_API_KEY=your-api-key
AI_MODEL_PROVIDER=openai
```

### Application Properties
```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  metrics:
    export:
      prometheus:
        enabled: true
```

## 🧪 Testing Scenarios

### 1. Basic Functionality
- Service health checks
- SBOM parsing validation
- CLI command execution
- API endpoint testing

### 2. Vulnerability Analysis
- Sample SBOM analysis
- CVE detection verification
- Severity classification
- Source attribution

### 3. Performance Testing
- Load testing with multiple files
- Concurrent analysis testing
- Memory and CPU monitoring
- Response time measurement

### 4. Integration Testing
- Inter-service communication
- Database connectivity
- External API integration
- Error handling

## 📚 Documentation

- [Testing Guide](TESTING_GUIDE.md) - Comprehensive testing instructions
- [Monitoring Setup](MONITORING_SETUP.md) - Grafana and Prometheus configuration
- [API Documentation](docs/api.md) - REST API reference
- [CLI Reference](docs/cli.md) - Command-line interface guide

## 🎯 Success Criteria

A successful deployment should show:
1. ✅ All services start without errors
2. ✅ Sample SBOM files parse successfully
3. ✅ Vulnerabilities are detected and categorized
4. ✅ Policy violations are identified
5. ✅ AI analysis provides risk scores
6. ✅ Metrics are collected in Prometheus
7. ✅ Dashboards display data in Grafana
8. ✅ Reports are generated in multiple formats
9. ✅ CLI commands execute successfully
10. ✅ All health endpoints return healthy status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions:
- Check the [Testing Guide](TESTING_GUIDE.md)
- Review [Monitoring Setup](MONITORING_SETUP.md)
- Open an issue on GitHub

---

**SBOMAI** - Secure your software supply chain with AI-powered analysis! 🔍🤖