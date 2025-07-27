"""
Graph Neural Network models for predictive vulnerability detection in SBOM dependency graphs
"""

import logging
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, GraphConv, global_mean_pool, global_max_pool
from torch_geometric.data import Data, DataLoader
import networkx as nx
from typing import Dict, List, Any, Optional, Tuple, Union
import joblib
import os
from datetime import datetime, timedelta
import json

from ..utils.exceptions import MlModelError
from ..config import get_config

logger = logging.getLogger(__name__)


class DependencyGraphBuilder:
    """Builds dependency graphs from SBOM data for GNN analysis"""
    
    def __init__(self):
        self.config = get_config()
        
    def build_graph_from_sbom(self, sbom_data: Dict[str, Any]) -> nx.DiGraph:
        """Build NetworkX directed graph from SBOM data"""
        G = nx.DiGraph()
        
        # Add nodes (components)
        for component in sbom_data.get('components', []):
            node_id = component.get('id', component.get('name', ''))
            G.add_node(node_id, **component)
        
        # Add edges (dependencies)
        for component in sbom_data.get('components', []):
            source_id = component.get('id', component.get('name', ''))
            
            # Add dependency relationships
            for dep in component.get('dependencies', []):
                target_id = dep.get('id', dep.get('name', ''))
                if target_id in G.nodes:
                    G.add_edge(source_id, target_id, **dep)
            
            # Add relationship edges
            for rel in component.get('relationships', []):
                target_id = rel.get('target', '')
                if target_id in G.nodes:
                    G.add_edge(source_id, target_id, **rel)
        
        return G
    
    def extract_graph_features(self, G: nx.DiGraph) -> Dict[str, Any]:
        """Extract graph-level features for vulnerability prediction"""
        features = {}
        
        # Basic graph metrics
        features['num_nodes'] = G.number_of_nodes()
        features['num_edges'] = G.number_of_edges()
        features['density'] = nx.density(G)
        features['avg_clustering'] = nx.average_clustering(G.to_undirected())
        
        # Centrality measures
        if G.number_of_nodes() > 1:
            features['avg_degree_centrality'] = np.mean(list(nx.degree_centrality(G).values()))
            features['avg_betweenness_centrality'] = np.mean(list(nx.betweenness_centrality(G).values()))
            features['avg_closeness_centrality'] = np.mean(list(nx.closeness_centrality(G).values()))
        else:
            features['avg_degree_centrality'] = 0.0
            features['avg_betweenness_centrality'] = 0.0
            features['avg_closeness_centrality'] = 0.0
        
        # Vulnerability-related features
        vulnerable_nodes = [n for n, d in G.nodes(data=True) if d.get('has_vulnerabilities', False)]
        features['vulnerability_ratio'] = len(vulnerable_nodes) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0.0
        
        # Dependency depth analysis
        depths = self._calculate_dependency_depths(G)
        features['max_dependency_depth'] = max(depths) if depths else 0
        features['avg_dependency_depth'] = np.mean(depths) if depths else 0.0
        
        # Critical path analysis
        features['critical_path_length'] = self._calculate_critical_path_length(G)
        
        return features
    
    def _calculate_dependency_depths(self, G: nx.DiGraph) -> List[int]:
        """Calculate dependency depth for each node"""
        depths = []
        for node in G.nodes():
            try:
                # Find longest path from root to this node
                depth = max(len(path) for path in nx.all_simple_paths(G, node, node))
                depths.append(depth)
            except:
                depths.append(1)
        return depths
    
    def _calculate_critical_path_length(self, G: nx.DiGraph) -> int:
        """Calculate critical path length in dependency graph"""
        try:
            # Find all paths and get the longest one
            all_paths = []
            for source in G.nodes():
                for target in G.nodes():
                    if source != target:
                        paths = list(nx.all_simple_paths(G, source, target))
                        all_paths.extend(paths)
            
            return max(len(path) for path in all_paths) if all_paths else 0
        except:
            return 0


