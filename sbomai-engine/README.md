# SBOMAI AI Engine

Advanced AI/ML engine for intelligent, explainable, and predictive SBOM analysis. Provides gRPC endpoints for risk explanation, prediction, remediation suggestions, and explainable chains.

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
   cd sbomai-ai-engine
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
docker build -t sbomai-ai-engine:latest .

# Run the container
docker run -d \
  --name sbomai-ai-engine \
  -p 50051:50051 \
  -p 9090:9090 \
  --env-file .env \
  sbomai-ai-engine:latest
```

## API Usage

### gRPC Methods

- **ExplainRisk**: Explain why a component is risky
- **PredictRiskScore**: Predict risk scores for components
- **SuggestFix**: Generate fix suggestions for vulnerabilities
- **ExplainableSbomChain**: Generate explainable analysis chains
- **PredictVulnerabilityPatterns**: Advanced GNN-based vulnerability prediction
- **GetServiceInfo**: Service health and capabilities

### Example Client Usage

```python
import grpc
from src import sbomai_ai_pb2, sbomai_ai_pb2_grpc

# Create channel
channel = grpc.aio.insecure_channel('localhost:50051')
stub = sbomai_ai_pb2_grpc.SbomaiAiServiceStub(channel)

# Explain risk
request = sbomai_ai_pb2.ExplainRiskRequest(
    component=sbomai_ai_pb2.SbomComponent(
        name="spring-boot",
        version="2.7.0"
    ),
    vulnerabilities=[...],
    analysis_context="Production deployment"
)

response = await stub.ExplainRisk(request)
print(f"Risk explanation: {response.explanation}")
```

## Configuration

### Environment Variables

```bash
# AI Provider Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# Service Configuration
GRPC_PORT=50051
METRICS_PORT=9090
LOG_LEVEL=INFO

# Model Configuration
DEFAULT_AI_PROVIDER=openai
DEFAULT_MODEL=gpt-4
MAX_TOKENS=4000
TEMPERATURE=0.1

# Cache Configuration
CACHE_ENABLED=true
CACHE_TTL=3600
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_ai_models.py
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

## Architecture

The AI Engine follows a modular architecture:

```
src/
├── sbomai_ai/
│   ├── __init__.py
│   ├── service.py          # Main gRPC service
│   ├── config.py           # Configuration management
│   ├── models/             # AI/ML models
│   │   ├── ai_models.py    # LLM integrations
│   │   ├── ml_models.py    # Traditional ML models
│   │   ├── risk_models.py  # Risk assessment models
│   │   ├── explainability_models.py  # Explainable AI
│   │   └── graph_neural_models.py    # GNN models
│   └── utils/              # Utilities
│       ├── exceptions.py   # Custom exceptions
│       ├── helpers.py      # Helper functions
│       ├── validators.py   # Input validation
│       ├── cache.py        # Caching utilities
│       └── monitoring.py   # Monitoring and metrics
├── protos/                 # Protocol buffer definitions
└── tests/                  # Test suite
```

## Integration

The AI Engine integrates with the Java-based SBOMAI core system through:

1. **gRPC Communication**: High-performance inter-service communication
2. **Protocol Buffers**: Language-agnostic data serialization
3. **Async Operations**: Non-blocking request handling
4. **Service Discovery**: Dynamic service location and health checking
5. **Error Handling**: Robust error propagation and recovery

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 