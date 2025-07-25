# SBOMAI Live Feed Module

Live feed service for SBOMAI - ingests real-time SBOMs from various sources and provides streaming analysis capabilities.

## Features

- **Real-time Ingestion**: Process SBOMs as they are generated
- **Multiple Sources**: Support for webhooks, message queues, and file watchers
- **Streaming Analysis**: Real-time vulnerability and policy analysis
- **Event Streaming**: Publish analysis results to message queues
- **Scalable Architecture**: Built for high-throughput processing
- **Monitoring**: Real-time metrics and health monitoring

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SBOM Sources  │───▶│   Live Feed     │───▶│   Analysis      │
│                 │    │   Service       │    │   Results       │
│ • Webhooks      │    │                 │    │                 │
│ • Message Queues│    │ • Ingestion     │    │ • Kafka Topics  │
│ • File Watchers │    │ • Validation    │    │ • WebSockets    │
│ • APIs          │    │ • Routing       │    │ • REST APIs     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### Prerequisites

- Java 17 or higher
- Maven 3.6 or higher
- Redis (for caching and pub/sub)
- Kafka (for event streaming)

### Running the Service

```bash
# Build the project
mvn clean install

# Run the livefeed service
cd sbomai-livefeed
mvn spring-boot:run
```

### Configuration

```yaml
# application.yml
spring:
  application:
    name: sbomai-livefeed
  
  # Redis Configuration
  redis:
    host: localhost
    port: 6379
    password: 
    database: 0
  
  # Kafka Configuration
  kafka:
    bootstrap-servers: localhost:9092
    consumer:
      group-id: sbomai-livefeed
      auto-offset-reset: earliest
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer

# SBOMAI Live Feed Configuration
sbomai:
  livefeed:
    # Ingestion Configuration
    ingestion:
      max-concurrent-streams: 10
      batch-size: 100
      batch-timeout: 5000
    
    # Source Configuration
    sources:
      webhook:
        enabled: true
        path: /webhook/sbom
        secret: ${WEBHOOK_SECRET:}
      kafka:
        enabled: true
        topics:
          - sbom-ingestion
      file-watcher:
        enabled: false
        directories:
          - /path/to/sbom/directory
    
    # Processing Configuration
    processing:
      enable-parallel-processing: true
      max-processing-time: 300000
      retry-attempts: 3
      retry-delay: 1000
```

## API Endpoints

### Webhook Ingestion

```bash
# POST SBOM via webhook
curl -X POST http://localhost:8080/webhook/sbom \
  -H "Content-Type: application/json" \
  -H "X-SBOMAI-Signature: sha256=..." \
  -d '{
    "sbom": "...",
    "format": "SPDX",
    "source": "ci-pipeline",
    "metadata": {
      "project": "my-project",
      "version": "1.0.0"
    }
  }'
```

### Streaming Results

```bash
# Subscribe to analysis results via WebSocket
ws://localhost:8080/ws/analysis-results

# Get recent results via REST API
curl http://localhost:8080/api/v1/livefeed/results/recent
```

### Health and Metrics

```bash
# Health check
curl http://localhost:8080/actuator/health

# Metrics
curl http://localhost:8080/actuator/metrics/sbomai.livefeed.ingestion.rate
```

## Integration Examples

### CI/CD Pipeline Integration

```yaml
# GitHub Actions example
- name: Send SBOM to Live Feed
  run: |
    curl -X POST ${{ secrets.SBOMAI_LIVEFEED_URL }}/webhook/sbom \
      -H "Content-Type: application/json" \
      -H "X-SBOMAI-Signature: sha256=$(echo -n "$SBOM_CONTENT" | sha256sum | cut -d' ' -f1)" \
      -d "{
        \"sbom\": \"$SBOM_CONTENT\",
        \"format\": \"SPDX\",
        \"source\": \"github-actions\",
        \"metadata\": {
          \"repository\": \"${{ github.repository }}\",
          \"commit\": \"${{ github.sha }}\",
          \"branch\": \"${{ github.ref_name }}\"
        }
      }"
```

### Kafka Integration

