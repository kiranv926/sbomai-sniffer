# SBOMAI AI Microservice

Advanced AI/ML microservice for intelligent, explainable, and predictive SBOM analysis. Provides gRPC endpoints for risk explanation, prediction, remediation suggestions, and explainable chains.

## Features

### 🤖 AI-Powered Analysis
- **Risk Explanation**: Explain why specific component versions are risky using AI models
- **Risk Prediction**: Predict risk scores for components using ML models
- **Fix Suggestions**: Generate intelligent remediation suggestions
- **Explainable Chains**: Create explainable analysis chains for entire SBOMs
- **Predictive Vulnerability Detection**: Advanced Graph Neural Network analysis for predicting vulnerabilities before they're disclosed

### 🧠 Multiple AI Providers
- **OpenAI GPT-4/3.5**: Advanced reasoning and analysis
- **Anthropic Claude**: Detailed explanations and safety-focused analysis
- **Google Gemini**: Fast and efficient analysis
- **Local Models**: BERT, sentence-transformers for privacy-sensitive environments

### 📊 ML Models
- **XGBoost**: Gradient boosting for risk prediction
- **LightGBM**: Light gradient boosting machine
- **Random Forest**: Ensemble learning for robust predictions
- **Logistic Regression**: Interpretable baseline models
- **Graph Neural Networks**: GCN, GAT, GraphConv for dependency graph analysis

### 🔗 LangChain Integration
- **Explainable Chains**: Step-by-step reasoning processes
- **Custom Analysis Steps**: Configurable analysis workflows
- **Chain Validation**: Confidence scoring and validation

### 🕸️ Graph Neural Network Analysis
- **Dependency Pattern Detection**: Identify long dependency chains and vulnerable clusters
- **Emerging Vulnerability Prediction**: Predict where new vulnerabilities are likely to emerge
- **Critical Path Analysis**: Find critical dependency paths that could cause widespread issues
- **Vulnerability Propagation**: Track how vulnerabilities spread through the dependency graph
- **Dependency Health Assessment**: Evaluate overall health of the dependency graph

### 📈 Monitoring & Observability
- **Prometheus Metrics**: Comprehensive monitoring
- **Structured Logging**: JSON-formatted logs with structlog
- **Health Checks**: HTTP health endpoints
- **Performance Tracking**: Request duration, model prediction times

### 🚀 Performance & Scalability
- **gRPC**: High-performance communication
- **Async/Await**: Non-blocking I/O operations
- **Caching**: Multi-level caching (memory + file)
- **Concurrent Processing**: Thread pool execution

## Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional)
- AI provider API keys (OpenAI, Anthropic, Google)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sbomai-models
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate gRPC code**
   ```bash
   python -m grpc_tools.protoc \
       --python_out=./src \
       --grpc_python_out=./src \
       --proto_path=./protos \
       ./protos/sbomai_ai.proto
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run the service**
   ```bash
   python server.py
   ```

### Docker Deployment

```bash
# Build the image
docker build -t sbomai-ai:latest .

# Run the container
docker run -d \
  --name sbomai-ai \
  -p 50051:50051 \
  -p 9090:9090 \
  -e OPENAI_API_KEY=your_key \
  -e ANTHROPIC_API_KEY=your_key \
  sbomai-ai:latest
```

## Configuration

### Environment Variables

```bash
# AI Provider Configuration
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4
ANTHROPIC_API_KEY=your_anthropic_key
ANTHROPIC_MODEL=claude-3-sonnet-20240229
GOOGLE_API_KEY=your_google_key
GOOGLE_MODEL=gemini-pro

# Service Configuration
GRPC_HOST=0.0.0.0
GRPC_PORT=50051
GRPC_MAX_WORKERS=10
GRPC_MAX_CONCURRENT_RPCS=100

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
LOG_LEVEL=INFO

# Performance
MAX_CONCURRENT_REQUESTS=50
REQUEST_TIMEOUT=300
CACHE_ENABLED=true
CACHE_TTL=3600
```

### Configuration File

Create a `.env` file with your settings:

```env
# AI Providers
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-key

# Service Settings
GRPC_PORT=50051
ENABLE_METRICS=true
LOG_LEVEL=INFO

# ML Models
XGBOOST_N_ESTIMATORS=100
LIGHTGBM_N_ESTIMATORS=100

