# SBOMAI Monitoring & Observability Setup

This guide provides complete instructions for setting up monitoring and observability for the SBOMAI project using Grafana, Prometheus, and Loki.

## 🎯 Overview

The monitoring stack provides:
- **Real-time metrics visualization** with Grafana dashboards
- **Time-series data collection** with Prometheus
- **Centralized logging** with Loki
- **Custom SBOMAI metrics** for parsing, scanning, AI analysis, and policy enforcement
- **System health monitoring** and alerting

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- SBOMAI services running (optional for initial setup)

### 1. Start Monitoring Stack

**Linux/macOS:**
```bash
cd monitoring
chmod +x start-monitoring.sh
./start-monitoring.sh
```

**Windows:**
```cmd
cd monitoring
start-monitoring.bat
```

**Manual:**
```bash
cd monitoring
docker-compose up -d
```

### 2. Access Services

- **Grafana**: http://localhost:3000 (admin/sbomai2024)
- **Prometheus**: http://localhost:9090
- **Loki**: http://localhost:3100

### 3. View Dashboards

1. Open Grafana at http://localhost:3000
2. Login with `admin` / `sbomai2024`
3. Navigate to Dashboards → SBOMAI folder
4. Explore the pre-configured dashboards

## 📊 Available Dashboards

### SBOMAI Overview Dashboard
- **Purpose**: Main operational dashboard
- **Key Metrics**:
  - SBOM parsing throughput and errors
  - Vulnerability scanning results by severity
  - AI analysis performance and accuracy
  - Policy enforcement violations
  - System health indicators

### System Health Dashboard
- **Purpose**: Infrastructure and application health
- **Key Metrics**:
  - JVM memory and CPU usage
  - HTTP request latency and error rates
  - Database connection pool status
  - Service uptime and availability

### Vulnerability Analysis Dashboard
- **Purpose**: Detailed security insights
- **Key Metrics**:
  - CVE distribution by source (NVD, OSS Index, OSV)
  - Top vulnerable packages
  - Risk score trends
  - Remediation recommendations

## 🔧 Configuration

### Spring Boot Metrics Integration

The SBOMAI modules are configured with Micrometer and Prometheus:

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
    tags:
      application: sbomai-core
      module: core
```

### Custom Metrics

The `MetricsService` class provides custom metrics:

```java
// Counters
sbomai_total_projects_scanned
sbomai_total_cves_found
sbomai_total_policy_violations
sbomai_parser_errors_total
sbomai_scanner_errors_total
sbomai_ai_analysis_errors_total

// Timers
sbomai_parser_parse_duration_seconds
sbomai_vulnscan_scan_duration_seconds
sbomai_ai_analysis_duration_seconds
sbomai_policy_enforcement_duration_seconds
```

### Prometheus Targets

Prometheus is configured to scrape these endpoints:
- Core: `http://localhost:8080/actuator/prometheus`
- Parser: `http://localhost:8081/actuator/prometheus`
- VulnScan: `http://localhost:8082/actuator/prometheus`
- Policy: `http://localhost:8083/actuator/prometheus`

## 📈 Key Metrics Explained

### SBOM Parsing Metrics
- **Files Parsed per Minute**: Throughput of SBOM processing
- **Parse Time**: Performance monitoring for different file formats
- **Format Distribution**: Usage statistics for SPDX, CycloneDX, SWID
- **Parser Errors**: Error rate and types for troubleshooting

### Vulnerability Scanning Metrics
- **CVEs Found**: Total vulnerabilities discovered
- **Severity Distribution**: Critical/High/Medium/Low breakdown
- **Scan Duration**: Performance monitoring per package
- **Source Breakdown**: NVD, OSS Index, OSV contribution

### AI Analysis Metrics
- **Analysis Requests**: AI processing throughput
- **Analysis Duration**: Performance monitoring
- **Risk Score Distribution**: AI prediction confidence
- **Accuracy Metrics**: Model performance tracking

### Policy Enforcement Metrics
- **Violations**: Policy rule violations by type
- **Enforcement Time**: Performance monitoring
- **Blocked Builds**: Security gate effectiveness
- **Custom Rules**: Usage of custom policy rules

