# SBOMAI CLI Module

Command-line interface for SBOMAI - an AI-powered Software Bill of Materials (SBOM) analysis tool. This module provides a user-friendly CLI for analyzing SBOM files locally or remotely.

## Features

- **Local Analysis**: Run SBOM analysis using embedded core services
- **Remote Analysis**: Connect to remote SBOMAI core services
- **Multiple Formats**: Support for SPDX, CycloneDX, and SWID formats
- **Flexible Output**: JSON, TEXT, and HTML output formats
- **Health Monitoring**: Check service health status
- **Auto-detection**: Automatic SBOM format detection

## Installation

### Prerequisites

- Java 17 or higher
- Maven 3.6 or higher

### Building the CLI

```bash
# Build the entire project
mvn clean install

# Build just the CLI module
cd sbomai-cli
mvn clean package
```

### Running the CLI

```bash
# Run from Maven
mvn spring-boot:run -- analyze /path/to/sbom.spdx

# Run the JAR file
java -jar target/sbomai-cli-1.0.0-SNAPSHOT.jar analyze /path/to/sbom.spdx

# Create an executable script (Linux/Mac)
echo '#!/bin/bash' > sbomai
echo 'java -jar target/sbomai-cli-1.0.0-SNAPSHOT.jar "$@"' >> sbomai
chmod +x sbomai
```

## Usage

### Basic Commands

```bash
# Show help
sbomai --help

# Show version
sbomai version

# Check health
sbomai health

# Analyze an SBOM file
sbomai analyze /path/to/sbom.spdx
```

### Analysis Options

```bash
# Analyze with specific format
sbomai analyze /path/to/sbom.spdx -f SPDX

# Use remote service
sbomai analyze /path/to/sbom.spdx -r -u http://sbomai-server:8080

# Custom output format
sbomai analyze /path/to/sbom.spdx -o JSON

# Skip specific analysis types
sbomai analyze /path/to/sbom.spdx --no-ai --no-vulnerability-scan

# Verbose output
sbomai analyze /path/to/sbom.spdx -v
```

### Health Check Options

```bash
# Check local health
sbomai health

# Check remote health
sbomai health -r -u http://sbomai-server:8080
```

## Command Reference

### `analyze` Command

Analyzes an SBOM file for vulnerabilities, policy violations, and AI insights.

**Syntax:**
```bash
sbomai analyze <file> [options]
```

**Parameters:**
- `file` - Path to the SBOM file to analyze

