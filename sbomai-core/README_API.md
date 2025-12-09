# SBOM AI - Spring Boot API

This is the Spring Boot backend API for the SBOM AI project management system. It provides comprehensive CRUD operations for managing software projects, SBOM uploads, vulnerability analysis, and dependency tracking.

## Features

- ✅ **Project Management**: Complete CRUD operations for software projects
- ✅ **SBOM Upload**: File upload with Go parser integration
- ✅ **Vulnerability Analysis**: Track and analyze security vulnerabilities
- ✅ **Dependency Management**: Monitor project dependencies
- ✅ **Bulk Operations**: Efficient bulk update and delete operations
- ✅ **Statistics**: Project analytics and risk assessment
- ✅ **RESTful API**: Standard REST endpoints with proper HTTP methods
- ✅ **Database Integration**: PostgreSQL with JPA/Hibernate
- ✅ **File Upload**: Multipart file handling for SBOM files
- ✅ **CORS Support**: Cross-origin resource sharing enabled
- ✅ **Health Checks**: Application health monitoring
- ✅ **Metrics**: Prometheus metrics integration
- ✅ **Docker Support**: Containerized deployment

## Technology Stack

- **Framework**: Spring Boot 3.x
- **Database**: PostgreSQL 15
- **ORM**: Spring Data JPA / Hibernate
- **Build Tool**: Maven
- **Container**: Docker & Docker Compose
- **Monitoring**: Prometheus & Grafana
- **Caching**: Redis (optional)
- **SBOM Parser**: Go-based parser integration

## API Endpoints

### Project Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/projects` | List all projects with filtering and pagination |
| POST | `/api/v1/projects` | Create a new project |
| GET | `/api/v1/projects/{id}` | Get project details |
| PUT | `/api/v1/projects/{id}` | Update project |
| DELETE | `/api/v1/projects/{id}` | Delete project |
| POST | `/api/v1/projects/{id}/upload-sbom` | Upload SBOM file for project |
| GET | `/api/v1/projects/{id}/scans` | Get project scans |
| GET | `/api/v1/projects/{id}/vulnerabilities` | Get project vulnerabilities |
| GET | `/api/v1/projects/{id}/dependencies` | Get project dependencies |

### Bulk Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/projects/bulk-delete` | Delete multiple projects |
| PUT | `/api/v1/projects/bulk-update` | Update multiple projects |

### Statistics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/projects/stats/summary` | Get project statistics |
| GET | `/api/v1/projects/stats/high-risk` | Get high-risk projects |

## Quick Start

### Prerequisites

- Java 17 or higher
- Maven 3.6+
- PostgreSQL 15
- Docker & Docker Compose (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sbomai-core
   ```

2. **Set up PostgreSQL**
   ```bash
   # Create database
   createdb sbomai
   
   # Or use Docker
   docker run --name sbomai-postgres \
     -e POSTGRES_DB=sbomai \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=password \
     -p 5432:5432 \
     -d postgres:15-alpine
   ```

3. **Configure environment variables**
   ```bash
   export DB_USERNAME=postgres
   export DB_PASSWORD=password
   export DB_HOST=localhost
   export DB_PORT=5432
   export DB_NAME=sbomai
   ```

4. **Build and run**
   ```bash
   mvn clean install
   mvn spring-boot:run
   ```

5. **Access the API**
   - API Base URL: `http://localhost:8080/api/v1`
   - Health Check: `http://localhost:8080/api/v1/actuator/health`
   - Swagger UI: `http://localhost:8080/api/v1/swagger-ui.html`

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose -f docker-compose-api.yml up -d
   ```

2. **Access services**
   - API: `http://localhost:8080/api/v1`
   - PostgreSQL: `localhost:5432`
   - Prometheus: `http://localhost:9090`
   - Grafana: `http://localhost:3000` (admin/admin)

## Configuration

### Application Properties

```yaml
server:
  port: 8080
  servlet:
    context-path: /api/v1

spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/sbomai
    username: postgres
    password: password
    
  servlet:
    multipart:
      max-file-size: 50MB
      max-request-size: 50MB

sbomai:
  upload:
    directory: ./uploads
  parser:
    go:
      executable: ./sbomai-parser-go/sbomai-parser.exe
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `sbomai` |
| `DB_USERNAME` | Database username | `postgres` |
| `DB_PASSWORD` | Database password | `password` |
| `SBOMAI_UPLOAD_DIRECTORY` | Upload directory | `./uploads` |
| `SBOMAI_PARSER_GO_EXECUTABLE` | Go parser executable path | `./sbomai-parser-go/sbomai-parser.exe` |

## API Usage Examples

### Create a Project

```bash
curl -X POST "http://localhost:8080/api/v1/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-project",
    "description": "A sample project",
    "version": "1.0.0",
    "classifier": "Application",
    "tags": ["java", "spring"],
    "team": "Backend Team",
    "language": "Java",
    "repository": {
      "url": "https://github.com/company/my-project",
      "type": "github",
      "branch": "main"
    }
  }'
```

### List Projects

```bash
curl -X GET "http://localhost:8080/api/v1/projects?page=0&size=10&search=java&status=active"
```

### Upload SBOM

```bash
curl -X POST "http://localhost:8080/api/v1/projects/{project-id}/upload-sbom" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sbom.json"
```

### Bulk Operations

```bash
# Bulk delete
curl -X POST "http://localhost:8080/api/v1/projects/bulk-delete" \
  -H "Content-Type: application/json" \
  -d '["uuid1", "uuid2", "uuid3"]'