class GNNVulnerabilityPredictor(nn.Module):
    """Graph Neural Network for predictive vulnerability detection"""
    
    def __init__(self, input_dim: int, hidden_dim: int = 64, output_dim: int = 1, 
                 num_layers: int = 3, dropout: float = 0.2, gnn_type: str = 'gcn'):
        super(GNNVulnerabilityPredictor, self).__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.num_layers = num_layers
        self.dropout = dropout
        self.gnn_type = gnn_type
        
        # GNN layers
        self.convs = nn.ModuleList()
        self.batch_norms = nn.ModuleList()
        
        # First layer
        if gnn_type == 'gcn':
            self.convs.append(GCNConv(input_dim, hidden_dim))
        elif gnn_type == 'gat':
            self.convs.append(GATConv(input_dim, hidden_dim, heads=4, dropout=dropout))
        elif gnn_type == 'graphconv':
            self.convs.append(GraphConv(input_dim, hidden_dim))
        
        self.batch_norms.append(nn.BatchNorm1d(hidden_dim))
        
        # Hidden layers
        for _ in range(num_layers - 2):
            if gnn_type == 'gcn':
                self.convs.append(GCNConv(hidden_dim, hidden_dim))
            elif gnn_type == 'gat':
                self.convs.append(GATConv(hidden_dim, hidden_dim, heads=4, dropout=dropout))
            elif gnn_type == 'graphconv':
                self.convs.append(GraphConv(hidden_dim, hidden_dim))
            
            self.batch_norms.append(nn.BatchNorm1d(hidden_dim))
        
        # Final layer
        if gnn_type == 'gcn':
            self.convs.append(GCNConv(hidden_dim, hidden_dim))
        elif gnn_type == 'gat':
            self.convs.append(GATConv(hidden_dim, hidden_dim, heads=1, concat=False, dropout=dropout))
        elif gnn_type == 'graphconv':
            self.convs.append(GraphConv(hidden_dim, hidden_dim))
        
        # Output layers
        self.global_pool = global_mean_pool
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, output_dim),
            nn.Sigmoid()
        )
        
        # Graph-level classifier for vulnerability prediction
        self.graph_classifier = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x, edge_index, batch):
        """Forward pass through the GNN"""
        # GNN layers
        for i in range(self.num_layers - 1):
            x = self.convs[i](x, edge_index)
            x = self.batch_norms[i](x)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        
        # Final GNN layer
        x = self.convs[-1](x, edge_index)
        
        # Global pooling
        x = self.global_pool(x, batch)
        
        # Graph-level prediction
        graph_pred = self.graph_classifier(x)
        
        return graph_pred
    
    def predict_node_vulnerabilities(self, x, edge_index, batch):
        """Predict vulnerability likelihood for individual nodes"""
        # GNN layers
        for i in range(self.num_layers - 1):
            x = self.convs[i](x, edge_index)
            x = self.batch_norms[i](x)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        
        # Final GNN layer
        x = self.convs[-1](x, edge_index)
        
        # Node-level prediction
        node_pred = self.classifier(x)
        
        return node_pred


