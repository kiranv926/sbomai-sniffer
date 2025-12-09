# Complete AI Backend API Documentation

## Overview

The SBOMAI Core project now includes a comprehensive AI-powered backend system that provides advanced analysis capabilities for Software Bill of Materials (SBOM). This system includes multiple AI models for vulnerability analysis, license compliance, supply chain security, and compliance assessment.

## Architecture

### Core Components

1. **AIService** - Core AI analysis service with multiple model types
2. **AIOrchestrationService** - Coordinates multiple AI operations and provides unified interface
3. **EnhancedAIController** - REST API endpoints for AI functionality
4. **AdvancedAIServiceImpl** - Advanced AI implementation with comprehensive analysis
5. **AIOrchestrationServiceImpl** - Orchestration service implementation

### AI Model Types

- **VULNERABILITY** - Security vulnerability analysis
- **LICENSE** - License compliance analysis
- **SUPPLY_CHAIN** - Supply chain security analysis
- **COMPLIANCE** - Regulatory compliance analysis

## API Endpoints

### Base URL
```
http://localhost:8081/api/v1/ai
```

### Enhanced AI Endpoints

#### 1. Comprehensive AI Analysis
**POST** `/enhanced/comprehensive-analysis`

Performs comprehensive AI analysis combining all analysis types.

**Parameters:**
- `sbomDocumentId` (UUID, required) - ID of the SBOM document to analyze

**Response:** `CompletableFuture<AIAnalysisDto>`

**Example:**
```bash
curl -X POST "http://localhost:8081/api/v1/ai/enhanced/comprehensive-analysis?sbomDocumentId=123e4567-e89b-12d3-a456-426614174000"
```

#### 2. Targeted AI Analysis
**POST** `/enhanced/targeted-analysis`

Performs targeted AI analysis for specific analysis type.

**Parameters:**
- `sbomDocumentId` (UUID, required) - ID of the SBOM document to analyze
- `analysisType` (String, required) - Type of analysis (VULNERABILITY, LICENSE, SUPPLY_CHAIN, COMPLIANCE)

**Response:** `CompletableFuture<AIAnalysisDto>`

**Example:**
```bash
curl -X POST "http://localhost:8081/api/v1/ai/enhanced/targeted-analysis?sbomDocumentId=123e4567-e89b-12d3-a456-426614174000&analysisType=VULNERABILITY"
```

#### 3. Synchronous SBOM Analysis
**POST** `/enhanced/analyze-sbom`

Performs synchronous AI analysis on SBOM.

**Parameters:**
- `sbomDocumentId` (UUID, required) - ID of the SBOM document to analyze
- `analysisType` (String, optional, default: VULNERABILITY) - Type of analysis

**Response:** `AIAnalysisDto`

**Example:**
```bash
curl -X POST "http://localhost:8081/api/v1/ai/enhanced/analyze-sbom?sbomDocumentId=123e4567-e89b-12d3-a456-426614174000&analysisType=LICENSE"
```

#### 4. Project Recommendations
**GET** `/enhanced/recommendations/project/{projectId}`

Generates AI recommendations for a specific project.

**Parameters:**
- `projectId` (UUID, path) - ID of the project

**Response:** `List<AIRecommendationDto>`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/recommendations/project/123e4567-e89b-12d3-a456-426614174000"
```

#### 5. Portfolio Recommendations
**GET** `/enhanced/recommendations/portfolio`

Generates AI recommendations for the entire portfolio.

**Response:** `List<AIRecommendationDto>`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/recommendations/portfolio"
```

#### 6. Vulnerability Recommendations
**GET** `/enhanced/recommendations/vulnerability/{vulnerabilityId}`

Generates AI recommendations for a specific vulnerability.

**Parameters:**
- `vulnerabilityId` (UUID, path) - ID of the vulnerability

**Response:** `List<AIRecommendationDto>`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/recommendations/vulnerability/123e4567-e89b-12d3-a456-426614174000"
```

#### 7. AI Model Health
**GET** `/enhanced/model-health`

Retrieves health status of all AI models.

**Response:** `AIModelHealth`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/model-health"
```

#### 8. AI Model Performance
**GET** `/enhanced/model-performance/{modelType}`

Retrieves performance metrics for a specific AI model.

**Parameters:**
- `modelType` (String, path) - Type of AI model

**Response:** `AIModelPerformance`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/model-performance/VULNERABILITY"
```

#### 9. Update Model Configuration
**PUT** `/enhanced/model-configuration`

Updates configuration for a specific AI model.

**Parameters:**
- `modelType` (String, query) - Type of AI model
- `configuration` (String, body) - New configuration JSON

**Example:**
```bash
curl -X PUT "http://localhost:8081/api/v1/ai/enhanced/model-configuration?modelType=VULNERABILITY" \
  -H "Content-Type: application/json" \
  -d '{"confidenceThreshold": 0.9, "maxAnalysisTime": 30000}'
```

#### 10. Retrain AI Model
**POST** `/enhanced/retrain-model`

Initiates retraining of a specific AI model.

**Parameters:**
- `modelType` (String, query) - Type of AI model to retrain

**Response:** `CompletableFuture<Void>`

**Example:**
```bash
curl -X POST "http://localhost:8081/api/v1/ai/enhanced/retrain-model?modelType=VULNERABILITY"
```

#### 11. Dashboard Insights
**GET** `/enhanced/dashboard-insights`

Retrieves AI-powered dashboard insights.

**Response:** `DashboardInsights`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/dashboard-insights"
```

