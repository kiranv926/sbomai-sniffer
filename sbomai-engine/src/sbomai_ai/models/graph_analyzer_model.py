"""
Dependency Graph Analyzer model for advanced graph analysis.
"""

from typing import List, Dict, Optional, Tuple, Set
import logging
from dataclasses import dataclass
import networkx as nx
import numpy as np
from sklearn.cluster import DBSCAN
from community import community_louvain
import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv, GATConv, global_mean_pool

from .graph_builder_model import DependencyGraphBuilder, DependencyGraphConfig

logger = logging.getLogger(__name__)

@dataclass
class DependencyGraphAnalyzerConfig:
    """Configuration for Dependency Graph Analyzer"""
    graph_builder_config: DependencyGraphConfig
    hidden_dim: int = 128
    num_heads: int = 4
    dropout: float = 0.2
    clustering_eps: float = 0.3
    clustering_min_samples: int = 3

class DependencyGraphAnalyzer:
    """
    Advanced dependency graph analysis using:
    - Graph algorithms
    - Community detection
    - Graph Neural Networks
    - Risk propagation
    """
    
    def __init__(self, config: DependencyGraphAnalyzerConfig):
        self.config = config
        self.graph_builder = DependencyGraphBuilder(config.graph_builder_config)
        
        # Initialize GNN model
        self.gnn = DependencyGNN(
            hidden_dim=config.hidden_dim,
            num_heads=config.num_heads,
            dropout=config.dropout
        )
    
    def analyze_dependencies(self, sbom_data: Dict) -> Dict:
        """
        Comprehensive dependency analysis.
        
        Args:
            sbom_data: SBOM document
        
        Returns:
            Analysis results including:
            - Graph metrics
            - Community structure
            - Risk propagation
            - Critical components
            - Recommendations
        """
        try:
            # Build graph
            graph = self.graph_builder.build_graph(sbom_data)
            
            # Basic analysis
            basic_analysis = self.graph_builder.analyze_graph(graph)
            
            # Advanced analysis
            advanced_analysis = {
                "community_analysis": self._analyze_communities(graph),
                "centrality_analysis": self._analyze_centrality(graph),
                "risk_propagation": self._analyze_risk_propagation(graph),
                "component_clusters": self._cluster_components(graph),
                "attack_surface": self._analyze_attack_surface(graph)
            }
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                graph,
                basic_analysis,
                advanced_analysis
            )
            
            return {
                **basic_analysis,
                **advanced_analysis,
                "recommendations": recommendations
            }
        
        except Exception as e:
            logger.error(f"Error in dependency analysis: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _analyze_communities(self, graph: nx.DiGraph) -> Dict:
        """Analyze community structure"""
        # Convert to undirected for community detection
        undirected = graph.to_undirected()
        
        # Detect communities
        communities = community_louvain.best_partition(undirected)
        
        # Group nodes by community
        community_groups = {}
        for node, community_id in communities.items():
            if community_id not in community_groups:
                community_groups[community_id] = []
            community_groups[community_id].append(node)
        
        # Analyze each community
        community_analysis = {
            "num_communities": len(community_groups),
            "communities": [
                {
                    "id": comm_id,
                    "size": len(nodes),
                    "components": [
                        graph.nodes[n]['data']
                        for n in nodes
                        if graph.nodes[n]['type'] == 'component'
                    ],
                    "vulnerabilities": [
                        graph.nodes[n]['data']
                        for n in nodes
                        if graph.nodes[n]['type'] == 'vulnerability'
                    ]
                }
                for comm_id, nodes in community_groups.items()
            ],
            "modularity": community_louvain.modularity(
                communities,
                undirected
            )
        }
        
        return community_analysis
    
    def _analyze_centrality(self, graph: nx.DiGraph) -> Dict:
        """Analyze node centrality metrics"""
        # Calculate various centrality measures
        degree_centrality = nx.degree_centrality(graph)
        betweenness_centrality = nx.betweenness_centrality(graph)
        closeness_centrality = nx.closeness_centrality(graph)
        pagerank = nx.pagerank(graph)
        
        # Find critical components
        critical_components = []
        for node, data in graph.nodes(data=True):
            if data['type'] == 'component':
                importance = (
                    degree_centrality[node] +
                    betweenness_centrality[node] +
                    closeness_centrality[node] +
                    pagerank[node]
                ) / 4.0
                
                if importance > 0.5:  # Threshold for criticality
                    critical_components.append({
                        "component": data['data'],
                        "importance_score": importance,
                        "metrics": {
                            "degree": degree_centrality[node],
                            "betweenness": betweenness_centrality[node],
                            "closeness": closeness_centrality[node],
                            "pagerank": pagerank[node]
                        }
                    })
        
        return {
            "critical_components": critical_components,
            "centrality_metrics": {
                "degree": degree_centrality,
                "betweenness": betweenness_centrality,
                "closeness": closeness_centrality,
                "pagerank": pagerank
            }
        }
    
    def _analyze_risk_propagation(self, graph: nx.DiGraph) -> Dict:
        """Analyze risk propagation using GNN"""
        # Convert graph to PyTorch Geometric format
        x, edge_index, batch = self._convert_graph(graph)
        
        # Get predictions
        with torch.no_grad():
            risk_scores, attention = self.gnn(x, edge_index, batch)
        
        # Map scores back to nodes
        node_risks = {}
        for i, node in enumerate(graph.nodes()):
            node_risks[node] = {
                "risk_score": float(risk_scores[i]),
                "attention_score": float(attention[i].mean())
            }
        
        # Find high-risk paths
        high_risk_paths = []
        for start_node in graph.nodes():
            if (graph.nodes[start_node]['type'] == 'vulnerability' and
                node_risks[start_node]['risk_score'] > 0.7):
                
                # Find paths to components
                for end_node in graph.nodes():
                    if graph.nodes[end_node]['type'] == 'component':
                        try:
                            paths = list(nx.all_simple_paths(
                                graph,
                                start_node,
                                end_node
                            ))
                            
                            for path in paths:
                                path_risk = sum(
                                    node_risks[n]['risk_score']
                                    for n in path
                                ) / len(path)
                                
                                if path_risk > 0.7:  # High-risk threshold
                                    high_risk_paths.append({
                                        "vulnerability": graph.nodes[start_node]['data'],
                                        "component": graph.nodes[end_node]['data'],
                                        "path": [
                                            {
                                                "node": n,
                                                "type": graph.nodes[n]['type'],
                                                "risk_score": node_risks[n]['risk_score']
                                            }
                                            for n in path
                                        ],
                                        "path_risk": path_risk
                                    })
                        except nx.NetworkXNoPath:
                            continue
        
        return {
            "node_risks": node_risks,
            "high_risk_paths": high_risk_paths
        }
    
    def _cluster_components(self, graph: nx.DiGraph) -> Dict:
        """Cluster components based on graph structure"""
        # Get component nodes
        components = [
            (n, d) for n, d in graph.nodes(data=True)
            if d['type'] == 'component'
        ]
        
        if not components:
            return {"clusters": []}
        
        # Create feature matrix
        features = []
        for node, data in components:
            # Node features
            degree = graph.degree(node)
            in_degree = graph.in_degree(node)
            out_degree = graph.out_degree(node)
            
            # Vulnerability features
            vulns = [
                n for n in graph.predecessors(node)
                if graph.nodes[n]['type'] == 'vulnerability'
            ]
            num_vulns = len(vulns)
            
            # License features
            licenses = [
                n for n in graph.successors(node)
                if graph.nodes[n]['type'] == 'license'
            ]
            num_licenses = len(licenses)
            
            features.append([
                degree,
                in_degree,
                out_degree,
                num_vulns,
                num_licenses
            ])
        
        # Normalize features
        X = np.array(features)
        X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)
        
        # Cluster components
        clustering = DBSCAN(
            eps=self.config.clustering_eps,
            min_samples=self.config.clustering_min_samples
        ).fit(X)
        
        # Group components by cluster
        clusters = {}
        for i, (node, _) in enumerate(components):
            cluster_id = int(clustering.labels_[i])
            
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            
            clusters[cluster_id].append(node)
        
        # Analyze clusters
        cluster_analysis = []
        for cluster_id, nodes in clusters.items():
            if cluster_id == -1:
                continue  # Skip noise
            
            # Calculate cluster metrics
            avg_degree = np.mean([graph.degree(n) for n in nodes])
            avg_vulns = np.mean([
                len([
                    v for v in graph.predecessors(n)
                    if graph.nodes[v]['type'] == 'vulnerability'
                ])
                for n in nodes
            ])
            
            cluster_analysis.append({
                "id": cluster_id,
                "size": len(nodes),
                "components": [
                    graph.nodes[n]['data']
                    for n in nodes
                ],
                "metrics": {
                    "avg_degree": avg_degree,
                    "avg_vulnerabilities": avg_vulns
                }
            })
        
        return {"clusters": cluster_analysis}
    
    def _analyze_attack_surface(self, graph: nx.DiGraph) -> Dict:
        """Analyze attack surface and entry points"""
        # Find entry points (nodes with high in-degree)
        entry_points = []
        for node, data in graph.nodes(data=True):
            if data['type'] == 'component':
                in_degree = graph.in_degree(node)
                vulns = [
                    n for n in graph.predecessors(node)
                    if graph.nodes[n]['type'] == 'vulnerability'
                ]
                
                if in_degree > 2 or len(vulns) > 0:
                    entry_points.append({
                        "component": data['data'],
                        "in_degree": in_degree,
                        "vulnerabilities": [
                            graph.nodes[v]['data']
                            for v in vulns
                        ]
                    })
        
        # Calculate attack paths
        attack_paths = []
        for entry in entry_points:
            # Find reachable components
            entry_node = next(
                n for n, d in graph.nodes(data=True)
                if d['type'] == 'component' and
                d['data'] == entry['component']
            )
            
            reachable = nx.descendants(graph, entry_node)
            reachable_components = [
                n for n in reachable
                if graph.nodes[n]['type'] == 'component'
            ]
            
            if reachable_components:
                attack_paths.append({
                    "entry_point": entry['component'],
                    "reachable_components": [
                        graph.nodes[n]['data']
                        for n in reachable_components
                    ],
                    "path_length": max(
                        nx.shortest_path_length(
                            graph,
                            entry_node,
                            target
                        )
                        for target in reachable_components
                    )
                })
        
        return {
            "entry_points": entry_points,
            "attack_paths": attack_paths,
            "total_surface": len(entry_points),
            "max_reach": max(
                (p['path_length'] for p in attack_paths),
                default=0
            )
        }
    
    def _generate_recommendations(
        self,
        graph: nx.DiGraph,
        basic_analysis: Dict,
        advanced_analysis: Dict
    ) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = set()
        
        # Add basic recommendations
        recommendations.update(
            basic_analysis.get('recommendations', [])
        )
        
        # Community-based recommendations
        communities = advanced_analysis['community_analysis']['communities']
        if len(communities) > 5:
            recommendations.add(
                "Consider refactoring to reduce number of isolated component groups"
            )
        
        # Centrality-based recommendations
        critical = advanced_analysis['centrality_analysis']['critical_components']
        if critical:
            recommendations.add(
                f"High-centrality components require additional security review: "
                f"{', '.join(c['component']['name'] for c in critical[:3])}"
            )
        
        # Risk-based recommendations
        risk_paths = advanced_analysis['risk_propagation']['high_risk_paths']
        if risk_paths:
            recommendations.add(
                "Critical risk propagation paths detected - "
                "Review dependency chain security"
            )
        
        # Cluster-based recommendations
        clusters = advanced_analysis['component_clusters']['clusters']
        large_clusters = [c for c in clusters if c['size'] > 10]
        if large_clusters:
            recommendations.add(
                "Large component clusters found - "
                "Consider breaking down into smaller units"
            )
        
        # Attack surface recommendations
        attack_surface = advanced_analysis['attack_surface']
        if attack_surface['total_surface'] > 5:
            recommendations.add(
                "Large attack surface detected - "
                "Review and minimize entry points"
            )
        
        if attack_surface['max_reach'] > 3:
            recommendations.add(
                "Deep attack paths found - "
                "Consider implementing additional security boundaries"
            )
        
        return list(recommendations)
    
    def _convert_graph(
        self,
        graph: nx.DiGraph
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Convert NetworkX graph to PyTorch Geometric format"""
        # Get node features
        x = []
        for node in graph.nodes():
            node_data = graph.nodes[node]
            
            # Basic features
            features = [
                float(graph.in_degree(node)),
                float(graph.out_degree(node))
            ]
            
            # Type-specific features
            if node_data['type'] == 'component':
                features.extend([
                    1.0,  # Component indicator
                    0.0,  # Vulnerability indicator
                    0.0   # License indicator
                ])
            elif node_data['type'] == 'vulnerability':
                features.extend([
                    0.0,  # Component indicator
                    1.0,  # Vulnerability indicator
                    0.0   # License indicator
                ])
            else:  # License
                features.extend([
                    0.0,  # Component indicator
                    0.0,  # Vulnerability indicator
                    1.0   # License indicator
                ])
            
            x.append(features)
        
        x = torch.tensor(x, dtype=torch.float)
        
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

class DependencyGNN(nn.Module):
    """GNN model for risk propagation analysis"""
    
    def __init__(
        self,
        hidden_dim: int = 128,
        num_heads: int = 4,
        dropout: float = 0.2
    ):
        super().__init__()
        
        self.conv1 = GCNConv(5, hidden_dim)  # 5 input features
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        
        self.gat = GATConv(
            hidden_dim,
            hidden_dim // num_heads,
            heads=num_heads,
            dropout=dropout
        )
        
        self.out = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid()
        )
    
    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        batch: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass"""
        # GCN layers
        h = torch.relu(self.conv1(x, edge_index))
        h = torch.relu(self.conv2(h, edge_index))
        
        # GAT layer
        h, attention = self.gat(h, edge_index, return_attention_weights=True)
        
        # Output layer
        risk_scores = self.out(h)
        
        return risk_scores, attention[1]  # Return attention coefficients