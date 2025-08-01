"""
Enhanced vulnerability data correlation and analysis system.
Combines and enriches data from multiple sources using advanced correlation techniques.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import re
from enum import Enum
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textdistance import levenshtein
import networkx as nx

logger = logging.getLogger(__name__)

class ExploitStatus(Enum):
    """Normalized exploit status across sources"""
    NONE = 0
    UNPROVEN = 1
    PROOF_OF_CONCEPT = 2
    ACTIVELY_EXPLOITED = 3
    WEAPONIZED = 4

class Severity(Enum):
    """Normalized severity levels"""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class EnrichedVulnerability:
    """Enriched vulnerability information with correlated data"""
    cve_id: str
    descriptions: List[str] = field(default_factory=list)
    cvss_scores: List[float] = field(default_factory=list)
    cvss_vectors: List[str] = field(default_factory=list)
    affected_packages: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))
    references: List[Dict] = field(default_factory=list)
    exploit_status: ExploitStatus = ExploitStatus.NONE
    severity: Severity = Severity.NONE
    source_data: Dict[str, Dict] = field(default_factory=dict)
    related_cves: List[str] = field(default_factory=list)
    attack_complexity: Optional[str] = None
    attack_vector: Optional[str] = None
    patch_status: Dict[str, str] = field(default_factory=dict)
    threat_intel: Dict = field(default_factory=dict)
    exploit_details: List[Dict] = field(default_factory=list)
    temporal_metrics: Dict = field(default_factory=dict)
    environmental_metrics: Dict = field(default_factory=dict)

class VulnerabilityCorrelator:
    """
    Advanced vulnerability data correlation system.
    Combines and analyzes data from multiple sources.
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=10000
        )
        
        # Correlation thresholds
        self.description_similarity_threshold = 0.8
        self.package_match_threshold = 0.9
        self.reference_match_threshold = 0.85
        
        # Graph for vulnerability relationships
        self.vuln_graph = nx.DiGraph()
    
    def correlate_vulnerabilities(self, source_data: Dict[str, List[Dict]]) -> Dict[str, EnrichedVulnerability]:
        """
        Correlate vulnerability data from multiple sources.
        
        Args:
            source_data: Dictionary mapping source names to their vulnerability data
        
        Returns:
            Dictionary mapping CVE IDs to enriched vulnerability information
        """
        # Initialize enriched vulnerabilities
        enriched_vulns: Dict[str, EnrichedVulnerability] = {}
        
        # First pass: Create base entries and exact matches
        for source, vulns in source_data.items():
            for vuln in vulns:
                cve_id = vuln.get('cve_id')
                if not cve_id:
                    continue
                
                if cve_id not in enriched_vulns:
                    enriched_vulns[cve_id] = EnrichedVulnerability(cve_id=cve_id)
                
                self._enrich_vulnerability(enriched_vulns[cve_id], vuln, source)
        
        # Second pass: Correlate related vulnerabilities
        self._correlate_related_vulnerabilities(enriched_vulns)
        
        # Third pass: Enrich with threat intelligence
        self._enrich_with_threat_intel(enriched_vulns)
        
        # Fourth pass: Calculate final metrics
        self._calculate_final_metrics(enriched_vulns)
        
        return enriched_vulns
    
    def _enrich_vulnerability(self, enriched: EnrichedVulnerability, vuln: Dict, source: str):
        """Enrich a vulnerability with data from a source"""
        # Store source data
        enriched.source_data[source] = vuln
        
        # Add descriptions
        if 'description' in vuln:
            enriched.descriptions.append(vuln['description'])
        
        # Add CVSS scores and vectors
        if 'cvss_score' in vuln:
            enriched.cvss_scores.append(vuln['cvss_score'])
        if 'cvss_vector' in vuln:
            enriched.cvss_vectors.append(vuln['cvss_vector'])
        
        # Add affected packages
        if 'affected_packages' in vuln:
            for pkg in vuln['affected_packages']:
                ecosystem = pkg.get('ecosystem', 'unknown')
                name = pkg.get('name')
                if name:
                    enriched.affected_packages[ecosystem].add(name)
        
        # Add references with source attribution
        if 'references' in vuln:
            for ref in vuln['references']:
                if isinstance(ref, str):
                    ref_dict = {'url': ref, 'source': source}
                else:
                    ref_dict = {**ref, 'source': source}
                enriched.references.append(ref_dict)
        
        # Update exploit status
        new_status = self._determine_exploit_status(vuln)
        if new_status.value > enriched.exploit_status.value:
            enriched.exploit_status = new_status
        
        # Update severity
        new_severity = self._determine_severity(vuln)
        if new_severity.value > enriched.severity.value:
            enriched.severity = new_severity
        
        # Add exploit details
        if source == 'exploitdb' or source == 'metasploit':
            exploit = {
                'source': source,
                'id': vuln.get('id') or vuln.get('module_name'),
                'type': vuln.get('type'),
                'verified': vuln.get('verified', False),
                'url': vuln.get('exploit_url') or vuln.get('path')
            }
            enriched.exploit_details.append(exploit)
        
        # Add patch information
        if 'fixed_version' in vuln or 'patch_status' in vuln:
            enriched.patch_status[source] = {
                'fixed_version': vuln.get('fixed_version'),
                'status': vuln.get('patch_status'),
                'notes': vuln.get('patch_notes')
            }
    
    def _correlate_related_vulnerabilities(self, vulns: Dict[str, EnrichedVulnerability]):
        """Correlate related vulnerabilities based on various factors"""
        # Create description vectors
        descriptions = []
        cve_ids = []
        for cve_id, vuln in vulns.items():
            if vuln.descriptions:
                descriptions.append(" ".join(vuln.descriptions))
                cve_ids.append(cve_id)
        
        if not descriptions:
            return
        
        # Calculate description similarity
        vectors = self.vectorizer.fit_transform(descriptions)
        similarity_matrix = cosine_similarity(vectors)
        
        # Build relationship graph
        for i, cve_id in enumerate(cve_ids):
            for j, other_cve in enumerate(cve_ids):
                if i != j and similarity_matrix[i][j] > self.description_similarity_threshold:
                    self.vuln_graph.add_edge(cve_id, other_cve, 
                                          weight=similarity_matrix[i][j],
                                          type='description_similarity')
        
        # Add package-based relationships
        for cve_id, vuln in vulns.items():
            for other_cve, other_vuln in vulns.items():
                if cve_id != other_cve:
                    # Check package overlap
                    for ecosystem, packages in vuln.affected_packages.items():
                        other_packages = other_vuln.affected_packages.get(ecosystem, set())
                        if packages & other_packages:  # Set intersection
                            self.vuln_graph.add_edge(cve_id, other_cve,
                                                  weight=1.0,
                                                  type='shared_package')
        
        # Find related vulnerabilities using graph analysis
        for cve_id in vulns:
            if cve_id in self.vuln_graph:
                # Get neighbors sorted by edge weight
                neighbors = sorted(
                    self.vuln_graph[cve_id].items(),
                    key=lambda x: x[1]['weight'],
                    reverse=True
                )
                vulns[cve_id].related_cves = [n[0] for n in neighbors[:5]]
    
    def _enrich_with_threat_intel(self, vulns: Dict[str, EnrichedVulnerability]):
        """Enrich vulnerabilities with threat intelligence"""
        for vuln in vulns.values():
            threat_intel = defaultdict(list)
            
            # Combine threat intel from different sources
            for source, data in vuln.source_data.items():
                # Threat actors
                if 'threat_actors' in data:
                    threat_intel['threat_actors'].extend(data['threat_actors'])
                
                # Malware families
                if 'malware_families' in data:
                    threat_intel['malware_families'].extend(data['malware_families'])
                
                # Targeted industries
                if 'targeted_industries' in data:
                    threat_intel['targeted_industries'].extend(data['targeted_industries'])
                
                # Campaign information
                if 'campaigns' in data:
                    threat_intel['campaigns'].extend(data['campaigns'])
            
            # Add CISA KEV data if available
            if 'cisa_kev' in vuln.source_data:
                kev_data = vuln.source_data['cisa_kev']
                threat_intel['known_exploited'] = True
                threat_intel['required_action'] = kev_data.get('required_action')
                threat_intel['due_date'] = kev_data.get('due_date')
                threat_intel['known_ransomware'] = kev_data.get('known_ransomware', False)
            
            # Deduplicate and clean threat intel
            for key in threat_intel:
                if isinstance(threat_intel[key], list):
                    threat_intel[key] = list(set(threat_intel[key]))
            
            vuln.threat_intel = dict(threat_intel)
    
    def _calculate_final_metrics(self, vulns: Dict[str, EnrichedVulnerability]):
        """Calculate final metrics for each vulnerability"""
        for vuln in vulns.values():
            temporal_metrics = {}
            environmental_metrics = {}
            
            # Calculate temporal metrics
            if vuln.cvss_scores:
                base_score = max(vuln.cvss_scores)
                
                # Exploit Code Maturity
                exploit_maturity = {
                    ExploitStatus.NONE: 0.0,
                    ExploitStatus.UNPROVEN: 0.2,
                    ExploitStatus.PROOF_OF_CONCEPT: 0.5,
                    ExploitStatus.ACTIVELY_EXPLOITED: 0.9,
                    ExploitStatus.WEAPONIZED: 1.0
                }[vuln.exploit_status]
                
                # Remediation Level
                if not vuln.patch_status:
                    remediation_level = 1.0  # Unavailable
                elif any('fixed_version' in status for status in vuln.patch_status.values()):
                    remediation_level = 0.5  # Available
                else:
                    remediation_level = 0.9  # Workaround
                
                # Report Confidence
                confidence = min(len(vuln.source_data) / 5.0, 1.0)
                
                temporal_score = base_score * exploit_maturity * remediation_level * confidence
                
                temporal_metrics.update({
                    'temporal_score': temporal_score,
                    'exploit_maturity': exploit_maturity,
                    'remediation_level': remediation_level,
                    'report_confidence': confidence
                })
            
            # Calculate environmental metrics
            if vuln.threat_intel:
                threat_score = 0.0
                
                # Threat Actor presence
                if vuln.threat_intel.get('threat_actors'):
                    threat_score += 0.3
                
                # Malware presence
                if vuln.threat_intel.get('malware_families'):
                    threat_score += 0.3
                
                # Known exploitation
                if vuln.threat_intel.get('known_exploited'):
                    threat_score += 0.4
                
                # Ransomware involvement
                if vuln.threat_intel.get('known_ransomware'):
                    threat_score += 0.3
                
                environmental_metrics.update({
                    'threat_score': min(threat_score, 1.0),
                    'targeted_industries': len(vuln.threat_intel.get('targeted_industries', [])),
                    'campaign_count': len(vuln.threat_intel.get('campaigns', [])),
                    'immediate_action_required': 'due_date' in vuln.threat_intel
                })
            
            vuln.temporal_metrics = temporal_metrics
            vuln.environmental_metrics = environmental_metrics
    
    @staticmethod
    def _determine_exploit_status(vuln: Dict) -> ExploitStatus:
        """Determine exploit status from vulnerability data"""
        status = ExploitStatus.NONE
        
        # Check various source-specific fields
        if vuln.get('exploit_status') == 'ACTIVELY_EXPLOITED':
            status = ExploitStatus.ACTIVELY_EXPLOITED
        elif vuln.get('exploit_maturity') == 'HIGH':
            status = ExploitStatus.WEAPONIZED
        elif vuln.get('exploit_maturity') == 'PROOF_OF_CONCEPT':
            status = ExploitStatus.PROOF_OF_CONCEPT
        elif vuln.get('exploit_available') or vuln.get('has_exploit'):
            status = ExploitStatus.PROOF_OF_CONCEPT
        
        # Check for exploit details
        if vuln.get('exploit_details') and status.value < ExploitStatus.PROOF_OF_CONCEPT.value:
            status = ExploitStatus.PROOF_OF_CONCEPT
        
        # Check CISA KEV
        if vuln.get('known_exploited'):
            status = ExploitStatus.ACTIVELY_EXPLOITED
        
        return status
    
    @staticmethod
    def _determine_severity(vuln: Dict) -> Severity:
        """Determine severity from vulnerability data"""
        # Start with CVSS-based severity
        cvss_score = vuln.get('cvss_score', 0.0)
        if cvss_score >= 9.0:
            severity = Severity.CRITICAL
        elif cvss_score >= 7.0:
            severity = Severity.HIGH
        elif cvss_score >= 4.0:
            severity = Severity.MEDIUM
        elif cvss_score > 0.0:
            severity = Severity.LOW
        else:
            severity = Severity.NONE
        
        # Check explicit severity
        explicit_severity = vuln.get('severity', '').upper()
        if explicit_severity == 'CRITICAL':
            severity = max(severity, Severity.CRITICAL)
        elif explicit_severity == 'HIGH':
            severity = max(severity, Severity.HIGH)
        elif explicit_severity == 'MEDIUM':
            severity = max(severity, Severity.MEDIUM)
        elif explicit_severity == 'LOW':
            severity = max(severity, Severity.LOW)
        
        return severity