```java
// Producer example
@Autowired
private KafkaTemplate<String, SbomIngestionEvent> kafkaTemplate;

public void sendSbomToLiveFeed(SbomDocument sbom) {
    SbomIngestionEvent event = new SbomIngestionEvent();
    event.setSbom(sbom);
    event.setTimestamp(Instant.now());
    event.setSource("my-application");
    
    kafkaTemplate.send("sbom-ingestion", event);
}
```

### File Watcher Integration

```yaml
# Configure file watcher
sbomai:
  livefeed:
    sources:
      file-watcher:
        enabled: true
        directories:
          - /var/sbom/incoming
        patterns:
          - "*.spdx"
          - "*.cyclonedx"
          - "*.json"
        recursive: true
```

## Event Schema

### SBOM Ingestion Event

```json
{
  "id": "uuid",
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "ci-pipeline",
  "sbom": {
    "format": "SPDX",
    "content": "base64-encoded-sbom",
    "metadata": {
      "project": "my-project",
      "version": "1.0.0",
      "generator": "syft"
    }
  }
}
```

### Analysis Result Event

```json
{
  "id": "uuid",
  "timestamp": "2024-01-01T12:01:00Z",
  "ingestionEventId": "original-uuid",
  "analysisResult": {
    "status": "COMPLETED",
    "vulnerabilities": {
      "total": 5,
      "critical": 1,
      "high": 2,
      "medium": 2
    },
    "policyViolations": {
      "total": 0,
      "blocking": 0
    },
    "aiAnalysis": {
      "riskLevel": "MEDIUM",
      "riskScore": 6.5
    }
  }
}
```

## Monitoring and Observability

### Metrics

The service exposes various metrics:

- `sbomai.livefeed.ingestion.rate` - SBOM ingestion rate
- `sbomai.livefeed.processing.duration` - Processing time
- `sbomai.livefeed.errors.rate` - Error rate
- `sbomai.livefeed.queue.size` - Queue size

### Health Checks

- **Ingestion Health**: Checks if ingestion endpoints are responding
- **Processing Health**: Checks if analysis pipeline is working
- **Storage Health**: Checks Redis and Kafka connectivity

### Alerts

Configure alerts for:

- High error rates
- Processing delays
- Queue backlogs
- Service unavailability

## Performance Tuning

### Scaling

```yaml
# Horizontal scaling configuration
sbomai:
  livefeed:
    scaling:
      max-instances: 10
      min-instances: 2
      target-cpu-utilization: 70
      target-memory-utilization: 80
```

### Batch Processing

```yaml
# Batch processing configuration
sbomai:
  livefeed:
    processing:
      batch:
        enabled: true
        size: 100
        timeout: 5000
        max-concurrency: 5
```

### Caching

```yaml
# Redis caching configuration
spring:
  redis:
    cache:
      ttl: 3600
      max-entries: 10000
```

## Security

### Authentication

```yaml
# Webhook authentication
sbomai:
  livefeed:
    security:
      webhook:
        enabled: true
        secret: ${WEBHOOK_SECRET}
        signature-header: X-SBOMAI-Signature
        signature-algorithm: SHA256
```

### Authorization

```yaml
# API authorization
sbomai:
  livefeed:
    security:
      api:
        enabled: true
        jwt:
          secret: ${JWT_SECRET}
          expiration: 3600
```

## Troubleshooting

### Common Issues

1. **High Latency**
   - Check Redis and Kafka connectivity
   - Monitor processing queue size
   - Consider scaling up resources

2. **Memory Issues**
   - Increase JVM heap size
   - Enable batch processing
   - Monitor memory usage

3. **Connection Issues**
   - Check network connectivity
   - Verify Redis and Kafka configurations
   - Review firewall settings

### Debug Mode

Enable debug logging:

```yaml
logging:
  level:
    com.sbomai.livefeed: DEBUG
    org.springframework.kafka: DEBUG
    org.springframework.data.redis: DEBUG
```

## Contributing

1. Follow the existing code style
2. Add comprehensive tests for new features
3. Update documentation for new endpoints
4. Ensure backward compatibility

## License

This project is licensed under the MIT License - see the LICENSE file for details. 