"""
Demonstrates Graph Neural Network analysis for dependency chain risk propagation.
"""

import json
import torch
import numpy as np
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv, GATConv, global_mean_pool
import networkx as nx
from pprint import pprint

from sbomai_ai.models.threat_intelligence import ThreatContextEmbedding
from sbomai_ai.models.threat_patterns import DependencyGraphAnalysis

# Initialize analyzers
threat_analyzer = ThreatContextEmbedding()
graph_analyzer = DependencyGraphAnalysis()

# Example: Complex Dependency Chain with Known Vulnerabilities
complex_dependency_chain = {
    'name': 'com.example:web-service',
    'version': '1.0.0',
    'description': 'Web service with multiple dependencies',
    'dependencies': [
        {
            'name': 'org.springframework.boot:spring-boot-starter-web',
            'version': '2.6.1',
            'risk_score': 0.7,
            'dependencies': [
                {
                    'name': 'org.springframework:spring-web',
                    'version': '5.3.13',
                    'risk_score': 0.9,
                    'vulnerabilities': [
                        {
                            'cve_id': 'CVE-2022-22965',
                            'severity': 'CRITICAL',
                            'cvss_score': 9.8,
                            'exploitability': 0.9
                        }
                    ]
                },
                {
                    'name': 'org.apache.tomcat.embed:tomcat-embed-core',
                    'version': '9.0.55',
                    'risk_score': 0.8,
                    'vulnerabilities': [
                        {
                            'cve_id': 'CVE-2022-23181',
                            'severity': 'HIGH',
                            'cvss_score': 8.2,
                            'exploitability': 0.7
                        }
                    ]
                }
            ]
        },
        {
            'name': 'com.fasterxml.jackson.core:jackson-databind',
            'version': '2.13.0',
            'risk_score': 0.6,
            'dependencies': [
                {
                    'name': 'com.fasterxml.jackson.core:jackson-core',
                    'version': '2.13.0',
                    'risk_score': 0.4,
                    'vulnerabilities': []
                }
            ]
        },
        {
            'name': 'org.apache.logging.log4j:log4j-core',
            'version': '2.14.1',
            'risk_score': 0.95,
            'vulnerabilities': [
                {
                    'cve_id': 'CVE-2021-44228',
                    'severity': 'CRITICAL',
                    'cvss_score': 10.0,
                    'exploitability': 1.0
                }
            ]
        }
    ]
}

class DependencyGNN(torch.nn.Module):
    """
    Graph Neural Network for analyzing dependency risk propagation.
    Uses both GCN and GAT layers for better feature learning.
    """
    
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        num_layers: int,
        heads: int = 4,
        dropout: float = 0.2
    ):
        super().__init__()
        
        self.num_layers = num_layers
        self.dropout = dropout
        
        # GCN layers for global structure learning
        self.gcn_layers = torch.nn.ModuleList([
            GCNConv(input_dim if i == 0 else hidden_dim, hidden_dim)
            for i in range(num_layers)
        ])
        
        # GAT layers for attention-based feature learning
        self.gat_layers = torch.nn.ModuleList([
            GATConv(
                hidden_dim,
                hidden_dim // heads,
                heads=heads,
                dropout=dropout
            )
            for _ in range(num_layers)
        ])
        
        # Output layers
        self.output_linear = torch.nn.Linear(hidden_dim, output_dim)
        self.risk_predictor = torch.nn.Linear(hidden_dim, 1)
    
    def forward(self, data):
        """Forward pass through the GNN"""
        x, edge_index = data.x, data.edge_index
        
        # Initial feature learning with GCN
        for i in range(self.num_layers):
            # GCN layer
            x = self.gcn_layers[i](x, edge_index)
            x = torch.relu(x)
            x = torch.dropout(x, p=self.dropout, train=self.training)
            
            # GAT layer for attention
            x = self.gat_layers[i](x, edge_index)
            x = torch.relu(x)
        
        # Global pooling
        global_features = global_mean_pool(x, data.batch)
        
        # Risk prediction
        risk_scores = torch.sigmoid(self.risk_predictor(x))
        
        return risk_scores, global_features

def analyze_dependency_risks(dependency_data):
    """
    Analyze dependency risks using GNN.
    """
    print("\n=== Analyzing Dependency Risks with GNN ===")
    
    # Convert dependency data to graph
    graph = build_dependency_graph(dependency_data)
    
    # Extract features
    node_features = extract_node_features(graph)
    
    # Create PyTorch Geometric data
    data = create_pytorch_geometric_data(graph, node_features)
    
    # Initialize and run GNN
    model = DependencyGNN(
        input_dim=node_features.shape[1],
        hidden_dim=64,
        output_dim=32,
        num_layers=3
    )
    
    # Get risk predictions
    risk_scores, global_features = model(data)
    
    # Analyze risk propagation
    risk_analysis = analyze_risk_propagation(graph, risk_scores)
    
    return risk_analysis

def build_dependency_graph(dependency_data, parent=None):
    """Build NetworkX graph from dependency data"""
    G = nx.DiGraph()
    
    # Add current node
    G.add_node(
        dependency_data['name'],
        version=dependency_data['version'],
        risk_score=dependency_data.get('risk_score', 0.0),
        vulnerabilities=dependency_data.get('vulnerabilities', [])
    )
    
    # Add edge from parent if exists
    if parent:
        G.add_edge(parent, dependency_data['name'])
    
    # Process dependencies recursively
    if 'dependencies' in dependency_data:
        for dep in dependency_data['dependencies']:
            sub_graph = build_dependency_graph(dep, dependency_data['name'])
            G = nx.compose(G, sub_graph)
    
    return G

