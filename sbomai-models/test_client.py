#!/usr/bin/env python3
"""
Test client for SBOMAI AI Microservice
Demonstrates how to use the gRPC endpoints
"""

import asyncio
import json
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import grpc
    from src.sbomai_ai import sbomai_ai_pb2, sbomai_ai_pb2_grpc
except ImportError as e:
    print(f"Error importing gRPC modules: {e}")
    print("Please run: python -m grpc_tools.protoc --python_out=./src --grpc_python_out=./src --proto_path=./protos ./protos/sbomai_ai.proto")
    sys.exit(1)


async def test_service_info(stub):
    """Test the GetServiceInfo endpoint"""
    print("\nℹ️  Testing GetServiceInfo endpoint...")
    
    try:
        response = await stub.GetServiceInfo(sbomai_ai_pb2.ServiceInfoRequest())
        print(f"✅ Service Info:")
        print(f"   Service Name: {response.service_name}")
        print(f"   Version: {response.version}")
        print(f"   Status: {response.status}")
        print(f"   gRPC Port: {response.grpc_port}")
        print(f"   Metrics Port: {response.metrics_port}")
        print(f"   Capabilities: {list(response.capabilities)}")
        return True
    except Exception as e:
        print(f"❌ GetServiceInfo failed: {e}")
        return False


async def test_explain_risk(stub):
    """Test the ExplainRisk endpoint"""
    print("\n🧠 Testing ExplainRisk endpoint...")
    
    # Create a sample component
    component = sbomai_ai_pb2.SbomComponent(
        name="log4j-core",
        version="2.14.1",
        group_id="org.apache.logging.log4j",
        license="Apache-2.0",
        purl="pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1"
    )
    
    # Create a sample vulnerability
    vulnerability = sbomai_ai_pb2.Vulnerability(
        id="CVE-2021-44228",
        description="Log4Shell vulnerability",
        severity=sbomai_ai_pb2.Severity.CRITICAL_SEVERITY,
        cvss_score=10.0,
        published_date="2021-12-10T00:00:00Z"
    )
    
    # Create the request
    request = sbomai_ai_pb2.ExplainRiskRequest(
        component=component,
        vulnerabilities=[vulnerability],
        analysis_context="Production web application"
    )
    
    try:
        response = await stub.ExplainRisk(request)
        print(f"✅ ExplainRisk Response:")
        print(f"   Explanation: {response.explanation}")
        print(f"   Confidence: {response.confidence_score}")
        print(f"   Risk Level: {response.risk_level}")
        print(f"   Model Used: {response.model_used}")
        print(f"   Processing Time: {response.processing_time_ms}ms")
        return True
    except Exception as e:
        print(f"❌ ExplainRisk failed: {e}")
        return False


async def test_predict_risk_score(stub):
    """Test the PredictRiskScore endpoint"""
    print("\n📊 Testing PredictRiskScore endpoint...")
    
    # Create a sample component
    component = sbomai_ai_pb2.SbomComponent(
        name="spring-boot-starter-web",
        version="2.7.0",
        group_id="org.springframework.boot"
    )
    
    # Create the request
    request = sbomai_ai_pb2.PredictRiskScoreRequest(
        component=component,
        features=["web_framework", "popular", "enterprise"]
    )
    
    try:
        response = await stub.PredictRiskScore(request)
        print(f"✅ PredictRiskScore Response:")
        print(f"   Risk Score: {response.risk_score}")
        print(f"   Model Used: {response.model_used}")
        print(f"   Processing Time: {response.processing_time_ms}ms")
        return True
    except Exception as e:
        print(f"❌ PredictRiskScore failed: {e}")
        return False


