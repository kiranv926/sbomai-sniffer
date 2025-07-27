"""
Risk assessment and vulnerability prediction models for SBOM analysis
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

from ..utils.exceptions import MlModelError
from ..config import get_config

logger = logging.getLogger(__name__)


class RiskAssessmentModel:
    """Model for assessing risk levels of SBOM components"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.config = get_config()
        self.model_path = model_path or os.path.join(self.config.ml_model.model_cache_dir, "risk_assessment_model.pkl")
        self.scaler_path = os.path.join(self.config.ml_model.model_cache_dir, "risk_scaler.pkl")
        
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'cvss_score', 'vulnerability_count', 'days_since_published',
            'component_age_days', 'license_risk_score', 'version_risk_score',
            'dependency_depth', 'maintainer_activity_score', 'download_count_log',
            'has_security_policy', 'has_documentation', 'is_prerelease'
        ]
        
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create a new one"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                logger.info("Loaded existing risk assessment model")
            else:
                self._create_new_model()
                logger.info("Created new risk assessment model")
        except Exception as e:
            logger.warning(f"Failed to load model: {e}")
            self._create_new_model()
    
    def _create_new_model(self):
        """Create a new risk assessment model"""
        self.model = RandomForestClassifier(
            n_estimators=self.config.ml_model.xgboost_n_estimators,
            max_depth=self.config.ml_model.xgboost_max_depth,
            random_state=self.config.ml_model.xgboost_random_state,
            n_jobs=-1
        )
    
    def extract_features(self, component: Dict[str, Any], vulnerabilities: List[Dict[str, Any]]) -> np.ndarray:
        """Extract features from component and vulnerabilities"""
        features = []
        
        # CVSS score (max if multiple vulnerabilities)
        cvss_score = max([v.get('cvss_score', 0) for v in vulnerabilities]) if vulnerabilities else 0
        features.append(cvss_score)
        
        # Vulnerability count
        features.append(len(vulnerabilities))
        
        # Days since vulnerability published
        if vulnerabilities:
            from datetime import datetime
            latest_date = max([v.get('published_date', '') for v in vulnerabilities])
            if latest_date:
                try:
                    pub_date = datetime.fromisoformat(latest_date.replace('Z', '+00:00'))
                    days_since = (datetime.now() - pub_date).days
                except:
                    days_since = 365  # Default to 1 year
            else:
                days_since = 365
        else:
            days_since = 0
        features.append(days_since)
        
        # Component age (simplified)
        component_age = 365  # Default
        features.append(component_age)
        
        # License risk score
        licenses = component.get('licenses', [])
        license_risk = self._calculate_license_risk(licenses)
        features.append(license_risk)
        
        # Version risk score
        version = component.get('version', '')
        version_risk = self._calculate_version_risk(version)
        features.append(version_risk)
        
        # Dependency depth (simplified)
        features.append(1)  # Default depth
        
        # Maintainer activity score (simplified)
        features.append(0.5)  # Default score
        
        # Download count (simplified)
        features.append(5.0)  # Default log value
        
        # Security policy flag
        features.append(1 if component.get('metadata', {}).get('has_security_policy') else 0)
        
        # Documentation flag
        features.append(1 if component.get('description') else 0)
        
        # Prerelease flag
        is_prerelease = any(x in version.lower() for x in ['alpha', 'beta', 'rc', 'pre']) if version else False
        features.append(1 if is_prerelease else 0)
        
        return np.array(features).reshape(1, -1)
    
    def _calculate_license_risk(self, licenses: List[str]) -> float:
        """Calculate risk score based on licenses"""
        if not licenses:
            return 0.8  # High risk for no license
        
        high_risk_licenses = ['gpl', 'agpl', 'lgpl']
        medium_risk_licenses = ['mpl', 'epl', 'cddl']
        
        for license_name in licenses:
            license_lower = license_name.lower()
            if any(risk_license in license_lower for risk_license in high_risk_licenses):
                return 0.9
            elif any(risk_license in license_lower for risk_license in medium_risk_licenses):
                return 0.6
        
        return 0.2  # Low risk for permissive licenses
    
    def _calculate_version_risk(self, version: str) -> float:
        """Calculate risk score based on version"""
        if not version:
            return 0.8
        
        # Major version 0 indicates unstable
        if version.startswith('0.'):
            return 0.7
        
        # Prerelease versions
        if any(x in version.lower() for x in ['alpha', 'beta', 'rc', 'pre']):
            return 0.8
        
        # Very old versions
        try:
            major = int(version.split('.')[0])
            if major < 1:
                return 0.6
        except:
            pass
        
        return 0.3  # Default low risk
    
    def predict_risk_level(self, component: Dict[str, Any], vulnerabilities: List[Dict[str, Any]]) -> Tuple[str, float]:
        """Predict risk level for a component"""
        try:
            features = self.extract_features(component, vulnerabilities)
            features_scaled = self.scaler.transform(features)
            
            # Predict probability
            proba = self.model.predict_proba(features_scaled)[0]
            prediction = self.model.predict(features_scaled)[0]
            
            # Map prediction to risk level
            risk_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
            risk_level = risk_levels[prediction] if prediction < len(risk_levels) else 'UNKNOWN'
            
            # Confidence is the probability of the predicted class
            confidence = max(proba)
            
            return risk_level, confidence
            
        except Exception as e:
            logger.error(f"Error predicting risk level: {e}")
            raise MlModelError(f"Failed to predict risk level: {e}")
    
    def train(self, training_data: List[Dict[str, Any]]):
        """Train the model with provided data"""
        try:
            X = []
            y = []
            
            for item in training_data:
                component = item['component']
                vulnerabilities = item.get('vulnerabilities', [])
                risk_level = item['risk_level']
                
                features = self.extract_features(component, vulnerabilities)
                X.append(features.flatten())
                
                # Convert risk level to numeric
                risk_mapping = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2, 'CRITICAL': 3}
                y.append(risk_mapping.get(risk_level, 0))
            
            X = np.array(X)
            y = np.array(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test_scaled)
            logger.info(f"Model accuracy: {self.model.score(X_test_scaled, y_test):.3f}")
            
            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            
            logger.info("Model trained and saved successfully")
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise MlModelError(f"Failed to train model: {e}")


