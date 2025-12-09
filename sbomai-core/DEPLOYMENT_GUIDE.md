# SBOM AI Spring Boot API - Deployment Guide

This guide provides step-by-step instructions for deploying the SBOM AI Spring Boot API in various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Configuration](#configuration)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Java 17** or higher
- **Maven 3.6+**
- **PostgreSQL 15**
- **Docker & Docker Compose** (for containerized deployment)
- **Go Parser Executable** (`sbomai-parser-go/sbomai-parser.exe`)

### System Requirements

- **Memory**: Minimum 2GB RAM, Recommended 4GB+
- **Storage**: Minimum 10GB free space
- **CPU**: 2+ cores recommended
- **Network**: Internet access for dependencies

## Local Development Setup

### 1. Database Setup

#### Option A: Local PostgreSQL

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE sbomai;
CREATE USER sbomai_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE sbomai TO sbomai_user;
\q
```

#### Option B: Docker PostgreSQL

```bash
# Run PostgreSQL in Docker
docker run --name sbomai-postgres \
  -e POSTGRES_DB=sbomai \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -d postgres:15-alpine
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sbomai
DB_USERNAME=postgres
DB_PASSWORD=password

# Application Configuration
SPRING_PROFILES_ACTIVE=local
SBOMAI_UPLOAD_DIRECTORY=./uploads
SBOMAI_PARSER_GO_EXECUTABLE=../sbomai-parser-go/sbomai-parser.exe

# Server Configuration
SERVER_PORT=8080
```

### 3. Build and Run

#### Windows
```cmd
# Run the startup script
start-api.bat
```

#### Linux/Mac
```bash
# Make script executable
chmod +x start-api.sh

# Run the startup script
./start-api.sh
```

#### Manual Build
```bash
# Build the project
mvn clean install

# Run the application
mvn spring-boot:run
```

### 4. Verify Installation

```bash
# Check application health
curl http://localhost:8080/api/v1/actuator/health

# Check parser health
curl http://localhost:8080/api/v1/health/parser

# List projects
curl http://localhost:8080/api/v1/projects
```

## Docker Deployment

### 1. Quick Start with Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd sbomai-core

# Start all services
docker-compose -f docker-compose-api.yml up -d

# Check service status
docker-compose -f docker-compose-api.yml ps

# View logs
docker-compose -f docker-compose-api.yml logs -f sbomai-api
```

### 2. Custom Docker Deployment

#### Build Docker Image

```bash
# Build the image
docker build -t sbomai-api:latest .

# Run the container
docker run -d \
  --name sbomai-api \
  -p 8080:8080 \
  -e DB_HOST=your-db-host \
  -e DB_PASSWORD=your-db-password \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/../sbomai-parser-go:/app/sbomai-parser-go \
  sbomai-api:latest
```

#### Docker Compose with Custom Configuration

```yaml
version: '3.8'

services:
  sbomai-api:
    build: .
    container_name: sbomai-api
    environment:
      - SPRING_PROFILES_ACTIVE=docker
      - DB_HOST=postgres
      - DB_PASSWORD=${DB_PASSWORD}
      - SBOMAI_UPLOAD_DIRECTORY=/app/uploads
    ports:
      - "8080:8080"
    volumes:
      - ./uploads:/app/uploads
      - ../sbomai-parser-go:/app/sbomai-parser-go
    depends_on:
      - postgres
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=sbomai
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
```

## Production Deployment

### 1. Environment Preparation

#### Security Considerations

```bash
# Create dedicated user
sudo useradd -r -s /bin/false sbomai

# Create application directory
sudo mkdir -p /opt/sbomai
sudo chown sbomai:sbomai /opt/sbomai

# Set up SSL certificates
sudo mkdir -p /etc/ssl/sbomai
sudo chmod 700 /etc/ssl/sbomai
```

#### Database Setup

```sql
-- Create production database
CREATE DATABASE sbomai_prod;

-- Create dedicated user with limited privileges
CREATE USER sbomai_prod WITH PASSWORD 'strong_password_here';
GRANT CONNECT ON DATABASE sbomai_prod TO sbomai_prod;
GRANT USAGE ON SCHEMA public TO sbomai_prod;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO sbomai_prod;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO sbomai_prod;
```

### 2. Application Configuration

#### Production Properties

Create `application-prod.yml`:

```yaml
server:
  port: 8080
  ssl:
    enabled: true
    key-store: /etc/ssl/sbomai/keystore.p12
    key-store-password: ${SSL_KEYSTORE_PASSWORD}
    key-store-type: PKCS12

spring:
  profiles:
    active: prod
  datasource:
    url: jdbc:postgresql://${DB_HOST}:${DB_PORT}/${DB_NAME}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect

logging:
  level:
    com.sbomai.core: INFO
    org.springframework.web: WARN
  file:
    name: /var/log/sbomai/application.log
    max-size: 100MB
    max-history: 30

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: never
```

### 3. Systemd Service

Create `/etc/systemd/system/sbomai-api.service`:

```ini
[Unit]
Description=SBOM AI Spring Boot API
After=network.target postgresql.service

[Service]
Type=simple
User=sbomai
Group=sbomai
WorkingDirectory=/opt/sbomai
ExecStart=/usr/bin/java -jar sbomai-core.jar
Environment="SPRING_PROFILES_ACTIVE=prod"
Environment="DB_HOST=localhost"
Environment="DB_PASSWORD=your_secure_password"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable sbomai-api

# Start service
sudo systemctl start sbomai-api

# Check status
sudo systemctl status sbomai-api
```

### 4. Nginx Reverse Proxy

Create `/etc/nginx/sites-available/sbomai-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/sbomai/cert.pem;
    ssl_certificate_key /etc/ssl/sbomai/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DB_HOST` | Database host | `localhost` | Yes |
| `DB_PORT` | Database port | `5432` | No |
| `DB_NAME` | Database name | `sbomai` | Yes |
| `DB_USERNAME` | Database username | `postgres` | Yes |
| `DB_PASSWORD` | Database password | - | Yes |
| `SBOMAI_UPLOAD_DIRECTORY` | Upload directory | `./uploads` | No |
| `SBOMAI_PARSER_GO_EXECUTABLE` | Go parser path | `./sbomai-parser-go/sbomai-parser.exe` | No |
| `SPRING_PROFILES_ACTIVE` | Spring profile | `local` | No |
| `SERVER_PORT` | Application port | `8080` | No |

### Application Properties

Key configuration options in `application.yml`:

```yaml
# File upload limits
spring:
  servlet:
    multipart:
      max-file-size: 50MB
      max-request-size: 50MB

# Database connection pool
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5

# Logging configuration
logging:
  level:
    com.sbomai.core: INFO
  file:
    name: /var/log/sbomai/application.log

# Metrics and monitoring
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
```

## Monitoring

### 1. Health Checks

```bash
# Application health
curl http://localhost:8080/api/v1/actuator/health

# Parser health
curl http://localhost:8080/api/v1/health/parser

# System health
curl http://localhost:8080/api/v1/health/system
```

### 2. Prometheus Metrics

```bash
# Prometheus metrics endpoint
curl http://localhost:8080/api/v1/actuator/prometheus

# Application metrics
curl http://localhost:8080/api/v1/actuator/metrics
```

### 3. Log Monitoring

```bash
# View application logs
tail -f /var/log/sbomai/application.log

# View systemd logs
journalctl -u sbomai-api -f

# View Docker logs
docker logs -f sbomai-api
```

### 4. Database Monitoring

```sql
-- Check database connections
SELECT count(*) FROM pg_stat_activity WHERE datname = 'sbomai';

-- Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables WHERE schemaname = 'public' ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test database connection
psql -h localhost -U postgres -d sbomai

# Check connection pool
curl http://localhost:8080/api/v1/actuator/health/db
```

#### 2. Go Parser Issues

```bash
# Test parser executable
./sbomai-parser-go/sbomai-parser.exe --help

# Check parser health
curl http://localhost:8080/api/v1/health/parser

# Check file permissions
ls -la ../sbomai-parser-go/sbomai-parser.exe
```

#### 3. File Upload Issues

```bash
# Check upload directory permissions
ls -la ./uploads

# Check disk space
df -h

# Check file size limits
curl -X POST http://localhost:8080/api/v1/projects/{id}/upload-sbom \
  -F "file=@large-file.json"
```

#### 4. Memory Issues

```bash
# Check memory usage
free -h

# Check Java heap
jstat -gc <pid>

# Increase heap size
java -Xmx2g -jar sbomai-core.jar
```

### Performance Tuning

#### 1. Database Optimization

```sql
-- Analyze tables
ANALYZE projects;
ANALYZE project_tags;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes ORDER BY idx_scan DESC;
```

#### 2. JVM Tuning

```bash
# Production JVM options
java -server \
  -Xms1g \
  -Xmx2g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -jar sbomai-core.jar
```

#### 3. Connection Pool Tuning

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
```

### Support and Maintenance

#### 1. Backup Strategy

```bash
# Database backup
pg_dump -h localhost -U postgres sbomai > backup_$(date +%Y%m%d_%H%M%S).sql

# Application backup
tar -czf sbomai_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  /opt/sbomai \
  /var/log/sbomai \
  /etc/ssl/sbomai
```

#### 2. Update Procedure

```bash
# Stop service
sudo systemctl stop sbomai-api

# Backup current version
cp sbomai-core.jar sbomai-core.jar.backup

# Deploy new version
cp new-sbomai-core.jar sbomai-core.jar

# Start service
sudo systemctl start sbomai-api

# Verify deployment
curl http://localhost:8080/api/v1/actuator/health
```

#### 3. Rollback Procedure

```bash
# Stop service
sudo systemctl stop sbomai-api

# Restore backup
cp sbomai-core.jar.backup sbomai-core.jar

# Start service
sudo systemctl start sbomai-api

# Verify rollback
curl http://localhost:8080/api/v1/actuator/health
```

## Security Considerations

### 1. Network Security

- Use HTTPS in production
- Configure firewall rules
- Implement rate limiting
- Use reverse proxy (Nginx)

### 2. Database Security

- Use strong passwords
- Limit database user privileges
- Enable SSL connections
- Regular security updates

### 3. Application Security

- Validate all inputs
- Implement proper error handling
- Use secure file upload validation
- Regular dependency updates

### 4. Monitoring Security

- Secure monitoring endpoints
- Implement access controls
- Monitor for suspicious activity
- Regular security audits

## Conclusion

This deployment guide provides comprehensive instructions for deploying the SBOM AI Spring Boot API in various environments. Follow the security best practices and monitor the application regularly to ensure optimal performance and security.

For additional support, refer to the main README file or create an issue in the project repository. 