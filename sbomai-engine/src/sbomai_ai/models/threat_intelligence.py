"""
Advanced threat intelligence using AI/ML models for SBOM analysis.
"""

import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import shap
import lime
import lime.lime_tabular
from sklearn.ensemble import RandomForestClassifier
import torch_geometric
from torch_geometric.nn import GCNConv, GATConv, global_mean_pool
import networkx as nx

from ..utils.cache import Cache
from ..utils.monitoring import record_model_metrics
from ..config import get_config

logger = logging.getLogger(__name__)

class ThreatContextEmbedding:
    """
    Embeds threat context using transformer models and matches with known exploit patterns.
    """
    
    def __init__(self):
        self.config = get_config()
        self.cache = Cache()
        
        # Initialize embedding models
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.code_model = AutoModel.from_pretrained("microsoft/codebert-base")
        self.text_model = SentenceTransformer('all-mpnet-base-v2')
        
        # Load fine-tuned models if available
        self._load_fine_tuned_models()
    
    def embed_component(self, component_data: Dict) -> Dict:
        """
        Generate embeddings for component data including name, description, changelog.
        """
        try:
            # Generate embeddings for different aspects
            name_embedding = self._embed_text(component_data['name'])
            desc_embedding = self._embed_text(component_data['description'])
            
            # Generate code embeddings if source code is available
            code_embedding = None
            if 'source_code' in component_data:
                code_embedding = self._embed_code(component_data['source_code'])
            
            # Generate changelog embeddings
            changelog_embedding = None
            if 'changelog' in component_data:
                changelog_embedding = self._embed_text(component_data['changelog'])
            
            return {
                'name_embedding': name_embedding,
                'description_embedding': desc_embedding,
                'code_embedding': code_embedding,
                'changelog_embedding': changelog_embedding
            }
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def match_exploit_patterns(self, embeddings: Dict) -> List[Dict]:
        """
        Match embeddings against known exploit patterns.
        """
        try:
            # Load known exploit patterns
            patterns = self._load_exploit_patterns()
            
            matches = []
            for pattern in patterns:
                similarity = self._calculate_similarity(
                    embeddings,
                    pattern['embeddings']
                )
                
                if similarity > self.config.ml_model.similarity_threshold:
                    matches.append({
                        'pattern_id': pattern['id'],
                        'pattern_type': pattern['type'],
                        'similarity_score': float(similarity),
                        'description': pattern['description']
                    })
            
            return sorted(matches, key=lambda x: x['similarity_score'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error matching exploit patterns: {str(e)}")
            raise
    
    def _embed_text(self, text: str) -> np.ndarray:
        """Embed text using sentence transformer"""
        return self.text_model.encode(text)
    
    def _embed_code(self, code: str) -> np.ndarray:
        """Embed code using CodeBERT"""
        inputs = self.tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.code_model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()
    
    def _load_fine_tuned_models(self):
        """Load fine-tuned models if available"""
        try:
            model_path = self.config.ml_model.threat_models_path
            # Load fine-tuned models here
            pass
        except Exception as e:
            logger.warning(f"Could not load fine-tuned models: {str(e)}")
    
    def _load_exploit_patterns(self) -> List[Dict]:
        """Load known exploit patterns from database/cache"""
        # Implementation depends on where patterns are stored
        pass

class HistoricalCveAnalysis:
    """
    Analyzes historical CVE patterns to build predictive models.
    """
    
    def __init__(self):
        self.config = get_config()
        self.cache = Cache()
        
        # Initialize ML models
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        # Load historical data
        self._load_historical_data()
    
    def train_predictive_model(self, training_data: pd.DataFrame) -> None:
        """
        Train predictive model on historical SBOM and CVE data.
        """
        try:
            # Prepare features and labels
            X = self._prepare_features(training_data)
            y = training_data['has_vulnerability']
            
            # Train model
            self.rf_model.fit(X, y)
            
            # Save model
            self._save_model()
            
        except Exception as e:
            logger.error(f"Error training predictive model: {str(e)}")
            raise
    
    def predict_vulnerability(self, component_data: Dict) -> Dict:
        """
        Predict vulnerability likelihood based on historical patterns.
        """
        try:
            # Prepare features
            features = self._prepare_features(pd.DataFrame([component_data]))
            
            # Get prediction and probability
            prediction = self.rf_model.predict(features)[0]
            probability = self.rf_model.predict_proba(features)[0][1]
            
            # Get feature importance explanation
            explanation = self._explain_prediction(features)
            
            return {
                'is_vulnerable': bool(prediction),
                'probability': float(probability),
                'explanation': explanation
            }
            
        except Exception as e:
            logger.error(f"Error predicting vulnerability: {str(e)}")
            raise
    
    def _prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare features for model"""
        # Feature engineering based on component data
        pass
    
    def _explain_prediction(self, features: np.ndarray) -> Dict:
        """Generate LIME/SHAP explanation for prediction"""
        try:
            # SHAP explanation
            explainer = shap.TreeExplainer(self.rf_model)
            shap_values = explainer.shap_values(features)
            
            # LIME explanation
            lime_explainer = lime.lime_tabular.LimeTabularExplainer(
                training_data=self.training_data,
                feature_names=self.feature_names,
                class_names=['safe', 'vulnerable'],
                mode='classification'
            )
            
            lime_exp = lime_explainer.explain_instance(
                features[0],
                self.rf_model.predict_proba
            )
            
            return {
                'shap_values': shap_values.tolist(),
                'lime_explanation': lime_exp.as_list(),
                'feature_importance': dict(zip(
                    self.feature_names,
                    self.rf_model.feature_importances_
                ))
            }
            
        except Exception as e:
            logger.error(f"Error generating prediction explanation: {str(e)}")
            raise

class DependencyGraphAnalysis:
    """
    Analyzes dependency graphs using Graph Neural Networks for risk propagation.
    """
    
    def __init__(self):
        self.config = get_config()
        self.cache = Cache()
        
        # Initialize GNN model
        self.gnn_model = DependencyGNN(
            input_dim=self.config.ml_model.embedding_dim,
            hidden_dim=self.config.ml_model.gnn_hidden_dim,
            num_layers=self.config.ml_model.gnn_num_layers,
            dropout=self.config.ml_model.gnn_dropout
        )
        
        # Load pre-trained model if available
        self._load_pretrained_model()
    
    def analyze_dependency_chain(self, dependency_data: Dict) -> Dict:
        """
        Analyze dependency chain for risk propagation.
        """
        try:
            # Convert dependency data to graph
            graph = self._build_dependency_graph(dependency_data)
            
            # Convert to PyTorch Geometric data
            data = self._convert_to_pytorch_geometric(graph)
            
            # Get GNN predictions
            risk_scores = self.gnn_model(data)
            
            # Analyze risk propagation
            propagation = self._analyze_risk_propagation(graph, risk_scores)
            
            return {
                'risk_scores': risk_scores.tolist(),
                'risk_propagation': propagation,
                'critical_paths': self._find_critical_paths(graph, risk_scores),
                'centrality_measures': self._calculate_centrality(graph)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing dependency chain: {str(e)}")
            raise
    
    def _build_dependency_graph(self, dependency_data: Dict) -> nx.DiGraph:
        """Build NetworkX graph from dependency data"""
        G = nx.DiGraph()
        
        # Add nodes and edges
        for dep in dependency_data['dependencies']:
            G.add_node(
                dep['name'],
                version=dep['version'],
                features=dep['features']
            )
            
            for child in dep.get('depends_on', []):
                G.add_edge(dep['name'], child['name'])
        
        return G
    
    def _convert_to_pytorch_geometric(self, G: nx.DiGraph) -> torch_geometric.data.Data:
        """Convert NetworkX graph to PyTorch Geometric format"""
        # Implementation depends on graph structure
        pass
    
    def _analyze_risk_propagation(
        self,
        graph: nx.DiGraph,
        risk_scores: torch.Tensor
    ) -> List[Dict]:
        """Analyze how risk propagates through dependency chain"""
        propagation = []
        
        # Analyze each node's impact on dependencies
        for node in graph.nodes():
            descendants = nx.descendants(graph, node)
            impact = sum(risk_scores[list(descendants)])
            
            propagation.append({
                'component': node,
                'impact_score': float(impact),
                'affected_dependencies': len(descendants),
                'propagation_path': list(nx.shortest_path(graph, node))
            })
        
        return propagation
    
    def _find_critical_paths(
        self,
        graph: nx.DiGraph,
        risk_scores: torch.Tensor
    ) -> List[List[str]]:
        """Find critical paths in dependency chain"""
        paths = []
        
        # Find paths with highest cumulative risk
        for source in graph.nodes():
            for target in graph.nodes():
                if source != target:
                    all_paths = list(nx.all_simple_paths(graph, source, target))
                    for path in all_paths:
                        path_risk = sum(risk_scores[path])
                        if path_risk > self.config.ml_model.critical_path_threshold:
                            paths.append(path)
        
        return paths
    
    def _calculate_centrality(self, graph: nx.DiGraph) -> Dict:
        """Calculate various centrality measures"""
        return {
            'degree': nx.degree_centrality(graph),
            'betweenness': nx.betweenness_centrality(graph),
            'eigenvector': nx.eigenvector_centrality(graph)
        }

class DependencyGNN(torch.nn.Module):
    """
    Graph Neural Network for dependency analysis.
    """
    
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        num_layers: int,
        dropout: float
    ):
        super().__init__()
        
        self.convs = torch.nn.ModuleList()
        
        # Input layer
        self.convs.append(GATConv(input_dim, hidden_dim))
        
        # Hidden layers
        for _ in range(num_layers - 2):
            self.convs.append(GATConv(hidden_dim, hidden_dim))
        
        # Output layer
        self.convs.append(GATConv(hidden_dim, 1))
        
        self.dropout = dropout
    
    def forward(self, data):
        """Forward pass"""
        x, edge_index = data.x, data.edge_index
        
        # Apply convolutions
        for conv in self.convs[:-1]:
            x = conv(x, edge_index)
            x = torch.relu(x)
            x = torch.dropout(x, p=self.dropout, training=self.training)
        
        # Final layer
        x = self.convs[-1](x, edge_index)
        
        # Global pooling
        x = global_mean_pool(x, data.batch)
        
        return torch.sigmoid(x)