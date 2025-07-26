#!/usr/bin/env python3
"""
Comprehensive Debug Summary for CuriousAgents
Shows all agent statuses, API usage, and system health
"""

import os
import sys
import time
from datetime import datetime

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

def test_gemini_direct_api():
    """Test direct Gemini API with detailed logging"""
    print("🔍 TESTING DIRECT GEMINI API")
    print("=" * 50)
    
    try:
        import google.generativeai as genai
        print("[DEBUG] Importing google.generativeai...")
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        print(f"[DEBUG] Configuring API with key: {os.environ['GOOGLE_API_KEY'][:20]}...")
        
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("[DEBUG] Creating Gemini model...")
        
        # Test API call
        print("[DEBUG] 📡 Making test API call...")
        start_time = time.time()
        response = model.generate_content("Hello! Can you confirm you're working?")
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"[DEBUG] ✅ API call successful!")
        print(f"[DEBUG] ⏱️  Response time: {response_time:.2f} seconds")
        print(f"[DEBUG] 📝 Response: {response.text[:100]}...")
        
        return True, response_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ Direct API test failed: {e}")
        return False, 0

def test_adk_agent():
    """Test ADK agent with detailed logging"""
    print("\n🔍 TESTING GOOGLE ADK AGENT")
    print("=" * 50)
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        print("[DEBUG] Importing Google ADK...")
        
        agent = LlmAgent(
            name="debug_agent",
            model="gemini-2.0-flash",
            description="Debug traffic agent",
            instruction="You are a traffic management AI expert."
        )
        print(f"[DEBUG] Created ADK agent: {agent.name}")
        
        runner = InMemoryRunner()
        print("[DEBUG] Created InMemoryRunner...")
        
        # Test ADK call
        prompt = "Analyze this traffic scenario: Downtown, 15 km/h, heavy rain. Provide severity level."
        print("[DEBUG] 📡 Making ADK API call...")
        start_time = time.time()
        result = runner.run(agent, prompt)
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"[DEBUG] ✅ ADK call successful!")
        print(f"[DEBUG] ⏱️  Response time: {response_time:.2f} seconds")
        
        # Extract response
        if hasattr(result, 'text'):
            response_text = result.text
        elif hasattr(result, 'content'):
            response_text = result.content
        else:
            response_text = str(result)
        
        print(f"[DEBUG] 📝 Response length: {len(response_text)} characters")
        print(f"[DEBUG] 📝 Response: {response_text[:100]}...")
        
        return True, response_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ ADK test failed: {e}")
        return False, 0

def test_ml_components():
    """Test ML components with detailed logging"""
    print("\n🔍 TESTING ML COMPONENTS")
    print("=" * 50)
    
    try:
        import pandas as pd
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        print("[DEBUG] Importing ML libraries...")
        
        # Create test data
        print("[DEBUG] Creating test data...")
        X = np.random.rand(100, 5)
        y = np.random.randint(0, 3, 100)
        
        # Train model
        print("[DEBUG] Training RandomForest model...")
        start_time = time.time()
        model = RandomForestClassifier(n_estimators=10)
        model.fit(X, y)
        end_time = time.time()
        
        training_time = end_time - start_time
        print(f"[DEBUG] ✅ Model training successful!")
        print(f"[DEBUG] ⏱️  Training time: {training_time:.2f} seconds")
        
        # Make predictions
        print("[DEBUG] Making predictions...")
        predictions = model.predict(X[:5])
        print(f"[DEBUG] ✅ Predictions: {predictions}")
        
        return True, training_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ ML test failed: {e}")
        return False, 0

def main():
    """Main debug summary function"""
    print("🚀 CURIOUSAGENTS COMPREHENSIVE DEBUG SUMMARY")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    # Test all components
    tests = [
        ("Direct Gemini API", test_gemini_direct_api),
        ("Google ADK Agent", test_adk_agent),
        ("ML Components", test_ml_components)
    ]
    
    results = []
    total_api_time = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success, response_time = test_func()
        results.append((test_name, success, response_time))
        if success:
            total_api_time += response_time
    
    # Summary
    print("\n📊 DEBUG SUMMARY RESULTS")
    print("=" * 80)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {passed/total:.0%}")
    print(f"Total API Time: {total_api_time:.2f} seconds")
    print(f"Average API Time: {total_api_time/passed:.2f} seconds" if passed > 0 else "No successful API calls")
    
    print(f"\n📋 DETAILED STATUS:")
    for test_name, success, response_time in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   • {test_name}: {status} ({response_time:.2f}s)")
    
    if passed == total:
        print(f"\n🎉 ALL SYSTEMS OPERATIONAL!")
        print(f"✅ Direct Gemini API: Working")
        print(f"✅ Google ADK: Working")
        print(f"✅ ML Components: Working")
        print(f"✅ API Response Times: Good ({total_api_time/passed:.2f}s avg)")
        
        print(f"\n🚀 FOR YOUR DEMO:")
        print(f"   • Run: python debug_gemini_agent.py")
        print(f"   • Run: python debug_adk_agent.py")
        print(f"   • Check Google Cloud dashboard for API usage")
        print(f"   • All agents are ready for production")
        
    elif passed >= total * 0.8:
        print(f"\n⚠️  MOSTLY WORKING ({passed}/{total})")
        print(f"✅ Core functionality available")
        print(f"⚠️  Some components need attention")
        
    else:
        print(f"\n❌ NEEDS ATTENTION ({passed}/{total})")
        print(f"❌ Core functionality needs fixes")
    
    print(f"\n🔗 USEFUL LINKS:")
    print(f"   • Google Cloud Console: https://console.cloud.google.com/apis/api/generativeai.googleapis.com")
    print(f"   • API Usage Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
    print(f"   • You should see {passed} API calls in your dashboard!")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 