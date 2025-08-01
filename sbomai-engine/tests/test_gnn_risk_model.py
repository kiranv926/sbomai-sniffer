"""
Test script for GNN-based risk propagation model.
"""

import sys
import os
import torch
import json
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import Dict, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sbomai_ai.models.gnn_risk_model import (
    GNNRiskPredictor,
    DependencyGraphDataset,
    train_gnn_model
)

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

def visualize_risk_graph(graph: Dict, risk_scores: Dict[str, float], output_file: str):
    """
    Create a visualization of the dependency graph with risk scores.
    """
    G = nx.DiGraph()
    
    # Add nodes with risk scores
    for node in graph["nodes"]:
        G.add_node(
            node["id"],
            name=f"{node['name']}@{node['version']}",
            risk=risk_scores[node["id"]]
        )
    
    # Add edges
    for edge in graph["edges"]:
        source_id = graph["nodes"][edge["source"]]["id"]
        target_id = graph["nodes"][edge["target"]]["id"]
        G.add_edge(source_id, target_id)
    
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

def print_risk_analysis(graph: Dict, risk_scores: Dict[str, float], explanations: Dict[str, Dict]):
    """Print detailed risk analysis results"""
    print("\n=== Dependency Graph Risk Analysis ===\n")
    
    # Overall statistics
    total_risk = sum(risk_scores.values())
    max_risk = max(risk_scores.values())
    avg_risk = total_risk / len(risk_scores)
    
    print(f"Overall Risk Metrics:")
    print(f"- Maximum Risk: {max_risk:.2f}")
    print(f"- Average Risk: {avg_risk:.2f}")
    print(f"- Total Risk: {total_risk:.2f}")
    
    # Individual component analysis
    print("\nComponent Risk Analysis:")
    for node in graph["nodes"]:
        node_id = node["id"]
        risk = risk_scores[node_id]
        explanation = explanations[node_id]
        
        print(f"\n{node['name']}@{node['version']}")
        print(f"Risk Score: {risk:.2f}")
        
        # Contributing factors
        print("Contributing Factors:")
        for factor, importance in explanation["contributing_factors"].items():
            print(f"- {factor}: {importance:.2f}")
        
        # Influential dependencies
        if explanation["influential_dependencies"]:
            print("Influential Dependencies:")
            for dep_id, weight in explanation["influential_dependencies"]:
                dep_node = next(n for n in graph["nodes"] if n["id"] == dep_id)
                print(f"- {dep_node['name']}: {weight:.2f}")

def main():
    """Run GNN risk model tests"""
    print("\n=== Testing GNN Risk Propagation Model ===\n")
    
    # Initialize predictor
    predictor = GNNRiskPredictor()
    
    # Generate training data (simplified for demonstration)
    training_graphs = [TEST_GRAPH]  # In practice, would use many more graphs
    known_risks = [0.8]  # Example risk scores for training
    
    # Train model
    print("Training GNN model...")
    model = train_gnn_model(
        graphs=training_graphs,
        risk_scores=known_risks,
        epochs=50,
        lr=0.001
    )
    predictor.model = model
    
    # Predict risks
    print("\nPredicting risk scores...")
    risk_scores = predictor.predict_risk(TEST_GRAPH)
    
    # Get explanations for all nodes
    explanations = {
        node["id"]: predictor.explain_prediction(TEST_GRAPH, node["id"])
        for node in TEST_GRAPH["nodes"]
    }
    
    # Print analysis
    print_risk_analysis(TEST_GRAPH, risk_scores, explanations)
    
    # Visualize results
    print("\nGenerating visualization...")
    visualize_risk_graph(
        TEST_GRAPH,
        risk_scores,
        "dependency_risk_analysis.png"
    )
    
    print("\nAnalysis complete! Check dependency_risk_analysis.png for visualization.")

if __name__ == "__main__":
    main()