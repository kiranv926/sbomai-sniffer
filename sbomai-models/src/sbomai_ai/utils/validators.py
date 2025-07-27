"""
Validation utilities for SBOMAI AI Microservice
"""

import re
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json

from ..utils.exceptions import ValidationError

logger = logging.getLogger(__name__)


class SbomValidator:
    """Validator for SBOM data structures"""
    
    @staticmethod
    def validate_component(component: Dict[str, Any]) -> List[str]:
        """Validate SBOM component data"""
        errors = []
        
        # Required fields
        if not component.get('name'):
            errors.append("Component name is required")
        
        if not component.get('version'):
            errors.append("Component version is required")
        
        # Validate version format
        version = component.get('version', '')
        if version and not SbomValidator._is_valid_version(version):
            errors.append(f"Invalid version format: {version}")
        
        # Validate PURL if present
        purl = component.get('purl', '')
        if purl and not SbomValidator._is_valid_purl(purl):
            errors.append(f"Invalid PURL format: {purl}")
        
        # Validate licenses
        licenses = component.get('licenses', [])
        if not isinstance(licenses, list):
            errors.append("Licenses must be a list")
        else:
            for license_name in licenses:
                if not isinstance(license_name, str) or not license_name.strip():
                    errors.append("License names must be non-empty strings")
        
        # Validate metadata
        metadata = component.get('metadata', {})
        if not isinstance(metadata, dict):
            errors.append("Metadata must be a dictionary")
        
        return errors
    
    @staticmethod
    def validate_vulnerability(vulnerability: Dict[str, Any]) -> List[str]:
        """Validate vulnerability data"""
        errors = []
        
        # Required fields
        if not vulnerability.get('id'):
            errors.append("Vulnerability ID is required")
        
        # Validate CVSS score
        cvss_score = vulnerability.get('cvss_score', 0)
        if not isinstance(cvss_score, (int, float)) or cvss_score < 0 or cvss_score > 10:
            errors.append(f"CVSS score must be between 0 and 10, got: {cvss_score}")
        
        # Validate severity
        severity = vulnerability.get('severity')
        valid_severities = ['UNKNOWN_SEVERITY', 'NONE', 'LOW_SEVERITY', 'MEDIUM_SEVERITY', 'HIGH_SEVERITY', 'CRITICAL_SEVERITY']
        if severity and severity not in valid_severities:
            errors.append(f"Invalid severity: {severity}. Must be one of: {valid_severities}")
        
        # Validate dates
        published_date = vulnerability.get('published_date', '')
        if published_date and not SbomValidator._is_valid_date(published_date):
            errors.append(f"Invalid published date format: {published_date}")
        
        # Validate references
        references = vulnerability.get('references', [])
        if not isinstance(references, list):
            errors.append("References must be a list")
        else:
            for ref in references:
                if not isinstance(ref, str) or not ref.strip():
                    errors.append("References must be non-empty strings")
        
        return errors
    
    @staticmethod
    def validate_sbom_document(sbom_doc: Dict[str, Any]) -> List[str]:
        """Validate SBOM document structure"""
        errors = []
        
        # Required fields
        if not sbom_doc.get('name'):
            errors.append("SBOM document name is required")
        
        if not sbom_doc.get('version'):
            errors.append("SBOM document version is required")
        
        # Validate format
        format_type = sbom_doc.get('format')
        valid_formats = ['UNKNOWN_FORMAT', 'SPDX', 'CYCLONEDX', 'SWID', 'CUSTOM']
        if format_type and format_type not in valid_formats:
            errors.append(f"Invalid SBOM format: {format_type}. Must be one of: {valid_formats}")
        
        # Validate created date
        created_date = sbom_doc.get('created_date', '')
        if created_date and not SbomValidator._is_valid_date(created_date):
            errors.append(f"Invalid created date format: {created_date}")
        
        # Validate components
        components = sbom_doc.get('components', [])
        if not isinstance(components, list):
            errors.append("Components must be a list")
        else:
            for i, component in enumerate(components):
                component_errors = SbomValidator.validate_component(component)
                for error in component_errors:
                    errors.append(f"Component {i}: {error}")
        
        # Validate metadata
        metadata = sbom_doc.get('metadata', {})
        if not isinstance(metadata, dict):
            errors.append("Metadata must be a dictionary")
        
        return errors
    
    @staticmethod
    def _is_valid_version(version: str) -> bool:
        """Check if version string has valid format"""
        # Basic semver-like validation
        pattern = r'^[0-9]+\.[0-9]+(\.[0-9]+)?(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$'
        return bool(re.match(pattern, version))
    
    @staticmethod
    def _is_valid_purl(purl: str) -> bool:
        """Check if PURL has valid format"""
        # Basic PURL validation
        pattern = r'^pkg:[a-zA-Z0-9]+(/[a-zA-Z0-9.-]+)*@[a-zA-Z0-9.-]+(\?[a-zA-Z0-9=&]+)?(#.*)?$'
        return bool(re.match(pattern, purl))
    
    @staticmethod
    def _is_valid_date(date_str: str) -> bool:
        """Check if date string has valid format"""
        try:
            # Try parsing as ISO format
            datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return True
        except ValueError:
            try:
                # Try parsing as RFC 3339 format
                datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                return True
            except ValueError:
                return False


