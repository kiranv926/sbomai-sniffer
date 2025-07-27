# SBOMAI Web Scanner

A comprehensive website security scanner for detecting outdated frontend JavaScript libraries, security headers, exposed metadata, and common web vulnerabilities.

## 🎯 Features

### JavaScript Library Detection
- **Version Analysis**: Detect and analyze JavaScript library versions
- **Outdated Detection**: Identify outdated libraries with known vulnerabilities
- **Vulnerability Check**: Check for known CVEs in detected libraries
- **Update Recommendations**: Provide upgrade paths for outdated libraries

### Security Headers Analysis
- **Header Detection**: Analyze presence and configuration of security headers
- **Best Practices**: Validate against security header best practices
- **Critical Headers**: Focus on essential security headers:
  - Strict-Transport-Security (HSTS)
  - Content-Security-Policy (CSP)
  - X-Frame-Options
  - X-Content-Type-Options
  - X-XSS-Protection
  - Referrer-Policy

### Metadata Detection
- **HTML Meta Tags**: Scan for exposed metadata in HTML
- **Comments Analysis**: Detect sensitive information in HTML comments
- **JavaScript Metadata**: Find exposed data in JavaScript code
- **Header Metadata**: Analyze HTTP headers for sensitive information
- **Sensitivity Classification**: Categorize metadata by sensitivity level

### Vulnerability Scanning
- **Common Vulnerabilities**: Detect common web security issues
- **SSL/TLS Analysis**: Check SSL/TLS configuration and certificates
- **CORS Analysis**: Validate Cross-Origin Resource Sharing settings
- **CSRF Detection**: Identify potential CSRF vulnerabilities

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Domain Layer                             │
├─────────────────────────────────────────────────────────────┤
│  WebScanResult  JavaScriptLibrary  SecurityHeader          │
│  ExposedMetadata  SecurityVulnerability  ScanStatus        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Ports Layer                              │
├─────────────────────────────────────────────────────────────┤
│  WebScanner  JavaScriptLibraryDetector  SecurityHeaderAnalyzer │
│  MetadataDetector  ScanOptions  ScannerCapabilities        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  Adapters Layer                             │
├─────────────────────────────────────────────────────────────┤
│  WebScannerImpl  JsoupLibraryDetector  HeaderAnalyzerImpl  │
│  MetadataDetectorImpl  VulnerabilityScannerImpl            │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Java 21
- Maven 3.8+
- Spring Boot 3.x

### Running the Application

1. **Build the project:**
   ```bash
   mvn clean install
   ```

2. **Run the application:**
   ```bash
   mvn spring-boot:run
   ```

3. **Access the application:**
   - API Base URL: `http://localhost:8084/api/v1/webscan`
   - Health Check: `http://localhost:8084/actuator/health`
   - H2 Console: `http://localhost:8084/h2-console`

## 📋 API Endpoints

### Website Scanning

- `POST /api/v1/webscan/scan` - Scan a website with default options
- `POST /api/v1/webscan/scan/custom` - Scan a website with custom options
- `GET /api/v1/webscan/results/{id}` - Get scan results by ID
- `GET /api/v1/webscan/results` - List all scan results

### Scanner Information

- `GET /api/v1/webscan/capabilities` - Get scanner capabilities
- `GET /api/v1/webscan/info` - Get scanner information
- `GET /api/v1/webscan/health` - Check scanner health

## 🔧 Configuration

### Application Properties

```yaml
sbomai:
  webscan:
    scanner:
      default-timeout: 30000
      max-concurrent-scans: 10
      user-agent: "SBOMAI-WebScanner/1.0"
    
    javascript:
      enabled: true
      check-versions: true
      vulnerability-check: true
    
    headers:
      enabled: true
      critical-headers:
        - "Strict-Transport-Security"
        - "Content-Security-Policy"
    
    metadata:
      enabled: true
      sensitive-patterns:
        - "api_key"
        - "secret"
```

### Environment Variables

```bash
# Scanner Configuration
WEBSCAN_TIMEOUT=30000
WEBSCAN_MAX_CONCURRENT=10
WEBSCAN_USER_AGENT="SBOMAI-WebScanner/1.0"

# Feature Toggles
WEBSCAN_JAVASCRIPT_ENABLED=true
WEBSCAN_HEADERS_ENABLED=true
WEBSCAN_METADATA_ENABLED=true
WEBSCAN_VULNERABILITIES_ENABLED=true
```

## 📊 Scan Results

### WebScanResult Structure

```json
{
  "id": "uuid",
  "targetUrl": "https://example.com",
  "scanDate": "2024-01-01T12:00:00",
  "scanDurationMs": 5000,
  "overallSecurityScore": "GOOD",
  "totalIssues": 5,
  "criticalIssues": 0,
  "highIssues": 2,
  "mediumIssues": 2,
  "lowIssues": 1,
  "javascriptLibraries": [...],
  "securityHeaders": [...],
  "exposedMetadata": [...],
  "securityVulnerabilities": [...],
  "status": "COMPLETED"
}
```

### Security Score Levels

- **EXCELLENT (90-100)**: Minimal security issues
- **GOOD (80-89)**: Minor issues that should be addressed
- **FAIR (70-79)**: Some issues that need attention
- **POOR (60-69)**: Significant issues requiring immediate attention
- **CRITICAL (0-59)**: Critical security issues posing serious risks

## 🔍 Usage Examples

### Basic Website Scan

```bash
curl -X POST http://localhost:8084/api/v1/webscan/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Custom Scan Options

```bash
curl -X POST http://localhost:8084/api/v1/webscan/scan/custom \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "scanOptions": {
      "scanJavaScriptLibraries": true,
      "scanSecurityHeaders": true,
      "scanMetadata": false,
      "timeoutSeconds": 60,
      "maxDepth": 2
    }
  }'
```

### Get Scan Results

```bash
curl http://localhost:8084/api/v1/webscan/results/{scan-id}
```

## 🧪 Testing

### Unit Tests

```bash
mvn test
```

### Integration Tests

```bash
mvn test -Dtest=WebScanIntegrationTest
```

### Manual Testing

```bash
# Test with a sample website
curl -X POST http://localhost:8084/api/v1/webscan/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://httpbin.org"}'
```

## 📈 Metrics & Monitoring

### Available Metrics

- `webscan_scans_total`: Total number of scans performed
- `webscan_scans_duration_seconds`: Scan duration histogram
- `webscan_issues_total`: Total issues found by severity
- `webscan_libraries_detected_total`: JavaScript libraries detected
- `webscan_headers_missing_total`: Missing security headers
- `webscan_metadata_exposed_total`: Exposed metadata items

### Prometheus Queries

```promql
# Scan success rate
rate(webscan_scans_total{status="completed"}[5m])

# Average scan duration
histogram_quantile(0.95, rate(webscan_scans_duration_seconds_bucket[5m]))

# Critical issues trend
rate(webscan_issues_total{severity="critical"}[5m])
```

## 🔒 Security Considerations

### Rate Limiting
- Implement rate limiting to prevent abuse
- Respect robots.txt and website terms of service
- Use appropriate delays between requests

### Privacy
- Don't store sensitive data from scanned websites
- Implement data retention policies
- Anonymize scan results when possible

### Legal Compliance
- Ensure scanning is authorized
- Respect website terms of service
- Comply with applicable laws and regulations

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
- Check the [API Documentation](docs/api.md)
- Review [Configuration Guide](docs/configuration.md)
- Open an issue on GitHub

---

**SBOMAI Web Scanner** - Secure your web applications with comprehensive security scanning! 🔍🌐 