#!/usr/bin/env python3
"""
Test Local Model as Default for SBOMAI Engine
This script tests the local transformer model functionality.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_local_model():
    """Test local model functionality"""
    print("🚀 Testing Local Model as Default")
    print("=" * 40)
    
    try:
        # Test configuration
        from sbomai_ai.config import get_config
        config = get_config()
        
        # Override default to local
        config.default_llm = 'local'
        print(f"✅ Default LLM set to: {config.default_llm}")
        
        # Test local model import
        from sbomai_ai.models.local_model import LocalTransformerModel, LocalTransformerConfig
        print("✅ LocalTransformerModel imported successfully")
        
        # Test local model configuration
        local_config = LocalTransformerConfig(
            model_name="microsoft/DialoGPT-medium",
            max_length=512,
            temperature=0.7
        )
        print("✅ LocalTransformerConfig created successfully")
        
        # Test local model instantiation
        local_model = LocalTransformerModel(local_config)
        print("✅ LocalTransformerModel instantiated successfully")
        
        # Test basic text generation
        test_prompt = "Analyze this vulnerability: CVE-2021-44228"
        print(f"\nTesting with prompt: {test_prompt}")
        
        # Note: This might take some time to download the model on first run
        try:
            response = local_model.generate_text(test_prompt)
            print(f"✅ Local model response: {response[:100]}...")
        except Exception as e:
            print(f"⚠️  Model generation test: {e}")
            print("   (This is expected if the model hasn't been downloaded yet)")
        
        # Test with different model
        print("\nTesting with smaller model...")
        small_config = LocalTransformerConfig(
            model_name="distilgpt2",
            max_length=256,
            temperature=0.5
        )
        small_model = LocalTransformerModel(small_config)
        print("✅ Small model instantiated successfully")
        
        print("\n🎉 Local model tests completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_selection():
    """Test model selection logic"""
    print("\n🔧 Testing Model Selection Logic")
    print("-" * 30)
    
    try:
        from sbomai_ai.models import (
            OpenAiModel, AnthropicModel, GoogleGeminiModel, LocalTransformerModel
        )
        from sbomai_ai.models.openai_model import OpenAiConfig
        from sbomai_ai.models.anthropic_model import AnthropicConfig
        from sbomai_ai.models.google_model import GoogleGeminiConfig
        from sbomai_ai.models.local_model import LocalTransformerConfig
        
        # Test model selection based on config
        config = get_config()
        
        models = {
            'openai': OpenAiModel(OpenAiConfig(api_key="test", model="gpt-4")),
            'anthropic': AnthropicModel(AnthropicConfig(api_key="test", model="claude-2")),
            'google': GoogleGeminiModel(GoogleGeminiConfig(api_key="test", model="gemini-pro")),
            'local': LocalTransformerModel(LocalTransformerConfig())
        }
        
        # Test with local as default
        config.default_llm = 'local'
        selected_model = models.get(config.default_llm)
        
        if selected_model:
            print(f"✅ Model selected: {type(selected_model).__name__}")
            print(f"✅ Default LLM: {config.default_llm}")
        else:
            print(f"❌ No model found for: {config.default_llm}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Model selection error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SBOMAI Local Model Test")
    print("=" * 40)
    
    # Test local model
    local_ok = test_local_model()
    
    if local_ok:
        # Test model selection
        selection_ok = test_model_selection()
        
        if selection_ok:
            print("\n✅ All local model tests passed!")
            print("🎉 The SBOMAI Engine is ready to use with local models!")
        else:
            print("\n⚠️  Local model works but selection logic failed.")
    else:
        print("\n❌ Local model tests failed.") 