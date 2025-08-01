"""
Standalone test for GNN risk model without service dependencies.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv
from torch_geometric.data import Data
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

# Test data: Complex dependency graph with known vulnerabilities
TEST_GRAPH = {
    "nodes": [
        {
            "id": "root",
            "name": "test-application",
            "version": "1.0.0",
            "is_direct": True,
            "vulnerabilities": []
        },
        {
            "id": "log4j",
            "name": "log4j-core",
            "version": "2.14.1",
            "is_direct": True,
            "vulnerabilities": [
                {
                    "cve_id": "CVE-2021-44228",
                    "cvss_score": 10.0,
                    "exploit_status": "ACTIVELY_EXPLOITED"
                }
            ]
        },
        {
            "id": "spring",
            "name": "spring-core",
            "version": "5.3.13",
            "is_direct": True,
            "vulnerabilities": [
                {
                    "cve_id": "CVE-2022-22965",
                    "cvss_score": 9.8,
                    "exploit_status": "PROOF_OF_CONCEPT"
                }
            ]
        },
        {
            "id": "jackson",
            "name": "jackson-databind",
            "version": "2.13.0",
            "is_direct": False,
            "vulnerabilities": [
                {
                    "cve_id": "CVE-2022-42003",
                    "cvss_score": 7.5,
                    "exploit_status": "UNPROVEN"
                }
            ]
        },
        {
            "id": "tomcat",
            "name": "tomcat-embed-core",
            "version": "9.0.55",
            "is_direct": False,
            "vulnerabilities": [
                {
                    "cve_id": "CVE-2022-23181",
                    "cvss_score": 8.2,
                    "exploit_status": "PROOF_OF_CONCEPT"
                }
            ]
        }
    ],
    "edges": [
        {"source": 0, "target": 1},  # root -> log4j
        {"source": 0, "target": 2},  # root -> spring
        {"source": 2, "target": 3},  # spring -> jackson
        {"source": 2, "target": 4},  # spring -> tomcat
        {"source": 1, "target": 3}   # log4j -> jackson (shared dependency)
    ]
}

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

class SimpleGNN(nn.Module):
    """
    Simplified GNN for risk propagation.
    """
    def __init__(self, input_dim=5, hidden_dim=32, output_dim=1):
        super().__init__()
        
        # GCN layers
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        
        # GAT layer
        self.gat = GATConv(hidden_dim, hidden_dim, heads=4, dropout=0.2)
        
        # Output layers
        self.fc = nn.Linear(hidden_dim * 4, output_dim)
        self.dropout = nn.Dropout(0.2)
    
    def forward(self, x, edge_index):
        # GCN layers
        x = F.relu(self.conv1(x, edge_index))
        x = self.dropout(x)
        x = F.relu(self.conv2(x, edge_index))
        x = self.dropout(x)
        
        # GAT layer
        x = self.gat(x, edge_index)
        x = F.relu(x)
        
        # Output layer
        x = self.fc(x)
        return torch.sigmoid(x)

def prepare_features(graph: Dict) -> tuple:
    """Prepare node features and edge index for GNN"""
    # Extract node features
    features = []
    for node in graph["nodes"]:
        # Get maximum CVSS score from vulnerabilities
        cvss_score = max(
            (v.get("cvss_score", 0.0) for v in node.get("vulnerabilities", [])),
            default=0.0
        )
        
        # Get exploit status weight
        exploit_weights = {
            "ACTIVELY_EXPLOITED": 1.0,
            "PROOF_OF_CONCEPT": 0.7,
            "UNPROVEN": 0.4,
            "NONE": 0.0
        }
        exploit_status = next(
            (v.get("exploit_status", "NONE") for v in node.get("vulnerabilities", [])
            if v.get("cvss_score", 0.0) > 0),
            "NONE"
        )
        exploit_weight = exploit_weights.get(exploit_status, 0.0)
        
        # Create feature vector
        feature_vector = [
            cvss_score / 10.0,  # Normalize CVSS
            exploit_weight,
            1.0 if node.get("is_direct", False) else 0.0,
            len(node.get("vulnerabilities", [])) / 5.0,  # Normalize vuln count
            len([e for e in graph["edges"] if e["source"] == graph["nodes"].index(node)]) / 10.0  # Normalize out degree
        ]
        features.append(feature_vector)
    
    # Create edge index
    edge_index = torch.tensor(
        [[e["source"], e["target"]] for e in graph["edges"]],
        dtype=torch.long
    ).t()
    
    return torch.tensor(features, dtype=torch.float), edge_index

def visualize_risk_graph(graph: Dict, risk_scores: torch.Tensor, output_file: str):
    """Create visualization of the dependency graph with risk scores"""
    G = nx.DiGraph()
    
    # Add nodes
    for i, node in enumerate(graph["nodes"]):
        G.add_node(
            i,
            name=f"{node['name']}@{node['version']}",
            risk=risk_scores[i].item()
        )
    
    # Add edges
    for edge in graph["edges"]:
        G.add_edge(edge["source"], edge["target"])
    
    # Create plot
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Draw nodes with risk-based colors
    node_colors = [G.nodes[node]["risk"] for node in G.nodes()]
    nodes = nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        node_size=1000,
        cmap=plt.cm.RdYlGn_r,
        vmin=0,
        vmax=1
    )
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    
    # Add labels
    labels = {
        node: f"{G.nodes[node]['name']}\nRisk: {G.nodes[node]['risk']:.2f}"
        for node in G.nodes()
    }
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    # Add colorbar
    plt.colorbar(nodes, label='Risk Score')
    
    plt.title("Dependency Graph Risk Analysis")
    plt.axis('off')
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()

def print_analysis(graph: Dict, risk_scores: torch.Tensor):
    """Print detailed analysis of risk scores"""
    print("\n=== Dependency Graph Risk Analysis ===\n")
    
    # Overall statistics
    print("Overall Risk Metrics:")
    print(f"Maximum Risk: {risk_scores.max().item():.2f}")
    print(f"Average Risk: {risk_scores.mean().item():.2f}")
    print(f"Total Risk: {risk_scores.sum().item():.2f}")
    
    # Component analysis
    print("\nComponent Risk Analysis:")
    for i, node in enumerate(graph["nodes"]):
        risk = risk_scores[i].item()
        vulns = node.get("vulnerabilities", [])
        
        print(f"\n{node['name']}@{node['version']}")
        print(f"Risk Score: {risk:.2f}")
        
        if vulns:
            print("Vulnerabilities:")
            for vuln in vulns:
                print(f"- {vuln['cve_id']}")
                print(f"  CVSS: {vuln['cvss_score']}")
                print(f"  Status: {vuln['exploit_status']}")
        
        # Show dependencies
        deps = [
            graph["nodes"][e["target"]]["name"]
            for e in graph["edges"]
            if e["source"] == i
        ]
        if deps:
            print("Dependencies:")
            for dep in deps:
                print(f"- {dep}")

def main():
    """Run GNN risk analysis"""
    print("\n=== Testing GNN Risk Analysis ===\n")
    
    # Prepare data
    features, edge_index = prepare_features(TEST_GRAPH)
    
    # Create and train model
    model = SimpleGNN(input_dim=features.size(1))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    print("Training GNN model...")
    model.train()
    for epoch in range(100):
        optimizer.zero_grad()
        
        # Forward pass
        risk_scores = model(features, edge_index)
        
        # Loss based on known high-risk nodes (log4j and spring)
        target = torch.zeros_like(risk_scores)
        target[1] = 1.0  # log4j (high risk)
        target[2] = 0.9  # spring (high risk)
        loss = F.mse_loss(risk_scores, target)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}/100, Loss: {loss.item():.4f}")
    
    # Generate predictions
    model.eval()
    with torch.no_grad():
        risk_scores = model(features, edge_index)
    
    # Print analysis
    print_analysis(TEST_GRAPH, risk_scores)
    
    # Create visualization
    print("\nGenerating visualization...")
    visualize_risk_graph(TEST_GRAPH, risk_scores, "dependency_risk_analysis.png")
    
    print("\nAnalysis complete! Check dependency_risk_analysis.png for visualization.")

if __name__ == "__main__":
    main()