class AiModelValidator:
    """Validator for AI model configurations"""
    
    @staticmethod
    def validate_ai_model_config(config: Dict[str, Any]) -> List[str]:
        """Validate AI model configuration"""
        errors = []
        
        # Validate model name
        model_name = config.get('model_name', '')
        if not model_name:
            errors.append("Model name is required")
        
        # Validate temperature
        temperature = config.get('temperature', 0.3)
        if not isinstance(temperature, (int, float)) or temperature < 0 or temperature > 2:
            errors.append(f"Temperature must be between 0 and 2, got: {temperature}")
        
        # Validate max tokens
        max_tokens = config.get('max_tokens', 4000)
        if not isinstance(max_tokens, int) or max_tokens < 1 or max_tokens > 100000:
            errors.append(f"Max tokens must be between 1 and 100000, got: {max_tokens}")
        
        # Validate provider
        provider = config.get('provider', '')
        valid_providers = ['openai', 'anthropic', 'google', 'local']
        if provider and provider not in valid_providers:
            errors.append(f"Invalid provider: {provider}. Must be one of: {valid_providers}")
        
        return errors
    
    @staticmethod
    def validate_ml_model_config(config: Dict[str, Any]) -> List[str]:
        """Validate ML model configuration"""
        errors = []
        
        # Validate model type
        model_type = config.get('model_type', '')
        valid_types = ['xgboost', 'lightgbm', 'logistic_regression', 'random_forest']
        if model_type and model_type not in valid_types:
            errors.append(f"Invalid model type: {model_type}. Must be one of: {valid_types}")
        
        # Validate hyperparameters
        hyperparameters = config.get('hyperparameters', {})
        if not isinstance(hyperparameters, dict):
            errors.append("Hyperparameters must be a dictionary")
        
        # Validate boolean flags
        use_feature_importance = config.get('use_feature_importance', True)
        if not isinstance(use_feature_importance, bool):
            errors.append("use_feature_importance must be a boolean")
        
        use_confidence_intervals = config.get('use_confidence_intervals', True)
        if not isinstance(use_confidence_intervals, bool):
            errors.append("use_confidence_intervals must be a boolean")
        
        return errors


class InputValidator:
    """General input validation utilities"""
    
    @staticmethod
    def validate_string(value: Any, field_name: str, max_length: int = 1000, required: bool = True) -> List[str]:
        """Validate string input"""
        errors = []
        
        if required and not value:
            errors.append(f"{field_name} is required")
            return errors
        
        if value is not None:
            if not isinstance(value, str):
                errors.append(f"{field_name} must be a string")
            elif len(value) > max_length:
                errors.append(f"{field_name} must be at most {max_length} characters")
        
        return errors
    
    @staticmethod
    def validate_number(value: Any, field_name: str, min_val: float = None, max_val: float = None, required: bool = True) -> List[str]:
        """Validate numeric input"""
        errors = []
        
        if required and value is None:
            errors.append(f"{field_name} is required")
            return errors
        
        if value is not None:
            if not isinstance(value, (int, float)):
                errors.append(f"{field_name} must be a number")
            else:
                if min_val is not None and value < min_val:
                    errors.append(f"{field_name} must be at least {min_val}")
                if max_val is not None and value > max_val:
                    errors.append(f"{field_name} must be at most {max_val}")
        
        return errors
    
    @staticmethod
    def validate_list(value: Any, field_name: str, max_items: int = 1000, required: bool = True) -> List[str]:
        """Validate list input"""
        errors = []
        
        if required and not value:
            errors.append(f"{field_name} is required")
            return errors
        
        if value is not None:
            if not isinstance(value, list):
                errors.append(f"{field_name} must be a list")
            elif len(value) > max_items:
                errors.append(f"{field_name} must have at most {max_items} items")
        
        return errors
    
    @staticmethod
    def validate_dict(value: Any, field_name: str, required: bool = True) -> List[str]:
        """Validate dictionary input"""
        errors = []
        
        if required and not value:
            errors.append(f"{field_name} is required")
            return errors
        
        if value is not None and not isinstance(value, dict):
            errors.append(f"{field_name} must be a dictionary")
        
        return errors
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """Sanitize string input"""
        if not isinstance(value, str):
            return ""
        
        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', value)
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @staticmethod
    def sanitize_json_string(value: str) -> str:
        """Sanitize JSON string input"""
        if not isinstance(value, str):
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', value)
        
        # Limit length
        if len(sanitized) > 10000:  # 10KB limit for JSON strings
            sanitized = sanitized[:10000]
        
        return sanitized


