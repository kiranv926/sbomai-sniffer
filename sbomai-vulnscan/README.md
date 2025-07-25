# SBOMAI Vulnerability Scanner Module

## Overview

The SBOMAI Vulnerability Scanner module is responsible for scanning SBOM components against various vulnerability databases to identify security issues. This module provides comprehensive vulnerability assessment capabilities by querying multiple sources and aggregating results.

## Features

- **Multi-source Scanning**: Scan against NVD, OSS Index, OSV, GitHub, SUSE, and Red Hat databases
- **Async Processing**: Support for asynchronous scanning of multiple components
- **Comprehensive Coverage**: CVE, GHSA, OSV, and vendor-specific advisories
- **CVSS Scoring**: Detailed vulnerability scoring and severity classification
- **Version Matching**: Smart version range matching for affected components
- **Rate Limiting**: Built-in rate limiting for API compliance
- **Caching**: Intelligent caching to reduce API calls and improve performance

## Supported Vulnerability Sources

### NVD (National Vulnerability Database)
- **URL**: https://nvd.nist.gov/
- **Coverage**: Comprehensive CVE database
- **API**: REST API with rate limiting
- **Features**: CVSS scoring, detailed descriptions, references

### OSS Index (Sonatype)
- **URL**: https://ossindex.sonatype.org/
- **Coverage**: Open source vulnerabilities
- **API**: REST API with authentication
- **Features**: Component-specific vulnerability data

### OSV (Open Source Vulnerabilities)
- **URL**: https://ossf.github.io/osv-schema/
- **Coverage**: Open source security advisories
- **API**: REST API and database dumps
- **Features**: GitHub, GitLab, and other platform advisories

### GitHub Security Advisories
- **URL**: https://github.com/advisories
- **Coverage**: GitHub-hosted project vulnerabilities
- **API**: GraphQL API
- **Features**: Real-time advisory updates

### Vendor Advisories
- **SUSE**: SUSE security advisories
- **Red Hat**: Red Hat security advisories
- **Coverage**: Enterprise Linux vulnerabilities

## Architecture

The vulnerability scanner module follows clean architecture principles:

```
src/main/java/com/sbomai/vulnscan/
├── domain/           # Domain models and entities
│   ├── Vulnerability.java
│   ├── Severity.java
│   └── VulnerabilitySource.java
├── ports/            # Interface contracts
│   ├── VulnerabilityScanner.java
│   ├── VulnerabilityScanException.java
│   └── ScannerInfo.java
└── SbomaiVulnscanApplication.java
```

## Quick Start

### Prerequisites
- Java 21+
- Maven 3.6+
- API keys for vulnerability sources (optional, for enhanced access)

### Building the Module
```bash
mvn clean install
```

### Running the Module
```bash
mvn spring-boot:run
```

## Usage

### Basic Component Scanning
```java
@Autowired
private VulnerabilityScanner vulnerabilityScanner;

// Scan a single component
List<Vulnerability> vulnerabilities = vulnerabilityScanner.scanComponent(
    "log4j-core", "2.14.1", 
    "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1", 
    "cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*"
);

// Scan with specific sources
List<VulnerabilitySource> sources = Arrays.asList(
    VulnerabilitySource.NVD, 
    VulnerabilitySource.OSS_INDEX
);
List<Vulnerability> vulnerabilities = vulnerabilityScanner.scanComponent(
    "log4j-core", "2.14.1", null, null, sources
);
```

### Async Multi-component Scanning
```java
// Prepare component list
List<VulnerabilityScanner.ComponentInfo> components = Arrays.asList(
    new VulnerabilityScanner.ComponentInfo("log4j-core", "2.14.1", 
        "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1", null),
    new VulnerabilityScanner.ComponentInfo("spring-boot", "2.7.0", 
        "pkg:maven/org.springframework.boot/spring-boot@2.7.0", null)
);

// Scan asynchronously
CompletableFuture<List<Vulnerability>> future = 
    vulnerabilityScanner.scanComponentsAsync(components);

// Get results
List<Vulnerability> allVulnerabilities = future.get();
```

### Scanner Information
```java
// Get scanner capabilities
ScannerInfo info = vulnerabilityScanner.getScannerInfo();
System.out.println("Scanner: " + info.getName());
System.out.println("Version: " + info.getVersion());
System.out.println("Available: " + info.isAvailable());

// Check source availability
boolean nvdAvailable = vulnerabilityScanner.isSourceAvailable(VulnerabilitySource.NVD);
List<VulnerabilitySource> supported = vulnerabilityScanner.getSupportedSources();
```

### Detailed Vulnerability Information
```java
// Get detailed vulnerability information
Vulnerability vuln = vulnerabilityScanner.getVulnerabilityDetails(
    "CVE-2021-44228", 
    VulnerabilitySource.NVD
);

System.out.println("Title: " + vuln.getTitle());
System.out.println("Severity: " + vuln.getSeverity());
System.out.println("CVSS Score: " + vuln.getCvssScore());
System.out.println("Description: " + vuln.getDescription());
```

## Configuration