def extract_node_features(graph):
    """Extract features for each node"""
    features = []
    
    for node in graph.nodes():
        node_data = graph.nodes[node]
        
        # Basic features
        node_features = [
            node_data.get('risk_score', 0.0),
            len(node_data.get('vulnerabilities', [])),
            max([v.get('cvss_score', 0.0) for v in node_data.get('vulnerabilities', [])], default=0.0),
            max([v.get('exploitability', 0.0) for v in node_data.get('vulnerabilities', [])], default=0.0)
        ]
        
        # Graph structure features
        node_features.extend([
            graph.in_degree(node),  # Number of dependencies
            graph.out_degree(node),  # Number of dependents
            nx.pagerank(graph)[node]  # Centrality
        ])
        
        features.append(node_features)
    
    return torch.tensor(features, dtype=torch.float)

def create_pytorch_geometric_data(graph, node_features):
    """Convert NetworkX graph to PyTorch Geometric data"""
    # Create edge index
    edge_index = []
    for edge in graph.edges():
        edge_index.append([
            list(graph.nodes()).index(edge[0]),
            list(graph.nodes()).index(edge[1])
        ])
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    
    # Create PyTorch Geometric data object
    data = Data(
        x=node_features,
        edge_index=edge_index,
        num_nodes=len(graph.nodes())
    )
    
    return data

def analyze_risk_propagation(graph, risk_scores):
    """Analyze how risks propagate through the dependency chain"""
    risk_analysis = {
        'high_risk_components': [],
        'risk_propagation_paths': [],
        'critical_dependencies': [],
        'risk_clusters': [],
        'mitigation_suggestions': []
    }
    
    # Convert risk scores to numpy for analysis
    risk_scores = risk_scores.detach().numpy()
    
    # Find high-risk components
    for i, node in enumerate(graph.nodes()):
        if risk_scores[i] > 0.7:  # High risk threshold
            risk_analysis['high_risk_components'].append({
                'name': node,
                'risk_score': float(risk_scores[i]),
                'direct_impact': len(list(graph.successors(node))),
                'vulnerabilities': graph.nodes[node].get('vulnerabilities', [])
            })
    
    # Find risk propagation paths
    for start_node in graph.nodes():
        for end_node in graph.nodes():
            if start_node != end_node:
                paths = list(nx.all_simple_paths(graph, start_node, end_node))
                for path in paths:
                    path_risk = sum(
                        risk_scores[list(graph.nodes()).index(n)]
                        for n in path
                    ) / len(path)
                    
                    if path_risk > 0.6:  # Significant path risk threshold
                        risk_analysis['risk_propagation_paths'].append({
                            'path': path,
                            'risk_score': float(path_risk),
                            'length': len(path)
                        })
    
    # Identify critical dependencies
    for node in graph.nodes():
        descendants = set(nx.descendants(graph, node))
        if len(descendants) > 2:  # Has multiple dependents
            node_idx = list(graph.nodes()).index(node)
            risk_analysis['critical_dependencies'].append({
                'name': node,
                'risk_score': float(risk_scores[node_idx]),
                'num_dependents': len(descendants),
                'dependents': list(descendants)
            })
    
    # Generate mitigation suggestions
    for comp in risk_analysis['high_risk_components']:
        suggestions = generate_mitigation_suggestions(comp, graph)
        risk_analysis['mitigation_suggestions'].extend(suggestions)
    
    return risk_analysis

def generate_mitigation_suggestions(component, graph):
    """Generate mitigation suggestions for high-risk components"""
    suggestions = []
    
    # Version update suggestion
    if component.get('vulnerabilities'):
        suggestions.append({
            'component': component['name'],
            'type': 'version_update',
            'priority': 'high',
            'description': f"Update {component['name']} to latest secure version",
            'impact': f"Affects {component['direct_impact']} dependent components"
        })
    
    # Dependency isolation
    if component['direct_impact'] > 3:
        suggestions.append({
            'component': component['name'],
            'type': 'architecture',
            'priority': 'medium',
            'description': 'Consider isolating this dependency to reduce risk propagation',
            'impact': 'Requires architectural changes'
        })
    
    # Alternative suggestion
    alternatives = find_alternative_dependencies(component['name'])
    if alternatives:
        suggestions.append({
            'component': component['name'],
            'type': 'alternative',
            'priority': 'low',
            'description': f"Consider alternatives: {', '.join(alternatives)}",
            'impact': 'Requires significant refactoring'
        })
    
    return suggestions

def find_alternative_dependencies(component_name):
    """Find alternative dependencies with similar functionality"""
    # This would typically query a package database
    # Simplified example
    alternatives = {
        'org.springframework:spring-web': [
            'io.micronaut:micronaut-http',
            'io.quarkus:quarkus-resteasy'
        ],
        'org.apache.logging.log4j:log4j-core': [
            'ch.qos.logback:logback-classic',
            'org.slf4j:slf4j-simple'
        ]
    }
    return alternatives.get(component_name, [])

def main():
    """Run GNN-based dependency analysis"""
    # Analyze complex dependency chain
    risk_analysis = analyze_dependency_risks(complex_dependency_chain)
    
    # Print results
    print("\nHigh Risk Components:")
    pprint(risk_analysis['high_risk_components'])
    
    print("\nRisk Propagation Paths:")
    pprint(risk_analysis['risk_propagation_paths'])
    
    print("\nCritical Dependencies:")
    pprint(risk_analysis['critical_dependencies'])
    
    print("\nMitigation Suggestions:")
    pprint(risk_analysis['mitigation_suggestions'])

if __name__ == '__main__':
    main()