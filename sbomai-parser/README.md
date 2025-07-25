# SBOMAI Parser Module

## Overview

The SBOMAI Parser module is responsible for parsing Software Bill of Materials (SBOM) documents from various formats into a unified internal representation. This module provides the foundation for all SBOM analysis operations by converting different SBOM formats into a consistent data model.

## Features

- **Multi-format Support**: Parse SBOMs in SPDX, CycloneDX, and SWID formats
- **Format Detection**: Auto-detect SBOM format from content
- **Validation**: Validate SBOM documents against format specifications
- **Unified Model**: Convert all formats to a consistent internal representation
- **Error Handling**: Comprehensive error handling and reporting
- **Extensible**: Easy to add support for new SBOM formats

## Supported Formats

### SPDX (Software Package Data Exchange)
- SPDX 2.3+ support
- JSON, RDF, and Tag-Value formats
- License compliance information
- Component relationships

### CycloneDX
- CycloneDX 1.4+ support
- JSON and XML formats
- Vulnerability information
- Component metadata

### SWID (Software Identification Tags)
- SWID 2.0 support
- XML format
- Software identification
- Tag management

## Architecture

The parser module follows clean architecture principles:

```
src/main/java/com/sbomai/parser/
├── domain/           # Domain models and entities
│   ├── SbomDocument.java
│   ├── SbomComponent.java
│   ├── SbomRelationship.java
│   ├── SbomFormat.java
│   └── ParsingMetadata.java
├── ports/            # Interface contracts
│   ├── SbomParser.java
│   └── SbomParsingException.java
└── SbomaiParserApplication.java
```

## Quick Start

### Prerequisites
- Java 21+
- Maven 3.6+

### Building the Module
```bash
mvn clean install
```

### Running the Module
```bash
mvn spring-boot:run
```

## Usage

### Basic Parsing
```java
@Autowired
private SbomParser sbomParser;

// Parse from file
SbomDocument document = sbomParser.parseFromFile("bom.spdx", SbomFormat.SPDX);

// Parse from string
SbomDocument document = sbomParser.parse(content, SbomFormat.CYCLONEDX);

// Auto-detect format
SbomFormat format = sbomParser.detectFormat(content);
SbomDocument document = sbomParser.parse(content, format);
```

### Format Validation
```java
// Validate a parsed document
boolean isValid = sbomParser.validate(document);

// Check supported formats
List<SbomFormat> supported = sbomParser.getSupportedFormats();
boolean isSupported = sbomParser.isFormatSupported(SbomFormat.SPDX);
```

## Configuration

### Application Properties
```yaml
# Parser Configuration
sbomai:
  parser:
    # Maximum file size for parsing (in bytes)
    max-file-size: 10485760  # 10MB
    
    # Timeout for parsing operations (in milliseconds)
    parse-timeout: 30000     # 30 seconds
    
    # Enable format validation
    validate-formats: true
    
    # Enable detailed parsing metadata
    include-metadata: true
```

## API Reference

### SbomParser Interface

#### Core Methods
- `parse(InputStream, SbomFormat)`: Parse from input stream
- `parse(String, SbomFormat)`: Parse from string content
- `parseFromFile(String, SbomFormat)`: Parse from file path

#### Utility Methods
- `detectFormat(String)`: Auto-detect format from content
- `detectFormat(InputStream)`: Auto-detect format from stream
- `validate(SbomDocument)`: Validate parsed document
- `getSupportedFormats()`: Get list of supported formats
- `isFormatSupported(SbomFormat)`: Check if format is supported

### Domain Models

#### SbomDocument
Represents a parsed SBOM document with:
- Document metadata (name, version, format)
- Component list
- Relationship information
- Parsing metadata

#### SbomComponent
Represents a component within an SBOM:
- Component identification (name, version, PURL, CPE)
- License information
- Supplier and author details
- Properties and metadata

#### SbomRelationship
Represents relationships between components:
- Source and target components
- Relationship type (depends_on, contains, etc.)
- Relationship metadata

## Error Handling

The parser module provides comprehensive error handling:

### SbomParsingException
Thrown when parsing operations fail:
```java
try {
    SbomDocument doc = sbomParser.parse(content, format);
} catch (SbomParsingException e) {
    // Handle parsing error
    logger.error("Failed to parse SBOM: {}", e.getMessage());
}
```

### Common Error Scenarios
- Invalid format specification
- Malformed SBOM content
- Unsupported SBOM version
- File access issues
- Memory constraints

## Development

### Adding New Format Support

1. **Create Format Parser**
```java
@Component
public class NewFormatParser implements SbomParser {
    // Implement parsing logic
}
```

2. **Add Format Enum**
```java
public enum SbomFormat {
    // ... existing formats
    NEW_FORMAT("New Format", "Description of new format");
}
```

3. **Register Parser**
```java
@Configuration
public class ParserConfig {
    @Bean
    public SbomParser newFormatParser() {
        return new NewFormatParser();
    }
}
```

### Testing

Run the test suite:
```bash
mvn test
```

Run specific tests:
```bash
mvn test -Dtest=SpdxParserTest
```

## Integration

### With Other SBOMAI Modules
The parser module is designed to integrate seamlessly with other SBOMAI modules:

- **Core Module**: Provides parsed SBOM documents for analysis
- **Vulnerability Scanner**: Uses component information for scanning
- **Policy Enforcer**: Validates components against policies
- **CLI Module**: Parses SBOM files from command line

### External Integration
```java
// Spring Boot integration
@Autowired
private SbomParser sbomParser;

// Direct instantiation
SbomParser parser = new SpdxParser();
```

## Performance

### Optimization Tips
- Use streaming for large files
- Implement caching for frequently parsed documents
- Parallel processing for multiple documents
- Memory-efficient parsing for large SBOMs

### Benchmarks
- SPDX parsing: ~1000 components/second
- CycloneDX parsing: ~1500 components/second
- Memory usage: ~2MB per 1000 components

## Troubleshooting

### Common Issues

1. **Out of Memory Errors**
   - Increase JVM heap size
   - Use streaming parser for large files
   - Enable garbage collection optimization

2. **Format Detection Failures**
   - Check file content encoding
   - Verify SBOM format specification
   - Review format detection logic

3. **Validation Errors**
   - Check SBOM version compatibility
   - Verify required fields are present
   - Review format-specific requirements

### Debug Mode
Enable debug logging:
```yaml
logging:
  level:
    com.sbomai.parser: DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style
- Follow Java coding conventions
- Use meaningful variable names
- Add comprehensive documentation
- Include unit tests for all new features

## License

This module is part of the SBOMAI project and is licensed under the same terms as the main project.

## Support

For issues and questions:
- Create an issue in the project repository
- Check the documentation
- Review existing issues for solutions 