### Application Properties
```yaml
# Vulnerability Scanner Configuration
sbomai:
  vulnscan:
    # API Configuration
    api:
      nvd:
        base-url: "https://services.nvd.nist.gov/rest/json/cves/2.0"
        api-key: "${NVD_API_KEY}"  # Optional, for higher rate limits
        rate-limit: 5  # requests per second
      oss-index:
        base-url: "https://ossindex.sonatype.org/api/v3"
        username: "${OSS_INDEX_USERNAME}"
        token: "${OSS_INDEX_TOKEN}"
        rate-limit: 10
      osv:
        base-url: "https://api.osv.dev/v1"
        rate-limit: 20
      github:
        base-url: "https://api.github.com/graphql"
        token: "${GITHUB_TOKEN}"
        rate-limit: 30
    
    # Scanning Configuration
    scanning:
      # Timeout for individual scans (in milliseconds)
      timeout: 30000  # 30 seconds
      
      # Maximum concurrent scans
      max-concurrent: 10
      
      # Enable caching
      enable-cache: true
      
      # Cache TTL (in minutes)
      cache-ttl: 60
      
      # Retry configuration
      max-retries: 3
      retry-delay: 1000  # milliseconds
```

### Environment Variables
```bash
# NVD API Key (optional, for higher rate limits)
export NVD_API_KEY="your-nvd-api-key"

# OSS Index credentials
export OSS_INDEX_USERNAME="your-username"
export OSS_INDEX_TOKEN="your-token"

# GitHub token (for GitHub advisories)
export GITHUB_TOKEN="your-github-token"
```

## API Reference

### VulnerabilityScanner Interface

#### Core Methods
- `scanComponent(String, String, String, String)`: Scan single component
- `scanComponent(String, String, String, String, List<VulnerabilitySource>)`: Scan with specific sources
- `scanComponentsAsync(List<ComponentInfo>)`: Async multi-component scanning

#### Utility Methods
- `isSourceAvailable(VulnerabilitySource)`: Check source availability
- `getScannerInfo()`: Get scanner information
- `getSupportedSources()`: Get supported sources
- `getVulnerabilityDetails(String, VulnerabilitySource)`: Get detailed vulnerability info

### Domain Models

#### Vulnerability
Represents a vulnerability with:
- Identifier (CVE, GHSA, OSV, etc.)
- Title and description
- Severity and CVSS score
- Source information
- Affected and fixed versions
- References and metadata

#### Severity
Enumeration of vulnerability severity levels:
- `CRITICAL` (9.0-10.0 CVSS)
- `HIGH` (7.0-8.9 CVSS)
- `MEDIUM` (4.0-6.9 CVSS)
- `LOW` (0.1-3.9 CVSS)
- `NONE` (0.0 CVSS)

#### VulnerabilitySource
Enumeration of vulnerability data sources:
- `NVD`, `OSS_INDEX`, `OSV`, `GITHUB`, `SUSE`, `REDHAT`

## Error Handling

### VulnerabilityScanException
Thrown when scanning operations fail:
```java
try {
    List<Vulnerability> vulns = vulnerabilityScanner.scanComponent(
        "component", "1.0.0", null, null);
} catch (VulnerabilityScanException e) {
    logger.error("Vulnerability scan failed: {}", e.getMessage());
}
```

### Common Error Scenarios
- API rate limiting exceeded
- Network connectivity issues
- Invalid component information
- Unsupported vulnerability sources
- Authentication failures

## Performance Optimization

### Caching Strategy
- Cache vulnerability data to reduce API calls
- Configurable TTL for different data types
- Memory-efficient caching implementation

### Rate Limiting
- Built-in rate limiting for all APIs
- Configurable limits per source
- Automatic retry with exponential backoff

### Async Processing
- Parallel scanning of multiple components
- Configurable concurrency limits
- Non-blocking operations

## Integration

### With Other SBOMAI Modules
The vulnerability scanner integrates with:

- **Parser Module**: Uses parsed component information
- **Core Module**: Provides vulnerability data for analysis
- **Policy Module**: Supplies vulnerability data for policy enforcement
- **CLI Module**: Enables vulnerability scanning from command line

### External Integration
```java
// Spring Boot integration
@Autowired
private VulnerabilityScanner vulnerabilityScanner;

// Direct instantiation
VulnerabilityScanner scanner = new NvdVulnerabilityScanner();
```

## Monitoring and Metrics

### Health Checks
```java
// Check scanner health
boolean healthy = vulnerabilityScanner.isSourceAvailable(VulnerabilitySource.NVD);

// Get scanner status
ScannerInfo info = vulnerabilityScanner.getScannerInfo();
```

### Performance Metrics
- Scan duration per component
- API response times
- Cache hit rates
- Error rates by source

## Troubleshooting

### Common Issues

1. **Rate Limiting Errors**
   - Increase rate limit configuration
   - Implement exponential backoff
   - Use API keys for higher limits

2. **Network Connectivity**
   - Check firewall settings
   - Verify proxy configuration
   - Test API endpoints directly

3. **Authentication Failures**
   - Verify API credentials
   - Check token expiration
   - Review API permissions

### Debug Mode
Enable debug logging:
```yaml
logging:
  level:
    com.sbomai.vulnscan: DEBUG
```

## Security Considerations

### API Key Management
- Store API keys securely
- Use environment variables
- Rotate keys regularly
- Monitor API usage

### Data Privacy
- Minimize data retention
- Secure data transmission
- Implement access controls
- Audit data access

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

### Adding New Vulnerability Sources

1. **Create Source Scanner**
```java
@Component
public class NewSourceScanner implements VulnerabilityScanner {
    // Implement scanning logic
}
```

2. **Add Source Enum**
```java
public enum VulnerabilitySource {
    // ... existing sources
    NEW_SOURCE("New Source", "Description", "https://api.example.com");
}
```

3. **Configure API Settings**
```yaml
sbomai:
  vulnscan:
    api:
      new-source:
        base-url: "https://api.example.com"
        rate-limit: 10
```

## License

This module is part of the SBOMAI project and is licensed under the same terms as the main project.

## Support

For issues and questions:
- Create an issue in the project repository
- Check the documentation
- Review existing issues for solutions 