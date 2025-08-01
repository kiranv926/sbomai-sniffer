"""
Graph Neural Network (GNN) for learning and predicting risk propagation in dependency graphs.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, global_mean_pool
from torch_geometric.data import Data, Batch
from typing import Dict, List, Tuple, Optional
import numpy as np
from dataclasses import dataclass

@dataclass
class ComponentFeatures:
    """Features extracted from component metadata"""
    name: str
    version: str
    cvss_score: float
    exploit_status: str
    dependency_count: int
    is_direct_dependency: bool
    vulnerability_count: int

class RiskGNNEncoder(nn.Module):
    """
    Encodes component metadata into node features.
    
    Input features:
    - CVSS score (normalized)
    - Exploit status embedding
    - Dependency count (normalized)
    - Is direct dependency
    - Vulnerability count (normalized)
    """
    
    def __init__(self, embedding_dim: int = 64):
        super().__init__()
        
        # Exploit status embedding
        self.exploit_embedding = nn.Embedding(4, 16)  # 4 status types
        
        # Feature combination layers
        self.fc1 = nn.Linear(20, 32)  # 16 (embed) + 4 (numerical)
        self.fc2 = nn.Linear(32, embedding_dim)
        
        self.dropout = nn.Dropout(0.2)
    
    def forward(self, features: List[ComponentFeatures]) -> torch.Tensor:
        """Encode component features into node embeddings"""
        # Convert exploit status to indices
        status_map = {
            'ACTIVELY_EXPLOITED': 0,
            'PROOF_OF_CONCEPT': 1,
            'UNPROVEN': 2,
            'NONE': 3
        }
        
        # Prepare feature tensors
        batch_size = len(features)
        exploit_indices = torch.tensor([
            status_map.get(f.exploit_status, 3) for f in features
        ], dtype=torch.long)
        
        numerical_features = torch.tensor([
            [
                f.cvss_score / 10.0,  # Normalize CVSS
                f.dependency_count / 100.0,  # Normalize dep count
                1.0 if f.is_direct_dependency else 0.0,
                f.vulnerability_count / 10.0  # Normalize vuln count
            ]
            for f in features
        ], dtype=torch.float)
        
        # Get exploit status embeddings
        status_embeddings = self.exploit_embedding(exploit_indices)
        
        # Combine features
        x = torch.cat([status_embeddings, numerical_features], dim=1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x

class RiskPropagationGNN(nn.Module):
    """
    Graph Neural Network for risk propagation learning.
    Uses a combination of GCN and GAT layers to learn:
    1. Local risk patterns (GCN)
    2. Attention-based risk propagation (GAT)
    """
    
    def __init__(self, 
                 input_dim: int = 64,
                 hidden_dim: int = 128,
                 output_dim: int = 1,
                 num_layers: int = 3):
        super().__init__()
        
        self.encoder = RiskGNNEncoder(input_dim)
        
        # GCN layers for local pattern learning
        self.gcn_layers = nn.ModuleList([
            GCNConv(input_dim, hidden_dim),
            GCNConv(hidden_dim, hidden_dim)
        ])
        
        # GAT layers for attention-based propagation
        self.gat_layers = nn.ModuleList([
            GATConv(hidden_dim, hidden_dim, heads=4, dropout=0.2),
            GATConv(hidden_dim * 4, hidden_dim, heads=1, dropout=0.2)
        ])
        
        # Output layers
        self.fc1 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.fc2 = nn.Linear(hidden_dim // 2, output_dim)
        
        self.dropout = nn.Dropout(0.2)
    
    def forward(self, data: Data) -> torch.Tensor:
        """
        Forward pass through the GNN.
        
        Args:
            data: Graph data containing:
                - x: Node features
                - edge_index: Graph connectivity
                - batch: Batch assignments
        
        Returns:
            Node-level risk predictions
        """
        # Encode node features
        x = self.encoder(data.x)
        
        # GCN layers for local patterns
        for gcn in self.gcn_layers:
            x = gcn(x, data.edge_index)
            x = F.relu(x)
            x = self.dropout(x)
        
        # GAT layers for risk propagation
        for gat in self.gat_layers:
            x = gat(x, data.edge_index)
            x = F.relu(x)
            x = self.dropout(x)
        
        # Output layers
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        risk_scores = torch.sigmoid(self.fc2(x))  # Normalize to [0, 1]
        
        return risk_scores

class DependencyGraphDataset:
    """Converts dependency graphs to PyTorch Geometric format"""
    
    @staticmethod
    def create_component_features(node: Dict) -> ComponentFeatures:
        """Extract features from component metadata"""
        return ComponentFeatures(
            name=node.get('name', ''),
            version=node.get('version', ''),
            cvss_score=max(
                (v.get('cvss_score', 0.0) for v in node.get('vulnerabilities', [])),
                default=0.0
            ),
            exploit_status=next(
                (v.get('exploit_status', 'NONE') for v in node.get('vulnerabilities', [])
                if v.get('cvss_score', 0.0) > 0),
                'NONE'
            ),
            dependency_count=len(node.get('dependencies', [])),
            is_direct_dependency=node.get('is_direct', False),
            vulnerability_count=len(node.get('vulnerabilities', []))
        )
    
    @staticmethod
    def create_pytorch_graph(graph: Dict) -> Data:
        """Convert dependency graph to PyTorch Geometric format"""
        # Extract nodes and edges
        nodes = graph['nodes']
        edges = graph['edges']
        
        # Create node features
        node_features = [
            DependencyGraphDataset.create_component_features(node)
            for node in nodes
        ]
        
        # Create edge index
        edge_index = torch.tensor(
            [[e['source'], e['target']] for e in edges],
            dtype=torch.long
        ).t()
        
        # Create PyG Data object
        return Data(
            x=node_features,
            edge_index=edge_index,
            num_nodes=len(nodes)
        )

class GNNRiskPredictor:
    """
    High-level interface for GNN-based risk prediction.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = RiskPropagationGNN()
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
    
    def predict_risk(self, graph: Dict) -> Dict[str, float]:
        """
        Predict risk scores for all nodes in the dependency graph.
        
        Args:
            graph: Dependency graph with nodes and edges
        
        Returns:
            Dictionary mapping node IDs to risk scores
        """
        # Convert graph to PyG format
        data = DependencyGraphDataset.create_pytorch_graph(graph)
        
        # Make predictions
        with torch.no_grad():
            risk_scores = self.model(data)
        
        # Convert to dictionary
        return {
            node['id']: score.item()
            for node, score in zip(graph['nodes'], risk_scores)
        }
    
    def explain_prediction(self, graph: Dict, node_id: str) -> Dict:
        """
        Explain risk prediction for a specific node using attention weights.
        
        Args:
            graph: Dependency graph
            node_id: ID of the node to explain
        
        Returns:
            Dictionary containing:
            - risk_score: Predicted risk score
            - contributing_factors: List of factors and their importance
            - attention_weights: Attention weights for connected nodes
        """
        data = DependencyGraphDataset.create_pytorch_graph(graph)
        
        # Get node index
        node_idx = next(
            i for i, node in enumerate(graph['nodes'])
            if node['id'] == node_id
        )
        
        # Get predictions and attention weights
        self.model.eval()
        with torch.no_grad():
            risk_scores = self.model(data)
            
            # Extract attention weights from last GAT layer
            attention_weights = self.model.gat_layers[-1].get_attention_weights()
            
            # Get weights for the target node
            node_attention = attention_weights[node_idx]
        
        # Get connected nodes
        connected_nodes = [
            (graph['nodes'][i]['id'], weight.item())
            for i, weight in enumerate(node_attention)
            if weight > 0.1  # Filter significant connections
        ]
        
        # Analyze feature importance
        node_features = data.x[node_idx]
        feature_importance = {
            'cvss_score': node_features[0].item(),
            'exploit_status': node_features[1].item(),
            'dependency_count': node_features[2].item(),
            'vulnerability_count': node_features[3].item()
        }
        
        return {
            'risk_score': risk_scores[node_idx].item(),
            'contributing_factors': feature_importance,
            'influential_dependencies': connected_nodes
        }

def train_gnn_model(graphs: List[Dict],
                   risk_scores: List[float],
                   epochs: int = 100,
                   lr: float = 0.001) -> RiskPropagationGNN:
    """
    Train the GNN model on historical dependency graphs.
    
    Args:
        graphs: List of dependency graphs
        risk_scores: Known risk scores for validation
        epochs: Number of training epochs
        lr: Learning rate
    
    Returns:
        Trained GNN model
    """
    # Create dataset
    dataset = [
        DependencyGraphDataset.create_pytorch_graph(g)
        for g in graphs
    ]
    
    # Create model and optimizer
    model = RiskPropagationGNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    # Training loop
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        
        for data, true_risk in zip(dataset, risk_scores):
            optimizer.zero_grad()
            
            # Forward pass
            pred_risk = model(data)
            
            # Calculate loss
            loss = F.mse_loss(pred_risk, torch.tensor(true_risk))
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        # Print progress
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataset):.4f}")
    
    return model