class VulnerabilityPredictor:
    """Model for predicting vulnerability likelihood"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.config = get_config()
        self.model_path = model_path or os.path.join(self.config.ml_model.model_cache_dir, "vuln_predictor_model.pkl")
        
        self.model = None
        self.feature_names = [
            'component_age_days', 'version_count', 'maintainer_count',
            'last_update_days', 'download_frequency', 'issue_count',
            'pr_count', 'star_count', 'fork_count', 'language_popularity'
        ]
        
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create a new one"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logger.info("Loaded existing vulnerability predictor model")
            else:
                self._create_new_model()
                logger.info("Created new vulnerability predictor model")
        except Exception as e:
            logger.warning(f"Failed to load model: {e}")
            self._create_new_model()
    
    def _create_new_model(self):
        """Create a new vulnerability predictor model"""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
    
    def extract_features(self, component: Dict[str, Any]) -> np.ndarray:
        """Extract features for vulnerability prediction"""
        features = []
        
        # Component age (simplified)
        features.append(365)  # Default age
        
        # Version count (simplified)
        features.append(10)  # Default version count
        
        # Maintainer count (simplified)
        features.append(2)  # Default maintainer count
        
        # Days since last update (simplified)
        features.append(30)  # Default days
        
        # Download frequency (simplified)
        features.append(1000)  # Default downloads per day
        
        # Issue count (simplified)
        features.append(50)  # Default issue count
        
        # PR count (simplified)
        features.append(20)  # Default PR count
        
        # Star count (simplified)
        features.append(100)  # Default star count
        
        # Fork count (simplified)
        features.append(25)  # Default fork count
        
        # Language popularity (simplified)
        features.append(0.7)  # Default popularity score
        
        return np.array(features).reshape(1, -1)
    
    def predict_vulnerability_likelihood(self, component: Dict[str, Any]) -> Tuple[float, float]:
        """Predict likelihood of vulnerabilities in component"""
        try:
            features = self.extract_features(component)
            
            # Predict probability
            proba = self.model.predict_proba(features)[0]
            
            # Assuming binary classification: vulnerable vs not vulnerable
            vulnerability_prob = proba[1] if len(proba) > 1 else 0.5
            confidence = max(proba)
            
            return vulnerability_prob, confidence
            
        except Exception as e:
            logger.error(f"Error predicting vulnerability likelihood: {e}")
            raise MlModelError(f"Failed to predict vulnerability likelihood: {e}")
    
    def train(self, training_data: List[Dict[str, Any]]):
        """Train the model with provided data"""
        try:
            X = []
            y = []
            
            for item in training_data:
                component = item['component']
                has_vulnerabilities = item['has_vulnerabilities']
                
                features = self.extract_features(component)
                X.append(features.flatten())
                y.append(1 if has_vulnerabilities else 0)
            
            X = np.array(X)
            y = np.array(y)
            
            # Train model
            self.model.fit(X, y)
            
            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            
            logger.info("Vulnerability predictor model trained and saved successfully")
            
        except Exception as e:
            logger.error(f"Error training vulnerability predictor: {e}")
            raise MlModelError(f"Failed to train vulnerability predictor: {e}")


class RiskScoreCalculator:
    """Utility class for calculating comprehensive risk scores"""
    
    @staticmethod
    def calculate_comprehensive_risk_score(
        component: Dict[str, Any],
        vulnerabilities: List[Dict[str, Any]],
        risk_level: str,
        vulnerability_likelihood: float
    ) -> float:
        """Calculate comprehensive risk score (0-100)"""
        base_score = 0.0
        
        # Base score from risk level
        risk_level_scores = {
            'LOW': 10.0,
            'MEDIUM': 30.0,
            'HIGH': 60.0,
            'CRITICAL': 90.0
        }
        base_score += risk_level_scores.get(risk_level, 50.0)
        
        # Adjust for vulnerabilities
        if vulnerabilities:
            max_cvss = max([v.get('cvss_score', 0) for v in vulnerabilities])
            base_score += max_cvss * 2.0  # CVSS score multiplier
        
        # Adjust for vulnerability likelihood
        base_score += vulnerability_likelihood * 20.0
        
        # Component-specific adjustments
        version = component.get('version', '')
        if version.startswith('0.'):
            base_score += 15.0  # Unstable version
        
        if not component.get('licenses'):
            base_score += 10.0  # No license
        
        # Normalize to 0-100 range
        return min(max(base_score, 0.0), 100.0)
    
    @staticmethod
    def calculate_confidence_interval(risk_score: float, confidence: float) -> Tuple[float, float]:
        """Calculate confidence interval for risk score"""
        margin = (1.0 - confidence) * 20.0  # 20 point margin at 0 confidence
        lower = max(0.0, risk_score - margin)
        upper = min(100.0, risk_score + margin)
        return lower, upper 