#### 12. Risk Assessment
**GET** `/enhanced/risk-assessment/{projectId}`

Generates AI risk assessment for a project.

**Parameters:**
- `projectId` (UUID, path) - ID of the project

**Response:** `RiskAssessment`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/risk-assessment/123e4567-e89b-12d3-a456-426614174000"
```

#### 13. Trend Analysis
**GET** `/enhanced/trend-analysis`

Generates AI trend analysis.

**Parameters:**
- `days` (int, optional, default: 30) - Number of days for analysis

**Response:** `TrendAnalysis`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/trend-analysis?days=60"
```

#### 14. Security Insights
**GET** `/enhanced/security-insights`

Retrieves comprehensive security insights.

**Response:** `SecurityInsights`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/security-insights"
```

#### 15. Get AI Analysis by ID
**GET** `/enhanced/analysis/{analysisId}`

Retrieves AI analysis by its ID.

**Parameters:**
- `analysisId` (UUID, path) - ID of the analysis

**Response:** `AIAnalysisDto`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/analysis/123e4567-e89b-12d3-a456-426614174000"
```

#### 16. Get AI Analysis by SBOM Document
**GET** `/enhanced/analysis/sbom/{sbomDocumentId}`

Retrieves AI analysis for a specific SBOM document.

**Parameters:**
- `sbomDocumentId` (UUID, path) - ID of the SBOM document

**Response:** `AIAnalysisDto`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/analysis/sbom/123e4567-e89b-12d3-a456-426614174000"
```

#### 17. Model Status
**GET** `/enhanced/model-status`

Retrieves current status of AI models.

**Response:** `ModelStatus`

**Example:**
```bash
curl -X GET "http://localhost:8081/api/v1/ai/enhanced/model-status"
```

## Data Models

### AIAnalysisDto
```json
{
  "id": "UUID",
  "sbomDocumentId": "UUID",
  "analysisType": "String",
  "status": "String",
  "riskScore": "Double",
  "riskLevel": "String",
  "analysisSummary": "String",
  "keyFindings": ["String"],
  "recommendations": ["String"],
  "modelUsed": "String",
  "modelVersion": "String",
  "confidenceScore": "Double",
  "analysisDurationMs": "Long",
  "analysisDate": "LocalDateTime"
}
```

### AIRecommendationDto
```json
{
  "id": "UUID",
  "title": "String",
  "description": "String",
  "category": "String",
  "priority": "String",
  "status": "String",
  "recommendation": "String",
  "confidenceScore": "Double",
  "modelUsed": "String",
  "createdDate": "LocalDateTime"
}
```

### AIModelHealth
```json
{
  "overallStatus": "String",
  "modelStatuses": [
    {
      "modelName": "String",
      "status": "String",
      "accuracy": "Double",
      "predictions": "Long",
      "lastUsed": "String"
    }
  ],
  "averageAccuracy": "Double",
  "totalPredictions": "Long",
  "lastUpdated": "String"
}
```

### AIModelPerformance
```json
{
  "modelName": "String",
  "accuracy": "Double",
  "precision": "Double",
  "recall": "Double",
  "f1Score": "Double",
  "totalPredictions": "Long",
  "correctPredictions": "Long",
  "averageResponseTime": "Double",
  "lastEvaluation": "String"
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- **200 OK** - Successful operation
- **202 Accepted** - Async operation initiated
- **400 Bad Request** - Invalid parameters
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

## Authentication & Security

Currently, the API endpoints are open for development. In production, implement:

1. JWT-based authentication
2. Role-based access control
3. API rate limiting
4. Input validation and sanitization
5. HTTPS encryption

## Performance Considerations

1. **Async Processing** - Long-running AI operations are handled asynchronously
2. **Thread Pool Management** - Dedicated thread pools for AI operations
3. **Caching** - Consider implementing Redis caching for frequent requests
4. **Database Optimization** - Use appropriate indexes for AI analysis queries
5. **Model Optimization** - AI models are optimized for inference speed

## Monitoring & Observability

1. **Logging** - Comprehensive logging for all AI operations
2. **Metrics** - Performance metrics for AI models
3. **Health Checks** - Model health monitoring
4. **Tracing** - Distributed tracing for AI operations

## Deployment

### Prerequisites
- Java 17+
- Maven 3.6+
- Spring Boot 3.2.0

### Build
```bash
mvn clean compile
```

### Run
```bash
mvn spring-boot:run
```

### Docker
```bash
docker build -t sbomai-core .
docker run -p 8081:8081 sbomai-core
```

## Testing

### Unit Tests
```bash
mvn test
```

### Integration Tests
```bash
mvn verify
```

### API Tests
Use the provided test-api.http file for testing endpoints.

## Future Enhancements

1. **Real AI Models** - Integration with actual ML models
2. **Model Versioning** - A/B testing for model versions
3. **Auto-scaling** - Kubernetes-based auto-scaling
4. **Model Registry** - Centralized model management
5. **Feature Store** - ML feature management
6. **Model Monitoring** - Drift detection and alerting
7. **Explainable AI** - Model interpretability features
8. **Federated Learning** - Distributed model training

## Support

For issues and questions:
1. Check the application logs
2. Review the API documentation
3. Test with the provided examples
4. Contact the development team

---

This completes the comprehensive AI backend implementation for the SBOMAI Core project. 