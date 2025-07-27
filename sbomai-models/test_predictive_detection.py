#!/usr/bin/env python3
"""
Test client for SBOMAI Predictive Vulnerability Detection using Graph Neural Networks
"""

import asyncio
import json
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock gRPC imports for demonstration
# In real usage, these would be the actual generated gRPC code
class MockSbomDocument:
    def __init__(self, name: str, version: str, components: List[Dict]):
        self.name = name
        self.version = version
        self.format = "SPDX"
        self.components = components

class MockSbomComponent:
    def __init__(self, name: str, version: str, licenses: List[str] = None, 
                 vulnerabilities: List[Dict] = None, dependencies: List[str] = None):
        self.name = name
        self.version = version
        self.group_id = f"org.example.{name}"
        self.description = f"Component {name} version {version}"
        self.licenses = licenses or ["Apache-2.0"]
        self.purl = f"pkg:maven/org.example/{name}@{version}"
        self.tags = []
        self.metadata = {}
        self.vulnerabilities = vulnerabilities or []
        self.dependencies = dependencies or []

class MockGnnConfig:
    def __init__(self, gnn_type: str = "gcn", hidden_dim: int = 64, 
                 num_layers: int = 3, dropout: float = 0.2):
        self.gnn_type = gnn_type
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.dropout = dropout
        self.use_node_features = True
        self.use_edge_features = False

class MockPredictVulnerabilityPatternsRequest:
    def __init__(self, sbom_document, gnn_config, analysis_types: List[str]):
        self.sbom_document = sbom_document
        self.gnn_config = gnn_config
        self.analysis_types = analysis_types

def create_sample_sbom() -> MockSbomDocument:
    """Create a sample SBOM with vulnerable components for testing"""
    
    # Create components with vulnerabilities
    spring_boot = MockSbomComponent(
        name="spring-boot",
        version="2.7.0",
        licenses=["Apache-2.0"],
        vulnerabilities=[
            {"id": "CVE-2023-1234", "description": "Spring Boot vulnerability", "cvss_score": 8.5}
        ],
        dependencies=["spring-core", "spring-web"]
    )
    
    spring_core = MockSbomComponent(
        name="spring-core",
        version="5.3.20",
        licenses=["Apache-2.0"],
        vulnerabilities=[
            {"id": "CVE-2023-5678", "description": "Spring Core vulnerability", "cvss_score": 7.2}
        ],
        dependencies=["jackson-databind"]
    )
    
    spring_web = MockSbomComponent(
        name="spring-web",
        version="5.3.20",
        licenses=["Apache-2.0"],
        dependencies=["spring-core", "tomcat-embed"]
    )
    
    jackson_databind = MockSbomComponent(
        name="jackson-databind",
        version="2.13.4",
        licenses=["Apache-2.0"],
        vulnerabilities=[
            {"id": "CVE-2023-9012", "description": "Jackson vulnerability", "cvss_score": 9.1}
        ],
        dependencies=["jackson-core", "jackson-annotations"]
    )
    
    jackson_core = MockSbomComponent(
        name="jackson-core",
        version="2.13.4",
        licenses=["Apache-2.0"],
        dependencies=[]
    )
    
    jackson_annotations = MockSbomComponent(
        name="jackson-annotations",
        version="2.13.4",
        licenses=["Apache-2.0"],
        dependencies=[]
    )
    
    tomcat_embed = MockSbomComponent(
        name="tomcat-embed",
        version="9.0.65",
        licenses=["Apache-2.0"],
        vulnerabilities=[
            {"id": "CVE-2023-3456", "description": "Tomcat vulnerability", "cvss_score": 6.8}
        ],
        dependencies=["tomcat-core"]
    )
    
    tomcat_core = MockSbomComponent(
        name="tomcat-core",
        version="9.0.65",
        licenses=["Apache-2.0"],
        dependencies=[]
    )
    
    # Create SBOM document
    sbom = MockSbomDocument(
        name="sample-spring-app",
        version="1.0.0",
        components=[
            spring_boot, spring_core, spring_web, jackson_databind,
            jackson_core, jackson_annotations, tomcat_embed, tomcat_core
        ]
    )
    
    return sbom

def create_gnn_config() -> MockGnnConfig:
    """Create GNN configuration for testing"""
    return MockGnnConfig(
        gnn_type="gcn",
        hidden_dim=64,
        num_layers=3,
        dropout=0.2
    )

def create_request() -> MockPredictVulnerabilityPatternsRequest:
    """Create a test request for predictive vulnerability detection"""
    
    sbom = create_sample_sbom()
    gnn_config = create_gnn_config()
    
    analysis_types = [
        "dependency_patterns",
        "emerging_vulnerabilities", 
        "critical_paths",
        "vulnerability_propagation",
        "critical_dependencies",
        "dependency_health"
    ]
    
    return MockPredictVulnerabilityPatternsRequest(sbom, gnn_config, analysis_types)

