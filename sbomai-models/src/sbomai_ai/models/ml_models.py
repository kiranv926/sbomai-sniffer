"""
ML model implementations for SBOM risk prediction
"""

import asyncio
import pickle
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
import logging
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import lightgbm as lgb

from ..config import get_config
from ..utils.exceptions import MlModelError

logger = logging.getLogger(__name__)


class BaseMlModel(ABC):
    """Base class for ML models"""
    
    def __init__(self, model_name: str, model_type: str):
        self.model_name = model_name
        self.model_type = model_type
        self.config = get_config()
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
    @abstractmethod
    async def train(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]) -> Dict[str, float]:
        """Train the ML model"""
        pass
    
    @abstractmethod
    async def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Predict risk scores and confidence intervals"""
        pass
    
    @abstractmethod
    def get_feature_importance(self) -> List[Dict[str, Any]]:
        """Get feature importance scores"""
        pass
    
    def save_model(self, filepath: str):
        """Save the trained model"""
        if not self.is_trained:
            raise MlModelError("Model must be trained before saving")
        
        model_data = {
            "model": self.model,
            "scaler": self.scaler,
            "feature_names": self.feature_names,
            "model_name": self.model_name,
            "model_type": self.model_type,
            "is_trained": self.is_trained
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load a trained model"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data["model"]
            self.scaler = model_data["scaler"]
            self.feature_names = model_data["feature_names"]
            self.model_name = model_data["model_name"]
            self.model_type = model_data["model_type"]
            self.is_trained = model_data["is_trained"]
            
            logger.info(f"Model loaded from {filepath}")
        except Exception as e:
            raise MlModelError(f"Failed to load model: {e}")
    
    def is_model_available(self) -> bool:
        """Check if the model is available and trained"""
        return self.is_trained and self.model is not None


class XGBoostRiskModel(BaseMlModel):
    """XGBoost model for risk prediction"""
    
    def __init__(self):
        super().__init__(
            model_name="xgboost_risk_model",
            model_type="xgboost"
        )
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize XGBoost model with configuration"""
        self.model = xgb.XGBRegressor(
            n_estimators=self.config.ml_model.xgboost_n_estimators,
            max_depth=self.config.ml_model.xgboost_max_depth,
            learning_rate=self.config.ml_model.xgboost_learning_rate,
            random_state=self.config.ml_model.xgboost_random_state,
            objective='reg:squarederror',
            eval_metric='rmse'
        )
    
    async def train(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]) -> Dict[str, float]:
        """Train XGBoost model"""
        try:
            self.feature_names = feature_names
            
            # Split data for validation
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = await asyncio.to_thread(self.scaler.fit_transform, X_train)
            X_val_scaled = await asyncio.to_thread(self.scaler.transform, X_val)
            
            # Train model
            await asyncio.to_thread(
                self.model.fit,
                X_train_scaled,
                y_train,
                eval_set=[(X_val_scaled, y_val)],
                early_stopping_rounds=10,
                verbose=False
            )
            
            # Evaluate model
            y_pred = await asyncio.to_thread(self.model.predict, X_val_scaled)
            mse = mean_squared_error(y_val, y_pred)
            r2 = r2_score(y_val, y_pred)
            
            self.is_trained = True
            
            metrics = {
                "mse": mse,
                "rmse": np.sqrt(mse),
                "r2": r2,
                "feature_count": len(feature_names)
            }
            
            logger.info(f"XGBoost model trained successfully. R²: {r2:.4f}, RMSE: {np.sqrt(mse):.4f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to train XGBoost model: {e}")
            raise MlModelError(f"XGBoost training failed: {e}")
    
    async def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Predict risk scores with confidence intervals"""
        if not self.is_trained:
            raise MlModelError("Model must be trained before prediction")
        
        try:
            # Scale features
            X_scaled = await asyncio.to_thread(self.scaler.transform, X)
            
            # Get predictions
            predictions = await asyncio.to_thread(self.model.predict, X_scaled)
            
            # Calculate confidence intervals using model's uncertainty
            # For XGBoost, we can use the variance of predictions from multiple trees
            if hasattr(self.model, 'estimators_'):
                tree_predictions = []
                for estimator in self.model.estimators_:
                    tree_pred = await asyncio.to_thread(estimator.predict, X_scaled)
                    tree_predictions.append(tree_pred)
                
                tree_predictions = np.array(tree_predictions)
                confidence_intervals = np.std(tree_predictions, axis=0) * 1.96  # 95% CI
            else:
                # Fallback: use a simple confidence interval based on prediction variance
                confidence_intervals = np.full_like(predictions, 0.1)  # 10% uncertainty
            
            return predictions, confidence_intervals
            
        except Exception as e:
            logger.error(f"XGBoost prediction failed: {e}")
            raise MlModelError(f"XGBoost prediction failed: {e}")
    
    def get_feature_importance(self) -> List[Dict[str, Any]]:
        """Get XGBoost feature importance"""
        if not self.is_trained:
            return []
        
        try:
            importance_scores = self.model.feature_importances_
            feature_importance = []
            
            for i, (feature, importance) in enumerate(zip(self.feature_names, importance_scores)):
                feature_importance.append({
                    "feature_name": feature,
                    "importance_score": float(importance),
                    "rank": i + 1,
                    "description": f"Feature importance for {feature}"
                })
            
            # Sort by importance
            feature_importance.sort(key=lambda x: x["importance_score"], reverse=True)
            
            return feature_importance
            
        except Exception as e:
            logger.error(f"Failed to get XGBoost feature importance: {e}")
            return []


class LightGBMRiskModel(BaseMlModel):
    """LightGBM model for risk prediction"""
    
    def __init__(self):
        super().__init__(
            model_name="lightgbm_risk_model",
            model_type="lightgbm"
        )
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize LightGBM model with configuration"""
        self.model = lgb.LGBMRegressor(
            n_estimators=self.config.ml_model.lightgbm_n_estimators,
            max_depth=self.config.ml_model.lightgbm_max_depth,
            learning_rate=self.config.ml_model.lightgbm_learning_rate,
            random_state=self.config.ml_model.lightgbm_random_state,
            objective='regression',
            metric='rmse',
            verbose=-1
        )
    
    async def train(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]) -> Dict[str, float]:
        """Train LightGBM model"""
        try:
            self.feature_names = feature_names
            
            # Split data for validation
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = await asyncio.to_thread(self.scaler.fit_transform, X_train)
            X_val_scaled = await asyncio.to_thread(self.scaler.transform, X_val)
            
            # Train model
            await asyncio.to_thread(
                self.model.fit,
                X_train_scaled,
                y_train,
                eval_set=[(X_val_scaled, y_val)],
                callbacks=[lgb.early_stopping(10), lgb.log_evaluation(0)]
            )
            
            # Evaluate model
            y_pred = await asyncio.to_thread(self.model.predict, X_val_scaled)
            mse = mean_squared_error(y_val, y_pred)
            r2 = r2_score(y_val, y_pred)
            
            self.is_trained = True
            
            metrics = {
                "mse": mse,
                "rmse": np.sqrt(mse),
                "r2": r2,
                "feature_count": len(feature_names)
            }
            
            logger.info(f"LightGBM model trained successfully. R²: {r2:.4f}, RMSE: {np.sqrt(mse):.4f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to train LightGBM model: {e}")
            raise MlModelError(f"LightGBM training failed: {e}")
    
    async def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Predict risk scores with confidence intervals"""
        if not self.is_trained:
            raise MlModelError("Model must be trained before prediction")
        
        try:
            # Scale features
            X_scaled = await asyncio.to_thread(self.scaler.transform, X)
            
            # Get predictions
            predictions = await asyncio.to_thread(self.model.predict, X_scaled)
            
            # Calculate confidence intervals
            # LightGBM can provide prediction intervals if configured
            confidence_intervals = np.full_like(predictions, 0.1)  # 10% uncertainty
            
            return predictions, confidence_intervals
            
        except Exception as e:
            logger.error(f"LightGBM prediction failed: {e}")
            raise MlModelError(f"LightGBM prediction failed: {e}")
    
    def get_feature_importance(self) -> List[Dict[str, Any]]:
        """Get LightGBM feature importance"""
        if not self.is_trained:
            return []
        
        try:
            importance_scores = self.model.feature_importances_
            feature_importance = []
            
            for i, (feature, importance) in enumerate(zip(self.feature_names, importance_scores)):
                feature_importance.append({
                    "feature_name": feature,
                    "importance_score": float(importance),
                    "rank": i + 1,
                    "description": f"Feature importance for {feature}"
                })
            
            # Sort by importance
            feature_importance.sort(key=lambda x: x["importance_score"], reverse=True)
            
            return feature_importance
            
        except Exception as e:
            logger.error(f"Failed to get LightGBM feature importance: {e}")
            return []


class LogisticRegressionModel(BaseMlModel):
    """Logistic Regression model for binary risk classification"""
    
    def __init__(self):
        super().__init__(
            model_name="logistic_regression_model",
            model_type="logistic_regression"
        )
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Logistic Regression model"""
        self.model = LogisticRegression(
            random_state=42,
            max_iter=1000,
            solver='liblinear'
        )
    
    async def train(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]) -> Dict[str, float]:
        """Train Logistic Regression model"""
        try:
            self.feature_names = feature_names
            
            # Convert continuous risk scores to binary (high risk vs low risk)
            # Threshold at median for binary classification
            threshold = np.median(y)
            y_binary = (y > threshold).astype(int)
            
            # Split data for validation
            X_train, X_val, y_train, y_val = train_test_split(
                X, y_binary, test_size=0.2, random_state=42, stratify=y_binary
            )
            
            # Scale features
            X_train_scaled = await asyncio.to_thread(self.scaler.fit_transform, X_train)
            X_val_scaled = await asyncio.to_thread(self.scaler.transform, X_val)
            
            # Train model
            await asyncio.to_thread(self.model.fit, X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = await asyncio.to_thread(self.model.predict, X_val_scaled)
            y_pred_proba = await asyncio.to_thread(self.model.predict_proba, X_val_scaled)
            
            accuracy = np.mean(y_pred == y_val)
            mse = mean_squared_error(y_val, y_pred)
            
            self.is_trained = True
            
            metrics = {
                "accuracy": accuracy,
                "mse": mse,
                "feature_count": len(feature_names),
                "threshold": float(threshold)
            }
            
            logger.info(f"Logistic Regression model trained successfully. Accuracy: {accuracy:.4f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to train Logistic Regression model: {e}")
            raise MlModelError(f"Logistic Regression training failed: {e}")
    
    async def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Predict risk probabilities with confidence intervals"""
        if not self.is_trained:
            raise MlModelError("Model must be trained before prediction")
        
        try:
            # Scale features
            X_scaled = await asyncio.to_thread(self.scaler.transform, X)
            
            # Get probability predictions
            probabilities = await asyncio.to_thread(self.model.predict_proba, X_scaled)
            risk_scores = probabilities[:, 1]  # Probability of high risk
            
            # Calculate confidence intervals based on probability uncertainty
            confidence_intervals = np.sqrt(risk_scores * (1 - risk_scores)) * 1.96  # 95% CI
            
            return risk_scores, confidence_intervals
            
        except Exception as e:
            logger.error(f"Logistic Regression prediction failed: {e}")
            raise MlModelError(f"Logistic Regression prediction failed: {e}")
    
    def get_feature_importance(self) -> List[Dict[str, Any]]:
        """Get Logistic Regression feature importance (coefficients)"""
        if not self.is_trained:
            return []
        
        try:
            coefficients = self.model.coef_[0]
            feature_importance = []
            
            for i, (feature, coef) in enumerate(zip(self.feature_names, coefficients)):
                feature_importance.append({
                    "feature_name": feature,
                    "importance_score": float(abs(coef)),
                    "coefficient": float(coef),
                    "rank": i + 1,
                    "description": f"Logistic regression coefficient for {feature}"
                })
            
            # Sort by absolute importance
            feature_importance.sort(key=lambda x: x["importance_score"], reverse=True)
            
            return feature_importance
            
        except Exception as e:
            logger.error(f"Failed to get Logistic Regression feature importance: {e}")
            return []


class MlModelFactory:
    """Factory for creating ML models"""
    
    @staticmethod
    def create_model(model_type: str) -> BaseMlModel:
        """Create ML model based on type"""
        if model_type == "xgboost":
            return XGBoostRiskModel()
        elif model_type == "lightgbm":
            return LightGBMRiskModel()
        elif model_type == "logistic_regression":
            return LogisticRegressionModel()
        else:
            raise ValueError(f"Unsupported ML model type: {model_type}")
    
    @staticmethod
    def get_available_models() -> List[str]:
        """Get list of available ML model types"""
        return ["xgboost", "lightgbm", "logistic_regression"]
    
    @staticmethod
    def get_default_model() -> BaseMlModel:
        """Get the default ML model (XGBoost)"""
        return XGBoostRiskModel() 