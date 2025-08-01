"""
Graph-based dependency analysis with risk aggregation and cycle detection.
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import heapq

@dataclass
class PackageNode:
    """Represents a package in the dependency graph"""
    name: str
    version: str
    purl: str
    direct_risk_score: float = 0.0
    aggregated_risk_score: float = 0.0
    vulnerabilities: List[Dict] = None
    
    def __hash__(self):
        return hash(self.purl)
    
    def __eq__(self, other):
        return self.purl == other.purl
    
    @property
    def identifier(self) -> str:
        return f"{self.name}@{self.version}"

@dataclass
class DependencyEdge:
    """Represents a dependency relationship between packages"""
    source: PackageNode
    target: PackageNode
    weight: float = 1.0  # Weight factor for risk propagation
    is_dev_dependency: bool = False
    
    def __hash__(self):
        return hash((self.source.purl, self.target.purl))

class DependencyGraph:
    """
    Graph-based dependency analyzer with risk aggregation.
    
    Features:
    - Cycle detection using DFS with path tracking
    - Risk aggregation with weighted propagation
    - Critical path identification
    - Transitive vulnerability analysis
    """
    
    def __init__(self):
        self.nodes: Dict[str, PackageNode] = {}  # purl -> node
        self.edges: Dict[str, Set[DependencyEdge]] = defaultdict(set)  # source_purl -> edges
        self.reverse_edges: Dict[str, Set[DependencyEdge]] = defaultdict(set)  # target_purl -> edges
        self.cycles: List[List[PackageNode]] = []
        
    def add_node(self, package: Dict) -> PackageNode:
        """Add a package node to the graph"""
        purl = package['purl']
        if purl not in self.nodes:
            node = PackageNode(
                name=package['name'],
                version=package['version'],
                purl=purl,
                vulnerabilities=package.get('vulnerabilities', [])
            )
            self.nodes[purl] = node
        return self.nodes[purl]
    
    def add_edge(self, source: PackageNode, target: PackageNode, 
                 weight: float = 1.0, is_dev: bool = False):
        """Add a dependency edge to the graph"""
        edge = DependencyEdge(source, target, weight, is_dev)
        self.edges[source.purl].add(edge)
        self.reverse_edges[target.purl].add(edge)
    
    def detect_cycles(self) -> List[List[PackageNode]]:
        """
        Detect cycles in the dependency graph using DFS.
        Returns list of cycles found.
        """
        visited: Set[str] = set()
        path: List[str] = []
        self.cycles = []
        
        def dfs(node_purl: str):
            if node_purl in path:
                # Found a cycle
                cycle_start = path.index(node_purl)
                cycle = [self.nodes[purl] for purl in path[cycle_start:]]
                self.cycles.append(cycle)
                return
            
            if node_purl in visited:
                return
            
            visited.add(node_purl)
            path.append(node_purl)
            
            for edge in self.edges[node_purl]:
                dfs(edge.target.purl)
            
            path.pop()
        
        # Start DFS from each node to find all cycles
        for node_purl in self.nodes:
            if node_purl not in visited:
                dfs(node_purl)
        
        return self.cycles
    
    def calculate_node_risk(self, node: PackageNode) -> float:
        """Calculate direct risk score for a node based on its vulnerabilities"""
        if not node.vulnerabilities:
            return 0.0
        
        # Weight factors for risk calculation
        severity_weights = {
            'CRITICAL': 1.0,
            'HIGH': 0.8,
            'MEDIUM': 0.5,
            'LOW': 0.2
        }
        
        # Calculate maximum weighted CVSS score
        max_weighted_score = 0.0
        for vuln in node.vulnerabilities:
            cvss_score = vuln.get('cvss_score', 0.0)
            severity = vuln.get('severity', 'LOW')
            weighted_score = cvss_score * severity_weights.get(severity, 0.1)
            max_weighted_score = max(max_weighted_score, weighted_score)
        
        return max_weighted_score
    
    def aggregate_risk_scores(self, root_purl: str) -> Dict[str, float]:
        """
        Aggregate risk scores from dependencies up to the root.
        Uses weighted propagation and handles cycles.
        """
        # Initialize scores
        scores: Dict[str, float] = defaultdict(float)
        visited: Set[str] = set()
        
        def aggregate_node(node_purl: str, path: Set[str], depth: int = 0) -> float:
            if node_purl in path:
                # We're in a cycle - use cached score if available
                return scores.get(node_purl, 0.0)
            
            if node_purl in visited:
                return scores[node_purl]
            
            node = self.nodes[node_purl]
            
            # Calculate direct risk
            direct_risk = self.calculate_node_risk(node)
            
            # Calculate propagated risk from dependencies
            propagated_risk = 0.0
            path.add(node_purl)
            
            for edge in self.edges[node_purl]:
                # Weight factor decreases with depth
                depth_factor = 1.0 / (depth + 1)
                dep_risk = aggregate_node(edge.target.purl, path, depth + 1)
                propagated_risk += dep_risk * edge.weight * depth_factor
            
            path.remove(node_purl)
            
            # Combine direct and propagated risk
            total_risk = direct_risk + (propagated_risk * 0.7)  # 70% weight to propagated risk
            scores[node_purl] = total_risk
            visited.add(node_purl)
            
            return total_risk
        
        # Start aggregation from root
        aggregate_node(root_purl, set())
        return scores
    
    def find_critical_paths(self, root_purl: str, risk_threshold: float = 7.0) -> List[List[PackageNode]]:
        """
        Find high-risk dependency paths using Dijkstra's algorithm.
        Risk is used as the distance metric (higher risk = shorter distance).
        """
        critical_paths: List[List[PackageNode]] = []
        visited: Set[str] = set()
        
        # Priority queue entries: (negative_risk, node_purl, path)
        # Using negative risk because heapq is min-heap
        queue: List[Tuple[float, str, List[PackageNode]]] = [
            (0.0, root_purl, [self.nodes[root_purl]])
        ]
        
        while queue:
            neg_risk, node_purl, path = heapq.heappop(queue)
            risk = -neg_risk
            
            if node_purl in visited:
                continue
            
            visited.add(node_purl)
            
            # If path risk exceeds threshold, add to critical paths
            if risk >= risk_threshold:
                critical_paths.append(path)
            
            # Explore dependencies
            for edge in self.edges[node_purl]:
                if edge.target.purl not in visited:
                    dep_risk = self.calculate_node_risk(edge.target)
                    new_risk = risk + (dep_risk * edge.weight)
                    new_path = path + [edge.target]
                    heapq.heappush(queue, (-new_risk, edge.target.purl, new_path))
        
        return critical_paths
    
    def analyze_dependencies(self, sbom_data: Dict) -> Dict:
        """
        Analyze SBOM dependencies and generate comprehensive report.
        """
        # Build graph from SBOM
        root_component = sbom_data['metadata']['component']
        root_node = self.add_node(root_component)
        
        for component in sbom_data['components']:
            node = self.add_node(component)
            self.add_edge(root_node, node)
        
        # Detect cycles
        cycles = self.detect_cycles()
        
        # Aggregate risk scores
        risk_scores = self.aggregate_risk_scores(root_node.purl)
        
        # Find critical paths
        critical_paths = self.find_critical_paths(root_node.purl)
        
        # Generate report
        report = {
            'root_component': root_node.identifier,
            'total_components': len(self.nodes),
            'risk_scores': dict(risk_scores),
            'max_risk_score': max(risk_scores.values()) if risk_scores else 0.0,
            'cycles_detected': [
                [node.identifier for node in cycle]
                for cycle in cycles
            ],
            'critical_paths': [
                {
                    'path': [node.identifier for node in path],
                    'risk_score': sum(self.calculate_node_risk(node) for node in path)
                }
                for path in critical_paths
            ]
        }
        
        return report

def create_graph_from_sbom(sbom_data: Dict) -> DependencyGraph:
    """Create a DependencyGraph instance from SBOM data"""
    graph = DependencyGraph()
    
    # Add root component
    root_component = sbom_data['metadata']['component']
    root_node = graph.add_node(root_component)
    
    # Add all components and their dependencies
    for component in sbom_data['components']:
        node = graph.add_node(component)
        
        # Add edge from root to direct dependency
        graph.add_edge(root_node, node)
        
        # Add edges for nested dependencies if present
        if 'dependencies' in component:
            for dep in component['dependencies']:
                dep_node = graph.add_node(dep)
                graph.add_edge(node, dep_node)
    
    return graph