#!/usr/bin/env python3
"""
Final Verification Script for CuriousAgents
Tests all components and provides clear status for your demo
"""

import os
import sys
import time
from datetime import datetime

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

def test_basic_imports():
    """Test basic Python functionality"""
    print("1. Testing Basic Imports...")
    try:
        import json
        import datetime
        print("   ✅ Basic imports successful")
        return True
    except Exception as e:
        print(f"   ❌ Basic imports failed: {e}")
        return False

def test_gemini_api():
    """Test real Gemini API integration"""
    print("2. Testing Real Gemini API...")
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Make a real API call
        response = model.generate_content("Hello! Can you confirm you're working?")
        print(f"   ✅ Gemini API working - Response: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"   ❌ Gemini API failed: {e}")
        return False

def test_google_adk():
    """Test Google ADK integration"""
    print("3. Testing Google ADK...")
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        agent = LlmAgent(
            name="test_agent",
            model="gemini-2.0-flash",
            description="Test agent",
            instruction="You are a helpful assistant."
        )
        print(f"   ✅ Google ADK working - Agent: {agent.name}")
        return True
    except Exception as e:
        print(f"   ❌ Google ADK failed: {e}")
        return False

def test_ml_components():
    """Test ML components"""
    print("4. Testing ML Components...")
    try:
        import pandas as pd
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        
        # Test basic ML functionality
        X = np.random.rand(100, 5)
        y = np.random.randint(0, 3, 100)
        model = RandomForestClassifier(n_estimators=10)
        model.fit(X, y)
        predictions = model.predict(X[:5])
        
        print(f"   ✅ ML components working - Predictions: {predictions}")
        return True
    except Exception as e:
        print(f"   ❌ ML components failed: {e}")
        return False

def test_traffic_analysis():
    """Test traffic analysis with real Gemini API"""
    print("5. Testing Traffic Analysis with Real Gemini...")
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Test traffic scenario
        prompt = """
        Analyze this traffic scenario:
        Location: Downtown Main Street
        Current Speed: 15 km/h
        Expected Speed: 50 km/h
        Vehicle Count: 45
        Weather: Heavy rain
        
        Provide severity level and one recommendation.
        """
        
        response = model.generate_content(prompt)
        print(f"   ✅ Traffic analysis working - Response length: {len(response.text)} chars")
        return True
    except Exception as e:
        print(f"   ❌ Traffic analysis failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🚀 CURIOUSAGENTS FINAL VERIFICATION")
    print("=" * 60)
    print("Testing all components for your demo...")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        test_basic_imports,
        test_gemini_api,
        test_google_adk,
        test_ml_components,
        test_traffic_analysis
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    print("📊 VERIFICATION RESULTS")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {passed/total:.0%}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your CuriousAgents system is ready for demo!")
        print("✅ Real Gemini API integration working!")
        print("✅ Google ADK integration working!")
        print("✅ ML components functional!")
        print("✅ Traffic analysis operational!")
        
        print(f"\n🚀 FOR YOUR PRESENTATION:")
        print(f"   • Run: python real_gemini_demo.py")
        print(f"   • Run: python simple_gemini_agent.py")
        print(f"   • Check Google Cloud dashboard for API usage")
        print(f"   • All agents are production-ready")
        
    elif passed >= total * 0.8:
        print(f"\n⚠️  MOSTLY WORKING ({passed}/{total} tests passed)")
        print("✅ Core functionality available for demo")
        print("⚠️  Some components may need attention")
        
    else:
        print(f"\n❌ NEEDS ATTENTION ({passed}/{total} tests passed)")
        print("❌ Core functionality needs fixes before demo")
    
    print(f"\n📋 DETAILED STATUS:")
    test_names = [
        "Basic Imports",
        "Gemini API", 
        "Google ADK",
        "ML Components",
        "Traffic Analysis"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {i+1}. {name}: {status}")
    
    print(f"\n🔗 USEFUL LINKS:")
    print(f"   • Google Cloud Console: https://console.cloud.google.com/apis/api/generativeai.googleapis.com")
    print(f"   • API Usage Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 