# Data Sources
NVD_API_KEY=your-nvd-key
OSS_INDEX_USERNAME=your-username
OSS_INDEX_TOKEN=your-token
```

## API Reference

### gRPC Endpoints

#### ExplainRisk
Explain why a specific component version is risky.

```protobuf
rpc ExplainRisk(ExplainRiskRequest) returns (ExplainRiskResponse)
```

**Request:**
```json
{
  "component": {
    "name": "log4j-core",
    "version": "2.14.1",
    "group_id": "org.apache.logging.log4j",
    "licenses": ["Apache-2.0"]
  },
  "vulnerabilities": [
    {
      "id": "CVE-2021-44228",
      "description": "Log4Shell vulnerability",
      "severity": "CRITICAL_SEVERITY",
      "cvss_score": 10.0
    }
  ],
  "analysis_context": "Production web application",
  "model_config": {
    "model_name": "gpt-4",
    "temperature": 0.3,
    "provider": "openai"
  }
}
```

**Response:**
```json
{
  "explanation": "This component is critically risky due to the Log4Shell vulnerability...",
  "confidence_score": 0.95,
  "sources": ["https://nvd.nist.gov/vuln/detail/CVE-2021-44228"],
  "key_factors": ["Remote code execution", "Widely exploited", "High CVSS score"],
  "risk_level": "CRITICAL",
  "model_used": "gpt-4",
  "processing_time_ms": 1250
}
```

#### PredictRiskScore
Predict risk score for a component.

```protobuf
rpc PredictRiskScore(PredictRiskScoreRequest) returns (PredictRiskScoreResponse)
```

**Request:**
```json
{
  "component": {
    "name": "spring-boot-starter-web",
    "version": "2.7.0"
  },
  "historical_vulnerabilities": [
    {
      "id": "CVE-2022-22965",
      "cvss_score": 9.8,
      "published_date": "2022-03-31T00:00:00Z"
    }
  ],
  "features": ["web_framework", "popular", "enterprise"],
  "ml_config": {
    "model_type": "xgboost",
    "use_feature_importance": true,
    "use_confidence_intervals": true
  }
}
```

**Response:**
```json
{
  "risk_score": 75.5,
  "confidence_interval_lower": 68.2,
  "confidence_interval_upper": 82.8,
  "feature_importance": [
    {
      "feature_name": "cvss_score",
      "importance_score": 0.45,
      "description": "Historical CVSS scores"
    }
  ],
  "model_used": "xgboost",
  "explanation": "High risk due to recent critical vulnerabilities...",
  "processing_time_ms": 320
}
```

#### SuggestFix
Suggest fixes for vulnerabilities.

```protobuf
rpc SuggestFix(SuggestFixRequest) returns (SuggestFixResponse)
```

**Request:**
```json
{
  "vulnerability_id": "CVE-2021-44228",
  "component": {
    "name": "log4j-core",
    "version": "2.14.1"
  },
  "constraints": ["no_breaking_changes", "apache_license"],
  "strategy": {
    "approach": "conservative",
    "consider_breaking_changes": false,
    "prefer_latest_versions": false
  }
}
```

**Response:**
```json
{
  "suggestions": [
    {
      "action": "upgrade",
      "suggested_component": {
        "name": "log4j-core",
        "version": "2.17.1"
      },
      "reasoning": "This version fixes the Log4Shell vulnerability...",
      "confidence": 0.98,
      "risks": ["Minor API changes"],
      "benefits": ["Security fix", "Performance improvements"]
    }
  ],
  "reasoning": "Upgrade recommended due to critical security vulnerability",
  "confidence_score": 0.98,
  "policy_rules": ["security_patch_required"],
  "processing_time_ms": 450
}
```

#### PredictVulnerabilityPatterns
Predict vulnerability patterns using Graph Neural Networks.

```protobuf
rpc PredictVulnerabilityPatterns(PredictVulnerabilityPatternsRequest) returns (PredictVulnerabilityPatternsResponse)
```

**Request:**
```json
{
  "sbom_document": {
    "name": "my-application",
    "version": "1.0.0",
    "format": "SPDX",
    "components": [
      {
        "name": "spring-boot",
        "version": "2.7.0",
        "licenses": ["Apache-2.0"],
        "purl": "pkg:maven/org.springframework.boot/spring-boot@2.7.0"
      }
    ]
  },
  "gnn_config": {
    "gnn_type": "gcn",
    "hidden_dim": 64,
    "num_layers": 3,
    "dropout": 0.2
  },
  "analysis_types": [
    "dependency_patterns",
    "emerging_vulnerabilities",
    "critical_paths"
  ]
}
```

**Response:**
```json
{
  "vulnerability_likelihood": 0.75,
  "confidence_score": 0.82,
  "graph_features": {
    "num_nodes": 8,
    "num_edges": 12,
    "density": 0.214,
    "vulnerability_ratio": 0.5,
    "max_dependency_depth": 4
  },
  "high_risk_components": [
    {
      "component_name": "jackson-databind",
      "risk_score": 0.91,
      "vulnerabilities": [{"id": "CVE-2023-9012", "cvss_score": 9.1}]
    }
  ],
  "emerging_vulnerabilities": [
    {
      "component_name": "spring-web",
      "emerging_risk_score": 0.65,
      "risk_factors": ["high_dependency_count", "vulnerable_neighbors"],
      "predicted_vulnerability_types": ["propagation_vulnerability", "cluster_attack"]
    }
  ],
  "critical_dependencies": [
    {
      "component_name": "spring-core",
      "critical_score": 0.85,
      "betweenness_centrality": 0.4,
      "impact_analysis": "Critical dependency with high centrality"
    }
  ],
  "dependency_health": {
    "overall_health_score": 65.0,
    "health_indicators": ["high_vulnerability_ratio", "deep_dependencies"]
  },
  "processing_time_ms": 1250
}
    }
  ],
  "reasoning": "Upgrade to version 2.17.1 to fix the critical vulnerability...",
  "confidence_score": 0.98,
  "policy_rules": ["Upgrade log4j-core to >=2.17.1"],
  "processing_time_ms": 890
}
```

#### ExplainableSbomChain
Generate explainable analysis chain for entire SBOM.

```protobuf
rpc ExplainableSbomChain(ExplainableSbomChainRequest) returns (ExplainableSbomChainResponse)
```

**Request:**
```json
{
  "sbom_document": {
    "name": "my-application",
    "version": "1.0.0",
    "format": "CYCLONEDX",
    "components": [
      {
        "name": "log4j-core",
        "version": "2.14.1"
      }
    ]
  },
  "chain_config": {
    "max_steps": 5,
    "confidence_threshold": 0.7,
    "include_detailed_explanations": true,
    "analysis_types": ["vulnerability", "license", "outdated"]
  }
}
```

**Response:**
```json
{
  "chain_steps": [
    {
      "step_name": "vulnerability_scan",
      "result": "Found 1 critical vulnerability",
      "confidence": 0.95,
      "findings": ["CVE-2021-44228 in log4j-core 2.14.1"],
      "duration_ms": 1200
    }
  ],
  "overall_assessment": "Critical security issues detected",
  "overall_risk_score": 85.0,
  "recommendations": [
    "Upgrade log4j-core to 2.17.1",
    "Implement security scanning in CI/CD"
  ],
  "critical_findings": [
    "Log4Shell vulnerability in production dependency"
  ],
  "processing_time_ms": 4500
}
```

## Client Examples

### Python Client

```python
import grpc
from src.sbomai_ai import sbomai_ai_pb2, sbomai_ai_pb2_grpc

