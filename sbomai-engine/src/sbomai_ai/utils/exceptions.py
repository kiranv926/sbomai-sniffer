"""
Custom exceptions for SBOMAI AI Engine
"""

class SbomaiAiError(Exception):
    """Base exception for SBOMAI AI Engine"""
    pass

class AiModelError(SbomaiAiError):
    """Exception raised for AI model errors"""
    pass

class MlModelError(SbomaiAiError):
    """Exception raised for ML model errors"""
    pass

class ExplainabilityError(SbomaiAiError):
    """Exception raised for explainability chain errors"""
    pass

class ServiceError(SbomaiAiError):
    """Exception raised for service-level errors"""
    pass

class ValidationError(SbomaiAiError):
    """Exception raised for validation errors"""
    pass

class CacheError(SbomaiAiError):
    """Exception raised for caching errors"""
    pass

class MonitoringError(SbomaiAiError):
    """Exception raised for monitoring/metrics errors"""
    pass

class GraphError(SbomaiAiError):
    """Exception raised for graph analysis errors"""
    pass 