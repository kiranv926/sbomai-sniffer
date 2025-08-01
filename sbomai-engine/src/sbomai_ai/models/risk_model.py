"""
Risk Assessment model combining multiple ML models.
"""

from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingRegressor
import shap

from .xgboost_model import XGBoostRiskModel, XGBoostConfig
from .lightgbm_model import LightGBMRiskModel, LightGBMConfig

logger = logging.getLogger(__name__)

@dataclass
class RiskAssessmentConfig:
    """Configuration for Risk Assessment model"""
    xgboost_config: XGBoostConfig
    lightgbm_config: LightGBMConfig
    voting_weights: Optional[List[float]] = None

class RiskAssessmentModel:
    """
    Ensemble model combining multiple risk assessment approaches.
    """
    
    def __init__(self, config: RiskAssessmentConfig):
        self.config = config
        
        # Initialize component models
        self.xgboost_model = XGBoostRiskModel(config.xgboost_config)
        self.lightgbm_model = LightGBMRiskModel(config.lightgbm_config)
        
        # Initialize ensemble
        self.ensemble = None
        self.feature_names = None
        self.explainer = None
    
    def train(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]):
        """
        Train all component models and create ensemble.
        
        Args:
            X: Feature matrix
            y: Target values
            feature_names: Names of features
        """
        # Train component models
        self.xgboost_model.train(X, y, feature_names)
        self.lightgbm_model.train(X, y, feature_names)
        
        # Create voting ensemble
        self.ensemble = VotingRegressor(
            estimators=[
                ('xgboost', self.xgboost_model.model),
                ('lightgbm', self.lightgbm_model.model)
            ],
            weights=self.config.voting_weights
        )
        
        # Train ensemble
        self.ensemble.fit(X, y)
        
        # Save feature names
        self.feature_names = feature_names
        
        # Initialize SHAP explainer using XGBoost model
        self.explainer = self.xgboost_model.explainer
        
        logger.info("Risk Assessment ensemble trained successfully")
    
    def predict(self, features: np.ndarray) -> Tuple[float, Dict[str, float]]:
        """
        Get ensemble prediction and feature importance.
        
        Args:
            features: Input features
        
        Returns:
            Tuple of (risk_score, feature_importance_dict)
        """
        if not self.feature_names:
            raise ValueError("Model not trained - no feature names available")
        
        # Get predictions from component models
        xgb_score, xgb_importance = self.xgboost_model.predict(features)
        lgb_score, lgb_importance = self.lightgbm_model.predict(features)
        
        # Get ensemble prediction
        ensemble_score = self.ensemble.predict(features)[0]
        
        # Combine feature importance
        importance_dict = {}
        for feature in self.feature_names:
            importance_dict[feature] = (
                xgb_importance.get(feature, 0.0) +
                lgb_importance.get(feature, 0.0)
            ) / 2.0
        
        return ensemble_score, importance_dict
    
    def analyze_vulnerability(self, vuln_data: Dict) -> Dict:
        """
        Analyze vulnerability using ensemble model.
        
        Args:
            vuln_data: Vulnerability information
        
        Returns:
            Analysis results including:
            - Risk score
            - Feature importance
            - Risk factors
            - Recommendations
            - Model-specific analyses
        """
        try:
            # Get analyses from component models
            xgb_analysis = self.xgboost_model.analyze_vulnerability(vuln_data)
            lgb_analysis = self.lightgbm_model.analyze_vulnerability(vuln_data)
            
            # Extract features
            features = self._extract_features(vuln_data)
            
            # Get ensemble prediction
            risk_score, importance = self.predict(features)
            
            # Generate combined analysis
            analysis = self._generate_analysis(
                vuln_data,
                risk_score,
                importance,
                xgb_analysis,
                lgb_analysis
            )
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error in Risk Assessment analysis: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _extract_features(self, vuln_data: Dict) -> np.ndarray:
        """Extract features from vulnerability data"""
        features = [
            # CVSS metrics
            vuln_data.get('cvss_score', 0.0) / 10.0,  # Normalize
            
            # Exploit status
            {
                'NONE': 0.0,
                'UNPROVEN': 0.25,
                'PROOF_OF_CONCEPT': 0.5,
                'ACTIVELY_EXPLOITED': 0.75,
                'WEAPONIZED': 1.0
            }.get(vuln_data.get('exploit_status', 'NONE'), 0.0),
            
            # Threat intelligence
            len(vuln_data.get('threat_actors', [])) / 10.0,  # Normalize
            len(vuln_data.get('malware_families', [])) / 5.0,
            1.0 if vuln_data.get('known_ransomware') else 0.0,
            
            # Temporal factors
            vuln_data.get('temporal_score', 0.0) / 10.0,
            1.0 if vuln_data.get('patch_available') else 0.0,
            
            # Attack complexity
            {
                'LOW': 1.0,
                'MEDIUM': 0.5,
                'HIGH': 0.25
            }.get(vuln_data.get('attack_complexity', 'HIGH'), 0.0),
            
            # Additional features
            len(vuln_data.get('affected_components', [])) / 5.0,  # Normalize
            len(vuln_data.get('known_exploits', [])) / 3.0,
            1.0 if vuln_data.get('public_exploit') else 0.0
        ]
        
        return np.array(features).reshape(1, -1)
    
    def _generate_analysis(
        self,
        vuln_data: Dict,
        risk_score: float,
        feature_importance: Dict[str, float],
        xgb_analysis: Dict,
        lgb_analysis: Dict
    ) -> Dict:
        """Generate combined analysis"""
        # Sort features by importance
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Identify key risk factors (combine from both models)
        risk_factors = set()
        risk_factors.update(xgb_analysis.get('key_risk_factors', []))
        risk_factors.update(lgb_analysis.get('key_risk_factors', []))
        
        # Combine recommendations
        recommendations = set()
        recommendations.update(xgb_analysis.get('recommendations', []))
        recommendations.update(lgb_analysis.get('recommendations', []))
        
        return {
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "key_risk_factors": list(risk_factors),
            "feature_importance": dict(sorted_features),
            "recommendations": list(recommendations),
            "model_specific_analysis": {
                "xgboost": xgb_analysis,
                "lightgbm": lgb_analysis
            }
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level from score"""
        if score >= 0.8:
            return "CRITICAL"
        elif score >= 0.6:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"