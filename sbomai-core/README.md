# SBOMAI Core Module

The core engine of SBOMAI - an AI-powered Software Bill of Materials (SBOM) analysis tool. This module provides the foundational services for parsing, scanning, analyzing, and enforcing policies on SBOM documents.

## Features

- **SBOM Parsing**: Support for SPDX, CycloneDX, and SWID formats
- **Vulnerability Scanning**: Integration with NVD, OSS Index, OSV, and other vulnerability databases
- **AI-Powered Analysis**: Risk assessment and recommendations using OpenAI or local models
- **Policy Enforcement**: License compliance, security thresholds, and custom business rules
- **REST API**: Comprehensive REST endpoints for external module integration
- **Clean Architecture**: Modular design with clear separation of concerns

## Architecture

The core module follows clean architecture principles with the following layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    REST API Layer                           │
├─────────────────────────────────────────────────────────────┤
│                   Service Layer                             │
├─────────────────────────────────────────────────────────────┤
│                   Domain Layer                              │
├─────────────────────────────────────────────────────────────┤
│                   Ports (Interfaces)                        │
├─────────────────────────────────────────────────────────────┤
│                   Adapters (Implementations)                │
└─────────────────────────────────────────────────────────────┘
```

### Domain Entities

- `SbomDocument`: Core SBOM document representation
- `SbomComponent`: Individual components within an SBOM
- `Vulnerability`: Vulnerability information for components
- `VulnerabilityReport`: Aggregated vulnerability scan results
- `PolicyViolation`: Policy enforcement violations
- `AiAnalysisResult`: AI-powered risk analysis results

### Core Interfaces

- `SbomParser`: SBOM document parsing
- `VulnerabilityScanner`: Vulnerability database scanning
- `AiAnalyzer`: AI-powered risk analysis
- `PolicyEnforcer`: Policy compliance checking

## Quick Start

### Prerequisites

- Java 17 or higher
- Maven 3.6 or higher
- OpenAI API key (for AI analysis)
- NVD API key (optional, for enhanced vulnerability scanning)

### Running the Application

1. **Clone and build the project:**
   ```bash
   mvn clean install
   ```

2. **Set environment variables:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export NVD_API_KEY="your-nvd-api-key"  # Optional
   ```

3. **Run the application:**
   ```bash
   mvn spring-boot:run
   ```

4. **Access the application:**
   - API Base URL: `http://localhost:8080/api/v1/sbom`
   - Health Check: `http://localhost:8080/api/v1/sbom/health`
   - H2 Console: `http://localhost:8080/h2-console`

## API Endpoints

### SBOM Analysis

- `POST /api/v1/sbom/analyze` - Analyze SBOM with default settings
- `POST /api/v1/sbom/analyze/custom` - Analyze SBOM with custom parameters
- `POST /api/v1/sbom/analyze/json` - Analyze SBOM from JSON content

### System Information

- `GET /api/v1/sbom/health` - Get system health status
- `GET /api/v1/sbom/capabilities` - Get component capabilities

### Example Usage

```bash
# Analyze an SBOM file
curl -X POST \
  http://localhost:8080/api/v1/sbom/analyze \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/sbom.spdx' \
  -F 'format=SPDX'

# Check system health
curl http://localhost:8080/api/v1/sbom/health

# Get capabilities
curl http://localhost:8080/api/v1/sbom/capabilities
```

## Configuration

The application can be configured through `application.yml` or environment variables:

### Key Configuration Options

```yaml
sbomai:
  core:
    analysis:
      default-timeout: 300000  # 5 minutes
      max-concurrent-analyses: 10
      enable-parallel-processing: true
    
    scanner:
      nvd:
        enabled: true
        api-key: ${NVD_API_KEY:}
        rate-limit: 1000
      oss-index:
        enabled: true
        username: ${OSS_INDEX_USERNAME:}
        token: ${OSS_INDEX_TOKEN:}
    
    ai:
      openai:
        enabled: true
        api-key: ${OPENAI_API_KEY:}
        model: gpt-4
        max-tokens: 4000
        temperature: 0.3
    
    policy:
      strict-mode: false
      default-policies:
        - license-compliance
        - security-thresholds
        - component-restrictions
```

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for AI analysis
- `NVD_API_KEY`: NVD API key for vulnerability scanning
- `OSS_INDEX_USERNAME`: OSS Index username
- `OSS_INDEX_TOKEN`: OSS Index API token
- `LOCAL_MODEL_PATH`: Path to local AI model (if using local models)

## Development

### Project Structure

```
src/main/java/com/sbomai/core/
├── controllers/          # REST API controllers
├── domain/              # Domain entities and enums
├── ports/               # Interface definitions
├── services/            # Business logic services
└── SbomaiCoreApplication.java
```

### Adding New Features

1. **New SBOM Format**: Implement `SbomParser` interface
2. **New Vulnerability Source**: Implement `VulnerabilityScanner` interface
3. **New AI Model**: Implement `AiAnalyzer` interface
4. **New Policy Type**: Implement `PolicyEnforcer` interface

### Testing

```bash
# Run unit tests
mvn test

# Run integration tests
mvn verify

# Run with coverage
mvn jacoco:report
```

## Integration with Other Modules

The core module is designed to be consumed by other SBOMAI modules:

- **CLI Module**: Uses REST API for local analysis
- **GitHub Action**: Integrates via REST API for CI/CD
- **Live Feed**: Processes real-time SBOMs via REST API
- **VSCode Extension**: Provides IDE integration via REST API
- **Dashboard**: Web UI consuming REST API

## Monitoring and Observability

- **Health Checks**: `/api/v1/sbom/health`
- **Metrics**: Available via Spring Boot Actuator
- **Logging**: Structured logging with SLF4J
- **Database**: H2 in-memory database with console access

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**: Check API key and rate limits
2. **Vulnerability Scanner Failures**: Verify API keys and network connectivity
3. **Memory Issues**: Adjust JVM heap size for large SBOMs
4. **Timeout Errors**: Increase analysis timeout in configuration

### Logs

Enable debug logging for troubleshooting:

```yaml
logging:
  level:
    com.sbomai: DEBUG
    org.springframework.web: DEBUG
```

## Contributing

1. Follow clean architecture principles
2. Add comprehensive unit tests
3. Update documentation
4. Ensure all tests pass
5. Follow the existing code style

## License

This project is licensed under the MIT License - see the LICENSE file for details. 