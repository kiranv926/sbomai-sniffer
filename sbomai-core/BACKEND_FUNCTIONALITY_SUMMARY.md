# SBOMAI Core Backend Functionality Summary

## Overview

This document provides a comprehensive summary of the backend functionality implemented in `sbomai-core` to support the `sbomai-ui` frontend application. The backend provides a complete REST API for project management, vulnerability analysis, scanning, AI-powered insights, and dashboard functionality.

## Architecture

The backend follows a layered architecture pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                    Controllers Layer                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │   Project   │ │Vulnerability│ │    Scan     │ │   AI    │ │
│  │ Controller  │ │ Controller  │ │ Controller  │ │Controller│ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                     Services Layer                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │   Project   │ │Vulnerability│ │    Scan     │ │   AI    │ │
│  │  Service    │ │  Service    │ │  Service    │ │ Service │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   Repository Layer                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │   Project   │ │Vulnerability│ │    Scan     │ │   AI    │ │
│  │ Repository  │ │ Repository  │ │ Repository  │ │Repository│ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Domain Layer                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │   Project   │ │Vulnerability│ │    Scan     │ │   AI    │ │
│  │   Entity    │ │   Entity    │ │   Entity    │ │ Entity  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Core Services

### 1. Project Management Service

**Purpose:** Manages software projects, their metadata, and associated SBOMs.

**Key Features:**
- CRUD operations for projects
- Project search and filtering
- SBOM file upload and processing
- Project statistics and metrics
- Bulk operations (update, delete)
- Team and repository management

**API Endpoints:**
- `GET /api/v1/projects` - List projects with filtering
- `POST /api/v1/projects` - Create new project
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project
- `POST /api/v1/projects/{id}/upload-sbom` - Upload SBOM file
- `GET /api/v1/projects/{id}/scans` - Get project scans
- `GET /api/v1/projects/{id}/vulnerabilities` - Get project vulnerabilities
- `GET /api/v1/projects/{id}/dependencies` - Get project dependencies

**Data Models:**
- `Project` - Core project entity
- `ProjectDto` - API request/response DTO
- `RepositoryInfo` - Repository metadata
- `VulnerabilityCount` - Vulnerability statistics

### 2. Vulnerability Management Service

**Purpose:** Manages security vulnerabilities, their analysis, and remediation.

**Key Features:**
- Vulnerability tracking and categorization
- CVE/CWE integration
- Severity-based filtering
- Vulnerability statistics and trends
- Bulk operations
- Component and project association

**API Endpoints:**
- `GET /api/v1/vulnerabilities` - List vulnerabilities
- `GET /api/v1/vulnerabilities/{id}` - Get vulnerability details
- `POST /api/v1/vulnerabilities` - Create vulnerability
- `PUT /api/v1/vulnerabilities/{id}` - Update vulnerability
- `DELETE /api/v1/vulnerabilities/{id}` - Delete vulnerability
- `GET /api/v1/vulnerabilities/statistics` - Get vulnerability statistics
- `GET /api/v1/vulnerabilities/trends` - Get vulnerability trends
- `GET /api/v1/vulnerabilities/cve/{cveId}` - Get by CVE ID
- `GET /api/v1/vulnerabilities/severity/{severity}` - Filter by severity

**Data Models:**
- `Vulnerability` - Core vulnerability entity
- `VulnerabilityDto` - API request/response DTO
- `VulnerabilityStatistics` - Statistics record
- `VulnerabilityTrend` - Trend data record

### 3. Scan Management Service

**Purpose:** Manages SBOM scanning, analysis, and processing workflows.

**Key Features:**
- Scan creation and execution
- Real-time scan progress tracking
- Scan results and logs
- Scan statistics and trends
- Retry mechanisms for failed scans
- Multiple scan types (SBOM, Vulnerability, Policy, Comprehensive)