class PredictiveVulnerabilityDetector:
    """Advanced predictive vulnerability detection using Graph Neural Networks"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.config = get_config()
        self.model_path = model_path or os.path.join(
            self.config.ml_model.model_cache_dir, "gnn_vulnerability_predictor.pth"
        )
        
        self.graph_builder = DependencyGraphBuilder()
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Feature dimensions
        self.node_feature_dim = 32  # Will be adjusted based on actual features
        self.hidden_dim = 64
        self.output_dim = 1
        
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create a new one"""
        try:
            if os.path.exists(self.model_path):
                self.model = GNNVulnerabilityPredictor(
                    input_dim=self.node_feature_dim,
                    hidden_dim=self.hidden_dim,
                    output_dim=self.output_dim
                )
                self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
                self.model.to(self.device)
                self.model.eval()
                logger.info("Loaded existing GNN vulnerability predictor model")
            else:
                self._create_new_model()
                logger.info("Created new GNN vulnerability predictor model")
        except Exception as e:
            logger.warning(f"Failed to load GNN model: {e}")
            self._create_new_model()
    
    def _create_new_model(self):
        """Create a new GNN model"""
        self.model = GNNVulnerabilityPredictor(
            input_dim=self.node_feature_dim,
            hidden_dim=self.hidden_dim,
            output_dim=self.output_dim,
            gnn_type='gcn'
        )
        self.model.to(self.device)
    
    def extract_node_features(self, component: Dict[str, Any]) -> np.ndarray:
        """Extract node features for GNN input"""
        features = []
        
        # Component metadata features
        features.append(1.0 if component.get('has_vulnerabilities', False) else 0.0)
        features.append(len(component.get('vulnerabilities', [])))
        features.append(component.get('cvss_score', 0.0) / 10.0)  # Normalize CVSS
        
        # Version features
        version = component.get('version', '')
        features.append(1.0 if version.startswith('0.') else 0.0)  # Unstable version
        features.append(1.0 if any(x in version.lower() for x in ['alpha', 'beta', 'rc']) else 0.0)
        
        # License features
        licenses = component.get('licenses', [])
        features.append(1.0 if not licenses else 0.0)  # No license
        features.append(1.0 if any('gpl' in l.lower() for l in licenses) else 0.0)
        
        # Age features (simplified)
        features.append(0.5)  # Normalized age
        features.append(0.3)  # Normalized last update
        
        # Popularity features (simplified)
        features.append(0.7)  # Download count
        features.append(0.6)  # Star count
        features.append(0.4)  # Fork count
        
        # Maintainer features
        features.append(len(component.get('maintainers', [])) / 10.0)  # Normalized maintainer count
        features.append(1.0 if component.get('has_security_policy', False) else 0.0)
        
        # Dependency features
        features.append(len(component.get('dependencies', [])) / 50.0)  # Normalized dependency count
        features.append(component.get('dependency_depth', 1) / 10.0)  # Normalized depth
        
        # Fill remaining features with zeros
        while len(features) < self.node_feature_dim:
            features.append(0.0)
        
        return np.array(features[:self.node_feature_dim])
    
    def prepare_graph_data(self, sbom_data: Dict[str, Any]) -> Data:
        """Prepare PyTorch Geometric Data object from SBOM"""
        # Build NetworkX graph
        G = self.graph_builder.build_graph_from_sbom(sbom_data)
        
        if G.number_of_nodes() == 0:
            raise MlModelError("No components found in SBOM data")
        
        # Create node mapping
        node_mapping = {node: idx for idx, node in enumerate(G.nodes())}
        
        # Extract node features
        node_features = []
        for node in G.nodes():
            node_data = G.nodes[node]
            features = self.extract_node_features(node_data)
            node_features.append(features)
        
        node_features = torch.FloatTensor(np.array(node_features))
        
        # Extract edge indices
        edge_indices = []
        for source, target in G.edges():
            edge_indices.append([node_mapping[source], node_mapping[target]])
        
        if edge_indices:
            edge_index = torch.LongTensor(edge_indices).t().contiguous()
        else:
            # Create self-loops if no edges
            edge_index = torch.LongTensor([[i, i] for i in range(len(node_mapping))]).t().contiguous()
        
        # Create PyTorch Geometric Data object
        data = Data(x=node_features, edge_index=edge_index)
        
        return data
    
    def predict_vulnerability_patterns(self, sbom_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict vulnerability patterns in the dependency graph"""
        try:
            # Prepare graph data
            graph_data = self.prepare_graph_data(sbom_data)
            graph_data = graph_data.to(self.device)
            
            # Build NetworkX graph for analysis
            G = self.graph_builder.build_graph_from_sbom(sbom_data)
            
            # Get graph-level features
            graph_features = self.graph_builder.extract_graph_features(G)
            
            # Predict graph-level vulnerability likelihood
            with torch.no_grad():
                graph_pred = self.model(graph_data.x, graph_data.edge_index, 
                                      torch.zeros(graph_data.x.size(0), dtype=torch.long, device=self.device))
                vulnerability_likelihood = graph_pred.item()
            
            # Analyze dependency patterns
            pattern_analysis = self._analyze_dependency_patterns(G)
            
            # Identify high-risk components
            high_risk_components = self._identify_high_risk_components(G, graph_data)
            
            # Predict emerging vulnerabilities
            emerging_vulnerabilities = self._predict_emerging_vulnerabilities(G, graph_features)
            
            return {
                'vulnerability_likelihood': vulnerability_likelihood,
                'graph_features': graph_features,
                'pattern_analysis': pattern_analysis,
                'high_risk_components': high_risk_components,
                'emerging_vulnerabilities': emerging_vulnerabilities,
                'confidence_score': self._calculate_confidence(graph_features, vulnerability_likelihood)
            }
            
        except Exception as e:
            logger.error(f"Error in vulnerability pattern prediction: {e}")
            raise MlModelError(f"Failed to predict vulnerability patterns: {e}")
    
    def _analyze_dependency_patterns(self, G: nx.DiGraph) -> Dict[str, Any]:
        """Analyze dependency patterns for vulnerability indicators"""
        patterns = {}
        
        # Analyze dependency chains
        dependency_chains = self._find_long_dependency_chains(G)
        patterns['long_dependency_chains'] = dependency_chains
        
        # Analyze vulnerable dependency clusters
        vulnerable_clusters = self._find_vulnerable_clusters(G)
        patterns['vulnerable_clusters'] = vulnerable_clusters
        
        # Analyze critical paths
        critical_paths = self._find_critical_paths(G)
        patterns['critical_paths'] = critical_paths
        
        # Analyze dependency depth distribution
        depth_distribution = self._analyze_depth_distribution(G)
        patterns['depth_distribution'] = depth_distribution
        
        return patterns
    
    def _find_long_dependency_chains(self, G: nx.DiGraph) -> List[List[str]]:
        """Find long dependency chains that might indicate vulnerability risk"""
        chains = []
        
        # Find all simple paths
        for source in G.nodes():
            for target in G.nodes():
                if source != target:
                    paths = list(nx.all_simple_paths(G, source, target))
                    # Filter for long chains (more than 3 levels)
                    long_paths = [path for path in paths if len(path) > 3]
                    chains.extend(long_paths)
        
        return chains[:10]  # Return top 10 longest chains
    
    def _find_vulnerable_clusters(self, G: nx.DiGraph) -> List[List[str]]:
        """Find clusters of vulnerable components"""
        vulnerable_nodes = [n for n, d in G.nodes(data=True) if d.get('has_vulnerabilities', False)]
        
        if not vulnerable_nodes:
            return []
        
        # Find connected components among vulnerable nodes
        vulnerable_subgraph = G.subgraph(vulnerable_nodes)
        clusters = list(nx.weakly_connected_components(vulnerable_subgraph))
        
        return [list(cluster) for cluster in clusters]
    
    def _find_critical_paths(self, G: nx.DiGraph) -> List[List[str]]:
        """Find critical paths in the dependency graph"""
        try:
            # Find all paths and identify critical ones
            all_paths = []
            for source in G.nodes():
                for target in G.nodes():
                    if source != target:
                        paths = list(nx.all_simple_paths(G, source, target))
                        all_paths.extend(paths)
            
            # Sort by length and return longest paths
            all_paths.sort(key=len, reverse=True)
            return all_paths[:5]  # Return top 5 longest paths
        except:
            return []
    
    def _analyze_depth_distribution(self, G: nx.DiGraph) -> Dict[str, Any]:
        """Analyze dependency depth distribution"""
        depths = []
        for node in G.nodes():
            try:
                # Calculate depth as longest path to this node
                depth = max(len(path) for path in nx.all_simple_paths(G, node, node))
                depths.append(depth)
            except:
                depths.append(1)
        
        return {
            'min_depth': min(depths) if depths else 0,
            'max_depth': max(depths) if depths else 0,
            'avg_depth': np.mean(depths) if depths else 0.0,
            'depth_distribution': np.bincount(depths).tolist() if depths else []
        }
    
    def _identify_high_risk_components(self, G: nx.DiGraph, graph_data: Data) -> List[Dict[str, Any]]:
        """Identify high-risk components based on graph structure"""
        high_risk = []
        
        # Calculate node-level risk scores
        with torch.no_grad():
            node_preds = self.model.predict_node_vulnerabilities(
                graph_data.x, graph_data.edge_index,
                torch.zeros(graph_data.x.size(0), dtype=torch.long, device=self.device)
            )
        
        # Identify high-risk nodes
        for idx, (node, pred) in enumerate(zip(G.nodes(), node_preds)):
            risk_score = pred.item()
            if risk_score > 0.7:  # High risk threshold
                node_data = G.nodes[node]
                high_risk.append({
                    'component_id': node,
                    'component_name': node_data.get('name', node),
                    'risk_score': risk_score,
                    'vulnerabilities': node_data.get('vulnerabilities', []),
                    'dependencies': list(G.predecessors(node)),
                    'dependents': list(G.successors(node))
                })
        
        # Sort by risk score
        high_risk.sort(key=lambda x: x['risk_score'], reverse=True)
        return high_risk[:10]  # Return top 10 high-risk components
    
    def _predict_emerging_vulnerabilities(self, G: nx.DiGraph, graph_features: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict where new vulnerabilities are likely to emerge"""
        emerging = []
        
        # Analyze components based on various risk factors
        for node, data in G.nodes(data=True):
            risk_factors = []
            
            # Factor 1: High dependency count
            if G.in_degree(node) > 10:
                risk_factors.append('high_dependency_count')
            
            # Factor 2: Deep in dependency tree
            try:
                depth = max(len(path) for path in nx.all_simple_paths(G, node, node))
                if depth > 5:
                    risk_factors.append('deep_dependency')
            except:
                pass
            
            # Factor 3: Connected to vulnerable components
            vulnerable_neighbors = [n for n in G.neighbors(node) 
                                  if G.nodes[n].get('has_vulnerabilities', False)]
            if len(vulnerable_neighbors) > 2:
                risk_factors.append('vulnerable_neighbors')
            
            # Factor 4: Unstable version
            version = data.get('version', '')
            if version.startswith('0.') or any(x in version.lower() for x in ['alpha', 'beta', 'rc']):
                risk_factors.append('unstable_version')
            
            # Factor 5: No security policy
            if not data.get('has_security_policy', False):
                risk_factors.append('no_security_policy')
            
            # Calculate emerging risk score
            if risk_factors:
                emerging_risk = len(risk_factors) * 0.2  # 20% per risk factor
                emerging.append({
                    'component_id': node,
                    'component_name': data.get('name', node),
                    'emerging_risk_score': min(emerging_risk, 1.0),
                    'risk_factors': risk_factors,
                    'predicted_vulnerability_types': self._predict_vulnerability_types(risk_factors)
                })
        
        # Sort by emerging risk score
        emerging.sort(key=lambda x: x['emerging_risk_score'], reverse=True)
        return emerging[:10]  # Return top 10 emerging risks
    
    def _predict_vulnerability_types(self, risk_factors: List[str]) -> List[str]:
        """Predict types of vulnerabilities likely to emerge"""
        vulnerability_types = []
        
        if 'high_dependency_count' in risk_factors:
            vulnerability_types.extend(['supply_chain_attack', 'dependency_confusion'])
        
        if 'deep_dependency' in risk_factors:
            vulnerability_types.extend(['transitive_vulnerability', 'inherited_risk'])
        
        if 'vulnerable_neighbors' in risk_factors:
            vulnerability_types.extend(['propagation_vulnerability', 'cluster_attack'])
        
        if 'unstable_version' in risk_factors:
            vulnerability_types.extend(['implementation_bug', 'security_oversight'])
        
        if 'no_security_policy' in risk_factors:
            vulnerability_types.extend(['security_misconfiguration', 'policy_violation'])
        
        return list(set(vulnerability_types))  # Remove duplicates
    
    def _calculate_confidence(self, graph_features: Dict[str, Any], vulnerability_likelihood: float) -> float:
        """Calculate confidence in the prediction"""
        # Base confidence on graph size and feature quality
        base_confidence = min(graph_features.get('num_nodes', 0) / 100.0, 1.0)
        
        # Adjust based on vulnerability likelihood
        if vulnerability_likelihood > 0.8 or vulnerability_likelihood < 0.2:
            confidence_boost = 0.2  # High confidence for extreme predictions
        else:
            confidence_boost = 0.0
        
        return min(base_confidence + confidence_boost, 1.0)
    
    def train(self, training_data: List[Dict[str, Any]]):
        """Train the GNN model with provided data"""
        try:
            # Prepare training data
            train_loader = []
            labels = []
            
            for item in training_data:
                sbom_data = item['sbom_data']
                has_vulnerabilities = item['has_vulnerabilities']
                
                # Prepare graph data
                graph_data = self.prepare_graph_data(sbom_data)
                train_loader.append(graph_data)
                labels.append(1.0 if has_vulnerabilities else 0.0)
            
            # Convert to PyTorch tensors
            labels = torch.FloatTensor(labels).to(self.device)
            
            # Training parameters
            optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
            criterion = nn.BCELoss()
            
            # Training loop
            self.model.train()
            for epoch in range(100):  # 100 epochs
                total_loss = 0
                
                for i, (data, label) in enumerate(zip(train_loader, labels)):
                    data = data.to(self.device)
                    
                    optimizer.zero_grad()
                    
                    # Forward pass
                    pred = self.model(data.x, data.edge_index, 
                                    torch.zeros(data.x.size(0), dtype=torch.long, device=self.device))
                    
                    # Calculate loss
                    loss = criterion(pred, label.unsqueeze(0))
                    
                    # Backward pass
                    loss.backward()
                    optimizer.step()
                    
                    total_loss += loss.item()
                
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch}, Loss: {total_loss / len(train_loader):.4f}")
            
            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            torch.save(self.model.state_dict(), self.model_path)
            
            logger.info("GNN vulnerability predictor model trained and saved successfully")
            
        except Exception as e:
            logger.error(f"Error training GNN model: {e}")
            raise MlModelError(f"Failed to train GNN model: {e}")


