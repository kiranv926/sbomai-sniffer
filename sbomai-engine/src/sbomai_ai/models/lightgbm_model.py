"""
LightGBM model for risk prediction and analysis.
"""

import lightgbm as lgb
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass
import pandas as pd
from sklearn.preprocessing import StandardScaler
import shap

logger = logging.getLogger(__name__)

@dataclass
class LightGBMConfig:
    """Configuration for LightGBM model"""
    num_leaves: int = 31
    learning_rate: float = 0.1
    n_estimators: int = 100
    objective: str = "regression"
    random_state: int = 42

class LightGBMRiskModel:
    """
    LightGBM model for vulnerability risk prediction and analysis.
    """
    
    def __init__(self, config: LightGBMConfig):
        self.config = config
        self.model = lgb.LGBMRegressor(
            num_leaves=config.num_leaves,
            learning_rate=config.learning_rate,
            n_estimators=config.n_estimators,
            objective=config.objective,
            random_state=config.random_state
        )
        self.scaler = StandardScaler()
        self.feature_names = None
        self.explainer = None
    
    def train(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]):
        """
        Train the LightGBM model.
        
        Args:
            X: Feature matrix
            y: Target values
            feature_names: Names of features
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        
        # Save feature names
        self.feature_names = feature_names
        
        # Initialize SHAP explainer
        self.explainer = shap.TreeExplainer(self.model)
        
        logger.info("LightGBM model trained successfully")
    
    def predict(self, features: np.ndarray) -> Tuple[float, Dict[str, float]]:
        """
        Predict risk score and get feature importance.
        
        Args:
            features: Input features
        
        Returns:
            Tuple of (risk_score, feature_importance_dict)
        """
        if not self.feature_names:
            raise ValueError("Model not trained - no feature names available")
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get prediction
        risk_score = self.model.predict(features_scaled)[0]
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(features_scaled)
        
        # Create feature importance dict
        importance_dict = {
            name: abs(value)
            for name, value in zip(self.feature_names, shap_values[0])
        }
        
        return risk_score, importance_dict
    
    def analyze_vulnerability(self, vuln_data: Dict) -> Dict:
        """
        Analyze vulnerability using LightGBM model.
        
        Args:
            vuln_data: Vulnerability information
        
        Returns:
            Analysis results including:
            - Risk score
            - Feature importance
            - Risk factors
            - Recommendations
        """
        try:
            # Extract features
            features = self._extract_features(vuln_data)
            
            # Get prediction and importance
            risk_score, importance = self.predict(features)
            
            # Generate analysis
            analysis = self._generate_analysis(
                vuln_data,
                risk_score,
                importance
            )
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error in LightGBM analysis: {e}")
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
        feature_importance: Dict[str, float]
    ) -> Dict:
        """Generate analysis from model outputs"""
        # Sort features by importance
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Identify key risk factors
        risk_factors = []
        for feature, importance in sorted_features[:3]:
            if importance > 0.1:  # Threshold for significance
                risk_factors.append(
                    f"{feature.replace('_', ' ').title()}: {importance:.2f}"
                )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            vuln_data,
            sorted_features
        )
        
        return {
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "key_risk_factors": risk_factors,
            "feature_importance": dict(sorted_features),
            "recommendations": recommendations
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
    
    def _generate_recommendations(
        self,
        vuln_data: Dict,
        feature_importance: List[Tuple[str, float]]
    ) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Add recommendations based on important features
        for feature, importance in feature_importance:
            if importance > 0.1:  # Significant feature
                if "cvss" in feature.lower():
                    recommendations.append(
                        "Prioritize remediation based on high CVSS score"
                    )
                elif "exploit" in feature.lower():
                    recommendations.append(
                        "Implement detection for known exploit patterns"
                    )
                elif "threat" in feature.lower():
                    recommendations.append(
                        "Monitor for threat actor activity"
                    )
                elif "malware" in feature.lower():
                    recommendations.append(
                        "Deploy malware detection controls"
                    )
                elif "patch" in feature.lower():
                    recommendations.append(
                        "Implement automated patch management"
                    )
                elif "component" in feature.lower():
                    recommendations.append(
                        "Review and minimize affected components"
                    )
        
        # Add general recommendations
        recommendations.extend([
            "Regular vulnerability scanning",
            "Security patch management",
            "Threat intelligence monitoring",
            "Component dependency analysis"
        ])
        
        return recommendations