# Create channel
channel = grpc.insecure_channel('localhost:50051')
stub = sbomai_ai_pb2_grpc.SbomaiAiServiceStub(channel)

# Explain risk
request = sbomai_ai_pb2.ExplainRiskRequest(
    component=sbomai_ai_pb2.SbomComponent(
        name="log4j-core",
        version="2.14.1"
    ),
    analysis_context="Production application"
)

response = stub.ExplainRisk(request)
print(f"Risk explanation: {response.explanation}")
print(f"Risk level: {response.risk_level}")
```

### Java Client

```java
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import com.sbomai.ai.SbomaiAiServiceGrpc;
import com.sbomai.ai.SbomaiAi;

// Create channel
ManagedChannel channel = ManagedChannelBuilder
    .forAddress("localhost", 50051)
    .usePlaintext()
    .build();

SbomaiAiServiceGrpc.SbomaiAiServiceBlockingStub stub = 
    SbomaiAiServiceGrpc.newBlockingStub(channel);

// Explain risk
SbomaiAi.ExplainRiskRequest request = SbomaiAi.ExplainRiskRequest.newBuilder()
    .setComponent(SbomaiAi.SbomComponent.newBuilder()
        .setName("log4j-core")
        .setVersion("2.14.1")
        .build())
    .setAnalysisContext("Production application")
    .build();

SbomaiAi.ExplainRiskResponse response = stub.explainRisk(request);
System.out.println("Risk explanation: " + response.getExplanation());
```

### cURL (Health Check)

```bash
# Health check
curl http://localhost:9090/health