def simulate_gnn_analysis(request: MockPredictVulnerabilityPatternsRequest) -> Dict[str, Any]:
    """Simulate GNN analysis results for demonstration"""
    
    logger.info("Starting GNN-based vulnerability pattern analysis...")
    
    # Simulate analysis results
    results = {
        "vulnerability_likelihood": 0.75,  # High likelihood
        "confidence_score": 0.82,
        "graph_features": {
            "num_nodes": len(request.sbom_document.components),
            "num_edges": 12,  # Estimated edges
            "density": 0.214,
            "avg_clustering": 0.45,
            "avg_degree_centrality": 0.375,
            "avg_betweenness_centrality": 0.125,
            "avg_closeness_centrality": 0.5,
            "vulnerability_ratio": 0.5,  # 4 out of 8 components have vulnerabilities
            "max_dependency_depth": 4,
            "avg_dependency_depth": 2.25,
            "critical_path_length": 4
        },
        "pattern_analysis": {
            "long_dependency_chains": [
                ["spring-boot", "spring-web", "tomcat-embed", "tomcat-core"],
                ["spring-boot", "spring-core", "jackson-databind", "jackson-core"]
            ],
            "vulnerable_clusters": [
                ["spring-boot", "spring-core", "spring-web"],
                ["jackson-databind", "jackson-core", "jackson-annotations"]
            ],
            "critical_paths": [
                ["spring-boot", "spring-web", "tomcat-embed", "tomcat-core"]
            ]
        },
        "high_risk_components": [
            {
                "component_id": "jackson-databind",
                "component_name": "jackson-databind",
                "risk_score": 0.91,
                "vulnerabilities": [{"id": "CVE-2023-9012", "cvss_score": 9.1}],
                "dependencies": ["jackson-core", "jackson-annotations"],
                "dependents": ["spring-core"]
            },
            {
                "component_id": "spring-boot",
                "component_name": "spring-boot",
                "risk_score": 0.85,
                "vulnerabilities": [{"id": "CVE-2023-1234", "cvss_score": 8.5}],
                "dependencies": ["spring-core", "spring-web"],
                "dependents": []
            }
        ],
        "emerging_vulnerabilities": [
            {
                "component_id": "spring-web",
                "component_name": "spring-web",
                "emerging_risk_score": 0.65,
                "risk_factors": ["high_dependency_count", "vulnerable_neighbors"],
                "predicted_vulnerability_types": ["propagation_vulnerability", "cluster_attack"]
            },
            {
                "component_id": "jackson-core",
                "component_name": "jackson-core",
                "emerging_risk_score": 0.55,
                "risk_factors": ["deep_dependency", "vulnerable_neighbors"],
                "predicted_vulnerability_types": ["transitive_vulnerability", "inherited_risk"]
            }
        ],
        "vulnerability_propagation": {
            "propagation_risk": 0.75,
            "affected_components": ["spring-boot", "spring-web", "spring-core"],
            "vulnerable_components": ["spring-boot", "spring-core", "jackson-databind", "tomcat-embed"],
            "total_components": 8,
            "analysis": "High propagation risk due to interconnected vulnerable components"
        },
        "critical_dependencies": [
            {
                "component_id": "spring-core",
                "component_name": "spring-core",
                "betweenness_centrality": 0.4,
                "in_degree": 2,
                "out_degree": 1,
                "has_vulnerabilities": True,
                "critical_score": 0.85,
                "impact_analysis": "Critical dependency with high centrality and vulnerabilities"
            },
            {
                "component_id": "jackson-databind",
                "component_name": "jackson-databind",
                "betweenness_centrality": 0.3,
                "in_degree": 1,
                "out_degree": 2,
                "has_vulnerabilities": True,
                "critical_score": 0.78,
                "impact_analysis": "Critical dependency with high CVSS score"
            }
        ],
        "dependency_health": {
            "density": 0.214,
            "clustering_coefficient": 0.45,
            "vulnerability_ratio": 0.5,
            "max_depth": 4,
            "avg_depth": 2.25,
            "overall_health_score": 65.0,  # Poor health due to high vulnerability ratio
            "health_indicators": ["high_vulnerability_ratio", "deep_dependencies", "vulnerable_clusters"]
        }
    }
    
    return results

