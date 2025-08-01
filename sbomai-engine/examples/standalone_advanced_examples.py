#!/usr/bin/env python3
"""
Standalone Advanced Analysis Examples for SBOMAI Engine
This example demonstrates the advanced vulnerability analysis capabilities
without relying on the gRPC service infrastructure.
"""

import json
import logging
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sbomai_ai.models.threat_intelligence import ThreatContextEmbedding
from sbomai_ai.models.vulnerability_intelligence import VulnerabilityIntelligence
from sbomai_ai.models.exploit_prediction import ExploitPredictor
from sbomai_ai.models.dependency_graph import DependencyGraph
from sbomai_ai.models.gnn_risk_model import RiskGNNEncoder, RiskPropagationGNN, GNNRiskPredictor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run advanced analysis examples"""
    print("🚀 SBOMAI Advanced Analysis Examples")
    print("=" * 50)
    
    # Example 1: Advanced Vulnerability Analysis
    print("\n1. Advanced Vulnerability Analysis")
    print("-" * 30)
    
    # Sample SBOM data with complex vulnerabilities
    sbom_data = {
        "components": [
            {
                "name": "log4j-core",
                "version": "2.14.1",
                "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1",
                "description": "Apache Log4j Core",
                "licenses": ["Apache-2.0"],
                "dependencies": [
                    {"name": "log4j-api", "version": "2.14.1"},
                    {"name": "slf4j-api", "version": "1.7.32"}
                ]
            },
            {
                "name": "spring-boot-starter-web",
                "version": "2.6.3",
                "purl": "pkg:maven/org.springframework.boot/spring-boot-starter-web@2.6.3",
                "description": "Spring Boot Web Starter",
                "licenses": ["Apache-2.0"],
                "dependencies": [
                    {"name": "spring-core", "version": "5.3.15"},
                    {"name": "spring-web", "version": "5.3.15"},
                    {"name": "tomcat-embed-core", "version": "9.0.56"}
                ]
            },
            {
                "name": "jackson-databind",
                "version": "2.13.2.1",
                "purl": "pkg:maven/com.fasterxml.jackson.core/jackson-databind@2.13.2.1",
                "description": "Jackson Data Binding",
                "licenses": ["Apache-2.0"],
                "dependencies": [
                    {"name": "jackson-core", "version": "2.13.2"},
                    {"name": "jackson-annotations", "version": "2.13.2"}
                ]
            }
        ],
        "vulnerabilities": [
            {
                "id": "CVE-2021-44228",
                "description": "Log4j2 JNDI features do not protect against attacker controlled LDAP and other JNDI related endpoints",
                "cvss_score": 10.0,
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
                "affected_components": ["log4j-core@2.14.1"],
                "exploit_status": "active",
                "references": [
                    "https://nvd.nist.gov/vuln/detail/CVE-2021-44228",
                    "https://logging.apache.org/log4j/2.x/security.html"
                ]
            },
            {
                "id": "CVE-2022-22965",
                "description": "Spring Framework RCE via Data Binding on JDK 9+",
                "cvss_score": 9.8,
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                "affected_components": ["spring-core@5.3.15"],
                "exploit_status": "active",
                "references": [
                    "https://nvd.nist.gov/vuln/detail/CVE-2022-22965"
                ]
            },
            {
                "id": "CVE-2022-42003",
                "description": "Jackson Databind Denial of Service",
                "cvss_score": 7.5,
                "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
                "affected_components": ["jackson-databind@2.13.2.1"],
                "exploit_status": "poc",
                "references": [
                    "https://nvd.nist.gov/vuln/detail/CVE-2022-42003"
                ]
            }
        ]
    }
    
    try:
        # Initialize vulnerability intelligence
        vuln_intel = VulnerabilityIntelligence()
        
        # Analyze vulnerabilities
        print("Analyzing vulnerabilities...")
        analysis_results = vuln_intel.analyze_vulnerabilities(sbom_data["vulnerabilities"])
        
        print(f"Found {len(analysis_results)} vulnerability analysis results")
        for i, result in enumerate(analysis_results[:3], 1):
            print(f"\nVulnerability {i}:")
            print(f"  ID: {result.get('id', 'N/A')}")
            print(f"  Risk Score: {result.get('risk_score', 'N/A'):.2f}")
            print(f"  Exploit Probability: {result.get('exploit_probability', 'N/A'):.2f}")
            print(f"  Criticality: {result.get('criticality_score', 'N/A'):.2f}")
            print(f"  Recommendations: {len(result.get('recommendations', []))} items")
        
        # Example 2: Dependency Graph Analysis
        print("\n\n2. Dependency Graph Analysis")
        print("-" * 30)
        
        # Build dependency graph
        graph = DependencyGraph()
        graph.build_from_sbom(sbom_data)
        
        # Analyze graph
        print("Analyzing dependency graph...")
        graph_analysis = graph.analyze_graph()
        
        print(f"Graph Metrics:")
        print(f"  Total Components: {graph_analysis.get('total_components', 0)}")
        print(f"  Total Dependencies: {graph_analysis.get('total_dependencies', 0)}")
        print(f"  Max Depth: {graph_analysis.get('max_depth', 0)}")
        print(f"  Cycles Detected: {len(graph_analysis.get('cycles', []))}")
        
        # Risk aggregation
        print("\nRisk Aggregation:")
        risk_scores = graph.aggregate_risk_scores()
        for component, score in risk_scores.items():
            print(f"  {component}: {score:.2f}")
        
        # Example 3: GNN Risk Prediction
        print("\n\n3. GNN Risk Prediction")
        print("-" * 30)
        
        # Initialize GNN predictor
        gnn_predictor = GNNRiskPredictor()
        
        # Convert graph to GNN format
        print("Converting graph to GNN format...")
        gnn_data = graph.to_gnn_format()
        
        # Make predictions
        print("Making GNN predictions...")
        predictions = gnn_predictor.predict_risk(gnn_data)
        
        print("GNN Risk Predictions:")
        for node_id, prediction in predictions.items():
            print(f"  {node_id}: {prediction:.3f}")
        
        # Example 4: Exploit Prediction
        print("\n\n4. Exploit Prediction")
        print("-" * 30)
        
        # Initialize exploit predictor
        exploit_predictor = ExploitPredictor()
        
        # Predict exploit probability
        print("Predicting exploit probabilities...")
        for vuln in sbom_data["vulnerabilities"]:
            prediction = exploit_predictor.predict_exploit(vuln)
            print(f"  {vuln['id']}: {prediction['probability']:.3f} "
                  f"(Confidence: {prediction['confidence']:.3f})")
        
        # Example 5: Threat Context Embedding
        print("\n\n5. Threat Context Embedding")
        print("-" * 30)
        
        # Initialize threat context embedding
        threat_embedding = ThreatContextEmbedding()
        
        # Generate embeddings for components
        print("Generating threat context embeddings...")
        for component in sbom_data["components"]:
            embedding = threat_embedding.embed_component(component)
            print(f"  {component['name']}: Embedding shape {embedding.shape}")
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        logger.exception("Error in advanced analysis examples")

if __name__ == "__main__":
    main() 