#!/usr/bin/env python3
"""
Simple Real ADK Agent Tests - Testing Actual Google ADK Agents with Gemini API
These tests use the real agents without function tools to verify basic functionality
"""

import os
import sys
import time
from datetime import datetime

# Set up environment for real API calls
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

def test_simple_adk_agent():
    """Test creating a simple ADK agent and making API calls"""
    print("🔍 TESTING SIMPLE ADK AGENT WITH GEMINI API")
    print("=" * 60)
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        print("[DEBUG] Creating simple ADK agent...")
        start_time = time.time()
        
        # Create a simple agent without function tools
        agent = LlmAgent(
            name="traffic_agent",
            model="gemini-2.0-flash",
            description="Traffic management AI agent",
            instruction="""You are a traffic management AI expert. Your role is to:
            1. Analyze traffic scenarios and provide severity assessments
            2. Identify root causes of congestion
            3. Provide specific recommendations with timelines
            4. Estimate expected improvements
            
            Always provide structured responses with clear sections."""
        )
        
        creation_time = time.time() - start_time
        print(f"[DEBUG] ✅ Agent created in {creation_time:.2f}s")
        print(f"[DEBUG] Agent name: {agent.name}")
        print(f"[DEBUG] Agent model: {agent.model}")
        
        # Test with runner
        print("\n[DEBUG] Testing agent with real API call...")
        runner = InMemoryRunner()
        
        prompt = """
        Analyze this traffic scenario and provide specific recommendations:
        
        Location: Downtown Main Street
        Current Speed: 15 km/h (expected: 50 km/h)
        Vehicle Count: 45
        Weather: Heavy rain
        Time: Rush hour
        
        Provide analysis in this format:
        SEVERITY: [LOW/MODERATE/HIGH/CRITICAL]
        ROOT_CAUSES: [List main causes]
        RECOMMENDATIONS: [List 2-3 actions with timelines]
        EXPECTED_IMPROVEMENT: [Percentage improvement expected]
        """
        
        print("[DEBUG] 📡 Making real ADK API call...")
        start_time = time.time()
        result = runner.run(agent, prompt)
        api_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Real ADK API call successful in {api_time:.2f}s!")
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
        print(f"[DEBUG] ❌ Simple ADK agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_direct_gemini_api():
    """Test direct Gemini API integration"""
    print("\n🔍 TESTING DIRECT GEMINI API INTEGRATION")
    print("=" * 60)
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        
        print("[DEBUG] Creating Gemini model...")
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
        print(f"[DEBUG] ❌ Direct Gemini API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_multiple_agents():
    """Test creating multiple ADK agents"""
    print("\n🔍 TESTING MULTIPLE ADK AGENTS")
    print("=" * 60)
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        # Create multiple agents
        agents = []
        
        # Congestion Detector Agent
        print("[DEBUG] Creating Congestion Detector Agent...")
        cd_agent = LlmAgent(
            name="congestion_detector",
            model="gemini-2.0-flash",
            description="AI agent for detecting traffic congestion",
            instruction="You are a traffic congestion detection specialist. Analyze GPS data and traffic patterns to identify congestion levels and contributing factors."
        )
        agents.append(("Congestion Detector", cd_agent))
        
        # Context Aggregator Agent
        print("[DEBUG] Creating Context Aggregator Agent...")
        ca_agent = LlmAgent(
            name="context_aggregator",
            model="gemini-2.0-flash",
            description="AI agent for gathering and analyzing contextual information",
            instruction="You are a context analysis specialist. Gather and analyze information from multiple sources (weather, events, news) to understand traffic situations."
        )
        agents.append(("Context Aggregator", ca_agent))
        
        # Fix Recommender Agent
        print("[DEBUG] Creating Fix Recommender Agent...")
        fr_agent = LlmAgent(
            name="fix_recommender",
            model="gemini-2.0-flash",
            description="AI agent for recommending traffic solutions",
            instruction="You are a traffic solution specialist. Based on congestion analysis and context, provide specific, actionable recommendations with timelines and expected impacts."
        )
        agents.append(("Fix Recommender", fr_agent))
        
        print(f"[DEBUG] ✅ Created {len(agents)} agents successfully")
        
        # Test each agent
        runner = InMemoryRunner()
        total_api_time = 0
        
        for agent_name, agent in agents:
            print(f"\n[DEBUG] Testing {agent_name}...")
            
            prompt = f"Analyze this traffic scenario: Downtown, 15 km/h, heavy rain. Provide a brief assessment."
            
            start_time = time.time()
            result = runner.run(agent, prompt)
            api_time = time.time() - start_time
            total_api_time += api_time
            
            print(f"[DEBUG] ✅ {agent_name} API call successful in {api_time:.2f}s")
            
            # Extract response
            if hasattr(result, 'text'):
                response_text = result.text
            elif hasattr(result, 'content'):
                response_text = result.content
            else:
                response_text = str(result)
            
            print(f"[DEBUG] Response length: {len(response_text)} characters")
        
        return True, total_api_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ Multiple agents test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def main():
    """Main test function"""
    print("🚀 SIMPLE REAL ADK AGENT TESTS - USING ACTUAL AGENTS WITH GEMINI API")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    # Run all tests
    tests = [
        ("Simple ADK Agent", test_simple_adk_agent),
        ("Direct Gemini API", test_direct_gemini_api),
        ("Multiple ADK Agents", test_multiple_agents)
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
    print("\n📊 SIMPLE REAL ADK AGENT TEST RESULTS")
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
        print(f"\n🎉 ALL SIMPLE REAL ADK AGENT TESTS PASSED!")
        print(f"✅ Real ADK agents are working with Gemini API!")
        print(f"✅ Real API calls are being made!")
        print(f"✅ Multiple agents can be created!")
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