# Metrics
curl http://localhost:9090/metrics
```

## Monitoring

### Prometheus Metrics

The service exposes the following metrics:

- `sbomai_ai_requests_total`: Total request count
- `sbomai_ai_request_duration_seconds`: Request duration
- `sbomai_ai_model_predictions_total`: Model prediction count
- `sbomai_ai_model_prediction_duration_seconds`: Model prediction duration
- `sbomai_ai_api_calls_total`: AI API call count
- `sbomai_ai_cache_hits_total`: Cache hit count
- `sbomai_ai_errors_total`: Error count

### Grafana Dashboard

Import the provided Grafana dashboard to visualize:

- Request rates and latencies
- Model performance metrics
- Cache hit rates
- Error rates and types
- System resource usage

### Logging

Structured JSON logs include:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info",
  "logger": "sbomai_ai.service",
  "message": "Processing explain risk request",
  "component": "log4j-core",
  "version": "2.14.1",
  "processing_time_ms": 1250
}
```

## Development

### Project Structure

```
sbomai-models/
├── src/
│   └── sbomai_ai/
│       ├── __init__.py
│       ├── config.py
│       ├── service.py
│       ├── models/
│       │   ├── ai_models.py
│       │   ├── ml_models.py
│       │   ├── risk_models.py
│       │   └── explainability_models.py
│       └── utils/
│           ├── cache.py
│           ├── exceptions.py
│           ├── helpers.py
│           ├── monitoring.py
│           └── validators.py
├── protos/
│   └── sbomai_ai.proto
├── tests/
├── requirements.txt
├── Dockerfile
├── server.py
└── README.md
```

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src/sbomai_ai tests/

# Run specific test
pytest tests/test_service.py::test_explain_risk

### Testing Predictive Vulnerability Detection

```bash
# Run the predictive detection test
python test_predictive_detection.py

# This will demonstrate:
# - GNN-based vulnerability pattern analysis
# - Emerging vulnerability prediction
# - Critical dependency identification
# - Dependency health assessment
# - Vulnerability propagation analysis
```
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Adding New Models

1. **Create model class** in `src/sbomai_ai/models/`
2. **Implement required methods** (predict, explain, etc.)
3. **Add to service** in `src/sbomai_ai/service.py`
4. **Add tests** in `tests/`
5. **Update configuration** in `src/sbomai_ai/config.py`

## Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  sbomai-ai:
    build: .
    ports:
      - "50051:50051"
      - "9090:9090"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GRPC_PORT=50051
      - ENABLE_METRICS=true
    volumes:
      - ./data:/app/data
      - ./cache:/app/cache
      - ./models:/app/models
    restart: unless-stopped
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sbomai-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sbomai-ai
  template:
    metadata:
      labels:
        app: sbomai-ai
    spec:
      containers:
      - name: sbomai-ai
        image: sbomai-ai:latest
        ports:
        - containerPort: 50051
        - containerPort: 9090
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

## Security

### API Security
- Input validation and sanitization
- Rate limiting
- Request size limits
- Secure error handling

### Model Security
- Model validation
- Input sanitization
- Output filtering
- Secure model loading

### Infrastructure Security
- Non-root container execution
- Minimal base images
- Regular security updates
- Network isolation

## Troubleshooting

### Common Issues

1. **gRPC connection refused**
   - Check if service is running on correct port
   - Verify firewall settings
   - Check service logs

2. **AI API errors**
   - Verify API keys are correct
   - Check API rate limits
   - Ensure sufficient credits

3. **Model loading failures**
   - Check model cache directory permissions
   - Verify model files are downloaded
   - Check available disk space

4. **High memory usage**
   - Reduce concurrent request limit
   - Enable model caching
   - Monitor memory metrics

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python server.py
```

### Health Checks

```bash
# Service health
curl http://localhost:9090/health

# gRPC health (using grpcurl)
grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check
```

## Documentation

- **[Predictive Vulnerability Detection](PREDICTIVE_VULNERABILITY_DETECTION.md)**: Comprehensive guide to the Graph Neural Network-based predictive vulnerability detection feature
- **[API Reference](API.md)**: Complete API documentation
- **[Configuration Guide](CONFIG.md)**: Detailed configuration options

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run code quality checks
6. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Support

- **Documentation**: [Project Wiki](https://github.com/your-org/sbomai/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-org/sbomai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/sbomai/discussions)
- **Email**: support@sbomai.com 