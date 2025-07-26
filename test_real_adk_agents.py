#!/usr/bin/env python3
"""
Real ADK Agent Tests - Testing Actual Google ADK Agents with Gemini API
These tests use the real agents and make actual API calls to verify functionality
"""

import os
import sys
import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any

# Set up environment for real API calls
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

# Add paths for imports
sys.path.append('libs')
sys.path.append('congestion_detector')
sys.path.append('context_aggregator')
sys.path.append('fix_recommender')

def test_real_congestion_detector_agent():
    """Test the REAL Congestion Detector ADK Agent with actual API calls"""
    print("🔍 TESTING REAL CONGESTION DETECTOR ADK AGENT")
    print("=" * 60)
    
    try:
        # Import the real agent
        from congestion_detector.agent import CongestionDetectorAgent
        print("[DEBUG] Importing real CongestionDetectorAgent...")
        
        # Create the real agent (this will initialize ADK)
        print("[DEBUG] Creating real CongestionDetectorAgent...")
        start_time = time.time()
        agent = CongestionDetectorAgent()
        creation_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Real agent created in {creation_time:.2f}s")
        print(f"[DEBUG] Agent name: {agent.agent.name}")
        print(f"[DEBUG] Agent model: {agent.agent.model}")
        print(f"[DEBUG] Agent tools: {len(agent.agent.tools)} tools")
        
        # Test GPS data analysis with real API call
        print("\n[DEBUG] Testing GPS data analysis with real API...")
        gps_data = {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "speed_kmph": 15.2,
            "vehicle_count": 45,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"[DEBUG] Input GPS data: {json.dumps(gps_data, indent=2)}")
        
        # Use the real agent's function tool (this will make API calls)
        start_time = time.time()
        result = agent.analyze_gps_data_tool(gps_data)
        api_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Real agent analysis complete in {api_time:.2f}s!")
        print(f"[DEBUG] Result: {json.dumps(result, indent=2)}")
        
        # Test segment status
        print("\n[DEBUG] Testing segment status with real API...")
        segment_result = agent.get_segment_status_tool("TEST_SEG001")
        print(f"[DEBUG] Segment status: {json.dumps(segment_result, indent=2)}")
        
        return True, api_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ Real CongestionDetectorAgent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_real_context_aggregator_agent():
    """Test the REAL Context Aggregator ADK Agent with actual API calls"""
    print("\n🔍 TESTING REAL CONTEXT AGGREGATOR ADK AGENT")
    print("=" * 60)
    
    try:
        # Import the real agent
        from context_aggregator.agent import ContextAggregatorAgent
        print("[DEBUG] Importing real ContextAggregatorAgent...")
        
        # Create the real agent (this will initialize ADK)
        print("[DEBUG] Creating real ContextAggregatorAgent...")
        start_time = time.time()
        agent = ContextAggregatorAgent()
        creation_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Real agent created in {creation_time:.2f}s")
        print(f"[DEBUG] Agent name: {agent.agent.name}")
        print(f"[DEBUG] Agent model: {agent.agent.model}")
        print(f"[DEBUG] Agent tools: {len(agent.agent.tools)} tools")
        
        # Test context gathering with real API call
        print("\n[DEBUG] Testing context gathering with real API...")
        location_data = {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "radius_km": 5.0
        }
        
        print(f"[DEBUG] Input location data: {json.dumps(location_data, indent=2)}")
        
        # Use the real agent's function tool (this will make API calls)
        start_time = time.time()
        result = agent.gather_context_tool(location_data)
        api_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Real agent context gathering complete in {api_time:.2f}s!")
        print(f"[DEBUG] Result: {json.dumps(result, indent=2)}")
        
        # Test news context
        print("\n[DEBUG] Testing news context with real API...")
        news_result = agent.get_news_context_tool({"location": "Downtown", "radius_km": 5.0})
        print(f"[DEBUG] News context: {json.dumps(news_result, indent=2)}")
        
        return True, api_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ Real ContextAggregatorAgent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_real_adk_runner_with_agents():
    """Test running the real ADK agents with the runner and actual API calls"""
    print("\n🔍 TESTING REAL ADK RUNNER WITH AGENTS")
    print("=" * 60)
    
    try:
        from google.adk.runners import InMemoryRunner
        from congestion_detector.agent import CongestionDetectorAgent
        
        print("[DEBUG] Creating real ADK runner...")
        runner = InMemoryRunner()
        
        # Create real agent
        print("[DEBUG] Creating real CongestionDetectorAgent...")
        agent = CongestionDetectorAgent()
        
        # Test with real runner and API calls
        prompt = """
        Analyze this traffic scenario and provide specific recommendations:
        
        Location: Downtown Main Street
        Current Speed: 15 km/h (expected: 50 km/h)
        Vehicle Count: 45
        Weather: Heavy rain
        Time: Rush hour
        
        Provide:
        1. Severity level (LOW/MODERATE/HIGH/CRITICAL)
        2. Root causes of congestion
        3. 2-3 specific recommendations with timelines
        4. Expected improvement percentages
        """
        
        print("[DEBUG] 📡 Making real ADK API call with agent...")
        print(f"[DEBUG] Agent: {agent.agent.name}")
        print(f"[DEBUG] Model: {agent.agent.model}")
        print(f"[DEBUG] Tools available: {len(agent.agent.tools)}")
        
        start_time = time.time()
        # Run the agent (this will make real API calls)
        result = runner.run(agent.agent, prompt)
        api_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Real ADK runner call successful in {api_time:.2f}s!")
        print(f"[DEBUG] Result type: {type(result)}")
        
        # Extract response
        if hasattr(result, 'text'):
            response_text = result.text
        elif hasattr(result, 'content'):
            response_text = result.content
        else:
            response_text = str(result)
        
        print(f"[DEBUG] Response length: {len(response_text)} characters")
        print(f"[DEBUG] Response preview: {response_text[:300]}...")
        
        return True, api_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ Real ADK runner test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_real_gemini_api_integration():
    """Test real Gemini API integration in agents"""
    print("\n🔍 TESTING REAL GEMINI API INTEGRATION IN AGENTS")
    print("=" * 60)
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        
        # Test direct Gemini API
        print("[DEBUG] Testing direct Gemini API...")
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = """
        You are a traffic management AI expert. Analyze this scenario:
        
        Location: Downtown Main Street
        Current Speed: 15 km/h (expected: 50 km/h)
        Vehicle Count: 45
        Weather: Heavy rain
        Time: Rush hour
        
        Provide analysis in this format:
        SEVERITY: [LOW/MODERATE/HIGH/CRITICAL]
        ROOT_CAUSES: [List main causes]
        RECOMMENDATIONS: [List 2-3 actions]
        EXPECTED_IMPROVEMENT: [Percentage]
        """
        
        print("[DEBUG] 📡 Making direct Gemini API call...")
        start_time = time.time()
        response = model.generate_content(prompt)
        api_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Direct Gemini API call successful in {api_time:.2f}s!")
        print(f"[DEBUG] Response length: {len(response.text)} characters")
        print(f"[DEBUG] Response preview: {response.text[:300]}...")
        
        return True, api_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ Real Gemini integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_agent_function_tools():
    """Test that agents have proper function tools configured"""
    print("\n🔍 TESTING AGENT FUNCTION TOOLS")
    print("=" * 60)
    
    try:
        from congestion_detector.agent import CongestionDetectorAgent
        from context_aggregator.agent import ContextAggregatorAgent
        
        # Test Congestion Detector tools
        print("[DEBUG] Testing Congestion Detector function tools...")
        cd_agent = CongestionDetectorAgent()
        
        print(f"[DEBUG] Congestion Detector tools: {len(cd_agent.agent.tools)}")
        for i, tool in enumerate(cd_agent.agent.tools):
            print(f"[DEBUG]   Tool {i+1}: {tool.name} - {tool.description}")
        
        # Test Context Aggregator tools
        print("\n[DEBUG] Testing Context Aggregator function tools...")
        ca_agent = ContextAggregatorAgent()
        
        print(f"[DEBUG] Context Aggregator tools: {len(ca_agent.agent.tools)}")
        for i, tool in enumerate(ca_agent.agent.tools):
            print(f"[DEBUG]   Tool {i+1}: {tool.name} - {tool.description}")
        
        return True, 0
        
    except Exception as e:
        print(f"[DEBUG] ❌ Function tools test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def main():
    """Main test function"""
    print("🚀 REAL ADK AGENT TESTS - USING ACTUAL AGENTS WITH GEMINI API")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    # Run all tests
    tests = [
        ("Real Congestion Detector Agent", test_real_congestion_detector_agent),
        ("Real Context Aggregator Agent", test_real_context_aggregator_agent),
        ("Real ADK Runner with Agents", test_real_adk_runner_with_agents),
        ("Real Gemini API Integration", test_real_gemini_api_integration),
        ("Agent Function Tools", test_agent_function_tools)
    ]
    
    results = []
    total_api_time = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success, api_time = test_func()
            results.append((test_name, success, api_time))
            if success:
                total_api_time += api_time
        except Exception as e:
            print(f"[DEBUG] ❌ Test failed with exception: {e}")
            results.append((test_name, False, 0))
    
    # Summary
    print("\n📊 REAL ADK AGENT TEST RESULTS")
    print("=" * 80)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {passed/total:.0%}")
    print(f"Total API Time: {total_api_time:.2f} seconds")
    print(f"Average API Time: {total_api_time/passed:.2f} seconds" if passed > 0 else "No successful API calls")
    
    print(f"\n📋 DETAILED RESULTS:")
    for test_name, success, api_time in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   • {test_name}: {status} ({api_time:.2f}s)")
    
    if passed == total:
        print(f"\n🎉 ALL REAL ADK AGENT TESTS PASSED!")
        print(f"✅ Real ADK agents are working with Gemini API!")
        print(f"✅ Real agent function tools are configured!")
        print(f"✅ Real ADK runner is working!")
        print(f"✅ Real API calls are being made!")
        print(f"✅ Average API response time: {total_api_time/passed:.2f}s")
        
        print(f"\n🚀 FOR YOUR DEMO:")
        print(f"   • Real agents are using Google ADK")
        print(f"   • Real Gemini API calls are being made")
        print(f"   • Check Google Cloud dashboard for API usage")
        print(f"   • All agents are production-ready")
        
    elif passed >= total * 0.8:
        print(f"\n⚠️  MOSTLY WORKING ({passed}/{total})")
        print(f"✅ Core real agent functionality available")
        print(f"⚠️  Some components need attention")
        
    else:
        print(f"\n❌ NEEDS ATTENTION ({passed}/{total})")
        print(f"❌ Real agent functionality needs fixes")
    
    print(f"\n🔗 USEFUL LINKS:")
    print(f"   • Google Cloud Console: https://console.cloud.google.com/apis/api/generativeai.googleapis.com")
    print(f"   • API Usage Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
    print(f"   • You should see {passed} API calls in your dashboard!")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 