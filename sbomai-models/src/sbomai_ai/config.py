"""
Configuration management for SBOMAI AI Microservice
"""

import os
from typing import Dict, List, Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()


class AiProviderConfig(BaseSettings):
    """Configuration for AI providers"""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_max_tokens: int = Field(default=4000, env="OPENAI_MAX_TOKENS")
    openai_temperature: float = Field(default=0.3, env="OPENAI_TEMPERATURE")
    openai_timeout: int = Field(default=60, env="OPENAI_TIMEOUT")
    
    # Anthropic Configuration
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-sonnet-20240229", env="ANTHROPIC_MODEL")
    anthropic_max_tokens: int = Field(default=4000, env="ANTHROPIC_MAX_TOKENS")
    anthropic_temperature: float = Field(default=0.3, env="ANTHROPIC_TEMPERATURE")
    
    # Google Gemini Configuration
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    google_model: str = Field(default="gemini-pro", env="GOOGLE_MODEL")
    google_max_tokens: int = Field(default=4000, env="GOOGLE_MAX_TOKENS")
    google_temperature: float = Field(default=0.3, env="GOOGLE_TEMPERATURE")
    
    # Local Models Configuration
    local_model_path: Optional[str] = Field(default=None, env="LOCAL_MODEL_PATH")
    local_model_type: str = Field(default="sentence-transformers", env="LOCAL_MODEL_TYPE")
    local_device: str = Field(default="cpu", env="LOCAL_DEVICE")  # cpu, cuda, mps
    
    class Config:
        env_file = ".env"


class MlModelConfig(BaseSettings):
    """Configuration for ML models"""
    
    # XGBoost Configuration
    xgboost_n_estimators: int = Field(default=100, env="XGBOOST_N_ESTIMATORS")
    xgboost_max_depth: int = Field(default=6, env="XGBOOST_MAX_DEPTH")
    xgboost_learning_rate: float = Field(default=0.1, env="XGBOOST_LEARNING_RATE")
    xgboost_random_state: int = Field(default=42, env="XGBOOST_RANDOM_STATE")
    
    # LightGBM Configuration
    lightgbm_n_estimators: int = Field(default=100, env="LIGHTGBM_N_ESTIMATORS")
    lightgbm_max_depth: int = Field(default=6, env="LIGHTGBM_MAX_DEPTH")
    lightgbm_learning_rate: float = Field(default=0.1, env="LIGHTGBM_LEARNING_RATE")
    lightgbm_random_state: int = Field(default=42, env="LIGHTGBM_RANDOM_STATE")
    
    # Model Storage
    model_cache_dir: str = Field(default="./models", env="MODEL_CACHE_DIR")
    model_auto_download: bool = Field(default=True, env="MODEL_AUTO_DOWNLOAD")
    
    class Config:
        env_file = ".env"


class ServiceConfig(BaseSettings):
    """Service configuration"""
    
    # gRPC Server Configuration
    grpc_host: str = Field(default="0.0.0.0", env="GRPC_HOST")
    grpc_port: int = Field(default=50051, env="GRPC_PORT")
    grpc_max_workers: int = Field(default=10, env="GRPC_MAX_WORKERS")
    grpc_max_concurrent_rpcs: int = Field(default=100, env="GRPC_MAX_CONCURRENT_RPCS")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # Monitoring Configuration
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    enable_tracing: bool = Field(default=True, env="ENABLE_TRACING")
    
    # Performance Configuration
    max_concurrent_requests: int = Field(default=50, env="MAX_CONCURRENT_REQUESTS")
    request_timeout: int = Field(default=300, env="REQUEST_TIMEOUT")
    cache_enabled: bool = Field(default=True, env="CACHE_ENABLED")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")
    
    class Config:
        env_file = ".env"


class DataConfig(BaseSettings):
    """Data and external services configuration"""
    
    # CVE Database Configuration
    nvd_api_key: Optional[str] = Field(default=None, env="NVD_API_KEY")
    nvd_base_url: str = Field(default="https://services.nvd.nist.gov/rest/json/cves/2.0", env="NVD_BASE_URL")
    nvd_rate_limit: int = Field(default=5, env="NVD_RATE_LIMIT")  # requests per second
    
    # OSS Index Configuration
    oss_index_url: str = Field(default="https://ossindex.sonatype.org/api/v3/component-report", env="OSS_INDEX_URL")
    oss_index_username: Optional[str] = Field(default=None, env="OSS_INDEX_USERNAME")
    oss_index_token: Optional[str] = Field(default=None, env="OSS_INDEX_TOKEN")
    
    # OSV Configuration
    osv_base_url: str = Field(default="https://api.osv.dev/v1", env="OSV_BASE_URL")
    
    # Data Storage
    data_dir: str = Field(default="./data", env="DATA_DIR")
    cache_dir: str = Field(default="./cache", env="CACHE_DIR")
    
    class Config:
        env_file = ".env"


class SecurityConfig(BaseSettings):
    """Security configuration"""
    
    # API Security
    enable_auth: bool = Field(default=False, env="ENABLE_AUTH")
    auth_token: Optional[str] = Field(default=None, env="AUTH_TOKEN")
    allowed_origins: List[str] = Field(default=["*"], env="ALLOWED_ORIGINS")
    
    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=3600, env="RATE_LIMIT_WINDOW")
    
    # Input Validation
    max_input_size: int = Field(default=10485760, env="MAX_INPUT_SIZE")  # 10MB
    max_components_per_request: int = Field(default=1000, env="MAX_COMPONENTS_PER_REQUEST")
    
    class Config:
        env_file = ".env"


class Config(BaseSettings):
    """Main configuration class"""
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Sub-configurations
    ai_provider: AiProviderConfig = Field(default_factory=AiProviderConfig)
    ml_model: MlModelConfig = Field(default_factory=MlModelConfig)
    service: ServiceConfig = Field(default_factory=ServiceConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    
    # Feature flags
    features: Dict[str, bool] = Field(default_factory=lambda: {
        "explain_risk": True,
        "predict_risk": True,
        "suggest_fix": True,
        "explainable_chain": True,
        "local_models": True,
        "external_apis": True,
        "caching": True,
        "metrics": True,
    })
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance"""
    return config


def validate_config() -> List[str]:
    """Validate configuration and return list of issues"""
    issues = []
    
    # Check required API keys
    if not config.ai_provider.openai_api_key and not config.ai_provider.anthropic_api_key and not config.ai_provider.google_api_key:
        issues.append("At least one AI provider API key is required (OpenAI, Anthropic, or Google)")
    
    # Check model paths
    if config.ai_provider.local_model_path and not os.path.exists(config.ai_provider.local_model_path):
        issues.append(f"Local model path does not exist: {config.ai_provider.local_model_path}")
    
    # Check directories
    for dir_path in [config.ml_model.model_cache_dir, config.data.data_dir, config.data.cache_dir]:
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
            except Exception as e:
                issues.append(f"Could not create directory {dir_path}: {e}")
    
    return issues 