"""
Verification script for SBOMAI capabilities.
Tests and demonstrates integration with various vulnerability sources and ML models.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Set
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.ensemble import RandomForestClassifier
import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv
import pandas as pd
from pprint import pprint

from src.sbomai_ai.feeds.vulnerability_sources import (
    NVDSource, OSVSource, GitHubAdvisoriesSource
)
from src.sbomai_ai.feeds.additional_sources import (
    CISAKEVSource, ExploitDBSource, MITRECVESource,
    RedHatSecuritySource, JFrogXraySource
)
from src.sbomai_ai.feeds.data_correlation import (
    VulnerabilityCorrelator,
    EnrichedVulnerability
)
from src.sbomai_ai.feeds.graph_analysis import (
    VulnerabilityGraphAnalyzer,
    NodeType,
    EdgeType
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CapabilityVerifier:
    """
    Verifies and demonstrates SBOMAI capabilities.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.sources = self._initialize_sources()
        self.correlator = VulnerabilityCorrelator()
        
        # ML Models
        self.clustering_model = None
        self.threat_predictor = None
        self.criticality_scorer = None
    
    def _initialize_sources(self) -> Dict:
        """Initialize all vulnerability data sources"""
        return {
            'nvd': NVDSource(self.config.get('nvd_api_key')),
            'osv': OSVSource(),
            'github': GitHubAdvisoriesSource(self.config.get('github_token')),
            'cisa': CISAKEVSource(),
            'exploitdb': ExploitDBSource(),
            'mitre': MITRECVESource(),
            'redhat': RedHatSecuritySource(),
            'jfrog': JFrogXraySource(
                self.config.get('jfrog_api_key'),
                self.config.get('jfrog_base_url')
            )
        }
    
    async def verify_data_sources(self):
        """Verify all data source integrations"""
        logger.info("Verifying data source integrations...")
        
        results = {}
        async with aiohttp.ClientSession() as session:
            for source_name, source in self.sources.items():
                try:
                    # Fetch last 7 days of vulnerabilities
                    since = datetime.now() - timedelta(days=7)
                    vulns = await source.fetch_vulnerabilities(session, since)
                    
                    results[source_name] = {
                        'status': 'success',
                        'count': len(vulns),
                        'sample': vulns[0] if vulns else None
                    }
                    logger.info(f"{source_name}: Successfully fetched {len(vulns)} vulnerabilities")
                
                except Exception as e:
                    results[source_name] = {
                        'status': 'error',
                        'error': str(e)
                    }
                    logger.error(f"Error fetching from {source_name}: {e}")
        
        return results

    class VulnerabilityClusteringModel(nn.Module):
        """
        Neural network for vulnerability clustering using learned embeddings.
        """
        def __init__(self, input_dim: int, hidden_dim: int, embedding_dim: int):
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, embedding_dim)
            )
            
            self.decoder = nn.Sequential(
                nn.Linear(embedding_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, input_dim)
            )
        
        def forward(self, x):
            embeddings = self.encoder(x)
            reconstructed = self.decoder(embeddings)
            return embeddings, reconstructed

    class ThreatPredictionModel(nn.Module):
        """
        GNN-based model for threat prediction.
        """
        def __init__(self, node_features: int, hidden_dim: int):
            super().__init__()
            self.conv1 = GCNConv(node_features, hidden_dim)
            self.conv2 = GCNConv(hidden_dim, hidden_dim)
            self.predictor = nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(),
                nn.Linear(hidden_dim // 2, 1),
                nn.Sigmoid()
            )
        
        def forward(self, x, edge_index):
            h = self.conv1(x, edge_index)
            h = torch.relu(h)
            h = self.conv2(h, edge_index)
            return self.predictor(h)

    def train_clustering_model(self, vulnerabilities: List[Dict]):
        """
        Train vulnerability clustering model using:
        - CVSS metrics
        - Description embeddings
        - Exploit characteristics
        - Temporal patterns
        """
        logger.info("Training vulnerability clustering model...")
        
        # Prepare features
        features = []
        for vuln in vulnerabilities:
            feature_vector = [
                vuln.get('cvss_score', 0.0) / 10.0,  # Normalize CVSS
                
                # Exploit status
                {
                    'NONE': 0.0,
                    'UNPROVEN': 0.25,
                    'PROOF_OF_CONCEPT': 0.5,
                    'ACTIVELY_EXPLOITED': 0.75,
                    'WEAPONIZED': 1.0
                }.get(vuln.get('exploit_status', 'NONE'), 0.0),
                
                # Temporal score
                vuln.get('temporal_score', 0.0) / 10.0,
                
                # Threat metrics
                len(vuln.get('threat_actors', [])) / 10.0,  # Normalize
                len(vuln.get('malware_families', [])) / 5.0,
                1.0 if vuln.get('known_ransomware') else 0.0,
                
                # Patch status
                1.0 if vuln.get('fixed_version') else 0.0
            ]
            features.append(feature_vector)
        
        if not features:
            logger.warning("No features available for clustering")
            return
        
        # Convert to tensor
        X = torch.tensor(features, dtype=torch.float32)
        
        # Create and train model
        self.clustering_model = self.VulnerabilityClusteringModel(
            input_dim=len(features[0]),
            hidden_dim=64,
            embedding_dim=32
        )
        
        # Training loop
        optimizer = torch.optim.Adam(self.clustering_model.parameters())
        criterion = nn.MSELoss()
        
        for epoch in range(100):
            optimizer.zero_grad()
            embeddings, reconstructed = self.clustering_model(X)
            loss = criterion(reconstructed, X)
            loss.backward()
            optimizer.step()
            
            if (epoch + 1) % 20 == 0:
                logger.info(f"Clustering model epoch {epoch+1}, Loss: {loss.item():.4f}")
        
        # Use embeddings for clustering
        embeddings = self.clustering_model.encoder(X).detach().numpy()
        clusters = DBSCAN(eps=0.3, min_samples=3).fit(embeddings)
        
        logger.info(f"Found {len(set(clusters.labels_))} vulnerability clusters")
        return clusters.labels_

    def train_threat_predictor(self, vulnerabilities: List[Dict], graph: nx.DiGraph):
        """
        Train threat prediction model using:
        - Historical patterns
        - Network structure
        - Temporal features
        """
        logger.info("Training threat prediction model...")
        
        # Prepare graph data
        node_features = []
        edge_index = []
        labels = []
        
        for idx, (node, attrs) in enumerate(graph.nodes(data=True)):
            if attrs.get('type') == NodeType.VULNERABILITY.value:
                vuln_data = attrs.get('data', {})
                
                # Create feature vector
                feature_vector = [
                    vuln_data.get('cvss_score', 0.0) / 10.0,
                    vuln_data.get('temporal_score', 0.0) / 10.0,
                    len(vuln_data.get('threat_actors', [])) / 10.0,
                    1.0 if vuln_data.get('known_exploited') else 0.0,
                    1.0 if vuln_data.get('exploit_available') else 0.0
                ]
                node_features.append(feature_vector)
                
                # Create label (1 if exploited within 30 days of disclosure)
                published = vuln_data.get('published_date')
                first_exploit = vuln_data.get('first_exploit_date')
                if published and first_exploit:
                    exploit_time = (first_exploit - published).days
                    labels.append(1.0 if exploit_time <= 30 else 0.0)
                else:
                    labels.append(0.0)
        
        # Convert to tensors
        X = torch.tensor(node_features, dtype=torch.float32)
        y = torch.tensor(labels, dtype=torch.float32)
        edge_index = torch.tensor(edge_index, dtype=torch.long)
        
        # Create and train model
        self.threat_predictor = self.ThreatPredictionModel(
            node_features=len(node_features[0]),
            hidden_dim=64
        )
        
        # Training loop
        optimizer = torch.optim.Adam(self.threat_predictor.parameters())
        criterion = nn.BCELoss()
        
        for epoch in range(100):
            optimizer.zero_grad()
            pred = self.threat_predictor(X, edge_index)
            loss = criterion(pred.squeeze(), y)
            loss.backward()
            optimizer.step()
            
            if (epoch + 1) % 20 == 0:
                logger.info(f"Threat predictor epoch {epoch+1}, Loss: {loss.item():.4f}")

    def train_criticality_scorer(self, vulnerabilities: List[Dict]):
        """
        Train criticality scoring model using:
        - CVSS metrics
        - Exploit status
        - Threat intelligence
        - Temporal patterns
        """
        logger.info("Training criticality scoring model...")
        
        # Prepare features and labels
        features = []
        labels = []
        
        for vuln in vulnerabilities:
            # Create feature vector
            feature_vector = [
                vuln.get('cvss_score', 0.0) / 10.0,
                
                # Exploit characteristics
                {
                    'NONE': 0.0,
                    'UNPROVEN': 0.25,
                    'PROOF_OF_CONCEPT': 0.5,
                    'ACTIVELY_EXPLOITED': 0.75,
                    'WEAPONIZED': 1.0
                }.get(vuln.get('exploit_status', 'NONE'), 0.0),
                
                # Threat intelligence
                len(vuln.get('threat_actors', [])) / 10.0,
                len(vuln.get('malware_families', [])) / 5.0,
                1.0 if vuln.get('known_ransomware') else 0.0,
                
                # Temporal factors
                vuln.get('temporal_score', 0.0) / 10.0,
                1.0 if vuln.get('patch_available') else 0.0,
                
                # Attack complexity
                {
                    'LOW': 1.0,
                    'MEDIUM': 0.5,
                    'HIGH': 0.25
                }.get(vuln.get('attack_complexity', 'HIGH'), 0.0)
            ]
            features.append(feature_vector)
            
            # Create label (actual criticality score)
            labels.append(vuln.get('criticality_score', 0.0) / 10.0)
        
        if not features:
            logger.warning("No features available for criticality scoring")
            return
        
        # Train Random Forest model
        X = np.array(features)
        y = np.array(labels)
        
        self.criticality_scorer = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.criticality_scorer.fit(X, y)
        logger.info("Criticality scoring model trained successfully")
    
    def verify_ml_capabilities(self, vulnerabilities: List[Dict], graph: nx.DiGraph):
        """Verify all ML model capabilities"""
        results = {}
        
        # 1. Vulnerability Clustering
        try:
            cluster_labels = self.train_clustering_model(vulnerabilities)
            results['clustering'] = {
                'status': 'success',
                'num_clusters': len(set(cluster_labels)),
                'sample_distribution': pd.Series(cluster_labels).value_counts().to_dict()
            }
        except Exception as e:
            results['clustering'] = {'status': 'error', 'error': str(e)}
        
        # 2. Threat Prediction
        try:
            self.train_threat_predictor(vulnerabilities, graph)
            # Test prediction
            sample_pred = self.threat_predictor(
                torch.randn(5, 5),  # Sample features
                torch.tensor([[0, 1], [1, 2]], dtype=torch.long)  # Sample edges
            )
            results['threat_prediction'] = {
                'status': 'success',
                'sample_predictions': sample_pred.detach().numpy().tolist()
            }
        except Exception as e:
            results['threat_prediction'] = {'status': 'error', 'error': str(e)}
        
        # 3. Criticality Scoring
        try:
            self.train_criticality_scorer(vulnerabilities)
            # Test scoring
            sample_score = self.criticality_scorer.predict(
                np.random.rand(5, 8)  # Sample features
            )
            results['criticality_scoring'] = {
                'status': 'success',
                'sample_scores': sample_score.tolist()
            }
        except Exception as e:
            results['criticality_scoring'] = {'status': 'error', 'error': str(e)}
        
        return results

async def main():
    """Run capability verification"""
    config = {
        'nvd_api_key': os.getenv('NVD_API_KEY'),
        'github_token': os.getenv('GITHUB_TOKEN'),
        'jfrog_api_key': os.getenv('JFROG_API_KEY'),
        'jfrog_base_url': os.getenv('JFROG_URL')
    }
    
    verifier = CapabilityVerifier(config)
    
    # 1. Verify data sources
    logger.info("\nVerifying data sources...")
    source_results = await verifier.verify_data_sources()
    print("\nData Source Results:")
    pprint(source_results)
    
    # 2. Verify ML capabilities
    logger.info("\nVerifying ML capabilities...")
    # Get sample data
    vulnerabilities = []
    graph = nx.DiGraph()
    
    for source_name, result in source_results.items():
        if result['status'] == 'success' and result['sample']:
            vulnerabilities.append(result['sample'])
    
    ml_results = verifier.verify_ml_capabilities(vulnerabilities, graph)
    print("\nML Capability Results:")
    pprint(ml_results)

if __name__ == "__main__":
    asyncio.run(main())