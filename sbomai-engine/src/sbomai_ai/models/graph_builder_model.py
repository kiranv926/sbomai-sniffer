"""
Dependency Graph Builder model for SBOM analysis.
"""

from typing import List, Dict, Optional, Tuple, Set
import logging
from dataclasses import dataclass
import networkx as nx
from packaging.version import parse as parse_version
import json

logger = logging.getLogger(__name__)

@dataclass
class DependencyGraphConfig:
    """Configuration for Dependency Graph Builder"""
    include_dev_dependencies: bool = False
    include_optional_dependencies: bool = False
    max_depth: Optional[int] = None
    include_vulnerabilities: bool = True
    include_licenses: bool = True

class DependencyGraphBuilder:
    """
    Builds and analyzes dependency graphs from SBOM data.
    """
    
    def __init__(self, config: DependencyGraphConfig):
        self.config = config
    
    def build_graph(self, sbom_data: Dict) -> nx.DiGraph:
        """
        Build dependency graph from SBOM data.
        
        Args:
            sbom_data: SBOM document
        
        Returns:
            NetworkX directed graph
        """
        graph = nx.DiGraph()
        
        # Process components
        self._add_components(graph, sbom_data)
        
        # Process dependencies
        self._add_dependencies(graph, sbom_data)
        
        # Process vulnerabilities
        if self.config.include_vulnerabilities:
            self._add_vulnerabilities(graph, sbom_data)
        
        # Process licenses
        if self.config.include_licenses:
            self._add_licenses(graph, sbom_data)
        
        return graph
    
    def analyze_graph(self, graph: nx.DiGraph) -> Dict:
        """
        Analyze dependency graph.
        
        Args:
            graph: NetworkX directed graph
        
        Returns:
            Analysis results including:
            - Graph metrics
            - Critical paths
            - Risk factors
            - License compliance
        """
        analysis = {
            "graph_metrics": self._calculate_metrics(graph),
            "critical_paths": self._find_critical_paths(graph),
            "risk_factors": self._analyze_risk_factors(graph),
            "license_analysis": self._analyze_licenses(graph)
            if self.config.include_licenses else None
        }
        
        return analysis
    
    def _add_components(self, graph: nx.DiGraph, sbom_data: Dict):
        """Add component nodes to graph"""
        components = sbom_data.get('components', [])
        
        for comp in components:
            # Create unique ID
            comp_id = self._create_component_id(comp)
            
            # Add node
            graph.add_node(
                comp_id,
                type='component',
                name=comp.get('name'),
                version=comp.get('version'),
                purl=comp.get('purl'),
                data=comp
            )
    
    def _add_dependencies(self, graph: nx.DiGraph, sbom_data: Dict):
        """Add dependency edges to graph"""
        components = sbom_data.get('components', [])
        
        for comp in components:
            comp_id = self._create_component_id(comp)
            
            # Process dependencies
            for dep in comp.get('dependencies', []):
                # Skip if filtered
                if not self._should_include_dependency(dep):
                    continue
                
                dep_id = self._create_component_id(dep)
                
                # Add edge
                graph.add_edge(
                    comp_id,
                    dep_id,
                    type='depends_on',
                    scope=dep.get('scope', 'runtime'),
                    data=dep
                )
    
    def _add_vulnerabilities(self, graph: nx.DiGraph, sbom_data: Dict):
        """Add vulnerability nodes and edges"""
        vulnerabilities = sbom_data.get('vulnerabilities', [])
        
        for vuln in vulnerabilities:
            # Create unique ID
            vuln_id = vuln.get('id') or vuln.get('cve_id')
            
            if not vuln_id:
                continue
            
            # Add node
            graph.add_node(
                vuln_id,
                type='vulnerability',
                data=vuln
            )
            
            # Add edges to affected components
            for comp in vuln.get('affected_components', []):
                comp_id = self._create_component_id(comp)
                
                graph.add_edge(
                    vuln_id,
                    comp_id,
                    type='affects',
                    data=vuln
                )
    
    def _add_licenses(self, graph: nx.DiGraph, sbom_data: Dict):
        """Add license nodes and edges"""
        components = sbom_data.get('components', [])
        
        for comp in components:
            comp_id = self._create_component_id(comp)
            
            # Process licenses
            for license_id in comp.get('licenses', []):
                if isinstance(license_id, dict):
                    license_id = license_id.get('id')
                
                if not license_id:
                    continue
                
                # Add node if not exists
                if not graph.has_node(license_id):
                    graph.add_node(
                        license_id,
                        type='license'
                    )
                
                # Add edge
                graph.add_edge(
                    comp_id,
                    license_id,
                    type='licensed_under'
                )
    
    def _calculate_metrics(self, graph: nx.DiGraph) -> Dict:
        """Calculate graph metrics"""
        metrics = {
            "num_nodes": graph.number_of_nodes(),
            "num_edges": graph.number_of_edges(),
            "num_components": len([
                n for n, d in graph.nodes(data=True)
                if d['type'] == 'component'
            ]),
            "num_vulnerabilities": len([
                n for n, d in graph.nodes(data=True)
                if d['type'] == 'vulnerability'
            ]),
            "num_licenses": len([
                n for n, d in graph.nodes(data=True)
                if d['type'] == 'license'
            ]),
            "avg_dependencies": (
                sum(graph.out_degree(n) for n, d in graph.nodes(data=True)
                    if d['type'] == 'component') /
                len([n for n, d in graph.nodes(data=True)
                     if d['type'] == 'component'])
                if len([n for n, d in graph.nodes(data=True)
                       if d['type'] == 'component']) > 0
                else 0
            ),
            "max_depth": max(
                nx.shortest_path_length(graph, source=n).values()
                for n in graph.nodes()
                if graph.out_degree(n) > 0
            ) if graph.number_of_edges() > 0 else 0
        }
        
        return metrics
    
    def _find_critical_paths(self, graph: nx.DiGraph) -> List[Dict]:
        """Find critical dependency paths"""
        critical_paths = []
        
        # Find paths from vulnerabilities to components
        vuln_nodes = [
            n for n, d in graph.nodes(data=True)
            if d['type'] == 'vulnerability'
        ]
        
        for vuln_node in vuln_nodes:
            # Get affected components
            affected = [
                n for n in graph.neighbors(vuln_node)
                if graph.nodes[n]['type'] == 'component'
            ]
            
            for comp in affected:
                # Find all dependency paths
                paths = list(nx.all_simple_paths(graph, vuln_node, comp))
                
                for path in paths:
                    path_info = {
                        "vulnerability": graph.nodes[vuln_node]['data'],
                        "component": graph.nodes[comp]['data'],
                        "path": [
                            {
                                "id": node,
                                "type": graph.nodes[node]['type'],
                                "data": graph.nodes[node].get('data', {})
                            }
                            for node in path
                        ],
                        "length": len(path)
                    }
                    
                    critical_paths.append(path_info)
        
        return critical_paths
    
    def _analyze_risk_factors(self, graph: nx.DiGraph) -> Dict:
        """Analyze risk factors in graph"""
        risk_factors = {
            "high_risk_components": [],
            "dependency_cycles": [],
            "outdated_components": [],
            "vulnerable_paths": []
        }
        
        # Find components with multiple vulnerabilities
        for node, data in graph.nodes(data=True):
            if data['type'] == 'component':
                # Count vulnerabilities
                vulns = [
                    n for n in graph.predecessors(node)
                    if graph.nodes[n]['type'] == 'vulnerability'
                ]
                
                if len(vulns) > 1:
                    risk_factors["high_risk_components"].append({
                        "component": data['data'],
                        "vulnerabilities": [
                            graph.nodes[v]['data']
                            for v in vulns
                        ]
                    })
        
        # Find dependency cycles
        cycles = list(nx.simple_cycles(graph))
        for cycle in cycles:
            if len(cycle) > 1:
                risk_factors["dependency_cycles"].append({
                    "components": [
                        graph.nodes[n]['data']
                        for n in cycle
                        if graph.nodes[n]['type'] == 'component'
                    ],
                    "length": len(cycle)
                })
        
        # Find outdated components
        components = [
            (n, d) for n, d in graph.nodes(data=True)
            if d['type'] == 'component'
        ]
        
        for node, data in components:
            if 'version' in data:
                try:
                    current_version = parse_version(data['version'])
                    latest_version = self._get_latest_version(data['name'])
                    
                    if latest_version and current_version < latest_version:
                        risk_factors["outdated_components"].append({
                            "component": data['data'],
                            "current_version": str(current_version),
                            "latest_version": str(latest_version)
                        })
                except Exception:
                    pass
        
        # Find vulnerable dependency paths
        vuln_nodes = [
            n for n, d in graph.nodes(data=True)
            if d['type'] == 'vulnerability'
        ]
        
        for vuln_node in vuln_nodes:
            # Get affected components and their dependencies
            affected = [
                n for n in graph.neighbors(vuln_node)
                if graph.nodes[n]['type'] == 'component'
            ]
            
            for comp in affected:
                # Find all downstream dependencies
                descendants = nx.descendants(graph, comp)
                if descendants:
                    risk_factors["vulnerable_paths"].append({
                        "vulnerability": graph.nodes[vuln_node]['data'],
                        "source_component": graph.nodes[comp]['data'],
                        "affected_dependencies": [
                            graph.nodes[n]['data']
                            for n in descendants
                            if graph.nodes[n]['type'] == 'component'
                        ]
                    })
        
        return risk_factors
    
    def _analyze_licenses(self, graph: nx.DiGraph) -> Dict:
        """Analyze license compliance"""
        if not self.config.include_licenses:
            return None
        
        analysis = {
            "license_usage": {},
            "incompatible_licenses": [],
            "unknown_licenses": []
        }
        
        # Count license usage
        for node, data in graph.nodes(data=True):
            if data['type'] == 'license':
                components = [
                    n for n in graph.predecessors(node)
                    if graph.nodes[n]['type'] == 'component'
                ]
                
                analysis["license_usage"][node] = {
                    "count": len(components),
                    "components": [
                        graph.nodes[n]['data']
                        for n in components
                    ]
                }
        
        # Check for incompatible licenses
        licenses = [
            n for n, d in graph.nodes(data=True)
            if d['type'] == 'license'
        ]
        
        for license1 in licenses:
            for license2 in licenses:
                if license1 < license2:  # Avoid duplicates
                    if self._are_licenses_incompatible(license1, license2):
                        # Find components using these licenses
                        components1 = [
                            n for n in graph.predecessors(license1)
                            if graph.nodes[n]['type'] == 'component'
                        ]
                        components2 = [
                            n for n in graph.predecessors(license2)
                            if graph.nodes[n]['type'] == 'component'
                        ]
                        
                        if components1 and components2:
                            analysis["incompatible_licenses"].append({
                                "license1": license1,
                                "license2": license2,
                                "components1": [
                                    graph.nodes[n]['data']
                                    for n in components1
                                ],
                                "components2": [
                                    graph.nodes[n]['data']
                                    for n in components2
                                ]
                            })
        
        # Find unknown licenses
        for node, data in graph.nodes(data=True):
            if data['type'] == 'component':
                licenses = [
                    n for n in graph.successors(node)
                    if graph.nodes[n]['type'] == 'license'
                ]
                
                if not licenses:
                    analysis["unknown_licenses"].append(data['data'])
        
        return analysis
    
    def _create_component_id(self, comp: Dict) -> str:
        """Create unique component ID"""
        if 'purl' in comp:
            return comp['purl']
        
        return f"{comp.get('name')}@{comp.get('version')}"
    
    def _should_include_dependency(self, dep: Dict) -> bool:
        """Check if dependency should be included"""
        scope = dep.get('scope', 'runtime')
        
        if scope == 'dev' and not self.config.include_dev_dependencies:
            return False
        
        if scope == 'optional' and not self.config.include_optional_dependencies:
            return False
        
        return True
    
    def _get_latest_version(self, package_name: str) -> Optional[str]:
        """Get latest version of package (placeholder)"""
        # TODO: Implement package registry lookup
        return None
    
    def _are_licenses_incompatible(self, license1: str, license2: str) -> bool:
        """Check if licenses are incompatible (placeholder)"""
        # TODO: Implement license compatibility check
        return False
    
    def export_graph(self, graph: nx.DiGraph, format: str = 'json') -> str:
        """
        Export graph to specified format.
        
        Args:
            graph: NetworkX directed graph
            format: Output format ('json' or 'dot')
        
        Returns:
            Graph representation in specified format
        """
        if format == 'json':
            # Convert to JSON-serializable format
            data = {
                "nodes": [
                    {
                        "id": node,
                        "type": attr['type'],
                        "data": attr.get('data', {})
                    }
                    for node, attr in graph.nodes(data=True)
                ],
                "edges": [
                    {
                        "source": u,
                        "target": v,
                        "type": attr['type'],
                        "data": attr.get('data', {})
                    }
                    for u, v, attr in graph.edges(data=True)
                ]
            }
            
            return json.dumps(data, indent=2)
        
        elif format == 'dot':
            return nx.drawing.nx_pydot.to_pydot(graph).to_string()
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def import_graph(self, data: str, format: str = 'json') -> nx.DiGraph:
        """
        Import graph from specified format.
        
        Args:
            data: Graph representation
            format: Input format ('json' or 'dot')
        
        Returns:
            NetworkX directed graph
        """
        if format == 'json':
            # Parse JSON data
            graph_data = json.loads(data)
            
            graph = nx.DiGraph()
            
            # Add nodes
            for node in graph_data['nodes']:
                graph.add_node(
                    node['id'],
                    type=node['type'],
                    data=node.get('data', {})
                )
            
            # Add edges
            for edge in graph_data['edges']:
                graph.add_edge(
                    edge['source'],
                    edge['target'],
                    type=edge['type'],
                    data=edge.get('data', {})
                )
            
            return graph
        
        elif format == 'dot':
            return nx.drawing.nx_pydot.from_pydot(data)
        
        else:
            raise ValueError(f"Unsupported format: {format}")