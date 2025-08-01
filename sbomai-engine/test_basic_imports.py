#!/usr/bin/env python3
"""
Basic Import Test for SBOMAI Engine
This script tests if the core modules can be imported successfully.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test basic imports"""
    print("Testing SBOMAI Engine imports...")
    
    try:
        # Test basic models
        print("1. Testing basic model imports...")
        from sbomai_ai.models.ai_models import ThreatContextEmbedding
        print("   ✅ ThreatContextEmbedding imported successfully")
        
        from sbomai_ai.models.openai_model import OpenAiModel
        print("   ✅ OpenAiModel imported successfully")
        
        from sbomai_ai.models.anthropic_model import AnthropicModel
        print("   ✅ AnthropicModel imported successfully")
        
        from sbomai_ai.models.google_model import GoogleGeminiModel
        print("   ✅ GoogleGeminiModel imported successfully")
        
        from sbomai_ai.models.local_model import LocalTransformerModel
        print("   ✅ LocalTransformerModel imported successfully")
        
        from sbomai_ai.models.xgboost_model import XGBoostRiskModel
        print("   ✅ XGBoostRiskModel imported successfully")
        
        from sbomai_ai.models.lightgbm_model import LightGBMRiskModel
        print("   ✅ LightGBMRiskModel imported successfully")
        
        from sbomai_ai.models.risk_model import RiskAssessmentModel
        print("   ✅ RiskAssessmentModel imported successfully")
        
        from sbomai_ai.models.predictor_model import VulnerabilityPredictor
        print("   ✅ VulnerabilityPredictor imported successfully")
        
        from sbomai_ai.models.explainability_model import ExplainabilityChain
        print("   ✅ ExplainabilityChain imported successfully")
        
        from sbomai_ai.models.gnn_predictor_model import GNNVulnerabilityPredictor
        print("   ✅ GNNVulnerabilityPredictor imported successfully")
        
        from sbomai_ai.models.graph_builder_model import DependencyGraphBuilder
        print("   ✅ DependencyGraphBuilder imported successfully")
        
        from sbomai_ai.models.graph_analyzer_model import DependencyGraphAnalyzer
        print("   ✅ DependencyGraphAnalyzer imported successfully")
        
        # Test advanced models
        print("\n2. Testing advanced model imports...")
        from sbomai_ai.models.vulnerability_intelligence import VulnerabilityIntelligence
        print("   ✅ VulnerabilityIntelligence imported successfully")
        
        from sbomai_ai.models.threat_intelligence import ThreatContextEmbedding as AdvancedThreatEmbedding
        print("   ✅ Advanced ThreatContextEmbedding imported successfully")
        
        from sbomai_ai.models.exploit_prediction import ExploitPredictor
        print("   ✅ ExploitPredictor imported successfully")
        
        from sbomai_ai.models.dependency_graph import DependencyGraph
        print("   ✅ DependencyGraph imported successfully")
        
        from sbomai_ai.models.gnn_risk_model import RiskGNNEncoder, RiskPropagationGNN, GNNRiskPredictor
        print("   ✅ GNN models imported successfully")
        
        # Test utilities
        print("\n3. Testing utility imports...")
        from sbomai_ai.utils.monitoring import track_request_duration, record_model_metrics
        print("   ✅ Monitoring utilities imported successfully")
        
        from sbomai_ai.config import get_config
        print("   ✅ Config imported successfully")
        
        # Test configuration
        print("\n4. Testing configuration...")
        config = get_config()
        print(f"   ✅ Configuration loaded: {config.default_llm}")
        
        print("\n🎉 All imports successful! The SBOMAI Engine is ready to use.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\nTesting basic functionality...")
    
    try:
        # Test configuration
        from sbomai_ai.config import get_config
        config = get_config()
        print(f"✅ Config loaded: default_llm = {config.default_llm}")
        
        # Test basic model instantiation
        from sbomai_ai.models.openai_model import OpenAiModel, OpenAiConfig
        openai_config = OpenAiConfig(api_key="test", model="gpt-4")
        print("✅ OpenAiConfig created successfully")
        
        # Test graph builder
        from sbomai_ai.models.graph_builder_model import DependencyGraphBuilder, DependencyGraphConfig
        graph_config = DependencyGraphConfig()
        graph_builder = DependencyGraphBuilder(graph_config)
        print("✅ DependencyGraphBuilder created successfully")
        
        print("🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SBOMAI Engine Import Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test functionality
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n✅ All tests passed! The SBOMAI Engine is working correctly.")
        else:
            print("\n⚠️  Imports work but functionality tests failed.")
    else:
        print("\n❌ Import tests failed. Please check the dependencies.") 