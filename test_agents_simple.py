#!/usr/bin/env python3
"""
Simple Test for Agents - Test each agent individually
"""

import os
import sys
import time
from datetime import datetime

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

def test_congestion_agent():
    """Test the congestion detector agent"""
    print("🔍 Testing Congestion Detector Agent...")
    
    try:
        sys.path.append('congestion_detector')
        from congestion_detector.agent import CongestionDetectorAgent
        
        agent = CongestionDetectorAgent()
        
        # Test data
        gps_data = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "speed_kmph": 15,
            "vehicle_count": 45,
            "timestamp": "2024-01-15T08:30:00",
            "weather": "heavy_rain",
            "temperature": 18,
            "humidity": 75
        }
        
        print("📡 Making API call to congestion detector...")
        start_time = time.time()
        
        result = agent.analyze_gps_data(gps_data)
        
        api_time = time.time() - start_time
        
        print(f"✅ Congestion analysis complete in {api_time:.2f}s!")
        print(f"✅ Result: {result}")
        
        return True, api_time
        
    except Exception as e:
        print(f"❌ Congestion agent failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_context_agent():
    """Test the context aggregator agent"""
    print("🔍 Testing Context Aggregator Agent...")
    
    try:
        sys.path.append('context_aggregator')
        from context_aggregator.agent import ContextAggregatorAgent
        
        agent = ContextAggregatorAgent()
        
        # Test data
        location_data = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "radius_km": 5.0,
            "weather": "heavy_rain",
            "events": ["football_game"],
            "news": ["construction_project"]
        }
        
        print("📡 Making API call to context aggregator...")
        start_time = time.time()
        
        result = agent.gather_context(location_data)
        
        api_time = time.time() - start_time
        
        print(f"✅ Context analysis complete in {api_time:.2f}s!")
        print(f"✅ Result: {result}")
        
        return True, api_time
        
    except Exception as e:
        print(f"❌ Context agent failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_fix_agent():
    """Test the fix recommender agent"""
    print("🔍 Testing Fix Recommender Agent...")
    
    try:
        sys.path.append('fix_recommender')
        from fix_recommender.agent import FixRecommenderAgent
        
        agent = FixRecommenderAgent()
        
        # Test data
        problem_data = {
            "segment_id": "downtown_main_street",
            "congestion_level": "HIGH",
            "root_causes": ["rush_hour", "weather", "high_density", "football_game"],
            "context_data": {
                "weather": "heavy_rain",
                "events": ["football_game"],
                "construction": "major_project_announced"
            }
        }
        
        print("📡 Making API call to fix recommender...")
        start_time = time.time()
        
        result = agent.recommend_solutions(problem_data)
        
        api_time = time.time() - start_time
        
        print(f"✅ Solution recommendations complete in {api_time:.2f}s!")
        print(f"✅ Result: {result}")
        
        return True, api_time
        
    except Exception as e:
        print(f"❌ Fix agent failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def main():
    """Run all agent tests"""
    print("🚀 SIMPLE AGENT TESTS")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    tests = [
        ("Congestion Detector", test_congestion_agent),
        ("Context Aggregator", test_context_agent),
        ("Fix Recommender", test_fix_agent)
    ]
    
    results = []
    total_api_time = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        success, api_time = test_func()
        results.append((test_name, success, api_time))
        
        if success:
            total_api_time += api_time
    
    # Summary
    print("\n📊 TEST RESULTS")
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
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"✅ All agents are working correctly!")
        print(f"✅ Real Gemini API calls are being made!")
        print(f"✅ Average API response time: {total_api_time/passed:.2f}s")
        
    elif passed >= total * 0.8:
        print(f"\n⚠️  MOSTLY WORKING ({passed}/{total})")
        print(f"✅ Core functionality available")
        
    else:
        print(f"\n❌ NEEDS ATTENTION ({passed}/{total})")
        print(f"❌ Some agents need fixes")
    
    print(f"\n🔗 USEFUL LINKS:")
    print(f"   • Google Cloud Console: https://console.cloud.google.com/apis/api/generativeai.googleapis.com")
    print(f"   • API Usage Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
    print(f"   • You should see {passed} API calls in your dashboard!")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 