**Options:**
- `-f, --format <format>` - SBOM format (SPDX, CYCLONEDX, SWID, AUTO)
- `-o, --output <format>` - Output format (JSON, TEXT, HTML)
- `-r, --remote` - Use remote SBOMAI core service
- `-u, --url <url>` - Remote service URL (default: http://localhost:8080)
- `-v, --verbose` - Enable verbose output
- `--no-ai` - Skip AI analysis
- `--no-vulnerability-scan` - Skip vulnerability scanning
- `--no-policy-check` - Skip policy enforcement

### `health` Command

Checks the health status of SBOMAI services.

**Syntax:**
```bash
sbomai health [options]
```

**Options:**
- `-r, --remote` - Check remote service health
- `-u, --url <url>` - Remote service URL (default: http://localhost:8080)

### `version` Command

Displays version information.

**Syntax:**
```bash
sbomai version
```

## Examples

### Local Analysis

```bash
# Analyze an SPDX file locally
sbomai analyze project.spdx

# Analyze with verbose output
sbomai analyze project.spdx -v

# Analyze and output JSON
sbomai analyze project.spdx -o JSON > results.json
```

### Remote Analysis

```bash
# Analyze using remote service
sbomai analyze project.spdx -r

# Analyze using specific remote service
sbomai analyze project.spdx -r -u https://sbomai.company.com

# Check remote service health first
sbomai health -r -u https://sbomai.company.com
```

### Advanced Usage

```bash
# Analyze only for vulnerabilities (skip AI and policy)
sbomai analyze project.spdx --no-ai --no-policy-check

# Analyze with custom format detection
sbomai analyze project.spdx -f AUTO

# Analyze with all options
sbomai analyze project.spdx \
  -f SPDX \
  -o JSON \
  -r \
  -u https://sbomai.company.com \
  -v
```

## Configuration

The CLI can be configured through environment variables or the `application.yml` file:

### Environment Variables

- `SBOMAI_REMOTE_URL` - Default remote service URL
- `SBOMAI_TIMEOUT` - Analysis timeout in milliseconds
- `SBOMAI_OUTPUT_FORMAT` - Default output format

### Configuration File

```yaml
sbomai:
  cli:
    default:
      remote-url: http://localhost:8080
      output-format: TEXT
      timeout: 300000
    remote:
      connection-timeout: 30000
      read-timeout: 300000
      max-retries: 3
```

## Output Formats

### TEXT Format (Default)

```
🔍 SBOMAI Analysis Starting...
📁 File: /path/to/project.spdx
📋 Format: SPDX
🌐 Mode: Local

📊 Analysis Results:
===================
📄 SBOM Document: project-1.0.0
📦 Components: 45
🔒 Vulnerabilities: 3
⚠️  Critical: 1
🚨 High: 2
📋 Policy Violations: 0
🤖 AI Risk Level: MEDIUM
📈 Risk Score: 6.5

✅ Analysis completed successfully!
```

### JSON Format

```json
{
  "successful": true,
  "sbomDocument": {
    "documentName": "project-1.0.0",
    "components": [...]
  },
  "vulnerabilityReport": {
    "totalVulnerabilities": 3,
    "criticalCount": 1,
    "highCount": 2
  },
  "aiAnalysisResult": {
    "riskLevel": "MEDIUM",
    "riskScore": 6.5
  },
  "policyViolations": []
}
```

## Error Handling

The CLI provides clear error messages and appropriate exit codes:

- `0` - Success
- `1` - Analysis failed or errors occurred
- `2` - Invalid arguments or configuration

### Common Error Scenarios

```bash
# File not found
❌ Error: SBOM file not found: /path/to/missing.spdx

# Invalid format
❌ Error: Invalid SBOM format: INVALID_FORMAT

# Remote service unavailable
❌ Error: Remote API call failed: 503 - Service Unavailable

# Analysis timeout
❌ Error: Analysis failed: Timeout after 5 minutes
```

## Integration

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Analyze SBOM
  run: |
    sbomai analyze bom.spdx -r -u ${{ secrets.SBOMAI_URL }} -o JSON > results.json
    
- name: Check for critical vulnerabilities
  run: |
    if jq -e '.vulnerabilityReport.criticalCount > 0' results.json; then
      echo "Critical vulnerabilities found!"
      exit 1
    fi
```

### Script Integration

```bash
#!/bin/bash
# Analyze multiple SBOMs
for sbom in *.spdx; do
    echo "Analyzing $sbom..."
    sbomai analyze "$sbom" -o JSON > "${sbom%.spdx}.results.json"
done
```

## Troubleshooting

### Common Issues

1. **Java Version**: Ensure Java 17+ is installed
2. **Memory Issues**: Increase JVM heap size for large SBOMs
3. **Network Issues**: Check connectivity for remote analysis
4. **File Permissions**: Ensure read access to SBOM files

### Debug Mode

Enable verbose logging:

```bash
# Set log level
export LOGGING_LEVEL_COM_SBOMAI_CLI=DEBUG

# Run with verbose output
sbomai analyze project.spdx -v
```

### Performance Tips

- Use local analysis for faster results
- Skip unnecessary analysis types with flags
- Use JSON output for programmatic processing
- Consider file size limits for remote analysis

## Contributing

1. Follow the existing code style
2. Add comprehensive tests for new commands
3. Update documentation for new features
4. Ensure all tests pass before submitting

## License

This project is licensed under the MIT License - see the LICENSE file for details. 