# Bulk update
curl -X PUT "http://localhost:8080/api/v1/projects/bulk-update" \
  -H "Content-Type: application/json" \
  -d '{
    "projectIds": ["uuid1", "uuid2"],
    "updates": {
      "status": "ARCHIVED",
      "active": false
    }
  }'
```

## Database Schema

### Projects Table

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    version VARCHAR(50) NOT NULL,
    latest_version VARCHAR(50),
    classifier VARCHAR(100) NOT NULL,
    last_bom_import TIMESTAMP,
    bom_format VARCHAR(50),
    risk_score INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT true,
    policy_violations INTEGER DEFAULT 0,
    vulnerabilities INTEGER DEFAULT 0,
    last_modified DATE,
    created_by VARCHAR(255),
    team VARCHAR(255),
    language VARCHAR(100),
    repo_url VARCHAR(500),
    repo_type VARCHAR(50),
    repo_branch VARCHAR(100),
    status VARCHAR(50) DEFAULT 'ACTIVE',
    critical_count INTEGER DEFAULT 0,
    high_count INTEGER DEFAULT 0,
    medium_count INTEGER DEFAULT 0,
    low_count INTEGER DEFAULT 0,
    dependency_count INTEGER DEFAULT 0,
    outdated_deps INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_tags (
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    tag VARCHAR(255),
    PRIMARY KEY (project_id, tag)
);
```

## Integration with Go Parser

The Spring Boot API integrates with the Go-based SBOM parser:

1. **File Upload**: SBOM files are uploaded via REST API
2. **Go Parser Execution**: The API executes the Go parser executable
3. **Result Processing**: Parsed results are stored and analyzed
4. **Vulnerability Detection**: Security vulnerabilities are identified
5. **Database Storage**: Results are persisted in PostgreSQL

### Parser Integration Flow

```
1. Client uploads SBOM file
   ↓
2. Spring Boot saves file temporarily
   ↓
3. Go parser executable is invoked
   ↓
4. Parser processes SBOM and returns JSON
   ↓
5. Spring Boot processes results
   ↓
6. Vulnerability data is stored in database
   ↓
7. Project statistics are updated
```

## Monitoring and Health Checks

### Health Endpoints

- **Application Health**: `GET /api/v1/actuator/health`
- **Database Health**: `GET /api/v1/actuator/health/db`
- **Disk Space**: `GET /api/v1/actuator/health/diskSpace`

### Metrics

- **Prometheus Metrics**: `GET /api/v1/actuator/prometheus`
- **Application Metrics**: `GET /api/v1/actuator/metrics`

### Grafana Dashboards

The application includes pre-configured Grafana dashboards for:
- Project statistics
- Vulnerability trends
- API performance metrics
- Database performance

## Development

### Project Structure

```
src/main/java/com/sbomai/core/
├── SbomaiCoreApplication.java
├── config/
│   └── WebConfig.java
├── controller/
│   └── ProjectController.java
├── domain/
│   ├── Project.java
│   ├── ProjectStatus.java
│   ├── RepositoryInfo.java
│   └── VulnerabilityCount.java
├── dto/
│   ├── ProjectDto.java
│   ├── RepositoryDto.java
│   └── VulnerabilityCountDto.java
├── repository/
│   └── ProjectRepository.java
└── service/
    ├── ProjectService.java
    ├── SbomParserService.java
    └── impl/
        └── ProjectServiceImpl.java
```

### Adding New Features

1. **Domain Model**: Create entity in `domain/` package
2. **DTO**: Create DTO in `dto/` package
3. **Repository**: Create repository interface in `repository/` package
4. **Service**: Create service interface and implementation
5. **Controller**: Add REST endpoints in controller
6. **Tests**: Write unit and integration tests

### Testing

```bash
# Run all tests
mvn test

# Run specific test
mvn test -Dtest=ProjectServiceTest

# Run integration tests
mvn verify
```

## Deployment

### Production Deployment

1. **Build Docker image**
   ```bash
   docker build -t sbomai-api:latest .
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose-api.yml up -d
   ```

3. **Environment-specific configuration**
   ```bash
   # Production environment
   export SPRING_PROFILES_ACTIVE=production
   export DB_HOST=production-db-host
   export DB_PASSWORD=secure-password
   ```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sbomai-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sbomai-api
  template:
    metadata:
      labels:
        app: sbomai-api
    spec:
      containers:
      - name: sbomai-api
        image: sbomai-api:latest
        ports:
        - containerPort: 8080
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: host
```

## Troubleshooting

### Common Issues

1. **Database Connection**
   ```bash
   # Check database connectivity
   psql -h localhost -U postgres -d sbomai
   ```

2. **Go Parser Issues**
   ```bash
   # Test parser executable
   ./sbomai-parser-go/sbomai-parser.exe --help
   ```

3. **File Upload Issues**
   ```bash
   # Check upload directory permissions
   ls -la ./uploads
   chmod 755 ./uploads
   ```

### Logs

```bash
# View application logs
docker logs sbomai-api

# View database logs
docker logs sbomai-postgres

# View real-time logs
docker-compose -f docker-compose-api.yml logs -f
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation 