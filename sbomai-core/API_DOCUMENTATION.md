# SBOMAI Core API Documentation

## Overview

The SBOMAI Core API provides comprehensive backend functionality for the SBOMAI platform, supporting project management, vulnerability analysis, scanning, AI-powered insights, and dashboard functionality.

## Base URL

```
http://localhost:8081/api/v1
```

## Authentication

All endpoints support Bearer token authentication:

```
Authorization: Bearer <token>
```

## API Endpoints

### 1. Projects Management

#### GET /projects
List all projects with filtering and pagination.

**Query Parameters:**
- `search` (optional): Search term for project name, description, or tags
- `status` (optional): Filter by project status (active, archived, deprecated)
- `team` (optional): Filter by team
- `sortBy` (optional, default: "name"): Sort field
- `sortOrder` (optional, default: "asc"): Sort direction (asc, desc)
- `page` (optional, default: 0): Page number
- `size` (optional, default: 10): Page size

**Response:**
```json
{
  "content": [
    {
      "id": "uuid",
      "name": "project-name",
      "description": "Project description",
      "version": "1.0.0",
      "classifier": "Application",
      "active": true,
      "riskScore": 75,
      "vulnerabilities": 5,
      "policyViolations": 2,
      "tags": ["frontend", "react"],
      "repository": {
        "url": "https://github.com/org/repo",
        "type": "github",
        "branch": "main"
      },
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-01-15T10:30:00Z"
    }
  ],
  "totalElements": 100,
  "totalPages": 10,
  "size": 10,
  "number": 0
}
```

#### POST /projects
Create a new project.

**Request Body:**
```json
{
  "name": "project-name",
  "description": "Project description",
  "version": "1.0.0",
  "classifier": "Application",
  "tags": ["frontend", "react"],
  "team": "Engineering",
  "language": "JavaScript",
  "repository": {
    "url": "https://github.com/org/repo",
    "type": "github",
    "branch": "main"
  }
}
```

#### GET /projects/{id}
Get project details by ID.

#### PUT /projects/{id}
Update project by ID.

#### DELETE /projects/{id}
Delete project by ID.

#### GET /projects/{id}/scans
Get scans for a project.

#### GET /projects/{id}/vulnerabilities
Get vulnerabilities for a project.

#### GET /projects/{id}/dependencies
Get dependencies for a project.

#### POST /projects/{id}/upload-sbom
Upload SBOM file for a project.

**Request:** Multipart form data with file

**Response:**
```json
{
  "projectId": "uuid",
  "uploadId": "uuid",
  "status": "processing",
  "processedComponents": 150,
  "vulnerabilitiesFound": 5
}
```

#### PUT /projects/bulk-update
Bulk update projects.

#### DELETE /projects/bulk-delete
Bulk delete projects.

#### GET /projects/statistics
Get project statistics.

### 2. Vulnerabilities Management

#### GET /vulnerabilities
List all vulnerabilities with filtering and pagination.

**Query Parameters:**
- `search` (optional): Search term
- `severity` (optional): Filter by severity (CRITICAL, HIGH, MEDIUM, LOW, NONE)
- `status` (optional): Filter by status (OPEN, FIXED, IGNORED)
- `cwe` (optional): Filter by CWE ID
- `sortBy` (optional, default: "createdDate"): Sort field
- `sortOrder` (optional, default: "desc"): Sort direction
- `page` (optional, default: 0): Page number
- `size` (optional, default: 20): Page size

**Response:**
```json
{
  "content": [
    {
      "id": "uuid",
      "cveId": "CVE-2024-1234",
      "title": "Vulnerability Title",
      "description": "Vulnerability description",
      "severity": "HIGH",
      "cvssScore": 8.5,
      "cvssVector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
      "cweIds": ["CWE-89", "CWE-74"],
      "affectedVersions": ["1.0.0", "1.1.0"],
      "fixedVersions": ["1.2.0"],
      "source": "NVD",
      "publishedDate": "2024-01-15T10:30:00Z",
      "componentName": "component-name",
      "projectName": "project-name",
      "status": "OPEN"
    }
  ],
  "totalElements": 500,
  "totalPages": 25,
  "size": 20,
  "number": 0
}
```

#### GET /vulnerabilities/{id}
Get vulnerability by ID.

#### POST /vulnerabilities
Create new vulnerability.

#### PUT /vulnerabilities/{id}
Update vulnerability.

#### DELETE /vulnerabilities/{id}
Delete vulnerability.

#### GET /vulnerabilities/project/{projectId}
Get vulnerabilities by project.

#### GET /vulnerabilities/component/{componentId}
Get vulnerabilities by component.

#### GET /vulnerabilities/statistics
Get vulnerability statistics.

**Response:**
```json
{
  "totalVulnerabilities": 1500,
  "criticalCount": 50,
  "highCount": 200,
  "mediumCount": 500,
  "lowCount": 750,
  "openCount": 1200,
  "fixedCount": 250,
  "ignoredCount": 50,
  "averageCvssScore": 6.8,
  "projectsAffected": 25
}
```

#### GET /vulnerabilities/trends
Get vulnerability trends.

#### GET /vulnerabilities/cve/{cveId}
Get vulnerability by CVE ID.

#### GET /vulnerabilities/severity/{severity}
Get vulnerabilities by severity.

#### GET /vulnerabilities/cwe/{cwe}
Get vulnerabilities by CWE.

#### PUT /vulnerabilities/bulk-update
Bulk update vulnerabilities.

#### DELETE /vulnerabilities/bulk-delete
Bulk delete vulnerabilities.

### 3. Scans Management

#### GET /scans
List all scans with filtering and pagination.

**Query Parameters:**
- `search` (optional): Search term
- `status` (optional): Filter by status
- `scanType` (optional): Filter by scan type
- `projectId` (optional): Filter by project ID
- `sortBy` (optional, default: "createdAt"): Sort field
- `sortOrder` (optional, default: "desc"): Sort direction
- `page` (optional, default: 0): Page number
- `size` (optional, default: 20): Page size

**Response:**
```json
{
  "content": [
    {
      "id": "uuid",
      "projectName": "project-name",
      "projectId": "uuid",
      "sourcePath": "/path/to/source",
      "sourceType": "FILE",
      "status": "COMPLETED",
      "scanType": "SBOM",
      "riskScore": 75.5,
      "vulnerabilitiesFound": 5,
      "createdAt": "2024-01-15T10:30:00Z",
      "startedAt": "2024-01-15T10:30:00Z",
      "completedAt": "2024-01-15T10:35:00Z",
      "scanDurationMs": 300000
    }
  ],
  "totalElements": 200,
  "totalPages": 10,
  "size": 20,
  "number": 0
}
```

#### GET /scans/{id}
Get scan by ID.

#### POST /scans
Create new scan.

#### PUT /scans/{id}
Update scan.

#### DELETE /scans/{id}
Delete scan.

#### POST /scans/{id}/start
Start a scan.

#### POST /scans/{id}/stop
Stop a scan.

#### GET /scans/{id}/status
Get scan status.

#### GET /scans/{id}/progress
Get scan progress.

**Response:**
```json
{
  "scanId": "uuid",
  "status": "IN_PROGRESS",
  "progressPercentage": 65,
  "currentStep": "Analyzing components",
  "estimatedTimeRemaining": "2 minutes",
  "processedItems": 130,
  "totalItems": 200
}
```

#### GET /scans/{id}/results
Get scan results.

#### GET /scans/statistics
Get scan statistics.

#### GET /scans/trends
Get scan trends.

#### POST /scans/{id}/retry
Retry failed scan.

#### GET /scans/{id}/logs
Get scan logs.

#### DELETE /scans/bulk-delete
Bulk delete scans.

### 4. AI Services

#### POST /ai/analyze-sbom
Analyze SBOM with AI.

**Query Parameters:**
- `sbomDocumentId` (required): SBOM document ID
- `analysisType` (optional, default: "VULNERABILITY"): Analysis type

**Response:**
```json
{
  "id": "uuid",
  "sbomDocumentId": "uuid",
  "analysisType": "VULNERABILITY",
  "status": "COMPLETED",
  "modelUsed": "GPT-4",
  "modelVersion": "1.0",
  "riskScore": 85.5,
  "riskLevel": "HIGH",
  "confidenceScore": 0.92,
  "analysisSummary": "Analysis summary...",
  "keyFindings": ["Finding 1", "Finding 2"],
  "recommendations": ["Recommendation 1", "Recommendation 2"],
  "analysisDate": "2024-01-15T10:30:00Z"
}
```

#### GET /ai/analysis/{analysisId}
Get AI analysis by ID.

#### GET /ai/analysis/sbom/{sbomDocumentId}
Get AI analysis by SBOM document ID.

#### GET /ai/recommendations/project/{projectId}
Get AI recommendations for project.

#### GET /ai/recommendations/vulnerability/{vulnerabilityId}
Get AI recommendations for vulnerability.

#### GET /ai/recommendations/portfolio
Get AI recommendations for portfolio.

#### GET /ai/dashboard-insights
Generate AI insights for dashboard.

#### GET /ai/risk-assessment/{projectId}
Get AI risk assessment.

#### GET /ai/trend-analysis
Get AI trend analysis.

#### GET /ai/security-insights
Get AI security insights.

#### GET /ai/model-status
Get AI model status.

#### PUT /ai/model-configuration
Update AI model configuration.

#### POST /ai/retrain-model
Retrain AI model.

#### GET /ai/model-performance
Get AI model performance metrics.

### 5. Dashboard Services

#### GET /dashboard/summary
Get dashboard summary statistics.

**Query Parameters:**
- `days` (optional, default: 30): Number of days for summary

**Response:**
```json
{
  "totalSboms": 1202,
  "openVulnerabilities": 1040,
  "criticalVulnerabilities": 342,
  "policyViolations": 58,
  "aiSuggestions": 214,
  "averageRiskScore": 65.5,
  "totalProjects": 45,
  "activeProjects": 42
}
```

#### GET /dashboard/trends
Get dashboard trends.

#### GET /dashboard/project-coverage
Get project coverage data.

#### GET /dashboard/at-risk-repos
Get at-risk repositories.

#### GET /dashboard/ai-recommendations
Get AI recommendations for dashboard.

#### GET /dashboard/security-metrics
Get security metrics.

#### GET /dashboard/recent-activity
Get recent activity.

#### GET /dashboard/alerts
Get dashboard alerts.

#### GET /dashboard/compliance-status
Get compliance status.

#### GET /dashboard/performance-metrics
Get performance metrics.

### 6. Health and Monitoring

#### GET /health
Get application health status.

#### GET /health/parser
Get parser health status.

## Error Responses

All endpoints return consistent error responses:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Validation failed",
  "path": "/api/v1/projects"
}
```

## Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

API endpoints are rate-limited to prevent abuse. Limits are:
- 1000 requests per hour per IP
- 100 requests per minute per authenticated user

## Pagination

All list endpoints support pagination with the following parameters:
- `page`: Page number (0-based)
- `size`: Page size (default varies by endpoint)

Response includes pagination metadata:
- `totalElements`: Total number of items
- `totalPages`: Total number of pages
- `size`: Current page size
- `number`: Current page number

## Filtering and Sorting

Most list endpoints support filtering and sorting:

**Filtering:**
- Use query parameters to filter results
- Multiple filters can be combined
- Filter values are case-insensitive

**Sorting:**
- `sortBy`: Field to sort by
- `sortOrder`: Sort direction (asc, desc)
- Default sorting varies by endpoint

## File Upload

File upload endpoints accept multipart form data:
- Maximum file size: 100MB
- Supported formats: JSON, XML, YAML
- Content-Type: multipart/form-data

## WebSocket Support

Real-time updates are available via WebSocket connections:
- Endpoint: `ws://localhost:8081/ws`
- Events: scan progress, vulnerability alerts, AI analysis updates

## SDKs and Libraries

Official SDKs are available for:
- JavaScript/TypeScript
- Python
- Java
- Go

## Examples

### JavaScript/TypeScript Example

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8081/api/v1',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

// Get projects
const projects = await api.get('/projects', {
  params: {
    page: 0,
    size: 10,
    sortBy: 'name',
    sortOrder: 'asc'
  }
});

// Create project
const newProject = await api.post('/projects', {
  name: 'my-project',
  description: 'A new project',
  version: '1.0.0',
  classifier: 'Application'
});

// Upload SBOM
const formData = new FormData();
formData.append('file', sbomFile);
const upload = await api.post(`/projects/${projectId}/upload-sbom`, formData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});
```

### Python Example

```python
import requests

base_url = 'http://localhost:8081/api/v1'
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Get projects
response = requests.get(f'{base_url}/projects', headers=headers, params={
    'page': 0,
    'size': 10,
    'sortBy': 'name',
    'sortOrder': 'asc'
})
projects = response.json()

# Create project
project_data = {
    'name': 'my-project',
    'description': 'A new project',
    'version': '1.0.0',
    'classifier': 'Application'
}
response = requests.post(f'{base_url}/projects', headers=headers, json=project_data)
new_project = response.json()
```

## Support

For API support and questions:
- Documentation: https://docs.sbomai.com/api
- Email: api-support@sbomai.com
- GitHub Issues: https://github.com/sbomai/sbomai-core/issues 