class DependencyGraphAnalyzer:
    """Utility class for analyzing dependency graph patterns"""
    
    @staticmethod
    def analyze_vulnerability_propagation(G: nx.DiGraph) -> Dict[str, Any]:
        """Analyze how vulnerabilities propagate through the dependency graph"""
        analysis = {}
        
        # Find vulnerable components
        vulnerable_nodes = [n for n, d in G.nodes(data=True) if d.get('has_vulnerabilities', False)]
        
        if not vulnerable_nodes:
            return {'propagation_risk': 0.0, 'affected_components': []}
        
        # Calculate propagation risk
        total_nodes = G.number_of_nodes()
        vulnerable_subgraph = G.subgraph(vulnerable_nodes)
        
        # Find components that depend on vulnerable components
        affected_components = set()
        for vulnerable_node in vulnerable_nodes:
            # Find all nodes that depend on this vulnerable node
            descendants = nx.descendants(G, vulnerable_node)
            affected_components.update(descendants)
        
        propagation_risk = len(affected_components) / total_nodes if total_nodes > 0 else 0.0
        
        analysis['propagation_risk'] = propagation_risk
        analysis['affected_components'] = list(affected_components)
        analysis['vulnerable_components'] = vulnerable_nodes
        analysis['total_components'] = total_nodes
        
        return analysis
    
    @staticmethod
    def identify_critical_dependencies(G: nx.DiGraph) -> List[Dict[str, Any]]:
        """Identify critical dependencies that could cause widespread issues"""
        critical_deps = []
        
        for node in G.nodes():
            # Calculate betweenness centrality
            betweenness = nx.betweenness_centrality(G)[node]
            
            # Calculate in-degree (how many components depend on this)
            in_degree = G.in_degree(node)
            
            # Calculate out-degree (how many dependencies this component has)
            out_degree = G.out_degree(node)
            
            # Identify critical components
            if betweenness > 0.1 or in_degree > 5:  # High centrality or many dependents
                critical_deps.append({
                    'component_id': node,
                    'component_name': G.nodes[node].get('name', node),
                    'betweenness_centrality': betweenness,
                    'in_degree': in_degree,
                    'out_degree': out_degree,
                    'has_vulnerabilities': G.nodes[node].get('has_vulnerabilities', False),
                    'critical_score': betweenness * 0.6 + (in_degree / 10.0) * 0.4
                })
        
        # Sort by critical score
        critical_deps.sort(key=lambda x: x['critical_score'], reverse=True)
        return critical_deps[:10]  # Return top 10 critical dependencies
    
    @staticmethod
    def analyze_dependency_health(G: nx.DiGraph) -> Dict[str, Any]:
        """Analyze overall health of the dependency graph"""
        health_metrics = {}
        
        # Calculate various health indicators
        total_nodes = G.number_of_nodes()
        total_edges = G.number_of_edges()
        
        # Density
        health_metrics['density'] = nx.density(G)
        
        # Clustering coefficient
        health_metrics['clustering_coefficient'] = nx.average_clustering(G.to_undirected())
        
        # Vulnerability ratio
        vulnerable_nodes = [n for n, d in G.nodes(data=True) if d.get('has_vulnerabilities', False)]
        health_metrics['vulnerability_ratio'] = len(vulnerable_nodes) / total_nodes if total_nodes > 0 else 0.0
        
        # Dependency depth analysis
        depths = []
        for node in G.nodes():
            try:
                depth = max(len(path) for path in nx.all_simple_paths(G, node, node))
                depths.append(depth)
            except:
                depths.append(1)
        
        health_metrics['max_depth'] = max(depths) if depths else 0
        health_metrics['avg_depth'] = np.mean(depths) if depths else 0.0
        
        # Health score calculation
        health_score = 100.0
        
        # Penalize high vulnerability ratio
        health_score -= health_metrics['vulnerability_ratio'] * 40.0
        
        # Penalize very deep dependencies
        if health_metrics['max_depth'] > 10:
            health_score -= 20.0
        
        # Penalize very low density (isolated components)
        if health_metrics['density'] < 0.01:
            health_score -= 15.0
        
        # Penalize very high density (overly complex)
        if health_metrics['density'] > 0.5:
            health_score -= 10.0
        
        health_metrics['overall_health_score'] = max(0.0, health_score)
        
        return health_metrics 