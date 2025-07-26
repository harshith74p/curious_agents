#!/usr/bin/env python3
"""
Test to find the correct InMemoryRunner API
"""

import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

def test_runner_methods():
    """Test different ways to use the runner"""
    print("🔍 TESTING RUNNER METHODS")
    print("=" * 50)
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        # Create agent
        agent = LlmAgent(
            name="test_agent",
            model="gemini-2.0-flash",
            description="Test agent",
            instruction="You are a helpful assistant."
        )
        
        # Create runner
        runner = InMemoryRunner(agent)
        
        print("✅ Runner created")
        print(f"✅ Runner type: {type(runner)}")
        print(f"✅ Runner methods: {[m for m in dir(runner) if not m.startswith('_')]}")
        
        # Try different ways to run
        print("\n🔍 Testing different run methods...")
        
        # Method 1: Try run() without parameters
        try:
            print("📡 Trying runner.run() without parameters...")
            result = runner.run()
            print(f"✅ runner.run() works: {type(result)}")
        except Exception as e:
            print(f"❌ runner.run() failed: {e}")
        
        # Method 2: Try run() with prompt as keyword argument
        try:
            print("📡 Trying runner.run(prompt='test')...")
            result = runner.run(prompt="Analyze this traffic scenario: Downtown, 15 km/h.")
            print(f"✅ runner.run(prompt=...) works: {type(result)}")
        except Exception as e:
            print(f"❌ runner.run(prompt=...) failed: {e}")
        
        # Method 3: Try run() with message parameter
        try:
            print("📡 Trying runner.run(message='test')...")
            result = runner.run(message="Analyze this traffic scenario: Downtown, 15 km/h.")
            print(f"✅ runner.run(message=...) works: {type(result)}")
        except Exception as e:
            print(f"❌ runner.run(message=...) failed: {e}")
        
        # Method 4: Try run() with text parameter
        try:
            print("📡 Trying runner.run(text='test')...")
            result = runner.run(text="Analyze this traffic scenario: Downtown, 15 km/h.")
            print(f"✅ runner.run(text=...) works: {type(result)}")
        except Exception as e:
            print(f"❌ runner.run(text=...) failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_agent_usage():
    """Test using agent directly without runner"""
    print("\n🔍 TESTING DIRECT AGENT USAGE")
    print("=" * 50)
    
    try:
        from google.adk.agents import LlmAgent
        
        # Create agent
        agent = LlmAgent(
            name="test_agent",
            model="gemini-2.0-flash",
            description="Test agent",
            instruction="You are a helpful assistant."
        )
        
        print("✅ Agent created")
        print(f"✅ Agent methods: {[m for m in dir(agent) if not m.startswith('_')]}")
        
        # Try calling agent directly
        try:
            print("📡 Trying agent.run()...")
            result = agent.run("Analyze this traffic scenario: Downtown, 15 km/h.")
            print(f"✅ agent.run() works: {type(result)}")
        except Exception as e:
            print(f"❌ agent.run() failed: {e}")
        
        # Try other methods
        try:
            print("📡 Trying agent.generate()...")
            result = agent.generate("Analyze this traffic scenario: Downtown, 15 km/h.")
            print(f"✅ agent.generate() works: {type(result)}")
        except Exception as e:
            print(f"❌ agent.generate() failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 TESTING CORRECT RUNNER API")
    print("=" * 80)
    
    test_runner_methods()
    test_direct_agent_usage()
    
    print("\n🎉 Runner API test complete!") 