"""
SBOMAI AI models initialization.
"""

from .ai_models import (
    ThreatContextEmbedding,
    VulnerabilityGNN,
    ExploitPredictor,
    CriticalityScorer,
    create_vulnerability_features,
    ModelPrediction
)

from .openai_model import OpenAiModel, OpenAiConfig
from .anthropic_model import AnthropicModel, AnthropicConfig
from .google_model import GoogleGeminiModel, GoogleGeminiConfig
from .local_model import LocalTransformerModel, LocalTransformerConfig
from .xgboost_model import XGBoostRiskModel, XGBoostConfig
from .lightgbm_model import LightGBMRiskModel, LightGBMConfig
from .risk_model import RiskAssessmentModel, RiskAssessmentConfig
from .predictor_model import VulnerabilityPredictor, VulnerabilityPredictorConfig
from .explainability_model import ExplainabilityChain, ExplainabilityConfig
from .gnn_predictor_model import GNNVulnerabilityPredictor, GNNVulnerabilityPredictorConfig
from .graph_builder_model import DependencyGraphBuilder, DependencyGraphConfig
from .graph_analyzer_model import DependencyGraphAnalyzer, DependencyGraphAnalyzerConfig

__all__ = [
    'ThreatContextEmbedding',
    'VulnerabilityGNN',
    'ExploitPredictor',
    'CriticalityScorer',
    'create_vulnerability_features',
    'ModelPrediction',
    'OpenAiModel',
    'OpenAiConfig',
    'AnthropicModel',
    'AnthropicConfig',
    'GoogleGeminiModel',
    'GoogleGeminiConfig',
    'LocalTransformerModel',
    'LocalTransformerConfig',
    'XGBoostRiskModel',
    'XGBoostConfig',
    'LightGBMRiskModel',
    'LightGBMConfig',
    'RiskAssessmentModel',
    'RiskAssessmentConfig',
    'VulnerabilityPredictor',
    'VulnerabilityPredictorConfig',
    'ExplainabilityChain',
    'ExplainabilityConfig',
    'GNNVulnerabilityPredictor',
    'GNNVulnerabilityPredictorConfig',
    'DependencyGraphBuilder',
    'DependencyGraphConfig',
    'DependencyGraphAnalyzer',
    'DependencyGraphAnalyzerConfig'
]