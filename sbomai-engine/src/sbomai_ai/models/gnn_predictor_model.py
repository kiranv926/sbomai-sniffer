"""
GNN-based Vulnerability Predictor model.
"""

from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass
import numpy as np
import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv, GATConv, global_mean_pool
import networkx as nx
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import shap

logger = logging.getLogger(__name__)

@dataclass
class GNNVulnerabilityPredictorConfig:
    """Configuration for GNN Vulnerability Predictor"""
    embedding_model: str = "microsoft/codebert-base"
    text_model: str = "all-mpnet-base-v2"
    hidden_dim: int = 256
    gnn_layers: int = 3
    num_heads: int = 4
    dropout: float = 0.2

class GNNVulnerabilityPredictor(nn.Module):
    """
    GNN-based vulnerability prediction model combining:
    - Code analysis (CodeBERT)
    - Text analysis (SentenceTransformer)
    - Graph structure (GNN)
    - Historical patterns
    """
    
    def __init__(self, config: GNNVulnerabilityPredictorConfig):
        super().__init__()
        self.config = config
        
        # Initialize code model
        self.code_tokenizer = AutoTokenizer.from_pretrained(config.embedding_model)
        self.code_model = AutoModel.from_pretrained(config.embedding_model)
        
        # Initialize text model
        self.text_model = SentenceTransformer(config.text_model)
        
        # Feature dimensions
        code_dim = self.code_model.config.hidden_size
        text_dim = self.text_model.get_sentence_embedding_dimension()
        node_dim = code_dim + text_dim
        
        # GNN layers
        self.gnn_layers = nn.ModuleList()
        self.gat_layers = nn.ModuleList()
        
        # First layer
        self.gnn_layers.append(GCNConv(node_dim, config.hidden_dim))
        self.gat_layers.append(
            GATConv(
                config.hidden_dim,
                config.hidden_dim // config.num_heads,
                heads=config.num_heads
            )
        )
        
        # Hidden layers
        for _ in range(config.gnn_layers - 2):
            self.gnn_layers.append(
                GCNConv(config.hidden_dim, config.hidden_dim)
            )
            self.gat_layers.append(
                GATConv(
                    config.hidden_dim,
                    config.hidden_dim // config.num_heads,
                    heads=config.num_heads
                )
            )
        
        # Final layer
        self.gnn_layers.append(GCNConv(config.hidden_dim, config.hidden_dim))
        self.gat_layers.append(
            GATConv(
                config.hidden_dim,
                config.hidden_dim // config.num_heads,
                heads=config.num_heads,
                concat=False
            )
        )
        
        # Output layers
        self.predictor = nn.Sequential(
            nn.Linear(config.hidden_dim * 2, config.hidden_dim),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_dim, config.hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_dim // 2, 1),
            nn.Sigmoid()
        )
    
    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        batch: torch.Tensor
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        """Forward pass through the model"""
        # Initial features
        h = x
        
        # Store intermediate representations
        layer_outputs = []
        attention_weights = []
        
        # GNN layers
        for gnn, gat in zip(self.gnn_layers, self.gat_layers):
            # GCN layer
            h1 = torch.relu(gnn(h, edge_index))
            
            # GAT layer
            h2, attention = gat(h1, edge_index, return_attention_weights=True)
            
            # Combine
            h = h1 + h2
            h = torch.relu(h)
            
            # Store outputs
            layer_outputs.append(h)
            attention_weights.append(attention)
        
        # Global pooling
        global_repr = global_mean_pool(h, batch)
        
        # Get node-specific representations
        node_repr = h
        
        # Combine for prediction
        combined = torch.cat([global_repr, node_repr], dim=1)
        prediction = self.predictor(combined)
        
        return prediction, {
            'layer_outputs': layer_outputs,
            'attention_weights': attention_weights,
            'node_representations': node_repr,
            'global_representation': global_repr
        }
    
    def analyze_vulnerability(self, vuln_data: Dict) -> Dict:
        """
        Comprehensive vulnerability analysis using GNN.
        
        Args:
            vuln_data: Vulnerability information
        
        Returns:
            Analysis results including:
            - Vulnerability prediction
            - Graph analysis
            - Node importance
            - Attack paths
            - Recommendations
        """
        try:
            # Create graph
            graph = self._create_dependency_graph(vuln_data)
            
            # Convert to PyTorch Geometric format
            x, edge_index, batch = self._convert_graph(graph)
            
            # Get prediction and features
            with torch.no_grad():
                prediction, features = self.forward(x, edge_index, batch)
            
            # Generate analysis
            analysis = self._generate_analysis(
                vuln_data,
                prediction.item(),
                features,
                graph
            )
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error in GNN analysis: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _create_dependency_graph(self, vuln_data: Dict) -> nx.DiGraph:
        """Create dependency graph from vulnerability data"""
        graph = nx.DiGraph()
        
        # Add component nodes
        for comp in vuln_data.get('affected_components', []):
            graph.add_node(
                comp['name'],
                type='component',
                version=comp.get('version'),
                data=comp
            )
            
            # Add dependency edges
            for dep in comp.get('dependencies', []):
                graph.add_edge(
                    comp['name'],
                    dep['name'],
                    type='depends_on'
                )
        
        # Add vulnerability nodes
        for vuln in vuln_data.get('vulnerabilities', []):
            graph.add_node(
                vuln['id'],
                type='vulnerability',
                data=vuln
            )
            
            # Add affects edges
            for comp in vuln.get('affected_components', []):
                graph.add_edge(
                    vuln['id'],
                    comp['name'],
                    type='affects'
                )
        
        return graph
    
    def _convert_graph(
        self,
        graph: nx.DiGraph
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Convert NetworkX graph to PyTorch Geometric format"""
        # Get node features
        x = []
        for node in graph.nodes():
            node_data = graph.nodes[node]
            
            if node_data['type'] == 'component':
                # Get component embeddings
                code_snippets = self._extract_code(node_data['data'])
                descriptions = self._extract_text(node_data['data'])
                
                code_inputs = self.code_tokenizer(
                    code_snippets,
                    padding=True,
                    truncation=True,
                    max_length=512,
                    return_tensors="pt"
                )
                
                code_outputs = self.code_model(**code_inputs)
                code_embedding = code_outputs.last_hidden_state[:, 0, :]
                
                text_embedding = self.text_model.encode(
                    descriptions,
                    convert_to_tensor=True
                )
                
                node_embedding = torch.cat([
                    code_embedding,
                    text_embedding
                ], dim=1)
            
            else:  # vulnerability
                # Get vulnerability embeddings
                descriptions = [node_data['data'].get('description', '')]
                text_embedding = self.text_model.encode(
                    descriptions,
                    convert_to_tensor=True
                )
                
                # Pad to match component embedding size
                code_dim = self.code_model.config.hidden_size
                padding = torch.zeros(1, code_dim)
                
                node_embedding = torch.cat([
                    padding,
                    text_embedding
                ], dim=1)
            
            x.append(node_embedding)
        
        x = torch.cat(x, dim=0)
        
        # Get edge indices
        edge_index = []
        for src, dst in graph.edges():
            src_idx = list(graph.nodes()).index(src)
            dst_idx = list(graph.nodes()).index(dst)
            edge_index.append([src_idx, dst_idx])
        
        edge_index = torch.tensor(edge_index).t().contiguous()
        
        # Create batch
        batch = torch.zeros(x.size(0), dtype=torch.long)
        
        return x, edge_index, batch
    
    def _extract_code(self, data: Dict) -> List[str]:
        """Extract code snippets from data"""
        code_snippets = []
        
        # Add source code
        if 'source_code' in data:
            code_snippets.append(data['source_code'])
        
        # Add affected functions
        for func in data.get('affected_functions', []):
            if 'code' in func:
                code_snippets.append(func['code'])
        
        # Add default if no code found
        if not code_snippets:
            code_snippets.append("")
        
        return code_snippets
    
    def _extract_text(self, data: Dict) -> List[str]:
        """Extract text descriptions from data"""
        texts = []
        
        # Add description
        if 'description' in data:
            texts.append(data['description'])
        
        # Add vulnerability descriptions
        for vuln in data.get('vulnerabilities', []):
            if 'description' in vuln:
                texts.append(vuln['description'])
        
        return texts
    
    def _generate_analysis(
        self,
        vuln_data: Dict,
        prediction: float,
        features: Dict[str, torch.Tensor],
        graph: nx.DiGraph
    ) -> Dict:
        """Generate comprehensive analysis"""
        # Get node importance from attention
        node_importance = {}
        for i, node in enumerate(graph.nodes()):
            # Average attention across all layers
            importance = 0.0
            for attention in features['attention_weights']:
                importance += attention[1][i].mean().item()
            importance /= len(features['attention_weights'])
            
            node_importance[node] = importance
        
        # Find critical paths
        critical_paths = []
        for vuln_node in [n for n, d in graph.nodes(data=True)
                         if d['type'] == 'vulnerability']:
            # Get affected components
            affected = [n for n, d in graph.nodes(data=True)
                      if d['type'] == 'component' and
                      graph.has_edge(vuln_node, n)]
            
            # Find paths to dependencies
            for comp in affected:
                paths = list(nx.all_simple_paths(graph, vuln_node, comp))
                critical_paths.extend(paths)
        
        # Generate recommendations
        recommendations = set()
        
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
        
        # Add graph-based recommendations
        high_risk_nodes = [
            node for node, importance in node_importance.items()
            if importance > 0.5
        ]
        
        if high_risk_nodes:
            recommendations.add(
                f"Focus on high-risk components: {', '.join(high_risk_nodes)}"
            )
        
        if len(critical_paths) > 3:
            recommendations.add(
                "Complex dependency chain detected - Review architecture"
            )
        
        return {
            "prediction": prediction,
            "risk_level": self._get_risk_level(prediction),
            "node_importance": node_importance,
            "critical_paths": [
                [str(n) for n in path]
                for path in critical_paths
            ],
            "graph_metrics": {
                "num_nodes": graph.number_of_nodes(),
                "num_edges": graph.number_of_edges(),
                "avg_degree": sum(dict(graph.degree()).values()) / graph.number_of_nodes()
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