class VulnerabilityAnalyzer:
    """
    Advanced vulnerability analysis system.
    Provides insights and recommendations based on correlated data.
    """
    
    def __init__(self, enriched_vulns: Dict[str, EnrichedVulnerability]):
        self.vulns = enriched_vulns
        self.vuln_graph = nx.DiGraph()
        self._build_analysis_graph()
    
    def _build_analysis_graph(self):
        """Build graph representation for analysis"""
        for cve_id, vuln in self.vulns.items():
            # Add vulnerability node
            self.vuln_graph.add_node(cve_id, 
                                   type='vulnerability',
                                   data=vuln)
            
            # Add package nodes and edges
            for ecosystem, packages in vuln.affected_packages.items():
                for package in packages:
                    pkg_node = f"{ecosystem}:{package}"
                    self.vuln_graph.add_node(pkg_node,
                                           type='package',
                                           ecosystem=ecosystem)
                    self.vuln_graph.add_edge(cve_id, pkg_node,
                                           type='affects')
            
            # Add relationships between vulnerabilities
            for related_cve in vuln.related_cves:
                if related_cve in self.vulns:
                    self.vuln_graph.add_edge(cve_id, related_cve,
                                           type='related')
    
    def get_critical_paths(self) -> List[List[str]]:
        """Find critical vulnerability paths in the graph"""
        critical_paths = []
        
        # Find paths between high-severity vulnerabilities
        critical_vulns = [
            cve_id for cve_id, vuln in self.vulns.items()
            if vuln.severity in (Severity.CRITICAL, Severity.HIGH)
        ]
        
        for start in critical_vulns:
            for end in critical_vulns:
                if start != end:
                    try:
                        paths = list(nx.all_simple_paths(
                            self.vuln_graph, start, end
                        ))
                        critical_paths.extend(paths)
                    except nx.NetworkXNoPath:
                        continue
        
        return critical_paths
    
    def get_vulnerability_clusters(self) -> List[Set[str]]:
        """Find clusters of related vulnerabilities"""
        # Use community detection to find clusters
        clusters = []
        
        # Create subgraph of only vulnerability nodes
        vuln_graph = self.vuln_graph.subgraph([
            node for node, attr in self.vuln_graph.nodes(data=True)
            if attr['type'] == 'vulnerability'
        ])
        
        # Find connected components
        components = nx.connected_components(vuln_graph.to_undirected())
        clusters.extend(components)
        
        return clusters
    
    def get_package_risk_scores(self) -> Dict[str, float]:
        """Calculate risk scores for affected packages"""
        package_risks = {}
        
        for node, attr in self.vuln_graph.nodes(data=True):
            if attr['type'] == 'package':
                # Get all vulnerabilities affecting this package
                affecting_vulns = [
                    self.vulns[pred] for pred in self.vuln_graph.predecessors(node)
                    if pred in self.vulns
                ]
                
                if affecting_vulns:
                    # Calculate risk based on vulnerability metrics
                    max_cvss = max(
                        max(vuln.cvss_scores) if vuln.cvss_scores else 0.0
                        for vuln in affecting_vulns
                    )
                    
                    exploit_factor = max(
                        vuln.exploit_status.value / len(ExploitStatus)
                        for vuln in affecting_vulns
                    )
                    
                    threat_factor = max(
                        vuln.environmental_metrics.get('threat_score', 0.0)
                        for vuln in affecting_vulns
                    )
                    
                    # Combine factors
                    risk_score = (
                        0.4 * (max_cvss / 10.0) +
                        0.3 * exploit_factor +
                        0.3 * threat_factor
                    )
                    
                    package_risks[node] = risk_score
        
        return package_risks
    
    def get_remediation_priorities(self) -> List[Dict]:
        """Get prioritized list of vulnerabilities for remediation"""
        priorities = []
        
        for cve_id, vuln in self.vulns.items():
            # Calculate priority score
            if not vuln.cvss_scores:
                continue
            
            base_score = max(vuln.cvss_scores)
            temporal_score = vuln.temporal_metrics.get('temporal_score', base_score)
            threat_score = vuln.environmental_metrics.get('threat_score', 0.0)
            
            # Factors that increase priority
            priority_factors = []
            
            if vuln.exploit_status in (ExploitStatus.ACTIVELY_EXPLOITED, ExploitStatus.WEAPONIZED):
                priority_factors.append("Active exploitation")
            
            if vuln.threat_intel.get('known_ransomware'):
                priority_factors.append("Known ransomware")
            
            if vuln.threat_intel.get('immediate_action_required'):
                priority_factors.append("Immediate action required")
            
            if vuln.severity in (Severity.CRITICAL, Severity.HIGH):
                priority_factors.append(f"Severity: {vuln.severity.name}")
            
            # Calculate final priority score
            priority_score = (
                0.4 * (base_score / 10.0) +
                0.3 * (temporal_score / 10.0) +
                0.3 * threat_score
            )
            
            # Add priority entry
            priorities.append({
                'cve_id': cve_id,
                'priority_score': priority_score,
                'factors': priority_factors,
                'affected_packages': vuln.affected_packages,
                'patch_status': vuln.patch_status,
                'exploit_status': vuln.exploit_status.name,
                'temporal_metrics': vuln.temporal_metrics,
                'environmental_metrics': vuln.environmental_metrics
            })
        
        # Sort by priority score
        return sorted(priorities, key=lambda x: x['priority_score'], reverse=True)

