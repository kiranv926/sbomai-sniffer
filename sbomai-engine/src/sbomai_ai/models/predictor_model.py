"""
Vulnerability Predictor model combining multiple approaches.
"""

from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass
import numpy as np
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import shap

from .risk_model import RiskAssessmentModel, RiskAssessmentConfig

logger = logging.getLogger(__name__)

@dataclass
class VulnerabilityPredictorConfig:
    """Configuration for Vulnerability Predictor"""
    risk_config: RiskAssessmentConfig
    embedding_model: str = "microsoft/codebert-base"
    text_model: str = "all-mpnet-base-v2"
    hidden_dim: int = 256
    dropout: float = 0.2

class VulnerabilityPredictor(nn.Module):
    """
    Advanced vulnerability prediction model combining:
    - Code analysis (CodeBERT)
    - Text analysis (SentenceTransformer)
    - Risk assessment (Ensemble)
    - Historical patterns
    """
    
    def __init__(self, config: VulnerabilityPredictorConfig):
        super().__init__()
        self.config = config
        
        # Initialize code model
        self.code_tokenizer = AutoTokenizer.from_pretrained(config.embedding_model)
        self.code_model = AutoModel.from_pretrained(config.embedding_model)
        
        # Initialize text model
        self.text_model = SentenceTransformer(config.text_model)
        
        # Initialize risk model
        self.risk_model = RiskAssessmentModel(config.risk_config)
        
        # Feature dimensions
        code_dim = self.code_model.config.hidden_size
        text_dim = self.text_model.get_sentence_embedding_dimension()
        risk_dim = 11  # Number of risk features
        
        # Neural network layers
        self.feature_encoder = nn.Sequential(
            nn.Linear(code_dim + text_dim + risk_dim, config.hidden_dim),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_dim, config.hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(config.dropout)
        )
        
        self.predictor = nn.Sequential(
            nn.Linear(config.hidden_dim // 2, config.hidden_dim // 4),
            nn.ReLU(),
            nn.Linear(config.hidden_dim // 4, 1),
            nn.Sigmoid()
        )
    
    def forward(
        self,
        code_snippets: List[str],
        descriptions: List[str],
        risk_features: torch.Tensor
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        """Forward pass through the model"""
        # Get code embeddings
        code_inputs = self.code_tokenizer(
            code_snippets,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )
        
        code_outputs = self.code_model(**code_inputs)
        code_embeddings = code_outputs.last_hidden_state[:, 0, :]  # CLS token
        
        # Get text embeddings
        text_embeddings = self.text_model.encode(
            descriptions,
            convert_to_tensor=True
        )
        
        # Combine features
        combined = torch.cat([
            code_embeddings,
            text_embeddings,
            risk_features
        ], dim=1)
        
        # Get prediction
        encoded = self.feature_encoder(combined)
        prediction = self.predictor(encoded)
        
        # Calculate attention weights
        attention = torch.softmax(
            torch.matmul(encoded, encoded.transpose(0, 1)) / np.sqrt(encoded.size(-1)),
            dim=-1
        )
        
        return prediction, {
            'attention': attention,
            'code_embeddings': code_embeddings,
            'text_embeddings': text_embeddings,
            'encoded_features': encoded
        }
    
    def analyze_vulnerability(self, vuln_data: Dict) -> Dict:
        """
        Comprehensive vulnerability analysis.
        
        Args:
            vuln_data: Vulnerability information
        
        Returns:
            Analysis results including:
            - Vulnerability prediction
            - Risk assessment
            - Code analysis
            - Feature importance
            - Recommendations
        """
        try:
            # Extract code and text
            code_snippets = self._extract_code(vuln_data)
            descriptions = self._extract_text(vuln_data)
            
            # Get risk features
            risk_features = torch.tensor(
                self._extract_risk_features(vuln_data),
                dtype=torch.float32
            )
            
            # Get prediction and features
            with torch.no_grad():
                prediction, features = self.forward(
                    code_snippets,
                    descriptions,
                    risk_features
                )
            
            # Get risk analysis
            risk_analysis = self.risk_model.analyze_vulnerability(vuln_data)
            
            # Generate analysis
            analysis = self._generate_analysis(
                vuln_data,
                prediction.item(),
                features,
                risk_analysis
            )
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error in vulnerability analysis: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _extract_code(self, vuln_data: Dict) -> List[str]:
        """Extract code snippets from vulnerability data"""
        code_snippets = []
        
        # Add affected functions
        for func in vuln_data.get('affected_functions', []):
            if 'code' in func:
                code_snippets.append(func['code'])
        
        # Add exploit code
        for exploit in vuln_data.get('known_exploits', []):
            if 'code' in exploit:
                code_snippets.append(exploit['code'])
        
        # Add default if no code found
        if not code_snippets:
            code_snippets.append("")
        
        return code_snippets
    
    def _extract_text(self, vuln_data: Dict) -> List[str]:
        """Extract text descriptions from vulnerability data"""
        texts = []
        
        # Add main description
        texts.append(vuln_data.get('description', ''))
        
        # Add exploit descriptions
        for exploit in vuln_data.get('known_exploits', []):
            if 'description' in exploit:
                texts.append(exploit['description'])
        
        return texts
    
    def _extract_risk_features(self, vuln_data: Dict) -> np.ndarray:
        """Extract risk features from vulnerability data"""
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
        prediction: float,
        features: Dict[str, torch.Tensor],
        risk_analysis: Dict
    ) -> Dict:
        """Generate comprehensive analysis"""
        # Get attention scores
        attention = features['attention'].numpy()
        
        # Get most attended features
        feature_importance = {}
        for i, score in enumerate(attention[0]):
            feature_importance[f"feature_{i}"] = float(score)
        
        # Generate recommendations
        recommendations = set()
        
        # Add risk-based recommendations
        recommendations.update(risk_analysis.get('recommendations', []))
        
        # Add prediction-based recommendations
        if prediction > 0.8:
            recommendations.update([
                "CRITICAL: Immediate patching required",
                "Implement detection rules",
                "Monitor for exploitation attempts"
            ])
        elif prediction > 0.6:
            recommendations.update([
                "HIGH: Prioritize remediation",
                "Review security controls",
                "Plan mitigation strategy"
            ])
        
        return {
            "prediction": prediction,
            "risk_level": self._get_risk_level(prediction),
            "feature_importance": feature_importance,
            "risk_analysis": risk_analysis,
            "code_analysis": {
                "attention_scores": attention.tolist()
            },
            "recommendations": list(recommendations)
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