**API Endpoints:**
- `GET /api/v1/scans` - List scans
- `GET /api/v1/scans/{id}` - Get scan details
- `POST /api/v1/scans` - Create scan
- `PUT /api/v1/scans/{id}` - Update scan
- `DELETE /api/v1/scans/{id}` - Delete scan
- `POST /api/v1/scans/{id}/start` - Start scan
- `POST /api/v1/scans/{id}/stop` - Stop scan
- `GET /api/v1/scans/{id}/status` - Get scan status
- `GET /api/v1/scans/{id}/progress` - Get scan progress
- `GET /api/v1/scans/{id}/results` - Get scan results
- `GET /api/v1/scans/statistics` - Get scan statistics

**Data Models:**
- `Scan` - Core scan entity
- `ScanDto` - API request/response DTO
- `ScanProgress` - Progress tracking record
- `ScanResults` - Results data record
- `ScanStatistics` - Statistics record

### 4. AI Service

**Purpose:** Provides AI-powered analysis, recommendations, and insights.

**Key Features:**
- SBOM analysis with AI models
- Vulnerability risk assessment
- AI-generated recommendations
- Trend analysis and predictions
- Model management and performance tracking
- Dashboard insights generation

**API Endpoints:**
- `POST /api/v1/ai/analyze-sbom` - Analyze SBOM with AI
- `GET /api/v1/ai/analysis/{analysisId}` - Get AI analysis
- `GET /api/v1/ai/recommendations/project/{projectId}` - Get project recommendations
- `GET /api/v1/ai/recommendations/vulnerability/{vulnerabilityId}` - Get vulnerability recommendations
- `GET /api/v1/ai/recommendations/portfolio` - Get portfolio recommendations
- `GET /api/v1/ai/dashboard-insights` - Generate dashboard insights
- `GET /api/v1/ai/risk-assessment/{projectId}` - Get risk assessment
- `GET /api/v1/ai/trend-analysis` - Get trend analysis
- `GET /api/v1/ai/model-status` - Get model status
- `GET /api/v1/ai/model-performance` - Get model performance

**Data Models:**
- `AIAnalysis` - AI analysis entity
- `AIAnalysisDto` - API request/response DTO
- `AIRecommendation` - Recommendation entity
- `AIRecommendationDto` - API request/response DTO

### 5. Dashboard Service

**Purpose:** Provides aggregated data and metrics for dashboard visualization.

**Key Features:**
- Summary statistics
- Trend data generation
- Project coverage metrics
- Security metrics
- Recent activity tracking
- Alert management
- Compliance status
- Performance metrics

**API Endpoints:**
- `GET /api/v1/dashboard/summary` - Get dashboard summary
- `GET /api/v1/dashboard/trends` - Get dashboard trends
- `GET /api/v1/dashboard/project-coverage` - Get project coverage
- `GET /api/v1/dashboard/at-risk-repos` - Get at-risk repositories
- `GET /api/v1/dashboard/ai-recommendations` - Get AI recommendations
- `GET /api/v1/dashboard/security-metrics` - Get security metrics
- `GET /api/v1/dashboard/recent-activity` - Get recent activity
- `GET /api/v1/dashboard/alerts` - Get alerts
- `GET /api/v1/dashboard/compliance-status` - Get compliance status
- `GET /api/v1/dashboard/performance-metrics` - Get performance metrics

**Data Models:**
- `DashboardSummary` - Summary statistics record
- `TrendData` - Trend data record
- `ProjectCoverage` - Coverage metrics record
- `SecurityMetrics` - Security metrics record
- `RecentActivity` - Activity record
- `Alert` - Alert record

## Integration with Frontend

### API Contract Alignment

The backend API is designed to match the frontend requirements identified in the UI analysis:

1. **Projects Page Requirements:**
   - ✅ Project listing with search and filtering
   - ✅ Project creation and editing
   - ✅ SBOM upload functionality
   - ✅ Project statistics and metrics
   - ✅ Bulk operations

2. **Dashboard Page Requirements:**
   - ✅ Summary statistics cards
   - ✅ Trend charts and graphs
   - ✅ Project coverage visualization
   - ✅ AI recommendations
   - ✅ Security metrics
   - ✅ Recent activity feed

3. **Vulnerabilities Page Requirements:**
   - ✅ Vulnerability listing with filtering
   - ✅ Severity-based categorization
   - ✅ CVE/CWE information
   - ✅ Vulnerability statistics
   - ✅ Bulk operations

4. **AI Features Requirements:**
   - ✅ AI-powered analysis
   - ✅ Risk assessments
   - ✅ Recommendations
   - ✅ Trend predictions
   - ✅ Model management

### Data Flow

```
Frontend (sbomai-ui) → API Gateway → Backend Services → Database
     ↓                    ↓              ↓              ↓
  React Components   REST Controllers  Business Logic  PostgreSQL
  TypeScript         Spring Boot       Java Services   H2 (dev)
  Axios Client       JSON Responses    JPA Entities    JPA Repositories
```

## Technology Stack

### Backend Technologies
- **Framework:** Spring Boot 3.2.0
- **Language:** Java 21
- **Database:** PostgreSQL (production), H2 (development)
- **ORM:** Spring Data JPA with Hibernate
- **Build Tool:** Maven
- **Containerization:** Docker
- **API Documentation:** OpenAPI/Swagger

### Key Dependencies
- Spring Boot Starter Web
- Spring Boot Starter Data JPA
- Spring Boot Starter Validation
- Spring Boot Starter Actuator
- Jackson for JSON processing
- SLF4J for logging

## Database Schema

The backend includes a comprehensive database schema with the following main entities:

1. **Projects** - Core project information
2. **Vulnerabilities** - Security vulnerability data
3. **Scans** - Scan execution and results
4. **SBOM Documents** - SBOM file storage and metadata
5. **SBOM Components** - Component information from SBOMs
6. **AI Analysis Results** - AI analysis data
7. **Policy Violations** - Policy compliance data

## Security Features

1. **Authentication:** Bearer token support
2. **Authorization:** Role-based access control (framework ready)
3. **Input Validation:** Comprehensive validation using Bean Validation
4. **CORS:** Cross-origin resource sharing configuration
5. **Rate Limiting:** API rate limiting (framework ready)
6. **Audit Logging:** Comprehensive logging for security events

## Monitoring and Observability

1. **Health Checks:** Application and component health endpoints
2. **Metrics:** Prometheus metrics integration
3. **Logging:** Structured logging with SLF4J
4. **Tracing:** Distributed tracing support (framework ready)
5. **Actuator:** Spring Boot Actuator for monitoring

## Deployment

### Local Development
```bash
# Start the application
cd sbomai-core
mvn spring-boot:run

# Access the API
curl http://localhost:8081/api/v1/health
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose -f docker-compose-api.yml up -d
```

### Production Deployment
- Systemd service configuration
- Nginx reverse proxy
- PostgreSQL database
- Redis for caching
- Prometheus for monitoring
- Grafana for visualization

## Testing

The backend includes comprehensive testing support:

1. **Unit Tests:** Service layer testing
2. **Integration Tests:** API endpoint testing
3. **Repository Tests:** Data access layer testing
4. **Test Data:** Sample data for development

## API Documentation

Complete API documentation is available at:
- **Swagger UI:** `http://localhost:8081/swagger-ui.html`
- **OpenAPI Spec:** `http://localhost:8081/v3/api-docs`
- **Markdown Docs:** `API_DOCUMENTATION.md`

## Future Enhancements

1. **Real-time Updates:** WebSocket support for live updates
2. **Advanced AI:** Integration with more AI models
3. **Workflow Engine:** Complex scanning workflows
4. **Plugin System:** Extensible architecture for custom analyzers
5. **Multi-tenancy:** Support for multiple organizations
6. **Advanced Analytics:** Machine learning for pattern detection

## Conclusion

The SBOMAI Core backend provides a comprehensive, production-ready API that fully supports the sbomai-ui frontend requirements. The architecture is scalable, maintainable, and follows industry best practices. The API is well-documented, tested, and ready for integration with the frontend application.

The backend successfully addresses all the requirements identified in the UI analysis:
- ✅ Complete project management functionality
- ✅ Comprehensive vulnerability tracking
- ✅ Advanced scanning capabilities
- ✅ AI-powered analysis and recommendations
- ✅ Rich dashboard and reporting features
- ✅ Robust API with proper error handling
- ✅ Security and monitoring features
- ✅ Production-ready deployment options 