"""
Custom exceptions for SBOMAI AI Microservice
"""


class SbomaiAiError(Exception):
    """Base exception for SBOMAI AI Microservice"""
    pass


class AiModelError(SbomaiAiError):
    """Exception raised when AI model operations fail"""
    pass


class MlModelError(SbomaiAiError):
    """Exception raised when ML model operations fail"""
    pass


class ExplainabilityError(SbomaiAiError):
    """Exception raised when explainability operations fail"""
    pass


class ServiceError(SbomaiAiError):
    """Exception raised when gRPC service operations fail"""
    pass


class ValidationError(SbomaiAiError):
    """Exception raised when input validation fails"""
    pass


class ConfigurationError(SbomaiAiError):
    """Exception raised when configuration is invalid"""
    pass


class ModelNotFoundError(SbomaiAiError):
    """Exception raised when a requested model is not found"""
    pass


class ApiKeyError(SbomaiAiError):
    """Exception raised when API keys are missing or invalid"""
    pass


class RateLimitError(SbomaiAiError):
    """Exception raised when rate limits are exceeded"""
    pass


class TimeoutError(SbomaiAiError):
    """Exception raised when operations timeout"""
    pass 