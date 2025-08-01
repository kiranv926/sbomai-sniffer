"""
Validation utilities for SBOMAI AI Engine
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

from .exceptions import ValidationError

class SbomComponent(BaseModel):
    """SBOM component validation model"""
    
    name: str = Field(..., min_length=1)
    version: str = Field(..., min_length=1)
    group_id: Optional[str] = None
    description: Optional[str] = None
    license: Optional[str] = None
    purl: Optional[str] = None
    cpe: Optional[str] = None
    sha256: Optional[str] = None
    md5: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = Field(None, ge=0)
    supplier: Optional[str] = None
    author: Optional[str] = None
    
    @validator("version")
    def validate_version(cls, v: str) -> str:
        """Validate version format"""
        if not any(c.isdigit() for c in v):
            raise ValidationError("Version must contain at least one digit")
        return v
    
    @validator("purl")
    def validate_purl(cls, v: Optional[str]) -> Optional[str]:
        """Validate Package URL format"""
        if v is not None and not v.startswith("pkg:"):
            raise ValidationError("Invalid Package URL format")
        return v

class Vulnerability(BaseModel):
    """Vulnerability validation model"""
    
    vulnerability_id: str = Field(..., min_length=1)
    title: Optional[str] = None
    description: Optional[str] = None
    severity: str = Field(..., regex="^(CRITICAL|HIGH|MEDIUM|LOW|INFO)$")
    cvss_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    cvss_vector: Optional[str] = None
    cwe_id: Optional[str] = None
    cve_id: Optional[str] = None
    source: str = Field(..., regex="^(NVD|OSS_INDEX|OSV|GITHUB|SUSE|REDHAT|DEBIAN|UBUNTU|ALPINE|UNKNOWN)$")
    source_url: Optional[str] = None
    published_date: Optional[datetime] = None
    last_modified_date: Optional[datetime] = None
    references: Optional[str] = None
    remediation: Optional[str] = None
    affected_versions: Optional[str] = None
    fixed_versions: Optional[str] = None

class SbomDocument(BaseModel):
    """SBOM document validation model"""
    
    document_name: str = Field(..., min_length=1)
    document_version: str = Field(..., min_length=1)
    sbom_format: str = Field(..., regex="^(SPDX|CYCLONEDX|SWID|UNKNOWN)$")
    description: Optional[str] = None
    author: Optional[str] = None
    supplier: Optional[str] = None
    created_date: Optional[datetime] = None
    last_modified_date: Optional[datetime] = None
    components: List[SbomComponent] = Field(default_factory=list)
    file_path: Optional[str] = None
    file_size: Optional[int] = Field(None, ge=0)
    checksum: Optional[str] = None
    checksum_algorithm: Optional[str] = None

class AiModelConfig(BaseModel):
    """AI model configuration validation model"""
    
    provider: str = Field(..., regex="^(openai|anthropic|google|local)$")
    model_name: str = Field(..., min_length=1)
    temperature: float = Field(0.1, ge=0.0, le=1.0)
    max_tokens: int = Field(4000, gt=0)

class MlModelConfig(BaseModel):
    """ML model configuration validation model"""
    
    model_type: str = Field(..., regex="^(xgboost|lightgbm|random_forest|logistic_regression)$")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    use_cached_model: bool = Field(False)

class GnnConfig(BaseModel):
    """GNN configuration validation model"""
    
    model_type: str = Field(..., regex="^(gcn|gat|graphconv)$")
    num_layers: int = Field(3, gt=0)
    hidden_dim: int = Field(64, gt=0)
    dropout: float = Field(0.2, ge=0.0, le=1.0)
    use_attention: bool = Field(False)
    model_parameters: Dict[str, Any] = Field(default_factory=dict)

class FixStrategy(BaseModel):
    """Fix strategy validation model"""
    
    strategy_type: str = Field(..., regex="^(conservative|aggressive)$")
    consider_breaking_changes: bool = Field(False)
    constraints: List[str] = Field(default_factory=list)
    preferences: Dict[str, str] = Field(default_factory=dict)

class ChainConfig(BaseModel):
    """Chain configuration validation model"""
    
    include_evidence: bool = Field(True)
    include_confidence: bool = Field(True)
    required_steps: List[str] = Field(default_factory=list)
    step_parameters: Dict[str, str] = Field(default_factory=dict)

def validate_request(request: Any, model_class: type) -> None:
    """Validate request against model class"""
    try:
        model_class.parse_obj(request)
    except Exception as e:
        raise ValidationError(f"Validation error: {str(e)}")

def validate_component_name(name: str) -> bool:
    """Validate component name format"""
    if not name:
        return False
    if len(name) > 255:
        return False
    return True

def validate_version_format(version: str) -> bool:
    """Validate version string format"""
    if not version:
        return False
    if len(version) > 100:
        return False
    if not any(c.isdigit() for c in version):
        return False
    return True

def validate_cvss_score(score: Optional[float]) -> bool:
    """Validate CVSS score"""
    if score is None:
        return True
    return 0.0 <= score <= 10.0

def validate_severity_level(severity: str) -> bool:
    """Validate severity level"""
    valid_levels = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"}
    return severity in valid_levels

def validate_source_type(source: str) -> bool:
    """Validate vulnerability source type"""
    valid_sources = {
        "NVD", "OSS_INDEX", "OSV", "GITHUB",
        "SUSE", "REDHAT", "DEBIAN", "UBUNTU",
        "ALPINE", "UNKNOWN"
    }
    return source in valid_sources

def validate_sbom_format(format_str: str) -> bool:
    """Validate SBOM format"""
    valid_formats = {"SPDX", "CYCLONEDX", "SWID", "UNKNOWN"}
    return format_str in valid_formats

def validate_checksum(checksum: str, algorithm: str) -> bool:
    """Validate checksum format"""
    if algorithm.upper() == "SHA256":
        return len(checksum) == 64 and all(c in "0123456789abcdefABCDEF" for c in checksum)
    elif algorithm.upper() == "MD5":
        return len(checksum) == 32 and all(c in "0123456789abcdefABCDEF" for c in checksum)
    return False 