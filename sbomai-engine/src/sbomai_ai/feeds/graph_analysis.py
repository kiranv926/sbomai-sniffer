"""
Advanced graph analysis for vulnerability relationships and risk propagation.
Uses graph algorithms to analyze vulnerability relationships, dependencies, and risk propagation.
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import community  # python-louvain package for community detection
from networkx.algorithms import centrality, shortest_paths, components
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.flow import minimum_cut
import logging

logger = logging.getLogger(__name__)

class NodeType(Enum):
    """Types of nodes in the vulnerability graph"""
    VULNERABILITY = "vulnerability"
    PACKAGE = "package"
    COMPONENT = "component"
    THREAT_ACTOR = "threat_actor"
    MALWARE = "malware"
    CAMPAIGN = "campaign"

class EdgeType(Enum):
    """Types of edges in the vulnerability graph"""
    AFFECTS = "affects"
    DEPENDS_ON = "depends_on"
    RELATED_TO = "related_to"
    EXPLOITED_BY = "exploited_by"
    USES = "uses"
    PART_OF = "part_of"

@dataclass
class GraphMetrics:
    """Metrics calculated from graph analysis"""
    centrality_scores: Dict[str, float]
    risk_propagation: Dict[str, float]
    critical_nodes: List[str]
    vulnerability_clusters: List[Set[str]]
    risk_paths: List[List[str]]
    cut_sets: List[Set[str]]
    component_risks: Dict[str, float]
    attack_surface: float
    risk_density: float
    propagation_impact: Dict[str, float]

class VulnerabilityGraphAnalyzer:
    """
    Advanced graph analysis for vulnerability relationships.
    """
    
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.metrics: Optional[GraphMetrics] = None
    
    def analyze_graph(self) -> GraphMetrics:
        """
        Perform comprehensive graph analysis.
        Returns calculated metrics.
        """
        # Calculate all metrics
        centrality_scores = self._calculate_centrality_metrics()
        risk_propagation = self._analyze_risk_propagation()
        critical_nodes = self._identify_critical_nodes()
        vulnerability_clusters = self._find_vulnerability_clusters()
        risk_paths = self._find_risk_paths()
        cut_sets = self._find_minimum_cut_sets()
        component_risks = self._calculate_component_risks()
        attack_surface = self._calculate_attack_surface()
        risk_density = self._calculate_risk_density()
        propagation_impact = self._calculate_propagation_impact()
        
        # Create metrics object
        self.metrics = GraphMetrics(
            centrality_scores=centrality_scores,
            risk_propagation=risk_propagation,
            critical_nodes=critical_nodes,
            vulnerability_clusters=vulnerability_clusters,
            risk_paths=risk_paths,
            cut_sets=cut_sets,
            component_risks=component_risks,
            attack_surface=attack_surface,
            risk_density=risk_density,
            propagation_impact=propagation_impact
        )
        
        return self.metrics
    
    def _calculate_centrality_metrics(self) -> Dict[str, float]:
        """
        Calculate multiple centrality metrics and combine them.
        Returns normalized centrality scores.
        """
        # Calculate different centrality measures
        degree_cent = centrality.degree_centrality(self.graph)
        between_cent = centrality.betweenness_centrality(self.graph)
        eigen_cent = centrality.eigenvector_centrality_numpy(self.graph)
        page_rank = nx.pagerank(self.graph)
        
        # Combine centrality measures with weights
        combined_scores = {}
        for node in self.graph.nodes():
            combined_scores[node] = (
                0.3 * degree_cent[node] +      # Connectivity importance
                0.3 * between_cent[node] +     # Path control importance
                0.2 * eigen_cent[node] +       # Network influence
                0.2 * page_rank[node]          # Overall importance
            )
        
        return combined_scores
    
    def _analyze_risk_propagation(self) -> Dict[str, float]:
        """
        Analyze how risk propagates through the graph using
        personalized PageRank and risk weights.
        """
        # Create personalization dict based on node types and attributes
        personalization = {}
        for node, attrs in self.graph.nodes(data=True):
            base_weight = 1.0
            
            # Adjust weight based on node type
            if attrs.get('type') == NodeType.VULNERABILITY.value:
                vuln_data = attrs.get('data', {})
                if vuln_data:
                    # Consider CVSS score
                    cvss_score = max(vuln_data.get('cvss_scores', [0.0]))
                    base_weight *= (cvss_score / 10.0)
                    
                    # Consider exploit status
                    exploit_status = vuln_data.get('exploit_status')
                    if exploit_status:
                        status_weights = {
                            'NONE': 1.0,
                            'UNPROVEN': 1.2,
                            'PROOF_OF_CONCEPT': 1.5,
                            'ACTIVELY_EXPLOITED': 2.0,
                            'WEAPONIZED': 2.5
                        }
                        base_weight *= status_weights.get(exploit_status.name, 1.0)
            
            elif attrs.get('type') == NodeType.PACKAGE.value:
                # Consider package metrics
                if attrs.get('is_direct_dependency'):
                    base_weight *= 1.5
                if attrs.get('is_critical'):
                    base_weight *= 2.0
            
            personalization[node] = base_weight
        
        # Calculate personalized PageRank
        risk_scores = nx.pagerank(
            self.graph,
            personalization=personalization,
            alpha=0.85  # Damping factor
        )
        
        return risk_scores
    
    def _identify_critical_nodes(self) -> List[str]:
        """
        Identify critical nodes using multiple metrics:
        - Centrality
        - Articulation points
        - Minimum cut sets
        - Risk scores
        """
        critical_nodes = set()
        
        # Add high centrality nodes
        if self.metrics and self.metrics.centrality_scores:
            centrality_threshold = np.percentile(
                list(self.metrics.centrality_scores.values()),
                90
            )
            critical_nodes.update(
                node for node, score in self.metrics.centrality_scores.items()
                if score >= centrality_threshold
            )
        
        # Add articulation points (nodes whose removal disconnects the graph)
        articulation_points = list(nx.articulation_points(self.graph.to_undirected()))
        critical_nodes.update(articulation_points)
        
        # Add nodes from minimum cut sets
        for s, t in self._get_critical_node_pairs():
            try:
                cut_value, partition = nx.minimum_cut(self.graph, s, t)
                if cut_value < 3:  # If removing < 3 nodes disconnects these components
                    critical_nodes.update(partition[0] & partition[1])
            except nx.NetworkXError:
                continue
        
        # Add high-risk nodes
        risk_scores = self._analyze_risk_propagation()
        risk_threshold = np.percentile(list(risk_scores.values()), 90)
        critical_nodes.update(
            node for node, score in risk_scores.items()
            if score >= risk_threshold
        )
        
        return list(critical_nodes)
    
    def _find_vulnerability_clusters(self) -> List[Set[str]]:
        """
        Find clusters of related vulnerabilities using multiple algorithms:
        - Community detection
        - Connected components
        - Similarity-based clustering
        """
        # Create undirected copy for community detection
        undirected = self.graph.to_undirected()
        
        # Find communities using Louvain method
        communities = community.best_partition(undirected)
        
        # Group nodes by community
        clusters = {}
        for node, community_id in communities.items():
            if community_id not in clusters:
                clusters[community_id] = set()
            clusters[community_id].add(node)
        
        # Filter clusters to include only vulnerability nodes
        vuln_clusters = []
        for cluster in clusters.values():
            vuln_nodes = {
                node for node in cluster
                if self.graph.nodes[node].get('type') == NodeType.VULNERABILITY.value
            }
            if vuln_nodes:
                vuln_clusters.append(vuln_nodes)
        
        # Merge small clusters based on connectivity
        merged_clusters = self._merge_small_clusters(vuln_clusters)
        
        return merged_clusters
    
    def _find_risk_paths(self) -> List[List[str]]:
        """
        Find critical paths of risk propagation using:
        - Shortest paths between high-risk nodes
        - Maximum flow paths
        - Edge risk weights
        """
        risk_paths = []
        
        # Get high-risk nodes
        risk_scores = self._analyze_risk_propagation()
        high_risk_nodes = [
            node for node, score in risk_scores.items()
            if score >= np.percentile(list(risk_scores.values()), 75)
        ]
        
        # Find paths between high-risk nodes
        for i, start in enumerate(high_risk_nodes):
            for end in high_risk_nodes[i+1:]:
                try:
                    # Get all simple paths
                    paths = list(nx.all_simple_paths(
                        self.graph, start, end, cutoff=5  # Limit path length
                    ))
                    
                    # Calculate path risks
                    path_risks = []
                    for path in paths:
                        path_risk = sum(risk_scores[node] for node in path)
                        path_risks.append((path_risk, path))
                    
                    # Add highest risk paths
                    path_risks.sort(reverse=True)
                    risk_paths.extend([path for _, path in path_risks[:3]])
                    
                except nx.NetworkXNoPath:
                    continue
        
        return risk_paths
    
    def _find_minimum_cut_sets(self) -> List[Set[str]]:
        """
        Find minimum cut sets that would disconnect critical components.
        """
        cut_sets = []
        
        # Get critical node pairs
        node_pairs = self._get_critical_node_pairs()
        
        # Find minimum cuts between pairs
        for source, target in node_pairs:
            try:
                # Get all minimum cuts
                cuts = list(nx.all_edge_cuts(self.graph, source, target))
                
                # Convert edge cuts to node sets
                for cut in cuts:
                    cut_nodes = set()
                    for u, v in cut:
                        cut_nodes.add(u)
                        cut_nodes.add(v)
                    cut_sets.append(cut_nodes)
            
            except nx.NetworkXError:
                continue
        
        return cut_sets
    
    def _calculate_component_risks(self) -> Dict[str, float]:
        """
        Calculate risk scores for components considering:
        - Direct vulnerabilities
        - Dependency chain
        - Network position
        - Exploit likelihood
        """
        component_risks = {}
        
        # Get base risk scores
        risk_scores = self._analyze_risk_propagation()
        
        for node, attrs in self.graph.nodes(data=True):
            if attrs.get('type') == NodeType.COMPONENT.value:
                # Start with base risk
                base_risk = risk_scores[node]
                
                # Add vulnerability impact
                vuln_neighbors = [
                    n for n in self.graph.neighbors(node)
                    if self.graph.nodes[n].get('type') == NodeType.VULNERABILITY.value
                ]
                
                vuln_impact = 0.0
                for vuln in vuln_neighbors:
                    vuln_data = self.graph.nodes[vuln].get('data', {})
                    if vuln_data:
                        # Consider CVSS and exploit status
                        cvss = max(vuln_data.get('cvss_scores', [0.0]))
                        exploit_weight = {
                            'NONE': 0.1,
                            'UNPROVEN': 0.3,
                            'PROOF_OF_CONCEPT': 0.6,
                            'ACTIVELY_EXPLOITED': 0.9,
                            'WEAPONIZED': 1.0
                        }.get(vuln_data.get('exploit_status', 'NONE').name, 0.1)
                        
                        vuln_impact += (cvss / 10.0) * exploit_weight
                
                # Normalize vulnerability impact
                if vuln_neighbors:
                    vuln_impact /= len(vuln_neighbors)
                
                # Calculate final risk score
                final_risk = (0.4 * base_risk) + (0.6 * vuln_impact)
                component_risks[node] = final_risk
        
        return component_risks
    
    def _calculate_attack_surface(self) -> float:
        """
        Calculate the overall attack surface considering:
        - Number of entry points
        - Vulnerability density
        - Exploit availability
        - Component connectivity
        """
        # Count entry points (nodes with in-degree 0)
        entry_points = sum(1 for n in self.graph.nodes()
                         if self.graph.in_degree(n) == 0)
        
        # Calculate vulnerability density
        total_nodes = self.graph.number_of_nodes()
        vuln_nodes = sum(
            1 for n, attrs in self.graph.nodes(data=True)
            if attrs.get('type') == NodeType.VULNERABILITY.value
        )
        vuln_density = vuln_nodes / total_nodes if total_nodes > 0 else 0
        
        # Calculate exploit availability
        exploit_available = sum(
            1 for n, attrs in self.graph.nodes(data=True)
            if attrs.get('type') == NodeType.VULNERABILITY.value
            and attrs.get('data', {}).get('exploit_status', 'NONE') != 'NONE'
        )
        exploit_ratio = exploit_available / vuln_nodes if vuln_nodes > 0 else 0
        
        # Calculate connectivity (average degree)
        avg_degree = sum(dict(self.graph.degree()).values()) / total_nodes
        
        # Combine metrics
        attack_surface = (
            0.3 * (entry_points / total_nodes) +
            0.3 * vuln_density +
            0.2 * exploit_ratio +
            0.2 * (avg_degree / total_nodes)
        )
        
        return attack_surface
    
    def _calculate_risk_density(self) -> float:
        """
        Calculate risk density metric considering:
        - Vulnerability concentration
        - Risk propagation paths
        - Component coupling
        """
        if not self.metrics:
            return 0.0
        
        # Calculate vulnerability concentration
        vuln_nodes = [
            n for n, attrs in self.graph.nodes(data=True)
            if attrs.get('type') == NodeType.VULNERABILITY.value
        ]
        vuln_subgraph = self.graph.subgraph(vuln_nodes)
        
        if not vuln_nodes:
            return 0.0
        
        # Calculate clustering coefficient
        clustering = nx.average_clustering(vuln_subgraph.to_undirected())
        
        # Calculate average path length between vulnerabilities
        path_lengths = []
        for i, start in enumerate(vuln_nodes):
            for end in vuln_nodes[i+1:]:
                try:
                    length = nx.shortest_path_length(self.graph, start, end)
                    path_lengths.append(length)
                except nx.NetworkXNoPath:
                    continue
        
        avg_path_length = np.mean(path_lengths) if path_lengths else float('inf')
        
        # Calculate component coupling
        coupling = len(self.graph.edges()) / (len(self.graph.nodes()) ** 2)
        
        # Combine metrics
        risk_density = (
            0.4 * clustering +
            0.4 * (1 / (1 + avg_path_length)) +  # Normalize path length
            0.2 * coupling
        )
        
        return risk_density
    
    def _calculate_propagation_impact(self) -> Dict[str, float]:
        """
        Calculate the impact of each node on risk propagation using:
        - Flow betweenness
        - Risk diffusion
        - Component dependencies
        """
        impacts = {}
        
        # Calculate flow betweenness centrality
        flow_btw = nx.approximate_current_flow_betweenness_centrality(
            self.graph.to_undirected()
        )
        
        # Get risk scores
        risk_scores = self._analyze_risk_propagation()
        
        for node in self.graph.nodes():
            # Start with flow betweenness
            impact = flow_btw[node]
            
            # Add risk influence
            risk_influence = risk_scores[node]
            
            # Consider dependencies
            dep_factor = 0.0
            if self.graph.nodes[node].get('type') == NodeType.COMPONENT.value:
                # Count dependent components
                descendants = nx.descendants(self.graph, node)
                if descendants:
                    dep_factor = len(descendants) / len(self.graph.nodes())
            
            # Calculate final impact
            impacts[node] = (
                0.4 * impact +
                0.4 * risk_influence +
                0.2 * dep_factor
            )
        
        return impacts
    
    def _get_critical_node_pairs(self) -> List[Tuple[str, str]]:
        """Get pairs of nodes for critical path analysis"""
        pairs = []
        
        # Get high-risk nodes
        risk_scores = self._analyze_risk_propagation()
        high_risk_nodes = [
            node for node, score in risk_scores.items()
            if score >= np.percentile(list(risk_scores.values()), 75)
        ]
        
        # Get entry points and sensitive components
        entry_points = [
            n for n in self.graph.nodes()
            if self.graph.in_degree(n) == 0
        ]
        
        sensitive_components = [
            n for n, attrs in self.graph.nodes(data=True)
            if attrs.get('is_critical') or attrs.get('is_sensitive')
        ]
        
        # Create pairs
        pairs.extend([
            (start, end)
            for start in entry_points
            for end in sensitive_components
        ])
        
        pairs.extend([
            (start, end)
            for i, start in enumerate(high_risk_nodes)
            for end in high_risk_nodes[i+1:]
        ])
        
        return pairs
    
    def _merge_small_clusters(self, clusters: List[Set[str]]) -> List[Set[str]]:
        """Merge small clusters based on connectivity"""
        MIN_CLUSTER_SIZE = 3
        merged = []
        
        # Sort clusters by size
        clusters = sorted(clusters, key=len, reverse=True)
        
        while clusters:
            current = clusters.pop(0)
            
            if len(current) < MIN_CLUSTER_SIZE:
                # Find best cluster to merge with
                best_match = None
                best_connectivity = 0
                
                for other in clusters:
                    connectivity = self._calculate_cluster_connectivity(
                        current, other
                    )
                    if connectivity > best_connectivity:
                        best_connectivity = connectivity
                        best_match = other
                
                if best_match:
                    # Merge clusters
                    clusters.remove(best_match)
                    current.update(best_match)
            
            merged.append(current)
        
        return merged
    
    def _calculate_cluster_connectivity(self, cluster1: Set[str], cluster2: Set[str]) -> float:
        """Calculate connectivity between two clusters"""
        edges_between = sum(
            1 for u in cluster1
            for v in cluster2
            if self.graph.has_edge(u, v) or self.graph.has_edge(v, u)
        )
        
        max_possible = len(cluster1) * len(cluster2)
        return edges_between / max_possible if max_possible > 0 else 0

def main():
    """Example usage of the graph analyzer"""
    # Create sample vulnerability graph
    G = nx.DiGraph()
    
    # Add nodes
    G.add_node('CVE-2021-44228', type=NodeType.VULNERABILITY.value,
               data={'cvss_scores': [10.0], 'exploit_status': 'ACTIVELY_EXPLOITED'})
    G.add_node('log4j-core', type=NodeType.COMPONENT.value,
               is_critical=True)
    G.add_node('app-server', type=NodeType.COMPONENT.value)
    
    # Add edges
    G.add_edge('CVE-2021-44228', 'log4j-core', type=EdgeType.AFFECTS.value)
    G.add_edge('log4j-core', 'app-server', type=EdgeType.DEPENDS_ON.value)
    
    # Create analyzer
    analyzer = VulnerabilityGraphAnalyzer(G)
    
    # Run analysis
    metrics = analyzer.analyze_graph()
    
    # Print results
    print("\nGraph Analysis Results:")
    print(f"Critical Nodes: {metrics.critical_nodes}")
    print(f"Attack Surface: {metrics.attack_surface:.2f}")
    print(f"Risk Density: {metrics.risk_density:.2f}")
    print("\nComponent Risks:")
    for component, risk in metrics.component_risks.items():
        print(f"- {component}: {risk:.2f}")

if __name__ == "__main__":
    main()