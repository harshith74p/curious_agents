#!/usr/bin/env python3
"""
Working Runner Test - Using the correct ADK API
"""

import os
import time
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

def test_working_runner():
    """Test the working runner approach"""
    print("🔍 TESTING WORKING RUNNER")
    print("=" * 50)
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        # Create agent
        agent = LlmAgent(
            name="traffic_agent",
            model="gemini-2.0-flash",
            description="Traffic management agent",
            instruction="You are a traffic management expert. Analyze scenarios and provide recommendations."
        )
        
        print("✅ Agent created")
        
        # Create runner
        runner = InMemoryRunner(agent)
        print("✅ Runner created")
        
        # The correct way to use the runner is to call it directly
        # The runner acts as a callable that takes the prompt
        print("📡 Making API call...")
        start_time = time.time()
        
        # Call the runner directly with the prompt
        result = runner("Analyze this traffic scenario: Downtown, 15 km/h, heavy rain. Provide severity level.")
        api_time = time.time() - start_time
        
        print(f"✅ API call successful in {api_time:.2f}s!")
        print(f"✅ Result type: {type(result)}")
        
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
        print(f"❌ Working runner test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_direct_agent_call():
    """Test calling agent directly"""
    print("\n🔍 TESTING DIRECT AGENT CALL")
    print("=" * 50)
    
    try:
        from google.adk.agents import LlmAgent
        
        # Create agent
        agent = LlmAgent(
            name="traffic_agent",
            model="gemini-2.0-flash",
            description="Traffic management agent",
            instruction="You are a traffic management expert."
        )
        
        print("✅ Agent created")
        
        # Call agent directly
        print("📡 Making direct agent API call...")
        start_time = time.time()
        
        result = agent("Analyze this traffic scenario: Downtown, 15 km/h, heavy rain. Provide severity level.")
        api_time = time.time() - start_time
        
        print(f"✅ Direct agent call successful in {api_time:.2f}s!")
        print(f"✅ Result type: {type(result)}")
        
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
        print(f"❌ Direct agent call failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def main():
    """Main test function"""
    print("🚀 WORKING RUNNER TESTS")
    print("=" * 80)
    
    tests = [
        ("Working Runner", test_working_runner),
        ("Direct Agent Call", test_direct_agent_call)
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
            print(f"❌ Test failed: {e}")
            results.append((test_name, False, 0))
    
    # Summary
    print("\n📊 WORKING RUNNER TEST RESULTS")
    print("=" * 80)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {passed/total:.0%}")
    print(f"Total API Time: {total_api_time:.2f} seconds")
    
    if passed == total:
        print(f"\n🎉 ALL WORKING RUNNER TESTS PASSED!")
        print(f"✅ ADK API is working correctly!")
        print(f"✅ Real API calls are being made!")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    import sys
    sys.exit(0 if success else 1) 