def print_analysis_results(results: Dict[str, Any]):
    """Print formatted analysis results"""
    
    print("\n" + "="*80)
    print("🔍 SBOMAI PREDICTIVE VULNERABILITY DETECTION RESULTS")
    print("="*80)
    
    # Overall assessment
    print(f"\n📊 OVERALL ASSESSMENT:")
    print(f"   Vulnerability Likelihood: {results['vulnerability_likelihood']:.1%}")
    print(f"   Confidence Score: {results['confidence_score']:.1%}")
    
    # Graph features
    graph_features = results['graph_features']
    print(f"\n📈 GRAPH FEATURES:")
    print(f"   Components: {graph_features['num_nodes']}")
    print(f"   Dependencies: {graph_features['num_edges']}")
    print(f"   Graph Density: {graph_features['density']:.3f}")
    print(f"   Vulnerability Ratio: {graph_features['vulnerability_ratio']:.1%}")
    print(f"   Max Dependency Depth: {graph_features['max_dependency_depth']}")
    print(f"   Avg Dependency Depth: {graph_features['avg_dependency_depth']:.1f}")
    
    # High-risk components
    print(f"\n⚠️  HIGH-RISK COMPONENTS:")
    for comp in results['high_risk_components']:
        print(f"   • {comp['component_name']} (Risk: {comp['risk_score']:.1%})")
        if comp['vulnerabilities']:
            vuln = comp['vulnerabilities'][0]
            print(f"     └─ {vuln['id']} (CVSS: {vuln['cvss_score']})")
    
    # Emerging vulnerabilities
    print(f"\n🚨 EMERGING VULNERABILITIES:")
    for vuln in results['emerging_vulnerabilities']:
        print(f"   • {vuln['component_name']} (Risk: {vuln['emerging_risk_score']:.1%})")
        print(f"     └─ Risk Factors: {', '.join(vuln['risk_factors'])}")
        print(f"     └─ Predicted Types: {', '.join(vuln['predicted_vulnerability_types'])}")
    
    # Critical dependencies
    print(f"\n🎯 CRITICAL DEPENDENCIES:")
    for dep in results['critical_dependencies']:
        print(f"   • {dep['component_name']} (Critical Score: {dep['critical_score']:.1%})")
        print(f"     └─ Centrality: {dep['betweenness_centrality']:.3f}")
        print(f"     └─ Dependents: {dep['in_degree']}")
        print(f"     └─ Vulnerable: {'Yes' if dep['has_vulnerabilities'] else 'No'}")
    
    # Vulnerability propagation
    propagation = results['vulnerability_propagation']
    print(f"\n🔄 VULNERABILITY PROPAGATION:")
    print(f"   Propagation Risk: {propagation['propagation_risk']:.1%}")
    print(f"   Affected Components: {len(propagation['affected_components'])}")
    print(f"   Vulnerable Components: {len(propagation['vulnerable_components'])}")
    print(f"   Analysis: {propagation['analysis']}")
    
    # Dependency health
    health = results['dependency_health']
    print(f"\n🏥 DEPENDENCY HEALTH:")
    print(f"   Overall Health Score: {health['overall_health_score']:.1f}/100")
    print(f"   Clustering Coefficient: {health['clustering_coefficient']:.3f}")
    print(f"   Health Indicators: {', '.join(health['health_indicators'])}")
    
    # Pattern analysis
    patterns = results['pattern_analysis']
    print(f"\n🔍 DEPENDENCY PATTERNS:")
    print(f"   Long Dependency Chains: {len(patterns['long_dependency_chains'])}")
    print(f"   Vulnerable Clusters: {len(patterns['vulnerable_clusters'])}")
    print(f"   Critical Paths: {len(patterns['critical_paths'])}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if results['vulnerability_likelihood'] > 0.7:
        print("   • IMMEDIATE ACTION REQUIRED: High vulnerability likelihood detected")
        print("   • Review and update vulnerable components")
        print("   • Consider alternative components for high-risk dependencies")
    
    if health['overall_health_score'] < 70:
        print("   • Dependency health is poor - consider refactoring")
        print("   • Reduce dependency depth where possible")
        print("   • Implement dependency monitoring")
    
    if propagation['propagation_risk'] > 0.6:
        print("   • High propagation risk - implement isolation strategies")
        print("   • Consider microservice architecture for better isolation")
    
    print("\n" + "="*80)

async def main():
    """Main test function"""
    
    logger.info("Starting SBOMAI Predictive Vulnerability Detection Test")
    
    try:
        # Create test request
        request = create_request()
        logger.info(f"Created test request with {len(request.sbom_document.components)} components")
        
        # Simulate GNN analysis
        results = simulate_gnn_analysis(request)
        logger.info("GNN analysis completed successfully")
        
        # Print results
        print_analysis_results(results)
        
        # Save results to file
        with open("predictive_detection_results.json", "w") as f:
            json.dump(results, f, indent=2)
        logger.info("Results saved to predictive_detection_results.json")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 