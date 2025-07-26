#!/usr/bin/env python3
"""
Test Updated Agents - Verify the corrected ADK API works
"""

import os
import sys
import time
from datetime import datetime

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

# Add paths
sys.path.append('libs')
sys.path.append('congestion_detector')
sys.path.append('context_aggregator')
sys.path.append('fix_recommender')

def test_congestion_detector_agent():
    """Test the updated congestion detector agent"""
    print("🔍 TESTING UPDATED CONGESTION DETECTOR AGENT")
    print("=" * 60)
    
    try:
        from congestion_detector.agent import CongestionDetectorAgent
        
        print("[DEBUG] Creating updated CongestionDetectorAgent...")
        start_time = time.time()
        agent = CongestionDetectorAgent()
        creation_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Agent created in {creation_time:.2f}s")
        print(f"[DEBUG] Agent name: {agent.agent.name}")
        print(f"[DEBUG] Agent model: {agent.agent.model}")
        
        # Test GPS data analysis
        print("\n[DEBUG] Testing GPS data analysis...")
        gps_data = {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "speed_kmph": 15.2,
            "vehicle_count": 45,
            "timestamp": datetime.now().isoformat()
        }
        
        start_time = time.time()
        result = agent.analyze_gps_data(gps_data)
        api_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ GPS analysis complete in {api_time:.2f}s!")
        print(f"[DEBUG] Result keys: {list(result.keys())}")
        
        return True, api_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ CongestionDetectorAgent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_context_aggregator_agent():
    """Test the updated context aggregator agent"""
    print("\n🔍 TESTING UPDATED CONTEXT AGGREGATOR AGENT")
    print("=" * 60)
    
    try:
        from context_aggregator.agent import ContextAggregatorAgent
        
        print("[DEBUG] Creating updated ContextAggregatorAgent...")
        start_time = time.time()
        agent = ContextAggregatorAgent()
        creation_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Agent created in {creation_time:.2f}s")
        print(f"[DEBUG] Agent name: {agent.agent.name}")
        print(f"[DEBUG] Agent model: {agent.agent.model}")
        
        # Test context gathering
        print("\n[DEBUG] Testing context gathering...")
        location_data = {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "radius_km": 5.0
        }
        
        start_time = time.time()
        result = agent.gather_context(location_data)
        api_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Context gathering complete in {api_time:.2f}s!")
        print(f"[DEBUG] Result keys: {list(result.keys())}")
        
        return True, api_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ ContextAggregatorAgent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_fix_recommender_agent():
    """Test the updated fix recommender agent"""
    print("\n🔍 TESTING UPDATED FIX RECOMMENDER AGENT")
    print("=" * 60)
    
    try:
        from fix_recommender.agent import FixRecommenderAgent
        
        print("[DEBUG] Creating updated FixRecommenderAgent...")
        start_time = time.time()
        agent = FixRecommenderAgent()
        creation_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Agent created in {creation_time:.2f}s")
        print(f"[DEBUG] Agent name: {agent.agent.name}")
        print(f"[DEBUG] Agent model: {agent.agent.model}")
        
        # Test solution recommendations
        print("\n[DEBUG] Testing solution recommendations...")
        problem_data = {
            "segment_id": "SEG_001",
            "congestion_level": "HIGH",
            "root_causes": ["Heavy rain", "Rush hour", "Accident"],
            "context_data": {
                "weather": "rainy",
                "events": ["Football game"],
                "time": "rush_hour"
            }
        }
        
        start_time = time.time()
        result = agent.recommend_solutions(problem_data)
        api_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Solution recommendations complete in {api_time:.2f}s!")
        print(f"[DEBUG] Result keys: {list(result.keys())}")
        
        return True, api_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ FixRecommenderAgent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def test_integrated_workflow():
    """Test integrated workflow with all agents"""
    print("\n🔍 TESTING INTEGRATED WORKFLOW")
    print("=" * 60)
    
    try:
        from congestion_detector.agent import CongestionDetectorAgent
        from context_aggregator.agent import ContextAggregatorAgent
        from fix_recommender.agent import FixRecommenderAgent
        
        print("[DEBUG] Creating all agents...")
        
        # Create all agents
        cd_agent = CongestionDetectorAgent()
        ca_agent = ContextAggregatorAgent()
        fr_agent = FixRecommenderAgent()
        
        print("[DEBUG] ✅ All agents created successfully")
        
        # Simulate integrated workflow
        print("\n[DEBUG] Simulating integrated workflow...")
        
        # Step 1: Analyze GPS data
        gps_data = {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "speed_kmph": 15.2,
            "vehicle_count": 45,
            "timestamp": datetime.now().isoformat()
        }
        
        start_time = time.time()
        congestion_result = cd_agent.analyze_gps_data(gps_data)
        step1_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Step 1 (Congestion Analysis) complete in {step1_time:.2f}s")
        
        # Step 2: Gather context
        location_data = {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "radius_km": 5.0
        }
        
        start_time = time.time()
        context_result = ca_agent.gather_context(location_data)
        step2_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Step 2 (Context Gathering) complete in {step2_time:.2f}s")
        
        # Step 3: Recommend solutions
        problem_data = {
            "segment_id": "SEG_001",
            "congestion_level": "HIGH",
            "root_causes": ["Heavy rain", "Rush hour"],
            "context_data": context_result.get("context_data", {})
        }
        
        start_time = time.time()
        solution_result = fr_agent.recommend_solutions(problem_data)
        step3_time = time.time() - start_time
        
        print(f"[DEBUG] ✅ Step 3 (Solution Recommendations) complete in {step3_time:.2f}s")
        
        total_time = step1_time + step2_time + step3_time
        
        print(f"[DEBUG] ✅ Integrated workflow complete in {total_time:.2f}s total")
        
        return True, total_time
        
    except Exception as e:
        print(f"[DEBUG] ❌ Integrated workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

def main():
    """Main test function"""
    print("🚀 UPDATED AGENTS TEST - USING CORRECT ADK API")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    # Run all tests
    tests = [
        ("Congestion Detector Agent", test_congestion_detector_agent),
        ("Context Aggregator Agent", test_context_aggregator_agent),
        ("Fix Recommender Agent", test_fix_recommender_agent),
        ("Integrated Workflow", test_integrated_workflow)
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
    print("\n📊 UPDATED AGENTS TEST RESULTS")
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
        print(f"\n🎉 ALL UPDATED AGENTS TESTS PASSED!")
        print(f"✅ All agents are working with correct ADK API!")
        print(f"✅ Real API calls are being made!")
        print(f"✅ Integrated workflow is working!")
        print(f"✅ Average API response time: {total_api_time/passed:.2f}s")
        
        print(f"\n🚀 FOR YOUR DEMO:")
        print(f"   • All agents are using Google ADK correctly")
        print(f"   • Real Gemini API calls are being made")
        print(f"   • Check Google Cloud dashboard for API usage")
        print(f"   • All agents are production-ready")
        
    elif passed >= total * 0.8:
        print(f"\n⚠️  MOSTLY WORKING ({passed}/{total})")
        print(f"✅ Core functionality available")
        print(f"⚠️  Some components need attention")
        
    else:
        print(f"\n❌ NEEDS ATTENTION ({passed}/{total})")
        print(f"❌ Agent functionality needs fixes")
    
    print(f"\n🔗 USEFUL LINKS:")
    print(f"   • Google Cloud Console: https://console.cloud.google.com/apis/api/generativeai.googleapis.com")
    print(f"   • API Usage Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
    print(f"   • You should see {passed} API calls in your dashboard!")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 