async def test_suggest_fix(stub):
    """Test the SuggestFix endpoint"""
    print("\n🔧 Testing SuggestFix endpoint...")
    
    # Create a sample component
    component = sbomai_ai_pb2.SbomComponent(
        name="log4j-core",
        version="2.14.1",
        group_id="org.apache.logging.log4j"
    )
    
    # Create the request
    request = sbomai_ai_pb2.SuggestFixRequest(
        vulnerability_id="CVE-2021-44228",
        component=component,
        constraints=["no_breaking_changes", "apache_license"]
    )
    
    try:
        response = await stub.SuggestFix(request)
        print(f"✅ SuggestFix Response:")
        print(f"   Confidence Score: {response.confidence_score}")
        print(f"   Number of Suggestions: {len(response.suggestions)}")
        if response.suggestions:
            suggestion = response.suggestions[0]
            print(f"   First Suggestion: {suggestion.action} to {suggestion.suggested_component.version}")
        print(f"   Processing Time: {response.processing_time_ms}ms")
        return True
    except Exception as e:
        print(f"❌ SuggestFix failed: {e}")
        return False


async def test_explainable_sbom_chain(stub):
    """Test the ExplainableSbomChain endpoint"""
    print("\n🔗 Testing ExplainableSbomChain endpoint...")
    
    # Create a sample SBOM document
    sbom_document = sbomai_ai_pb2.SbomDocument(
        name="test-application",
        version="1.0.0",
        format=sbomai_ai_pb2.SbomFormat.CYCLONEDX,
        created_date="2024-01-15T10:00:00Z"
    )
    
    # Add components
    component1 = sbomai_ai_pb2.SbomComponent(
        name="log4j-core",
        version="2.14.1",
        group_id="org.apache.logging.log4j"
    )
    component2 = sbomai_ai_pb2.SbomComponent(
        name="spring-boot-starter-web",
        version="2.7.0",
        group_id="org.springframework.boot"
    )
    sbom_document.components.extend([component1, component2])
    
    # Create the request
    request = sbomai_ai_pb2.ExplainableSbomChainRequest(
        sbom_document=sbom_document,
        chain_config=sbomai_ai_pb2.ChainConfig(
            max_steps=3,
            confidence_threshold=0.7,
            include_detailed_explanations=True,
            analysis_types=["vulnerability", "license"]
        )
    )
    
    try:
        response = await stub.ExplainableSbomChain(request)
        print(f"✅ ExplainableSbomChain Response:")
        print(f"   Overall Assessment: {response.overall_assessment}")
        print(f"   Overall Risk Score: {response.overall_risk_score}")
        print(f"   Number of Steps: {len(response.chain_steps)}")
        print(f"   Number of Recommendations: {len(response.recommendations)}")
        print(f"   Processing Time: {response.processing_time_ms}ms")
        return True
    except Exception as e:
        print(f"❌ ExplainableSbomChain failed: {e}")
        return False


async def main():
    """Main test function"""
    print("🚀 SBOMAI AI Microservice Test Client")
    print("=" * 50)
    
    # Connect to the gRPC server
    server_address = "localhost:50051"
    print(f"Connecting to server at {server_address}...")
    
    try:
        async with grpc.aio.insecure_channel(server_address) as channel:
            stub = sbomai_ai_pb2_grpc.SbomaiAiServiceStub(channel)
            
            # Test all endpoints
            tests = [
                test_service_info,
                test_explain_risk,
                test_predict_risk_score,
                test_suggest_fix,
                test_explainable_sbom_chain
            ]
            
            results = []
            for test in tests:
                try:
                    result = await test(stub)
                    results.append(result)
                except Exception as e:
                    print(f"❌ Test {test.__name__} failed with exception: {e}")
                    results.append(False)
            
            # Summary
            print("\n" + "=" * 50)
            print("📋 Test Summary:")
            passed = sum(results)
            total = len(results)
            print(f"   Passed: {passed}/{total}")
            print(f"   Success Rate: {(passed/total)*100:.1f}%")
            
            if passed == total:
                print("🎉 All tests passed!")
            else:
                print("⚠️  Some tests failed. Check the server logs for details.")
                
    except Exception as e:
        print(f"❌ Failed to connect to server: {e}")
        print("Make sure the Python AI microservice is running:")
        print("  python server.py")
        return False
    
    return True


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1) 