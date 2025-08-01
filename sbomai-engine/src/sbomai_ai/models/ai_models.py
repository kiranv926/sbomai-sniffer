"""
Core AI models for SBOMAI vulnerability analysis.
"""

import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv, GATConv
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ModelPrediction:
    """Container for model predictions"""
    prediction: float
    confidence: float
    features: Dict[str, float]
    explanation: Dict[str, float]

class ThreatContextEmbedding(nn.Module):
    """
    Generates embeddings for vulnerability context using transformer models.
    Uses CodeBERT for code analysis and SentenceTransformer for text.
    """
    
    def __init__(self):
        super().__init__()
        self.code_model = AutoModel.from_pretrained("microsoft/codebert-base")
        self.code_tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.text_model = SentenceTransformer('all-mpnet-base-v2')
    
    def encode_code(self, code_snippets: List[str]) -> torch.Tensor:
        """Encode code snippets using CodeBERT"""
        inputs = self.code_tokenizer(
            code_snippets,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )
        
        with torch.no_grad():
            outputs = self.code_model(**inputs)
            return outputs.last_hidden_state[:, 0, :]  # CLS token
    
    def encode_text(self, texts: List[str]) -> torch.Tensor:
        """Encode text using SentenceTransformer"""
        embeddings = self.text_model.encode(
            texts,
            convert_to_tensor=True,
            show_progress_bar=False
        )
        return embeddings
    
    def forward(self, code_snippets: List[str], descriptions: List[str]) -> torch.Tensor:
        """Generate combined embeddings"""
        code_embeddings = self.encode_code(code_snippets)
        text_embeddings = self.encode_text(descriptions)
        
        # Combine embeddings
        combined = torch.cat([code_embeddings, text_embeddings], dim=1)
        return combined

class VulnerabilityGNN(nn.Module):
    """
    Graph Neural Network for vulnerability analysis.
    Uses combination of GCN and GAT layers.
    """
    
    def __init__(self, 
                 input_dim: int,
                 hidden_dim: int = 128,
                 num_heads: int = 4,
                 dropout: float = 0.2):
        super().__init__()
        
        # GCN layers for local pattern learning
        self.gcn1 = GCNConv(input_dim, hidden_dim)
        self.gcn2 = GCNConv(hidden_dim, hidden_dim)
        
        # GAT layers for attention-based aggregation
        self.gat1 = GATConv(hidden_dim, hidden_dim // num_heads, heads=num_heads)
        self.gat2 = GATConv(hidden_dim, hidden_dim // num_heads, heads=num_heads)
        
        # Output layers
        self.fc1 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.fc2 = nn.Linear(hidden_dim // 2, 1)
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        """Forward pass through the GNN"""
        # GCN layers
        x = torch.relu(self.gcn1(x, edge_index))
        x = self.dropout(x)
        x = torch.relu(self.gcn2(x, edge_index))
        x = self.dropout(x)
        
        # GAT layers
        x = torch.relu(self.gat1(x, edge_index))
        x = self.dropout(x)
        x = torch.relu(self.gat2(x, edge_index))
        x = self.dropout(x)
        
        # Output layers
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.sigmoid(self.fc2(x))
        
        return x

class ExploitPredictor(nn.Module):
    """
    Predicts exploit likelihood using transformer-based model.
    """
    
    def __init__(self, embedding_dim: int = 768):
        super().__init__()
        
        self.text_encoder = SentenceTransformer('all-mpnet-base-v2')
        
        self.fc_layers = nn.Sequential(
            nn.Linear(embedding_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )
    
    def forward(self, descriptions: List[str], metadata: Dict[str, torch.Tensor]) -> ModelPrediction:
        """Predict exploit likelihood"""
        # Get text embeddings
        text_embeddings = self.text_encoder.encode(
            descriptions,
            convert_to_tensor=True
        )
        
        # Combine with metadata
        if metadata:
            meta_tensor = torch.cat(list(metadata.values()), dim=1)
            combined = torch.cat([text_embeddings, meta_tensor], dim=1)
        else:
            combined = text_embeddings
        
        # Get prediction
        prediction = self.fc_layers(combined)
        
        # Calculate confidence and feature importance
        with torch.no_grad():
            confidence = torch.sigmoid(prediction).item()
            
            # Simple feature importance
            feature_importance = {}
            for name, tensor in metadata.items():
                importance = torch.norm(tensor, p=2).item()
                feature_importance[name] = importance
        
        return ModelPrediction(
            prediction=prediction.item(),
            confidence=confidence,
            features=metadata,
            explanation=feature_importance
        )

class CriticalityScorer(nn.Module):
    """
    Scores vulnerability criticality using multiple factors.
    """
    
    def __init__(self, num_features: int):
        super().__init__()
        
        self.feature_encoder = nn.Sequential(
            nn.Linear(num_features, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        
        self.score_predictor = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
    
    def forward(self, features: torch.Tensor) -> ModelPrediction:
        """Calculate criticality score"""
        # Encode features
        encoded = self.feature_encoder(features)
        
        # Get prediction
        score = self.score_predictor(encoded)
        
        # Calculate feature importance
        with torch.no_grad():
            importance = torch.abs(
                features * self.feature_encoder[0].weight[0]
            )
            feature_imp = {
                f"feature_{i}": imp.item()
                for i, imp in enumerate(importance)
            }
        
        return ModelPrediction(
            prediction=score.item(),
            confidence=0.8,  # Fixed for now
            features={"raw_features": features.tolist()},
            explanation=feature_imp
        )

def create_vulnerability_features(vuln_data: Dict) -> torch.Tensor:
    """Create feature vector from vulnerability data"""
    features = [
        vuln_data.get('cvss_score', 0.0) / 10.0,  # Normalize CVSS
        
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
        }.get(vuln_data.get('attack_complexity', 'HIGH'), 0.0)
    ]
    
    return torch.tensor(features, dtype=torch.float32)