def main():
    """Example usage of the correlation system"""
    # Sample data from different sources
    source_data = {
        'nvd': [{
            'cve_id': 'CVE-2021-44228',
            'description': 'Apache Log4j2 vulnerability...',
            'cvss_score': 10.0
        }],
        'github': [{
            'cve_id': 'CVE-2021-44228',
            'description': 'Log4j RCE vulnerability...',
            'affected_packages': [{'ecosystem': 'maven', 'name': 'log4j-core'}]
        }]
    }
    
    # Create correlator
    correlator = VulnerabilityCorrelator()
    
    # Correlate vulnerabilities
    enriched_vulns = correlator.correlate_vulnerabilities(source_data)
    
    # Create analyzer
    analyzer = VulnerabilityAnalyzer(enriched_vulns)
    
    # Get analysis results
    critical_paths = analyzer.get_critical_paths()
    clusters = analyzer.get_vulnerability_clusters()
    package_risks = analyzer.get_package_risk_scores()
    priorities = analyzer.get_remediation_priorities()
    
    # Print results
    print("\nCritical Paths:", critical_paths)
    print("\nVulnerability Clusters:", clusters)
    print("\nPackage Risk Scores:", package_risks)
    print("\nRemediation Priorities:", priorities)

if __name__ == "__main__":
    main()