class RequestValidator:
    """Validator for gRPC request data"""
    
    @staticmethod
    def validate_explain_risk_request(request: Dict[str, Any]) -> List[str]:
        """Validate ExplainRiskRequest"""
        errors = []
        
        # Validate component
        component = request.get('component')
        if not component:
            errors.append("Component is required")
        else:
            errors.extend(SbomValidator.validate_component(component))
        
        # Validate vulnerabilities (optional)
        vulnerabilities = request.get('vulnerabilities', [])
        if not isinstance(vulnerabilities, list):
            errors.append("Vulnerabilities must be a list")
        else:
            for i, vuln in enumerate(vulnerabilities):
                vuln_errors = SbomValidator.validate_vulnerability(vuln)
                for error in vuln_errors:
                    errors.append(f"Vulnerability {i}: {error}")
        
        # Validate analysis context
        analysis_context = request.get('analysis_context', '')
        errors.extend(InputValidator.validate_string(analysis_context, 'analysis_context', max_length=5000, required=False))
        
        # Validate model config (optional)
        model_config = request.get('model_config')
        if model_config:
            errors.extend(AiModelValidator.validate_ai_model_config(model_config))
        
        return errors
    
    @staticmethod
    def validate_predict_risk_score_request(request: Dict[str, Any]) -> List[str]:
        """Validate PredictRiskScoreRequest"""
        errors = []
        
        # Validate component
        component = request.get('component')
        if not component:
            errors.append("Component is required")
        else:
            errors.extend(SbomValidator.validate_component(component))
        
        # Validate historical vulnerabilities (optional)
        historical_vulnerabilities = request.get('historical_vulnerabilities', [])
        if not isinstance(historical_vulnerabilities, list):
            errors.append("Historical vulnerabilities must be a list")
        else:
            for i, vuln in enumerate(historical_vulnerabilities):
                vuln_errors = SbomValidator.validate_vulnerability(vuln)
                for error in vuln_errors:
                    errors.append(f"Historical vulnerability {i}: {error}")
        
        # Validate features (optional)
        features = request.get('features', [])
        errors.extend(InputValidator.validate_list(features, 'features', max_items=100, required=False))
        
        # Validate ML config (optional)
        ml_config = request.get('ml_config')
        if ml_config:
            errors.extend(AiModelValidator.validate_ml_model_config(ml_config))
        
        return errors
    
    @staticmethod
    def validate_suggest_fix_request(request: Dict[str, Any]) -> List[str]:
        """Validate SuggestFixRequest"""
        errors = []
        
        # Validate vulnerability ID
        vulnerability_id = request.get('vulnerability_id', '')
        errors.extend(InputValidator.validate_string(vulnerability_id, 'vulnerability_id', max_length=100))
        
        # Validate component
        component = request.get('component')
        if not component:
            errors.append("Component is required")
        else:
            errors.extend(SbomValidator.validate_component(component))
        
        # Validate constraints (optional)
        constraints = request.get('constraints', [])
        errors.extend(InputValidator.validate_list(constraints, 'constraints', max_items=50, required=False))
        
        # Validate strategy (optional)
        strategy = request.get('strategy')
        if strategy:
            errors.extend(RequestValidator._validate_fix_strategy(strategy))
        
        return errors
    
    @staticmethod
    def validate_explainable_sbom_chain_request(request: Dict[str, Any]) -> List[str]:
        """Validate ExplainableSbomChainRequest"""
        errors = []
        
        # Validate SBOM document
        sbom_document = request.get('sbom_document')
        if not sbom_document:
            errors.append("SBOM document is required")
        else:
            errors.extend(SbomValidator.validate_sbom_document(sbom_document))
        
        # Validate steps (optional)
        steps = request.get('steps', [])
        if not isinstance(steps, list):
            errors.append("Steps must be a list")
        else:
            for i, step in enumerate(steps):
                step_errors = RequestValidator._validate_analysis_step(step)
                for error in step_errors:
                    errors.append(f"Step {i}: {error}")
        
        # Validate chain config (optional)
        chain_config = request.get('chain_config')
        if chain_config:
            errors.extend(RequestValidator._validate_chain_config(chain_config))
        
        return errors
    
    @staticmethod
    def _validate_fix_strategy(strategy: Dict[str, Any]) -> List[str]:
        """Validate fix strategy configuration"""
        errors = []
        
        approach = strategy.get('approach', '')
        valid_approaches = ['conservative', 'aggressive', 'balanced']
        if approach and approach not in valid_approaches:
            errors.append(f"Invalid approach: {approach}. Must be one of: {valid_approaches}")
        
        consider_breaking_changes = strategy.get('consider_breaking_changes', False)
        if not isinstance(consider_breaking_changes, bool):
            errors.append("consider_breaking_changes must be a boolean")
        
        prefer_latest_versions = strategy.get('prefer_latest_versions', False)
        if not isinstance(prefer_latest_versions, bool):
            errors.append("prefer_latest_versions must be a boolean")
        
        priority_criteria = strategy.get('priority_criteria', [])
        errors.extend(InputValidator.validate_list(priority_criteria, 'priority_criteria', max_items=20, required=False))
        
        return errors
    
    @staticmethod
    def _validate_analysis_step(step: Dict[str, Any]) -> List[str]:
        """Validate analysis step configuration"""
        errors = []
        
        step_name = step.get('step_name', '')
        errors.extend(InputValidator.validate_string(step_name, 'step_name', max_length=100))
        
        description = step.get('description', '')
        errors.extend(InputValidator.validate_string(description, 'description', max_length=500, required=False))
        
        parameters = step.get('parameters', {})
        errors.extend(InputValidator.validate_dict(parameters, 'parameters', required=False))
        
        return errors
    
    @staticmethod
    def _validate_chain_config(config: Dict[str, Any]) -> List[str]:
        """Validate chain configuration"""
        errors = []
        
        max_steps = config.get('max_steps', 10)
        errors.extend(InputValidator.validate_number(max_steps, 'max_steps', min_val=1, max_val=100, required=False))
        
        confidence_threshold = config.get('confidence_threshold', 0.5)
        errors.extend(InputValidator.validate_number(confidence_threshold, 'confidence_threshold', min_val=0.0, max_val=1.0, required=False))
        
        include_detailed_explanations = config.get('include_detailed_explanations', True)
        if not isinstance(include_detailed_explanations, bool):
            errors.append("include_detailed_explanations must be a boolean")
        
        analysis_types = config.get('analysis_types', [])
        valid_types = ['vulnerability', 'license', 'outdated', 'custom']
        if analysis_types:
            for analysis_type in analysis_types:
                if analysis_type not in valid_types:
                    errors.append(f"Invalid analysis type: {analysis_type}. Must be one of: {valid_types}")
        
        return errors


def validate_and_sanitize_request(request_data: Dict[str, Any], request_type: str) -> Dict[str, Any]:
    """Validate and sanitize request data"""
    errors = []
    
    # Validate based on request type
    if request_type == 'explain_risk':
        errors = RequestValidator.validate_explain_risk_request(request_data)
    elif request_type == 'predict_risk_score':
        errors = RequestValidator.validate_predict_risk_score_request(request_data)
    elif request_type == 'suggest_fix':
        errors = RequestValidator.validate_suggest_fix_request(request_data)
    elif request_type == 'explainable_sbom_chain':
        errors = RequestValidator.validate_explainable_sbom_chain_request(request_data)
    else:
        errors.append(f"Unknown request type: {request_type}")
    
    if errors:
        raise ValidationError(f"Validation failed: {'; '.join(errors)}")
    
    # Sanitize string fields
    sanitized_data = _sanitize_request_data(request_data)
    
    return sanitized_data


def _sanitize_request_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively sanitize request data"""
    if isinstance(data, dict):
        return {key: _sanitize_request_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [_sanitize_request_data(item) for item in data]
    elif isinstance(data, str):
        return InputValidator.sanitize_string(data)
    else:
        return data 