"""
Advanced threat pattern analysis using machine learning and deep learning models.
"""

import logging
from typing import Dict, List, Optional, Tuple, Set
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import torch
import torch.nn as nn
from transformers import (
    AutoTokenizer, AutoModel, AutoModelForSequenceClassification,
    Trainer, TrainingArguments
)
from sentence_transformers import SentenceTransformer, util
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import networkx as nx
from collections import defaultdict

from ..utils.cache import Cache
from ..utils.monitoring import record_model_metrics
from ..config import get_config

logger = logging.getLogger(__name__)

class ExploitPatternDetector:
    """
    Detects exploit patterns in component metadata and code using deep learning.
    """
    
    def __init__(self):
        self.config = get_config()
        self.cache = Cache()
        
        # Initialize models
        self.code_tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.code_model = AutoModelForSequenceClassification.from_pretrained(
            "microsoft/codebert-base",
            num_labels=1  # Binary classification
        )
        
        self.text_model = SentenceTransformer('all-mpnet-base-v2')
        
        # Initialize anomaly detector
        self.anomaly_detector = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
        )
        
        # Load exploit patterns
        self.exploit_patterns = self._load_exploit_patterns()
    
    def analyze_component(self, component_data: Dict) -> Dict:
        """
        Analyze component for potential exploit patterns.
        """
        try:
            # Generate embeddings
            embeddings = self._generate_embeddings(component_data)
            
            # Match against known patterns
            pattern_matches = self._match_patterns(embeddings)
            
            # Detect anomalies
            anomaly_score = self._detect_anomalies(embeddings)
            
            # Analyze code patterns if available
            code_analysis = None
            if 'source_code' in component_data:
                code_analysis = self._analyze_code_patterns(component_data['source_code'])
            
            # Combine results
            return {
                'pattern_matches': pattern_matches,
                'anomaly_score': float(anomaly_score),
                'code_analysis': code_analysis,
                'risk_factors': self._identify_risk_factors(
                    pattern_matches,
                    anomaly_score,
                    code_analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing component: {str(e)}")
            raise
    
    def _generate_embeddings(self, component_data: Dict) -> Dict:
        """Generate embeddings for different aspects of the component"""
        return {
            'name': self.text_model.encode(component_data['name']),
            'description': self.text_model.encode(component_data['description']),
            'version': self.text_model.encode(component_data['version']),
            'metadata': self.text_model.encode(
                self._combine_metadata(component_data.get('metadata', {}))
            )
        }
    
    def _match_patterns(self, embeddings: Dict) -> List[Dict]:
        """Match embeddings against known exploit patterns"""
        matches = []
        
        for pattern in self.exploit_patterns:
            # Calculate similarity scores
            name_sim = util.pytorch_cos_sim(
                embeddings['name'],
                pattern['embeddings']['name']
            ).item()
            
            desc_sim = util.pytorch_cos_sim(
                embeddings['description'],
                pattern['embeddings']['description']
            ).item()
            
            # Calculate combined score
            combined_score = (name_sim + desc_sim) / 2
            
            if combined_score > self.config.ml_model.similarity_threshold:
                matches.append({
                    'pattern_id': pattern['id'],
                    'pattern_type': pattern['type'],
                    'similarity_score': combined_score,
                    'description': pattern['description'],
                    'cve_references': pattern['cve_references'],
                    'attack_vectors': pattern['attack_vectors']
                })
        
        return sorted(matches, key=lambda x: x['similarity_score'], reverse=True)
    
    def _detect_anomalies(self, embeddings: Dict) -> float:
        """Detect anomalies in component patterns"""
        # Combine embeddings
        combined = np.concatenate([
            embeddings['name'],
            embeddings['description'],
            embeddings['version'],
            embeddings['metadata']
        ])
        
        # Get anomaly score (-1 for anomalies, 1 for normal)
        score = self.anomaly_detector.score_samples([combined])[0]
        
        # Convert to probability-like score (0 to 1, higher means more anomalous)
        return 1 - ((score + 1) / 2)
    
    def _analyze_code_patterns(self, code: str) -> Dict:
        """Analyze code for suspicious patterns"""
        try:
            # Tokenize code
            inputs = self.code_tokenizer(
                code,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            )
            
            # Get model prediction
            with torch.no_grad():
                outputs = self.code_model(**inputs)
                score = torch.sigmoid(outputs.logits).item()
            
            # Analyze specific patterns
            patterns = self._identify_code_patterns(code)
            
            return {
                'risk_score': score,
                'suspicious_patterns': patterns,
                'risk_level': self._determine_code_risk_level(score, patterns)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing code patterns: {str(e)}")
            return None
    
    def _identify_code_patterns(self, code: str) -> List[Dict]:
        """Identify specific patterns in code"""
        patterns = []
        
        # Define pattern matchers
        pattern_matchers = {
            'command_injection': r'exec\s*\(|eval\s*\(|system\s*\(',
            'sql_injection': r'execute\s*\(|executeQuery\s*\(',
            'deserialization': r'deserialize|fromJson|parseXml',
            'file_operations': r'readFile|writeFile|unlink',
            'network_ops': r'socket\.|connect\s*\(|fetch\s*\(',
            'crypto_ops': r'decrypt|encrypt|createHash'
        }
        
        # Check each pattern
        for pattern_type, regex in pattern_matchers.items():
            matches = re.finditer(regex, code, re.IGNORECASE)
            for match in matches:
                patterns.append({
                    'type': pattern_type,
                    'line': code.count('\n', 0, match.start()) + 1,
                    'snippet': code[max(0, match.start()-20):match.end()+20]
                })
        
        return patterns
    
    def _determine_code_risk_level(
        self,
        risk_score: float,
        patterns: List[Dict]
    ) -> str:
        """Determine overall code risk level"""
        if risk_score > 0.8 or len(patterns) > 5:
            return 'high'
        elif risk_score > 0.5 or len(patterns) > 2:
            return 'medium'
        else:
            return 'low'
    
    def _identify_risk_factors(
        self,
        pattern_matches: List[Dict],
        anomaly_score: float,
        code_analysis: Optional[Dict]
    ) -> List[Dict]:
        """Identify key risk factors"""
        risk_factors = []
        
        # Pattern-based risks
        if pattern_matches:
            risk_factors.append({
                'type': 'pattern_match',
                'severity': 'high' if any(m['similarity_score'] > 0.9 for m in pattern_matches) else 'medium',
                'description': f"Matches {len(pattern_matches)} known exploit patterns",
                'details': [m['description'] for m in pattern_matches]
            })
        
        # Anomaly-based risks
        if anomaly_score > 0.8:
            risk_factors.append({
                'type': 'anomaly',
                'severity': 'high',
                'description': "Highly anomalous behavior detected",
                'score': anomaly_score
            })
        elif anomaly_score > 0.6:
            risk_factors.append({
                'type': 'anomaly',
                'severity': 'medium',
                'description': "Moderately anomalous behavior detected",
                'score': anomaly_score
            })
        
        # Code-based risks
        if code_analysis and code_analysis['risk_level'] in ['medium', 'high']:
            risk_factors.append({
                'type': 'code_pattern',
                'severity': code_analysis['risk_level'],
                'description': "Suspicious code patterns detected",
                'patterns': code_analysis['suspicious_patterns']
            })
        
        return risk_factors
    
    def _combine_metadata(self, metadata: Dict) -> str:
        """Combine metadata fields into a single string"""
        combined = []
        for key, value in metadata.items():
            if isinstance(value, (list, set)):
                value = ' '.join(str(v) for v in value)
            elif isinstance(value, dict):
                value = self._combine_metadata(value)
            combined.append(f"{key}: {value}")
        return ' '.join(combined)

class VulnerabilityCorrelation:
    """
    Analyzes correlations between vulnerabilities and identifies patterns.
    """
    
    def __init__(self):
        self.config = get_config()
        self.cache = Cache()
        
        # Initialize clustering model
        self.clustering = DBSCAN(
            eps=0.3,
            min_samples=2,
            metric='cosine'
        )
        
        # Load vulnerability database
        self.vuln_db = self._load_vulnerability_database()
    
    def analyze_correlations(self, vulnerability_data: List[Dict]) -> Dict:
        """
        Analyze correlations between vulnerabilities.
        """
        try:
            # Generate embeddings
            embeddings = self._generate_vuln_embeddings(vulnerability_data)
            
            # Cluster vulnerabilities
            clusters = self._cluster_vulnerabilities(embeddings)
            
            # Analyze temporal patterns
            temporal = self._analyze_temporal_patterns(vulnerability_data)
            
            # Find attack pattern correlations
            attack_patterns = self._correlate_attack_patterns(vulnerability_data)
            
            # Analyze dependency relationships
            dependency_impact = self._analyze_dependency_impact(vulnerability_data)
            
            return {
                'clusters': clusters,
                'temporal_patterns': temporal,
                'attack_patterns': attack_patterns,
                'dependency_impact': dependency_impact,
                'risk_assessment': self._assess_overall_risk(
                    clusters,
                    temporal,
                    attack_patterns,
                    dependency_impact
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing correlations: {str(e)}")
            raise
    
    def _generate_vuln_embeddings(self, vulns: List[Dict]) -> np.ndarray:
        """Generate embeddings for vulnerabilities"""
        texts = [
            f"{v['description']} {v['attack_vector']} {v['impact']}"
            for v in vulns
        ]
        return self.text_model.encode(texts)
    
    def _cluster_vulnerabilities(self, embeddings: np.ndarray) -> List[Dict]:
        """Cluster similar vulnerabilities"""
        # Perform clustering
        labels = self.clustering.fit_predict(embeddings)
        
        clusters = defaultdict(list)
        for i, label in enumerate(labels):
            if label != -1:  # Not noise
                clusters[label].append(i)
        
        return [
            {
                'cluster_id': cid,
                'size': len(indices),
                'members': indices,
                'centroid': embeddings[indices].mean(axis=0)
            }
            for cid, indices in clusters.items()
        ]
    
    def _analyze_temporal_patterns(self, vulns: List[Dict]) -> Dict:
        """Analyze temporal patterns in vulnerabilities"""
        # Sort by date
        sorted_vulns = sorted(vulns, key=lambda x: x['published_date'])
        
        # Analyze frequency over time
        freq_by_month = defaultdict(int)
        for vuln in sorted_vulns:
            month = vuln['published_date'].strftime('%Y-%m')
            freq_by_month[month] += 1
        
        # Find temporal clusters
        temporal_clusters = self._find_temporal_clusters(sorted_vulns)
        
        return {
            'frequency_by_month': dict(freq_by_month),
            'temporal_clusters': temporal_clusters,
            'trend_analysis': self._analyze_trends(freq_by_month)
        }
    
    def _correlate_attack_patterns(self, vulns: List[Dict]) -> Dict:
        """Analyze correlations between attack patterns"""
        # Count pattern co-occurrences
        pattern_pairs = defaultdict(int)
        pattern_counts = defaultdict(int)
        
        for vuln in vulns:
            patterns = vuln.get('attack_patterns', [])
            for i, p1 in enumerate(patterns):
                pattern_counts[p1] += 1
                for p2 in patterns[i+1:]:
                    pair = tuple(sorted([p1, p2]))
                    pattern_pairs[pair] += 1
        
        # Calculate correlation scores
        correlations = {}
        for (p1, p2), count in pattern_pairs.items():
            score = count / min(pattern_counts[p1], pattern_counts[p2])
            correlations[(p1, p2)] = score
        
        return {
            'pattern_frequencies': dict(pattern_counts),
            'pattern_correlations': correlations,
            'common_sequences': self._find_pattern_sequences(vulns)
        }
    
    def _analyze_dependency_impact(self, vulns: List[Dict]) -> Dict:
        """Analyze vulnerability impact through dependencies"""
        # Build dependency graph
        G = nx.DiGraph()
        
        for vuln in vulns:
            component = vuln['component']
            G.add_node(
                component['name'],
                vulnerabilities=[vuln]
            )
            
            for dep in component.get('dependencies', []):
                G.add_edge(component['name'], dep['name'])
        
        # Analyze impact
        impact_scores = {}
        for node in G.nodes():
            # Calculate impact based on number of affected dependencies
            descendants = nx.descendants(G, node)
            impact_scores[node] = len(descendants)
        
        return {
            'impact_scores': impact_scores,
            'critical_components': self._identify_critical_components(G),
            'vulnerability_paths': self._find_vulnerability_paths(G)
        }
    
    def _assess_overall_risk(
        self,
        clusters: List[Dict],
        temporal: Dict,
        attack_patterns: Dict,
        dependency_impact: Dict
    ) -> Dict:
        """Assess overall risk based on all analyses"""
        # Calculate risk scores
        cluster_risk = self._calculate_cluster_risk(clusters)
        temporal_risk = self._calculate_temporal_risk(temporal)
        pattern_risk = self._calculate_pattern_risk(attack_patterns)
        impact_risk = self._calculate_impact_risk(dependency_impact)
        
        # Combine scores
        total_risk = (
            0.3 * cluster_risk +
            0.2 * temporal_risk +
            0.3 * pattern_risk +
            0.2 * impact_risk
        )
        
        return {
            'total_risk_score': total_risk,
            'risk_factors': {
                'cluster_risk': cluster_risk,
                'temporal_risk': temporal_risk,
                'pattern_risk': pattern_risk,
                'impact_risk': impact_risk
            },
            'risk_level': self._determine_risk_level(total_risk),
            'recommendations': self._generate_recommendations(
                clusters,
                temporal,
                attack_patterns,
                dependency_impact
            )
        }