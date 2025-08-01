"""
SBOMAI Engine

Advanced AI/ML engine for intelligent, explainable, and predictive SBOM analysis.
Provides gRPC endpoints for risk explanation, prediction, remediation suggestions, and explainable chains.
"""

__version__ = "1.0.0"
__author__ = "SBOMAI Team"
__description__ = "Advanced AI/ML engine for SBOM analysis"

from .service import SbomaiAiService
from .models import *
from .utils import *

__all__ = [
    "SbomaiAiService",
    "__version__",
    "__author__",
    "__description__",
] 