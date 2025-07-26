#!/usr/bin/env python3
"""
Test ADK API to understand correct usage
"""

import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

def test_adk_imports():
    """Test basic ADK imports"""
    print("Testing ADK imports...")
    
    try:
        from google.adk.agents import LlmAgent
        print("✅ LlmAgent imported")
        
        from google.adk.runners import InMemoryRunner
        print("✅ InMemoryRunner imported")
        
        from google.adk.tools import FunctionTool
        print("✅ FunctionTool imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_simple_agent():
    """Test creating a simple agent without tools"""
    print("\nTesting simple agent creation...")
    
    try:
        from google.adk.agents import LlmAgent
        
        agent = LlmAgent(
            name="test_agent",
            model="gemini-2.0-flash",
            description="Test agent",
            instruction="You are a helpful assistant."
        )
        
        print(f"✅ Simple agent created: {agent.name}")
        print(f"✅ Model: {agent.model}")
        
        return True
    except Exception as e:
        print(f"❌ Simple agent creation failed: {e}")
        return False

def test_agent_with_runner():
    """Test running an agent with the runner"""
    print("\nTesting agent with runner...")
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        agent = LlmAgent(
            name="test_agent",
            model="gemini-2.0-flash",
            description="Test agent",
            instruction="You are a traffic management expert."
        )
        
        runner = InMemoryRunner()
        
        prompt = "Analyze this traffic scenario: Downtown, 15 km/h, heavy rain. Provide severity level."
        
        print("📡 Making API call...")
        result = runner.run(agent, prompt)
        
        print(f"✅ API call successful!")
        print(f"✅ Result type: {type(result)}")
        
        if hasattr(result, 'text'):
            print(f"✅ Response: {result.text[:100]}...")
        else:
            print(f"✅ Response: {str(result)[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ Agent with runner failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🔍 TESTING ADK API")
    print("=" * 50)
    
    tests = [
        ("ADK Imports", test_adk_imports),
        ("Simple Agent", test_simple_agent),
        ("Agent with Runner", test_agent_with_runner)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        if success:
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n🎉 ADK API test complete!")

if __name__ == "__main__":
    main() 