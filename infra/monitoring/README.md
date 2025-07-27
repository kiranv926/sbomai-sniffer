# SBOMAI Monitoring & Observability Stack

This directory contains the complete monitoring and observability stack for SBOMAI, providing comprehensive visibility into the system's performance, security metrics, and operational health.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SBOMAI Apps   │    │   Prometheus    │    │     Grafana     │
│                 │    │                 │    │                 │
│ • Core Service  │───▶│ • Metrics Store │───▶│ • Dashboards    │
│ • Parser        │    │ • Alert Rules   │    │ • Visualizations│
│ • Scanner       │    │ • Service Disc. │    │ • Alerts        │
│ • Policy        │    └─────────────────┘    └─────────────────┘
└─────────────────┘              │
                                 │
┌─────────────────┐              │
│     Loki        │◀─────────────┘
│                 │
│ • Log Storage   │
│ • Log Querying  │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- At least 4GB RAM available
- Ports 3000, 9090, 3100, 9093 available

### Start the Monitoring Stack

```bash
# Make the startup script executable
chmod +x start-monitoring.sh

# Start the complete stack
./start-monitoring.sh
```

### Access URLs

- **Grafana Dashboard**: http://localhost:3000 (admin/sbomai2024)
- **Prometheus**: http://localhost:9090
- **Alertmanager**: http://localhost:9093
- **Loki**: http://localhost:3100

## 📊 Available Dashboards

### 1. SBOMAI Overview Dashboard
- **Location**: Automatically loaded in Grafana
- **Features**:
  - Real-time SBOM parsing metrics
  - Vulnerability scanning statistics
  - Policy enforcement overview
  - System health indicators
  - AI prediction insights

### 2. Key Metrics Tracked

#### SBOM Parsing Metrics
- Files parsed per minute
- Parse time per file
- Parser errors and failures
- SBOM format distribution (SPDX, CycloneDX)

#### Vulnerability Scanning Metrics
- CVEs found per minute
- Vulnerabilities by severity (Critical/High/Medium/Low)
- Scan duration per package
- Most vulnerable packages
- CVE source breakdown (NVD, OSV, OSS Index)

#### AI Risk Prediction Metrics
- Risk score prediction histogram
- Model confidence intervals
- Types of predicted threats
- Accuracy vs feedback

#### Policy Enforcement Metrics
- Violated rules count
- Blocked builds
- Total policy checks performed
- Custom rule hit count

#### System Health Metrics
- JVM memory & CPU usage
- Thread count
- Uptime
- HTTP request latency
- Error rates

## 🔔 Alerting

### Alert Rules

The monitoring stack includes comprehensive alerting for:

1. **Security Alerts**
   - High/Critical CVEs detected (>10)
   - Policy violations detected
   - AI model anomalies

2. **Operational Alerts**
   - Service downtime
   - High memory/CPU usage
   - Slow scan performance
   - High error rates

3. **Infrastructure Alerts**
   - Low disk space
   - Database connection issues
   - High API error rates

### Alert Channels

- **Slack**: For warnings and notifications
- **PagerDuty**: For critical alerts
- **Email**: For security team alerts
- **Webhook**: For custom integrations

## 📝 Logging

### Log Aggregation with Loki

- **Centralized Log Storage**: All SBOMAI service logs
- **Real-time Log Querying**: Using LogQL
- **Log Filtering**: By service, severity, and time
- **Log Correlation**: With metrics and traces

### Log Queries Examples

```logql
# All SBOMAI service logs
{job="sbomai"}

# Error logs only
{job="sbomai"} |= "ERROR"

# Parser service logs
{job="sbomai", service="parser"}

# High severity logs
{job="sbomai"} | json | level="ERROR"
```

## 🔧 Configuration

### Environment Variables

```bash
# OAuth Configuration (Optional)
export GITHUB_CLIENT_ID="your_github_client_id"
export GITHUB_CLIENT_SECRET="your_github_client_secret"
export GITHUB_TEAM_IDS="team1,team2"
export GITHUB_ORGS="your_org"

# Alerting Configuration
export SLACK_WEBHOOK_URL="your_slack_webhook"
export PAGERDUTY_KEY="your_pagerduty_key"
```

### Customizing Dashboards

1. **Add Custom Metrics**:
   ```java
   @Component
   public class CustomMetricsService {
       private final Counter customCounter = Counter.builder("sbomai_custom_metric")
           .description("Custom metric description")
           .register(Metrics.globalRegistry);
   }
   ```

2. **Create New Dashboards**:
   - Use Grafana UI or JSON templates
   - Place dashboard JSON files in `grafana/dashboards/`
   - They will be automatically loaded

### Scaling the Stack

For production deployments:

1. **High Availability**:
   ```yaml
   # Add to docker-compose.yml
   deploy:
     replicas: 3
     restart_policy:
       condition: on-failure
   ```

2. **Persistent Storage**:
   ```yaml
   volumes:
     - prometheus_data:/prometheus
     - grafana_data:/var/lib/grafana
     - loki_data:/loki
   ```

3. **Load Balancing**:
   - Use the provided Nginx configuration
   - Configure SSL certificates
   - Set up proper DNS

## 🛠️ Development

### Adding New Metrics

1. **Instrument Your Code**:
   ```java
   @Timed(value = "sbomai.custom.operation", description = "Custom operation timing")
   public void customOperation() {
       // Your code here
   }
   ```

2. **Create Custom Counters**:
   ```java
   private final Counter customCounter = Counter.builder("sbomai_custom_counter")
       .tag("operation", "custom")
       .description("Custom operation counter")
       .register(Metrics.globalRegistry);
   ```

3. **Add to Dashboard**:
   - Create new panels in Grafana
   - Use PromQL queries
   - Set appropriate thresholds

### Testing Alerts

```bash
# Test alert rule
curl -X POST http://localhost:9090/api/v1/query \
  -d 'query=sbomai_vulnerabilities_total{severity="critical"} > 10'

# Check alert status
curl http://localhost:9093/api/v1/alerts
```

## 🔍 Troubleshooting

### Common Issues

1. **Services Not Starting**:
   ```bash
   # Check logs
   docker-compose logs -f [service-name]
   
   # Check resource usage
   docker stats
   ```

2. **Metrics Not Appearing**:
   - Verify SBOMAI services are exposing `/actuator/prometheus`
   - Check Prometheus targets at http://localhost:9090/targets
   - Verify network connectivity

3. **Dashboard Not Loading**:
   - Check Grafana logs: `docker-compose logs grafana`
   - Verify datasource configuration
   - Check dashboard JSON syntax

### Performance Tuning

1. **Prometheus**:
   ```yaml
   command:
     - '--storage.tsdb.retention.time=30d'
     - '--storage.tsdb.path=/prometheus'
     - '--web.enable-lifecycle'
   ```

2. **Grafana**:
   ```ini
   [security]
   admin_user = admin
   admin_password = sbomai2024
   
   [server]
   http_port = 3000
   ```

3. **Loki**:
   ```yaml
   limits_config:
     reject_old_samples: true
     reject_old_samples_max_age: 168h
   ```

## 📚 Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [Micrometer Documentation](https://micrometer.io/docs)
- [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)

## 🤝 Contributing

To add new dashboards or metrics:

1. Create dashboard JSON in `grafana/dashboards/`
2. Add alert rules in `prometheus/rules/`
3. Update this README with new features
4. Test thoroughly before submitting

## 📄 License

This monitoring stack is part of the SBOMAI project and follows the same license terms. 