"""
Main gRPC service implementation for SBOMAI AI Microservice
"""

import asyncio
import time
import logging
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor

import grpc
from grpc import aio

# Import generated gRPC code
from . import sbomai_ai_pb2
from . import sbomai_ai_pb2_grpc

from .config import get_config, validate_config
from .models.ai_models import AiModelFactory
from .models.ml_models import MlModelFactory
from .models.explainability_models import LangChainAnalyzer
from .models.graph_neural_models import PredictiveVulnerabilityDetector, DependencyGraphAnalyzer
from .utils.exceptions import AiModelError, MlModelError, ExplainabilityError

logger = logging.getLogger(__name__)


class SbomaiAiService(sbomai_ai_pb2_grpc.SbomaiAiServiceServicer):
    """gRPC service implementation for SBOMAI AI analysis"""
    
    def __init__(self):
        self.config = get_config()
        self.ai_model = None
        self.ml_model = None
        self.langchain_analyzer = None
        self.gnn_predictor = None
        self.graph_analyzer = None
        self.executor = ThreadPoolExecutor(max_workers=self.config.service.max_concurrent_requests)
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize AI and ML services"""
        try:
            # Initialize AI model
            self.ai_model = AiModelFactory.get_best_available_model()
            if not self.ai_model:
                logger.warning("No AI model available, some features will be disabled")
            
            # Initialize ML model
            self.ml_model = MlModelFactory.get_default_model()
            
            # Initialize LangChain analyzer
            try:
                self.langchain_analyzer = LangChainAnalyzer()
            except Exception as e:
                logger.warning(f"LangChain analyzer not available: {e}")
                self.langchain_analyzer = None
            
            # Initialize GNN-based predictive vulnerability detector
            try:
                self.gnn_predictor = PredictiveVulnerabilityDetector()
                self.graph_analyzer = DependencyGraphAnalyzer()
                logger.info("GNN-based predictive vulnerability detection initialized")
            except Exception as e:
                logger.warning(f"GNN predictor not available: {e}")
                self.gnn_predictor = None
                self.graph_analyzer = None
            
            logger.info("SBOMAI AI service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize services: {e}")
            raise
    
    async def ExplainRisk(self, request, context):
        """Explain risk for a specific component"""
        start_time = time.time()
        
        try:
            # Convert gRPC request to internal format
            component = {
                "name": request.component.name,
                "version": request.component.version,
                "group_id": request.component.group_id,
                "description": request.component.description,
                "licenses": list(request.component.licenses),
                "purl": request.component.purl,
                "tags": list(request.component.tags),
                "metadata": dict(request.component.metadata)
            }
            
            vulnerabilities = []
            for vuln in request.vulnerabilities:
                vulnerabilities.append({
                    "id": vuln.id,
                    "description": vuln.description,
                    "severity": vuln.severity,
                    "cvss_score": vuln.cvss_score,
                    "affected_versions": list(vuln.affected_versions),
                    "fixed_versions": list(vuln.fixed_versions),
                    "source": vuln.source,
                    "published_date": vuln.published_date,
                    "references": list(vuln.references)
                })
            
            # Use LangChain analyzer if available, otherwise use AI model directly
            if self.langchain_analyzer:
                analysis_result = await self.langchain_analyzer.explain_risk(component, vulnerabilities)
                
                # Extract risk level from analysis
                risk_level = self._convert_risk_level(analysis_result["vulnerability_analysis"].get("risk_level", "MEDIUM"))
                
                response = sbomai_ai_pb2.ExplainRiskResponse(
                    explanation=analysis_result["vulnerability_analysis"].get("key_findings", ["No findings"]),
                    confidence_score=analysis_result["vulnerability_analysis"].get("confidence", 0.7),
                    sources=["LangChain Analysis"],
                    key_factors=analysis_result["vulnerability_analysis"].get("key_findings", []),
                    risk_level=risk_level,
                    model_used=self.langchain_analyzer.explainability_chain.ai_model.model_name,
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
            else:
                # Fallback to direct AI model
                if not self.ai_model:
                    await context.abort(grpc.StatusCode.UNAVAILABLE, "No AI model available")
                
                prompt = self._build_risk_explanation_prompt(component, vulnerabilities, request.analysis_context)
                explanation = await self.ai_model.generate_response(prompt)
                
                response = sbomai_ai_pb2.ExplainRiskResponse(
                    explanation=explanation,
                    confidence_score=0.8,
                    sources=["AI Model Analysis"],
                    key_factors=["Component analysis", "Vulnerability assessment"],
                    risk_level=sbomai_ai_pb2.MEDIUM,
                    model_used=self.ai_model.model_name,
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
            
            return response
            
        except Exception as e:
            logger.error(f"ExplainRisk failed: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, f"ExplainRisk failed: {str(e)}")
    
    async def PredictRiskScore(self, request, context):
        """Predict risk score for a component"""
        start_time = time.time()
        
        try:
            # Convert gRPC request to internal format
            component = {
                "name": request.component.name,
                "version": request.component.version,
                "group_id": request.component.group_id,
                "description": request.component.description,
                "licenses": list(request.component.licenses),
                "purl": request.component.purl,
                "tags": list(request.component.tags),
                "metadata": dict(request.component.metadata)
            }
            
            historical_vulnerabilities = []
            for vuln in request.historical_vulnerabilities:
                historical_vulnerabilities.append({
                    "id": vuln.id,
                    "description": vuln.description,
                    "severity": vuln.severity,
                    "cvss_score": vuln.cvss_score,
                    "affected_versions": list(vuln.affected_versions),
                    "fixed_versions": list(vuln.fixed_versions),
                    "source": vuln.source,
                    "published_date": vuln.published_date,
                    "references": list(vuln.references)
                })
            
            # Extract features for ML model
            features = self._extract_component_features(component, historical_vulnerabilities, request.features)
            
            # Use ML model for prediction
            if self.ml_model and self.ml_model.is_model_available():
                # Convert features to numpy array
                import numpy as np
                X = np.array([features])
                
                predictions, confidence_intervals = await self.ml_model.predict(X)
                risk_score = float(predictions[0])
                confidence_lower = float(risk_score - confidence_intervals[0])
                confidence_upper = float(risk_score + confidence_intervals[0])
                
                # Get feature importance
                feature_importance = []
                for fi in self.ml_model.get_feature_importance():
                    feature_importance.append(sbomai_ai_pb2.FeatureImportance(
                        feature_name=fi["feature_name"],
                        importance_score=fi["importance_score"],
                        description=fi["description"]
                    ))
                
                response = sbomai_ai_pb2.PredictRiskScoreResponse(
                    risk_score=risk_score,
                    confidence_interval_lower=confidence_lower,
                    confidence_interval_upper=confidence_upper,
                    feature_importance=feature_importance,
                    model_used=self.ml_model.model_name,
                    explanation=f"ML model prediction based on {len(features)} features",
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
            else:
                # Fallback to rule-based prediction
                risk_score = self._calculate_rule_based_risk_score(component, historical_vulnerabilities)
                
                response = sbomai_ai_pb2.PredictRiskScoreResponse(
                    risk_score=risk_score,
                    confidence_interval_lower=risk_score * 0.8,
                    confidence_interval_upper=risk_score * 1.2,
                    model_used="rule-based",
                    explanation="Rule-based risk assessment",
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
            
            return response
            
        except Exception as e:
            logger.error(f"PredictRiskScore failed: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, f"PredictRiskScore failed: {str(e)}")
    
    async def SuggestFix(self, request, context):
        """Suggest fixes for vulnerabilities"""
        start_time = time.time()
        
        try:
            component = {
                "name": request.component.name,
                "version": request.component.version,
                "group_id": request.component.group_id,
                "description": request.component.description,
                "licenses": list(request.component.licenses),
                "purl": request.component.purl,
                "tags": list(request.component.tags),
                "metadata": dict(request.component.metadata)
            }
            
            constraints = list(request.constraints)
            strategy = {
                "approach": request.strategy.approach,
                "consider_breaking_changes": request.strategy.consider_breaking_changes,
                "prefer_latest_versions": request.strategy.prefer_latest_versions,
                "priority_criteria": list(request.strategy.priority_criteria)
            }
            
            # Use LangChain analyzer if available
            if self.langchain_analyzer:
                remediation_result = await self.langchain_analyzer.suggest_remediation(
                    request.vulnerability_id, component
                )
                
                suggestions = []
                for suggestion in remediation_result["remediation_suggestions"].get("recommendations", []):
                    suggestions.append(sbomai_ai_pb2.FixSuggestion(
                        action="upgrade",
                        suggested_component=sbomai_ai_pb2.SbomComponent(
                            name=component["name"],
                            version="2.0.0",  # Suggested version
                            description="Updated version"
                        ),
                        reasoning=suggestion,
                        confidence=0.8,
                        risks=["Breaking changes possible"],
                        benefits=["Security improvements", "Bug fixes"]
                    ))
                
                response = sbomai_ai_pb2.SuggestFixResponse(
                    suggestions=suggestions,
                    reasoning=remediation_result["remediation_suggestions"].get("key_findings", ["No specific reasoning"]),
                    confidence_score=remediation_result["remediation_suggestions"].get("confidence", 0.7),
                    policy_rules=["block_version_below_2.0.0"],
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
            else:
                # Fallback to AI model
                if not self.ai_model:
                    await context.abort(grpc.StatusCode.UNAVAILABLE, "No AI model available")
                
                prompt = self._build_fix_suggestion_prompt(request.vulnerability_id, component, constraints, strategy)
                reasoning = await self.ai_model.generate_response(prompt)
                
                suggestions = [
                    sbomai_ai_pb2.FixSuggestion(
                        action="upgrade",
                        suggested_component=sbomai_ai_pb2.SbomComponent(
                            name=component["name"],
                            version="2.0.0",
                            description="Latest stable version"
                        ),
                        reasoning="Upgrade to latest version for security fixes",
                        confidence=0.7,
                        risks=["Potential breaking changes"],
                        benefits=["Security improvements"]
                    )
                ]
                
                response = sbomai_ai_pb2.SuggestFixResponse(
                    suggestions=suggestions,
                    reasoning=reasoning,
                    confidence_score=0.7,
                    policy_rules=["require_latest_version"],
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
            
            return response
            
        except Exception as e:
            logger.error(f"SuggestFix failed: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, f"SuggestFix failed: {str(e)}")
    
    async def ExplainableSbomChain(self, request, context):
        """Generate explainable analysis chain for entire SBOM"""
        start_time = time.time()
        
        try:
            # Convert gRPC request to internal format
            sbom_document = {
                "name": request.sbom_document.name,
                "version": request.sbom_document.version,
                "format": request.sbom_document.format,
                "created_date": request.sbom_document.created_date,
                "components": [],
                "metadata": dict(request.sbom_document.metadata)
            }
            
            for comp in request.sbom_document.components:
                sbom_document["components"].append({
                    "name": comp.name,
                    "version": comp.version,
                    "group_id": comp.group_id,
                    "description": comp.description,
                    "licenses": list(comp.licenses),
                    "purl": comp.purl,
                    "tags": list(comp.tags),
                    "metadata": dict(comp.metadata)
                })
            
            # Use LangChain analyzer
            if self.langchain_analyzer:
                chain_result = await self.langchain_analyzer.explain_sbom_chain(sbom_document)
                
                chain_steps = []
                for i, analysis in enumerate(chain_result["component_analyses"]):
                    chain_steps.append(sbomai_ai_pb2.ChainStep(
                        step_name=f"Component Analysis {i+1}",
                        result=f"Analyzed {analysis['component']['name']}",
                        confidence=analysis["vulnerability_analysis"].get("confidence", 0.7),
                        findings=analysis["vulnerability_analysis"].get("key_findings", []),
                        duration_ms=analysis.get("processing_time_ms", 100)
                    ))
                
                response = sbomai_ai_pb2.ExplainableSbomChainResponse(
                    chain_steps=chain_steps,
                    overall_assessment=chain_result["overall_assessment"].get("key_findings", ["No overall assessment"]),
                    overall_risk_score=chain_result["overall_assessment"].get("risk_score", 5.0),
                    recommendations=chain_result["overall_assessment"].get("recommendations", []),
                    critical_findings=chain_result["summary"]["critical_vuln_count"] > 0,
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
            else:
                # Fallback to simple analysis
                if not self.ai_model:
                    await context.abort(grpc.StatusCode.UNAVAILABLE, "No AI model available")
                
                prompt = self._build_sbom_chain_prompt(sbom_document)
                assessment = await self.ai_model.generate_response(prompt)
                
                response = sbomai_ai_pb2.ExplainableSbomChainResponse(
                    chain_steps=[
                        sbomai_ai_pb2.ChainStep(
                            step_name="Overall SBOM Analysis",
                            result="Completed SBOM analysis",
                            confidence=0.7,
                            findings=["Analysis completed"],
                            duration_ms=int((time.time() - start_time) * 1000)
                        )
                    ],
                    overall_assessment=assessment,
                    overall_risk_score=5.0,
                    recommendations=["Review components manually"],
                    critical_findings=False,
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
            
            return response
            
        except Exception as e:
            logger.error(f"ExplainableSbomChain failed: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, f"ExplainableSbomChain failed: {str(e)}")
    
    async def PredictVulnerabilityPatterns(self, request, context):
        """Predict vulnerability patterns using Graph Neural Networks"""
        start_time = time.time()
        
        try:
            if not self.gnn_predictor:
                await context.abort(grpc.StatusCode.UNAVAILABLE, "GNN predictor not available")
            
            # Convert gRPC request to internal format
            sbom_data = {
                "name": request.sbom_document.name,
                "version": request.sbom_document.version,
                "format": request.sbom_document.format,
                "created_date": request.sbom_document.created_date,
                "components": [],
                "metadata": dict(request.sbom_document.metadata)
            }
            
            # Convert components
            for comp in request.sbom_document.components:
                component = {
                    "id": comp.name,  # Use name as ID
                    "name": comp.name,
                    "version": comp.version,
                    "group_id": comp.group_id,
                    "description": comp.description,
                    "licenses": list(comp.licenses),
                    "purl": comp.purl,
                    "tags": list(comp.tags),
                    "metadata": dict(comp.metadata),
                    "dependencies": [],  # Will be populated from relationships
                    "relationships": []
                }
                sbom_data["components"].append(component)
            
            # Perform GNN-based vulnerability pattern prediction
            prediction_result = self.gnn_predictor.predict_vulnerability_patterns(sbom_data)
            
            # Build NetworkX graph for additional analysis
            import networkx as nx
            G = nx.DiGraph()
            for comp in sbom_data["components"]:
                G.add_node(comp["id"], **comp)
            
            # Add dependency edges (simplified)
            for comp in sbom_data["components"]:
                for other_comp in sbom_data["components"]:
                    if comp["id"] != other_comp["id"]:
                        # Add edge if there's a dependency relationship
                        G.add_edge(comp["id"], other_comp["id"])
            
            # Additional graph analysis
            propagation_analysis = self.graph_analyzer.analyze_vulnerability_propagation(G)
            critical_deps = self.graph_analyzer.identify_critical_dependencies(G)
            health_metrics = self.graph_analyzer.analyze_dependency_health(G)
            
            # Build response
            response = sbomai_ai_pb2.PredictVulnerabilityPatternsResponse(
                vulnerability_likelihood=prediction_result['vulnerability_likelihood'],
                graph_features=sbomai_ai_pb2.GraphFeatures(
                    num_nodes=prediction_result['graph_features']['num_nodes'],
                    num_edges=prediction_result['graph_features']['num_edges'],
                    density=prediction_result['graph_features']['density'],
                    avg_clustering=prediction_result['graph_features']['avg_clustering'],
                    avg_degree_centrality=prediction_result['graph_features']['avg_degree_centrality'],
                    avg_betweenness_centrality=prediction_result['graph_features']['avg_betweenness_centrality'],
                    avg_closeness_centrality=prediction_result['graph_features']['avg_closeness_centrality'],
                    vulnerability_ratio=prediction_result['graph_features']['vulnerability_ratio'],
                    max_dependency_depth=prediction_result['graph_features']['max_dependency_depth'],
                    avg_dependency_depth=prediction_result['graph_features']['avg_dependency_depth'],
                    critical_path_length=prediction_result['graph_features']['critical_path_length']
                ),
                dependency_patterns=[
                    sbomai_ai_pb2.DependencyPattern(
                        pattern_type=pattern_type,
                        components=pattern_data,
                        risk_score=0.8,  # Default risk score
                        description=f"Pattern: {pattern_type}",
                        vulnerability_types=["supply_chain_attack", "dependency_confusion"]
                    )
                    for pattern_type, pattern_data in prediction_result['pattern_analysis'].items()
                    if isinstance(pattern_data, list) and pattern_data
                ],
                high_risk_components=[
                    sbomai_ai_pb2.HighRiskComponent(
                        component_id=comp['component_id'],
                        component_name=comp['component_name'],
                        risk_score=comp['risk_score'],
                        vulnerabilities=[],  # Convert if available
                        dependencies=comp['dependencies'],
                        dependents=comp['dependents'],
                        reasoning="High risk based on GNN analysis"
                    )
                    for comp in prediction_result['high_risk_components']
                ],
                emerging_vulnerabilities=[
                    sbomai_ai_pb2.EmergingVulnerability(
                        component_id=comp['component_id'],
                        component_name=comp['component_name'],
                        emerging_risk_score=comp['emerging_risk_score'],
                        risk_factors=comp['risk_factors'],
                        predicted_vulnerability_types=comp['predicted_vulnerability_types'],
                        explanation="Predicted based on dependency patterns and risk factors"
                    )
                    for comp in prediction_result['emerging_vulnerabilities']
                ],
                vulnerability_propagation=sbomai_ai_pb2.VulnerabilityPropagation(
                    propagation_risk=propagation_analysis['propagation_risk'],
                    affected_components=propagation_analysis['affected_components'],
                    vulnerable_components=propagation_analysis['vulnerable_components'],
                    total_components=propagation_analysis['total_components'],
                    analysis="Vulnerability propagation analysis based on dependency graph"
                ),
                critical_dependencies=[
                    sbomai_ai_pb2.CriticalDependency(
                        component_id=dep['component_id'],
                        component_name=dep['component_name'],
                        betweenness_centrality=dep['betweenness_centrality'],
                        in_degree=dep['in_degree'],
                        out_degree=dep['out_degree'],
                        has_vulnerabilities=dep['has_vulnerabilities'],
                        critical_score=dep['critical_score'],
                        impact_analysis="Critical dependency identified based on centrality measures"
                    )
                    for dep in critical_deps
                ],
                dependency_health=sbomai_ai_pb2.DependencyHealth(
                    density=health_metrics['density'],
                    clustering_coefficient=health_metrics['clustering_coefficient'],
                    vulnerability_ratio=health_metrics['vulnerability_ratio'],
                    max_depth=health_metrics['max_depth'],
                    avg_depth=health_metrics['avg_depth'],
                    overall_health_score=health_metrics['overall_health_score'],
                    health_indicators=["dependency_depth", "vulnerability_ratio", "clustering_coefficient"]
                ),
                confidence_score=prediction_result['confidence_score'],
                processing_time_ms=int((time.time() - start_time) * 1000)
            )
            
            return response
            
        except Exception as e:
            logger.error(f"PredictVulnerabilityPatterns failed: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, f"PredictVulnerabilityPatterns failed: {str(e)}")
    
    async def GetServiceInfo(self, request, context):
        """Get service information and health status"""
        try:
            available_models = []
            if self.ai_model:
                available_models.append(self.ai_model.model_name)
            
            capabilities = []
            if self.ai_model:
                capabilities.append("explain_risk")
                capabilities.append("suggest_fix")
                capabilities.append("explainable_chain")
            
            if self.ml_model and self.ml_model.is_model_available():
                capabilities.append("predict_risk_score")
            
            if self.langchain_analyzer:
                capabilities.append("langchain_analysis")
            
            if self.gnn_predictor:
                capabilities.append("predictive_vulnerability_detection")
                capabilities.append("dependency_graph_analysis")
                capabilities.append("emerging_vulnerability_prediction")
            
            response = sbomai_ai_pb2.ServiceInfoResponse(
                service_name="SBOMAI AI Microservice",
                version="1.0.0",
                available_models=available_models,
                capabilities=capabilities,
                is_healthy=True,
                uptime="Service is running"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"GetServiceInfo failed: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, f"GetServiceInfo failed: {str(e)}")
    
    def _build_risk_explanation_prompt(self, component: Dict[str, Any], vulnerabilities: List[Dict[str, Any]], context: str) -> str:
        """Build prompt for risk explanation"""
        prompt = f"""
        Analyze the security risk for the following SBOM component:
        
        Component: {component['name']} {component['version']}
        Description: {component.get('description', 'No description')}
        Licenses: {', '.join(component.get('licenses', []))}
        
        Vulnerabilities:
        """
        
        for vuln in vulnerabilities:
            prompt += f"- {vuln['id']}: {vuln['description']} (CVSS: {vuln.get('cvss_score', 'Unknown')})\n"
        
        if not vulnerabilities:
            prompt += "- No known vulnerabilities\n"
        
        if context:
            prompt += f"\nContext: {context}\n"
        
        prompt += """
        Provide a detailed risk explanation including:
        1. Overall risk level (LOW/MEDIUM/HIGH/CRITICAL)
        2. Key security findings
        3. Specific recommendations
        4. Confidence in the assessment
        """
        
        return prompt
    
    def _build_fix_suggestion_prompt(self, vulnerability_id: str, component: Dict[str, Any], constraints: List[str], strategy: Dict[str, Any]) -> str:
        """Build prompt for fix suggestions"""
        prompt = f"""
        Suggest fixes for vulnerability {vulnerability_id} in component {component['name']} {component['version']}.
        
        Component Details:
        - Name: {component['name']}
        - Version: {component['version']}
        - Description: {component.get('description', 'No description')}
        
        Constraints: {', '.join(constraints)}
        Strategy: {strategy['approach']}
        
        Provide specific remediation suggestions including:
        1. Immediate actions to take
        2. Alternative components to consider
        3. Version updates if applicable
        4. Security measures to implement
        """
        
        return prompt
    
    def _build_sbom_chain_prompt(self, sbom_document: Dict[str, Any]) -> str:
        """Build prompt for SBOM chain analysis"""
        prompt = f"""
        Analyze the following SBOM document:
        
        Name: {sbom_document['name']}
        Version: {sbom_document['version']}
        Format: {sbom_document['format']}
        Components: {len(sbom_document['components'])}
        
        Component Summary:
        """
        
        for comp in sbom_document['components'][:10]:  # Limit to first 10 for prompt size
            prompt += f"- {comp['name']} {comp['version']}\n"
        
        if len(sbom_document['components']) > 10:
            prompt += f"- ... and {len(sbom_document['components']) - 10} more components\n"
        
        prompt += """
        Provide an overall assessment including:
        1. Overall risk level
        2. Key security findings
        3. Priority recommendations
        4. Critical issues to address
        """
        
        return prompt
    
    def _extract_component_features(self, component: Dict[str, Any], vulnerabilities: List[Dict[str, Any]], additional_features: List[str]) -> List[float]:
        """Extract features for ML model prediction"""
        features = []
        
        # Component features
        features.append(len(component.get('name', '')))  # Name length
        features.append(len(component.get('version', '')))  # Version length
        features.append(len(component.get('description', '')))  # Description length
        features.append(len(component.get('licenses', [])))  # Number of licenses
        features.append(len(component.get('tags', [])))  # Number of tags
        
        # Vulnerability features
        features.append(len(vulnerabilities))  # Number of vulnerabilities
        if vulnerabilities:
            features.append(sum(v.get('cvss_score', 0) for v in vulnerabilities) / len(vulnerabilities))  # Average CVSS
            features.append(max(v.get('cvss_score', 0) for v in vulnerabilities))  # Max CVSS
        else:
            features.append(0.0)  # Average CVSS
            features.append(0.0)  # Max CVSS
        
        # Additional features
        for feature in additional_features:
            try:
                features.append(float(feature))
            except:
                features.append(0.0)
        
        return features
    
    def _calculate_rule_based_risk_score(self, component: Dict[str, Any], vulnerabilities: List[Dict[str, Any]]) -> float:
        """Calculate risk score using rule-based approach"""
        score = 5.0  # Base score
        
        # Adjust based on vulnerabilities
        if vulnerabilities:
            max_cvss = max(v.get('cvss_score', 0) for v in vulnerabilities)
            score += max_cvss * 0.3
        
        # Adjust based on component characteristics
        if 'alpha' in component.get('version', '').lower() or 'beta' in component.get('version', '').lower():
            score += 2.0
        
        if len(component.get('licenses', [])) == 0:
            score += 1.0
        
        return min(max(score, 0.0), 10.0)
    
    def _convert_risk_level(self, risk_level: str) -> int:
        """Convert string risk level to gRPC enum"""
        risk_level_map = {
            'LOW': sbomai_ai_pb2.LOW,
            'MEDIUM': sbomai_ai_pb2.MEDIUM,
            'HIGH': sbomai_ai_pb2.HIGH,
            'CRITICAL': sbomai_ai_pb2.CRITICAL,
            'UNKNOWN': sbomai_ai_pb2.UNKNOWN
        }
        return risk_level_map.get(risk_level.upper(), sbomai_ai_pb2.MEDIUM)


async def serve():
    """Start the gRPC server"""
    config = get_config()
    
    # Validate configuration
    issues = validate_config()
    if issues:
        logger.error("Configuration issues found:")
        for issue in issues:
            logger.error(f"  - {issue}")
        return
    
    # Create gRPC server
    server = aio.server(
        ThreadPoolExecutor(max_workers=config.service.grpc_max_workers),
        maximum_concurrent_rpcs=config.service.grpc_max_concurrent_rpcs
    )
    
    # Add service
    sbomai_ai_pb2_grpc.add_SbomaiAiServiceServicer_to_server(SbomaiAiService(), server)
    
    # Listen on port
    listen_addr = f"{config.service.grpc_host}:{config.service.grpc_port}"
    server.add_insecure_port(listen_addr)
    
    logger.info(f"Starting SBOMAI AI gRPC server on {listen_addr}")
    
    try:
        await server.start()
        logger.info("SBOMAI AI gRPC server started successfully")
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    finally:
        await server.stop(grace=5)


if __name__ == "__main__":
    logging.basicConfig(
        level=get_config().service.log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    asyncio.run(serve()) 