# SBOMAI Monitoring & Observability Stack

This directory contains the complete monitoring and observability setup for SBOMAI using Grafana, Prometheus, and Loki.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SBOMAI Apps   │    │   Prometheus    │    │     Grafana     │
│                 │    │                 │    │                 │
│ • Core (8080)   │───▶│ • Metrics       │───▶│ • Dashboards    │
│ • Parser (8081) │    │ • Scraping      │    │ • Visualization │
│ • VulnScan      │    │ • Storage       │    │ • Alerts        │
│ • Policy (8083) │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Promtail    │    │      Loki       │    │   AlertManager  │
│                 │    │                 │    │                 │
│ • Log Collection│───▶│ • Log Storage   │───▶│ • Notifications │
│ • Log Parsing   │    │ • Log Querying  │    │ • Slack/Email   │
│ • Log Shipping  │    │ • Log Retention │    │ • PagerDuty     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Start the Monitoring Stack

```bash
# Start all monitoring services
docker-compose up -d

# Check service status
docker-compose ps
```

### 2. Access the Services

- **Grafana**: http://localhost:3000 (admin/sbomai2024)
- **Prometheus**: http://localhost:9090
- **Loki**: http://localhost:3100

### 3. Import Dashboards

1. Open Grafana at http://localhost:3000
2. Login with `admin` / `sbomai2024`
3. Navigate to Dashboards → Import
4. Import the dashboard JSON files from `grafana/dashboards/`

## 📊 Available Dashboards

### 1. SBOMAI Overview Dashboard
- **File**: `grafana/dashboards/sbomai-overview.json`
- **Description**: Main dashboard with key metrics across all modules
- **Panels**:
  - SBOM Files Parsed per Minute
  - SBOM Format Distribution (Pie Chart)
  - 95th Percentile Parse Time
  - CVEs Found per Minute
  - CVEs by Severity (Pie Chart)
  - Policy Violations per Minute
  - AI Analysis Requests per Minute
  - 95th Percentile AI Analysis Time
  - Key Statistics (Total Projects, Success Rate, CVEs, Violations)

### 2. System Health Dashboard
- **File**: `grafana/dashboards/system-health.json` (to be created)
- **Description**: System-level metrics and health indicators

### 3. Vulnerability Analysis Dashboard
- **File**: `grafana/dashboards/vulnerability-analysis.json` (to be created)
- **Description**: Detailed vulnerability scanning metrics

## 🔧 Configuration

### Prometheus Configuration
- **File**: `prometheus/prometheus.yml`
- **Scrape Interval**: 15s (global), 10s (SBOMAI services)
- **Targets**: All SBOMAI modules on different ports

### Grafana Configuration
- **Datasources**: Auto-configured via `grafana/provisioning/datasources/`
- **Dashboards**: Auto-loaded via `grafana/provisioning/dashboards/`
- **Plugins**: Clock panel, Simple JSON datasource

### Loki Configuration
- **File**: `loki/loki-config.yml`
- **Retention**: 168 hours (7 days)
- **Storage**: Local filesystem

## 📈 Metrics Collected

### SBOM Parser Metrics
- `sbomai_parser_files_parsed_total` - Total files parsed
- `sbomai_parser_parse_duration_seconds` - Parse time histogram
- `sbomai_parser_format_distribution` - Format breakdown
- `sbomai_parser_errors_total` - Parse errors

### Vulnerability Scanner Metrics
- `sbomai_vulnscan_cves_found_total` - Total CVEs found
- `sbomai_vulnscan_cves_by_severity` - CVE severity distribution
- `sbomai_vulnscan_scan_duration_seconds` - Scan time histogram
- `sbomai_scanner_errors_total` - Scanner errors

### AI Analysis Metrics
- `sbomai_ai_analysis_requests_total` - AI analysis requests
- `sbomai_ai_analysis_duration_seconds` - Analysis time histogram
- `sbomai_ai_analysis_errors_total` - AI analysis errors

### Policy Enforcement Metrics
- `sbomai_policy_violations_total` - Policy violations
- `sbomai_policy_enforcement_duration_seconds` - Enforcement time
- `sbomai_total_policy_violations` - Total violations

### System Metrics
- `sbomai_total_projects_scanned` - Total projects
- `sbomai_success_rate` - Success rate percentage
- `sbomai_total_cves_found` - Total CVEs found

## 🚨 Alerting

### Pre-configured Alerts
1. **High Error Rate**: Alert when error rate > 5%
2. **Slow Response Time**: Alert when 95th percentile > 30s
3. **Critical CVEs**: Alert when critical CVEs found
4. **Service Down**: Alert when metrics stop flowing

### Alert Channels
- Slack notifications
- Email alerts
- PagerDuty integration
- Webhook notifications

## 🔍 Logging

### Log Sources
- SBOMAI application logs
- Docker container logs
- System logs
- Access logs

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

1. Create JSON file in `grafana/dashboards/`
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
```

## 🔧 Troubleshooting

### Common Issues

1. **Prometheus can't scrape targets**:
   - Check if SBOMAI services are running
   - Verify ports in `prometheus.yml`
   - Check firewall settings

2. **Grafana can't connect to Prometheus**:
   - Verify Prometheus is running on port 9090
   - Check datasource configuration
   - Restart Grafana container

3. **No metrics appearing**:
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
3. Update this README
4. Test with local development environment

## 📄 License

This monitoring setup is part of the SBOMAI project and follows the same license terms. 