#!/usr/bin/env python3
"""
Test Fixed ADK API - Verify the corrected ADK usage works
"""

import os
import sys
import time
from datetime import datetime

# Set up environment for real API calls
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

def test_basic_adk_imports():
    """Test basic ADK imports work"""
    print("🔍 TESTING BASIC ADK IMPORTS")
    print("=" * 50)
    
    try:
        from google.adk.agents import LlmAgent
        print("✅ LlmAgent imported successfully")
        
        from google.adk.runners import InMemoryRunner
        print("✅ InMemoryRunner imported successfully")
        
        from google.adk.tools import FunctionTool
        print("✅ FunctionTool imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_simple_agent_creation():
    """Test creating a simple agent"""
    print("\n🔍 TESTING SIMPLE AGENT CREATION")
    print("=" * 50)
    
    try:
        from google.adk.agents import LlmAgent
        
        agent = LlmAgent(
            name="test_agent",
            model="gemini-2.0-flash",
            description="Test agent",
            instruction="You are a helpful assistant."
        )
        
        print(f"✅ Agent created: {agent.name}")
        print(f"✅ Model: {agent.model}")
        
        return True
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def test_runner_with_agent():
    """Test runner with agent"""
    print("\n🔍 TESTING RUNNER WITH AGENT")
    print("=" * 50)
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        # Create agent
        agent = LlmAgent(
            name="traffic_agent",
            model="gemini-2.0-flash",
            description="Traffic management agent",
            instruction="You are a traffic management expert."
        )
        
        # Create runner with agent
        runner = InMemoryRunner(agent)
        print("✅ Runner created with agent")
        
        # Test API call with correct parameters
        prompt = "Analyze this traffic scenario: Downtown, 15 km/h, heavy rain. Provide severity level."
        
        print("📡 Making API call...")
        start_time = time.time()
        
        # Use the correct API with required parameters
        result = runner.run(
            user_id="test_user",
            session_id="test_session",
            new_message=prompt
        )
        api_time = time.time() - start_time
        
        print(f"✅ API call successful in {api_time:.2f}s!")
        
        # Extract response
        if hasattr(result, 'text'):
            response_text = result.text
        elif hasattr(result, 'content'):
            response_text = result.content
        else:
            response_text = str(result)
        
        print(f"✅ Response length: {len(response_text)} characters")
        print(f"✅ Response preview: {response_text[:200]}...")
        
        return True, api_time
        
    except Exception as e:
        print(f"❌ Runner test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_function_tool_creation():
    """Test creating function tools"""
    print("\n🔍 TESTING FUNCTION TOOL CREATION")
    print("=" * 50)
    
    try:
        from google.adk.tools import FunctionTool
        
        # Define a simple function
        def analyze_traffic(data):
            """Analyze traffic data"""
            return {"analysis": "Traffic analysis complete"}
        
        # Create function tool
        tool = FunctionTool(analyze_traffic)
        tool.name = "analyze_traffic"
        tool.description = "Analyze traffic data"
        
        print(f"✅ Function tool created: {tool.name}")
        print(f"✅ Tool description: {tool.description}")
        
        return True
    except Exception as e:
        print(f"❌ Function tool creation failed: {e}")
        return False

def test_agent_with_tools():
    """Test agent with function tools"""
    print("\n🔍 TESTING AGENT WITH FUNCTION TOOLS")
    print("=" * 50)
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.tools import FunctionTool
        
        # Define a function
        def analyze_gps_data(data):
            """Analyze GPS data for traffic patterns"""
            return {
                "congestion_level": "HIGH",
                "speed": data.get("speed", 0),
                "analysis": "Heavy congestion detected"
            }
        
        # Create function tool
        tool = FunctionTool(analyze_gps_data)
        tool.name = "analyze_gps_data"
        tool.description = "Analyze GPS data for traffic congestion patterns"
        
        # Create agent with tool
        agent = LlmAgent(
            name="traffic_agent_with_tools",
            model="gemini-2.0-flash",
            description="Traffic agent with tools",
            instruction="You are a traffic management expert with tools to analyze GPS data.",
            tools=[tool]
        )
        
        print(f"✅ Agent with tools created: {agent.name}")
        print(f"✅ Tools count: {len(agent.tools)}")
        
        return True
    except Exception as e:
        print(f"❌ Agent with tools failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 FIXED ADK API TESTS")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    # Run all tests
    tests = [
        ("Basic ADK Imports", test_basic_adk_imports),
        ("Simple Agent Creation", test_simple_agent_creation),
        ("Runner with Agent", test_runner_with_agent),
        ("Function Tool Creation", test_function_tool_creation),
        ("Agent with Tools", test_agent_with_tools)
    ]
    
    results = []
    total_api_time = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_name == "Runner with Agent":
                success, api_time = test_func()
                if success:
                    total_api_time += api_time
            else:
                success = test_func()
                api_time = 0
            results.append((test_name, success, api_time))
        except Exception as e:
            print(f"[DEBUG] ❌ Test failed with exception: {e}")
            results.append((test_name, False, 0))
    
    # Summary
    print("\n📊 FIXED ADK API TEST RESULTS")
    print("=" * 80)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {passed/total:.0%}")
    print(f"Total API Time: {total_api_time:.2f} seconds")
    
    print(f"\n📋 DETAILED RESULTS:")
    for test_name, success, api_time in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   • {test_name}: {status} ({api_time:.2f}s)")
    
    if passed == total:
        print(f"\n🎉 ALL FIXED ADK API TESTS PASSED!")
        print(f"✅ ADK API is working correctly!")
        print(f"✅ Agents can be created!")
        print(f"✅ Runners work with agents!")
        print(f"✅ Function tools can be created!")
        print(f"✅ Real API calls are working!")
        
    elif passed >= total * 0.8:
        print(f"\n⚠️  MOSTLY WORKING ({passed}/{total})")
        print(f"✅ Core ADK functionality available")
        
    else:
        print(f"\n❌ NEEDS ATTENTION ({passed}/{total})")
        print(f"❌ ADK API needs more fixes")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 