"""
Tests for SBOMAI AI Microservice
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any

from src.sbomai_ai.service import SbomaiAiService
from src.sbomai_ai.utils.exceptions import AiModelError, MlModelError, ValidationError


class TestSbomaiAiService:
    """Test cases for SbomaiAiService"""
    
    @pytest.fixture
    async def service(self):
        """Create a service instance for testing"""
        service = SbomaiAiService()
        await service.initialize()
        yield service
        await service.cleanup()
    
    @pytest.fixture
    def sample_component(self) -> Dict[str, Any]:
        """Sample SBOM component for testing"""
        return {
            "name": "log4j-core",
            "version": "2.14.1",
            "group_id": "org.apache.logging.log4j",
            "licenses": ["Apache-2.0"],
            "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1"
        }
    
    @pytest.fixture
    def sample_vulnerability(self) -> Dict[str, Any]:
        """Sample vulnerability for testing"""
        return {
            "id": "CVE-2021-44228",
            "description": "Log4Shell vulnerability",
            "severity": "CRITICAL_SEVERITY",
            "cvss_score": 10.0,
            "published_date": "2021-12-10T00:00:00Z",
            "references": ["https://nvd.nist.gov/vuln/detail/CVE-2021-44228"]
        }
    
    @pytest.fixture
    def sample_sbom_document(self) -> Dict[str, Any]:
        """Sample SBOM document for testing"""
        return {
            "name": "test-application",
            "version": "1.0.0",
            "format": "CYCLONEDX",
            "created_date": "2024-01-15T10:00:00Z",
            "components": [
                {
                    "name": "log4j-core",
                    "version": "2.14.1",
                    "group_id": "org.apache.logging.log4j"
                },
                {
                    "name": "spring-boot-starter-web",
                    "version": "2.7.0",
                    "group_id": "org.springframework.boot"
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_initialize_service(self, service):
        """Test service initialization"""
        assert service.ai_models is not None
        assert service.ml_models is not None
        assert service.explainability_chain is not None
        assert service.cache_manager is not None
    
    @pytest.mark.asyncio
    async def test_explain_risk_success(self, service, sample_component, sample_vulnerability):
        """Test successful risk explanation"""
        request = {
            "component": sample_component,
            "vulnerabilities": [sample_vulnerability],
            "analysis_context": "Production web application"
        }
        
        with patch.object(service.ai_models, 'explain_risk', return_value={
            "explanation": "This component is critically risky due to Log4Shell",
            "confidence_score": 0.95,
            "sources": ["https://nvd.nist.gov/vuln/detail/CVE-2021-44228"],
            "key_factors": ["Remote code execution", "Widely exploited"],
            "risk_level": "CRITICAL"
        }):
            response = await service.ExplainRisk(request, Mock())
            
            assert response.explanation == "This component is critically risky due to Log4Shell"
            assert response.confidence_score == 0.95
            assert response.risk_level == "CRITICAL"
            assert len(response.sources) == 1
            assert len(response.key_factors) == 2
    
    @pytest.mark.asyncio
    async def test_explain_risk_validation_error(self, service):
        """Test risk explanation with invalid input"""
        request = {
            "component": {},  # Invalid component
            "vulnerabilities": []
        }
        
        with pytest.raises(ValidationError):
            await service.ExplainRisk(request, Mock())
    
    @pytest.mark.asyncio
    async def test_explain_risk_ai_error(self, service, sample_component, sample_vulnerability):
        """Test risk explanation when AI model fails"""
        request = {
            "component": sample_component,
            "vulnerabilities": [sample_vulnerability],
            "analysis_context": "Production web application"
        }
        
        with patch.object(service.ai_models, 'explain_risk', side_effect=AiModelError("AI service unavailable")):
            with pytest.raises(AiModelError):
                await service.ExplainRisk(request, Mock())
    
    @pytest.mark.asyncio
    async def test_predict_risk_score_success(self, service, sample_component):
        """Test successful risk score prediction"""
        request = {
            "component": sample_component,
            "historical_vulnerabilities": [],
            "features": ["web_framework", "popular"],
            "ml_config": {
                "model_type": "xgboost",
                "use_feature_importance": True
            }
        }
        
        with patch.object(service.ml_models, 'predict_risk_score', return_value={
            "risk_score": 75.5,
            "confidence_interval_lower": 68.2,
            "confidence_interval_upper": 82.8,
            "feature_importance": [
                {
                    "feature_name": "cvss_score",
                    "importance_score": 0.45,
                    "description": "Historical CVSS scores"
                }
            ],
            "model_used": "xgboost",
            "explanation": "High risk due to recent vulnerabilities"
        }):
            response = await service.PredictRiskScore(request, Mock())
            
            assert response.risk_score == 75.5
            assert response.confidence_interval_lower == 68.2
            assert response.confidence_interval_upper == 82.8
            assert response.model_used == "xgboost"
            assert len(response.feature_importance) == 1
    
    @pytest.mark.asyncio
    async def test_predict_risk_score_ml_error(self, service, sample_component):
        """Test risk prediction when ML model fails"""
        request = {
            "component": sample_component,
            "historical_vulnerabilities": [],
            "features": ["web_framework"]
        }
        
        with patch.object(service.ml_models, 'predict_risk_score', side_effect=MlModelError("Model not available")):
            with pytest.raises(MlModelError):
                await service.PredictRiskScore(request, Mock())
    
    @pytest.mark.asyncio
    async def test_suggest_fix_success(self, service, sample_component):
        """Test successful fix suggestion"""
        request = {
            "vulnerability_id": "CVE-2021-44228",
            "component": sample_component,
            "constraints": ["no_breaking_changes", "apache_license"],
            "strategy": {
                "approach": "conservative",
                "consider_breaking_changes": False
            }
        }
        
        with patch.object(service.ai_models, 'suggest_fix', return_value={
            "suggestions": [
                {
                    "action": "upgrade",
                    "suggested_component": {
                        "name": "log4j-core",
                        "version": "2.17.1"
                    },
                    "reasoning": "This version fixes the Log4Shell vulnerability",
                    "confidence": 0.98,
                    "risks": ["Minor API changes"],
                    "benefits": ["Security fix", "Performance improvements"]
                }
            ],
            "reasoning": "Upgrade to version 2.17.1 to fix the critical vulnerability",
            "confidence_score": 0.98,
            "policy_rules": ["Upgrade log4j-core to >=2.17.1"]
        }):
            response = await service.SuggestFix(request, Mock())
            
            assert len(response.suggestions) == 1
            assert response.suggestions[0].action == "upgrade"
            assert response.suggestions[0].suggested_component.version == "2.17.1"
            assert response.confidence_score == 0.98
            assert len(response.policy_rules) == 1
    
    @pytest.mark.asyncio
    async def test_explainable_sbom_chain_success(self, service, sample_sbom_document):
        """Test successful explainable SBOM chain"""
        request = {
            "sbom_document": sample_sbom_document,
            "chain_config": {
                "max_steps": 3,
                "confidence_threshold": 0.7,
                "include_detailed_explanations": True,
                "analysis_types": ["vulnerability", "license"]
            }
        }
        
        with patch.object(service.explainability_chain, 'analyze_sbom_chain', return_value={
            "chain_steps": [
                {
                    "step_name": "vulnerability_scan",
                    "result": "Found 1 critical vulnerability",
                    "confidence": 0.95,
                    "findings": ["CVE-2021-44228 in log4j-core 2.14.1"],
                    "duration_ms": 1200
                }
            ],
            "overall_assessment": "Critical security issues detected",
            "overall_risk_score": 85.0,
            "recommendations": [
                "Upgrade log4j-core to 2.17.1",
                "Implement security scanning in CI/CD"
            ],
            "critical_findings": [
                "Log4Shell vulnerability in production dependency"
            ]
        }):
            response = await service.ExplainableSbomChain(request, Mock())
            
            assert len(response.chain_steps) == 1
            assert response.chain_steps[0].step_name == "vulnerability_scan"
            assert response.overall_assessment == "Critical security issues detected"
            assert response.overall_risk_score == 85.0
            assert len(response.recommendations) == 2
            assert len(response.critical_findings) == 1
    
    @pytest.mark.asyncio
    async def test_get_service_info(self, service):
        """Test service info endpoint"""
        response = await service.GetServiceInfo({}, Mock())
        
        assert response.service_name == "SBOMAI AI Microservice"
        assert response.version == "1.0.0"
        assert response.status == "HEALTHY"
        assert len(response.capabilities) > 0
        assert response.grpc_port == 50051
        assert response.metrics_port == 9090
    
    @pytest.mark.asyncio
    async def test_cache_integration(self, service, sample_component, sample_vulnerability):
        """Test caching functionality"""
        request = {
            "component": sample_component,
            "vulnerabilities": [sample_vulnerability],
            "analysis_context": "Production web application"
        }
        
        # Mock AI model response
        mock_response = {
            "explanation": "Cached explanation",
            "confidence_score": 0.95,
            "sources": ["https://example.com"],
            "key_factors": ["Factor 1"],
            "risk_level": "HIGH"
        }
        
        with patch.object(service.ai_models, 'explain_risk', return_value=mock_response) as mock_explain:
            # First call should hit the AI model
            response1 = await service.ExplainRisk(request, Mock())
            
            # Second call should use cache
            response2 = await service.ExplainRisk(request, Mock())
            
            # Verify AI model was called only once
            mock_explain.assert_called_once()
            
            # Verify both responses are identical
            assert response1.explanation == response2.explanation
            assert response1.confidence_score == response2.confidence_score
    
    @pytest.mark.asyncio
    async def test_error_handling(self, service):
        """Test error handling for various scenarios"""
        # Test with invalid request
        with pytest.raises(ValidationError):
            await service.ExplainRisk({}, Mock())
        
        # Test with missing required fields
        with pytest.raises(ValidationError):
            await service.PredictRiskScore({"component": {}}, Mock())
    
    @pytest.mark.asyncio
    async def test_cleanup(self, service):
        """Test service cleanup"""
        await service.cleanup()
        # Verify cleanup was called on dependencies
        assert service.ai_models is None
        assert service.ml_models is None
        assert service.explainability_chain is None


class TestServiceIntegration:
    """Integration tests for the service"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test complete workflow from request to response"""
        service = SbomaiAiService()
        await service.initialize()
        
        try:
            # Test data
            component = {
                "name": "spring-boot-starter-web",
                "version": "2.7.0",
                "group_id": "org.springframework.boot"
            }
            
            vulnerability = {
                "id": "CVE-2022-22965",
                "description": "Spring4Shell vulnerability",
                "severity": "CRITICAL_SEVERITY",
                "cvss_score": 9.8
            }
            
            # Test explain risk
            explain_request = {
                "component": component,
                "vulnerabilities": [vulnerability],
                "analysis_context": "Production application"
            }
            
            # Mock the AI model to return a response
            with patch.object(service.ai_models, 'explain_risk', return_value={
                "explanation": "Spring4Shell allows remote code execution",
                "confidence_score": 0.9,
                "sources": ["https://nvd.nist.gov/vuln/detail/CVE-2022-22965"],
                "key_factors": ["Remote code execution", "Widely exploited"],
                "risk_level": "CRITICAL"
            }):
                response = await service.ExplainRisk(explain_request, Mock())
                assert response.explanation is not None
                assert response.risk_level == "CRITICAL"
        
        finally:
            await service.cleanup()
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        service = SbomaiAiService()
        await service.initialize()
        
        try:
            component = {
                "name": "test-component",
                "version": "1.0.0"
            }
            
            request = {
                "component": component,
                "vulnerabilities": [],
                "analysis_context": "Test"
            }
            
            # Mock AI model response
            with patch.object(service.ai_models, 'explain_risk', return_value={
                "explanation": "Test explanation",
                "confidence_score": 0.8,
                "sources": [],
                "key_factors": [],
                "risk_level": "LOW"
            }):
                # Create multiple concurrent requests
                tasks = [
                    service.ExplainRisk(request, Mock())
                    for _ in range(5)
                ]
                
                responses = await asyncio.gather(*tasks)
                
                # Verify all requests completed successfully
                assert len(responses) == 5
                for response in responses:
                    assert response.explanation == "Test explanation"
        
        finally:
            await service.cleanup()


if __name__ == "__main__":
    pytest.main([__file__]) 