## 🚨 Alerting

### Pre-configured Alerts

1. **High Error Rate**
   - Trigger: Error rate > 5%
   - Action: Slack/Email notification

2. **Slow Response Time**
   - Trigger: 95th percentile > 30s
   - Action: Performance alert

3. **Critical CVEs Found**
   - Trigger: Critical vulnerabilities detected
   - Action: Security team notification

4. **Service Down**
   - Trigger: No metrics received for 5 minutes
   - Action: PagerDuty escalation

### Alert Channels

Configure alert channels in Grafana:
- Slack webhooks
- Email notifications
- PagerDuty integration
- Webhook endpoints

## 🔍 Logging

### Log Sources

- **Application Logs**: SBOMAI service logs
- **Container Logs**: Docker container logs
- **System Logs**: Host system logs
- **Access Logs**: HTTP request logs

### Log Queries (Loki)

```logql
# All SBOMAI logs
{job="sbomai"}

# Error logs only
{job="sbomai"} |= "ERROR"

# Parser errors
{job="sbomai"} |= "parser" |= "error"

# Slow operations (>5s)
{job="sbomai"} |~ "duration.*[5-9][0-9][0-9][0-9]ms"

# Specific service logs
{job="sbomai"} |= "sbomai-core"
```

## 🛠️ Development

### Adding New Metrics

1. **Update MetricsService.java**:
```java
private final Counter newMetric = Counter.builder("sbomai_new_metric")
    .description("Description of new metric")
    .register(meterRegistry);
```

2. **Add to Dashboard**:
```json
{
  "targets": [
    {
      "expr": "rate(sbomai_new_metric[5m])",
      "refId": "A"
    }
  ]
}
```

### Adding New Dashboards

1. Create JSON file in `monitoring/grafana/dashboards/`
2. Use Prometheus queries for metrics
3. Import via Grafana UI or auto-provisioning

### Custom Prometheus Queries

```promql
# Rate of operations per minute
rate(sbomai_parser_files_parsed_total[5m]) * 60

# 95th percentile response time
histogram_quantile(0.95, rate(sbomai_parser_parse_duration_seconds_bucket[5m]))

# Error rate percentage
(rate(sbomai_parser_errors_total[5m]) / rate(sbomai_parser_files_parsed_total[5m])) * 100

# Success rate
(1 - (rate(sbomai_parser_errors_total[5m]) / rate(sbomai_parser_files_parsed_total[5m]))) * 100
```

## 🔧 Troubleshooting

### Common Issues

1. **Prometheus can't scrape targets**
   - Check if SBOMAI services are running
   - Verify ports in `prometheus.yml`
   - Check firewall settings

2. **Grafana can't connect to Prometheus**
   - Verify Prometheus is running on port 9090
   - Check datasource configuration
   - Restart Grafana container

3. **No metrics appearing**
   - Ensure Spring Boot Actuator is enabled
   - Check `/actuator/prometheus` endpoint
   - Verify Micrometer dependencies

### Useful Commands

```bash
# Check container logs
docker-compose logs prometheus
docker-compose logs grafana
docker-compose logs loki

# Restart specific service
docker-compose restart prometheus

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check metrics endpoint
curl http://localhost:8080/actuator/prometheus

# View service status
docker-compose ps

# Stop monitoring stack
docker-compose down
```

### Debugging Steps

1. **Check Service Status**:
   ```bash
   docker-compose ps
   ```

2. **Check Service Logs**:
   ```bash
   docker-compose logs -f [service-name]
   ```

3. **Test Endpoints**:
   ```bash
   curl http://localhost:9090/api/v1/status/config
   curl http://localhost:3000/api/health
   curl http://localhost:3100/ready
   ```

4. **Check Metrics Endpoint**:
   ```bash
   curl http://localhost:8080/actuator/prometheus
   ```

## 📚 Resources

- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [Micrometer Documentation](https://micrometer.io/docs)
- [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)

## 🤝 Contributing

1. Add new metrics to `MetricsService.java`
2. Create dashboard JSON files
3. Update configuration files
4. Test with local development environment
5. Update documentation

## 📄 License

This monitoring setup is part of the SBOMAI project and follows the same license terms. 