"""
Configuration management for SBOMAI.
"""

import os
from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    openai_api_key: Optional[str] = Field(None, env='OPENAI_API_KEY')
    anthropic_api_key: Optional[str] = Field(None, env='ANTHROPIC_API_KEY')
    google_api_key: Optional[str] = Field(None, env='GOOGLE_API_KEY')
    github_token: Optional[str] = Field(None, env='GITHUB_TOKEN')
    
    # Data Source API Keys
    nvd_api_key: Optional[str] = Field(None, env='NVD_API_KEY')
    osv_api_key: Optional[str] = Field(None, env='OSV_API_KEY')
    exploitdb_api_key: Optional[str] = Field(None, env='EXPLOITDB_API_KEY')
    mitre_api_key: Optional[str] = Field(None, env='MITRE_API_KEY')
    cisa_api_key: Optional[str] = Field(None, env='CISA_API_KEY')
    redhat_api_key: Optional[str] = Field(None, env='REDHAT_API_KEY')
    jfrog_api_key: Optional[str] = Field(None, env='JFROG_API_KEY')
    
    # Model Settings
    default_llm: str = Field('local', env='DEFAULT_LLM')
    openai_model: str = Field('gpt-4', env='OPENAI_MODEL')
    anthropic_model: str = Field('claude-2', env='ANTHROPIC_MODEL')
    google_model: str = Field('gemini-pro', env='GOOGLE_MODEL')
    local_model: str = Field('microsoft/DialoGPT-medium', env='LOCAL_MODEL')
    
    # Cache Settings
    cache_type: str = Field('memory', env='CACHE_TYPE')  # memory, redis, file
    cache_ttl: int = Field(3600, env='CACHE_TTL')  # seconds
    redis_url: Optional[str] = Field(None, env='REDIS_URL')
    cache_dir: str = Field('.cache', env='CACHE_DIR')
    
    # Monitoring Settings
    enable_monitoring: bool = Field(True, env='ENABLE_MONITORING')
    prometheus_port: int = Field(9090, env='PROMETHEUS_PORT')
    grafana_port: int = Field(3000, env='GRAFANA_PORT')
    
    # Logging Settings
    log_level: str = Field('INFO', env='LOG_LEVEL')
    log_format: str = Field(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        env='LOG_FORMAT'
    )
    
    # Model Configuration
    model_config = SettingsConfigDict(
        env_file=None,  # Temporarily disable .env file loading
        case_sensitive=False
    )

def get_config() -> Settings:
    """Get application configuration"""
    return Settings()