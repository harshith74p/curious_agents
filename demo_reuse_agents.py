#!/usr/bin/env python3
"""
Demo Reuse Agents - Reuse existing agents instead of recreating
"""

import os
import sys
import time
from datetime import datetime

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

def demo_reuse_agents():
    """Demo using existing agents without recreating them"""
    print("🚀 DEMO: REUSE EXISTING AGENTS")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    try:
        # Import existing agents (reuse them)
        print("🔍 Importing existing agents...")
        
        # Import the existing agents from their modules
        sys.path.append('congestion_detector')
        sys.path.append('context_aggregator')
        sys.path.append('fix_recommender')
        
        from congestion_detector.agent import CongestionDetectorAgent
        from context_aggregator.agent import ContextAggregatorAgent
        from fix_recommender.agent import FixRecommenderAgent
        
        # Create agent instances
        congestion_agent = CongestionDetectorAgent()
        context_agent = ContextAggregatorAgent()
        fix_agent = FixRecommenderAgent()
        
        print("✅ Successfully imported existing agents!")
        print(f"   • Congestion Detector: {congestion_agent.agent.name}")
        print(f"   • Context Aggregator: {context_agent.agent.name}")
        print(f"   • Fix Recommender: {fix_agent.agent.name}")
        
        # Test scenarios using existing agents
        scenarios = [
            {
                "name": "Congestion Analysis",
                "agent": congestion_agent,
                "method": "analyze_gps_data",
                "data": {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "speed_kmph": 15,
                    "vehicle_count": 45,
                    "timestamp": "2024-01-15T08:30:00",
                    "weather": "heavy_rain",
                    "temperature": 18,
                    "humidity": 75
                }
            },
            {
                "name": "Context Analysis",
                "agent": context_agent,
                "method": "gather_context",
                "data": {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "radius_km": 5.0,
                    "weather": "heavy_rain",
                    "events": ["football_game"],
                    "news": ["construction_project"]
                }
            },
            {
                "name": "Solution Recommendations",
                "agent": fix_agent,
                "method": "recommend_solutions",
                "data": {
                    "segment_id": "downtown_main_street",
                    "congestion_level": "HIGH",
                    "root_causes": ["rush_hour", "weather", "high_density", "football_game"],
                    "context_data": {
                        "weather": "heavy_rain",
                        "events": ["football_game"],
                        "construction": "major_project_announced"
                    }
                }
            }
        ]
        
        results = []
        total_api_time = 0
        
        for scenario in scenarios:
            print(f"\n{'='*20} {scenario['name']} {'='*20}")
            
            try:
                # Use the existing agent through its specific method
                agent = scenario['agent']
                method_name = scenario['method']
                data = scenario['data']
                
                print(f"📡 Making API call to {agent.agent.name} using {method_name}...")
                start_time = time.time()
                
                # Call the specific method on the agent
                method = getattr(agent, method_name)
                result = method(data)
                
                api_time = time.time() - start_time
                total_api_time += api_time
                
                # Extract response
                if isinstance(result, dict):
                    response_text = str(result)
                elif hasattr(result, 'text'):
                    response_text = result.text
                elif hasattr(result, 'content'):
                    response_text = result.content
                elif hasattr(result, '__iter__'):
                    try:
                        response_text = ''.join(result)
                    except:
                        response_text = str(result)
                else:
                    response_text = str(result)
                
                print(f"✅ {scenario['name']} complete in {api_time:.2f}s!")
                print(f"✅ Response length: {len(response_text)} characters")
                print(f"✅ Processing time: {api_time:.2f}s")
                
                print(f"\n📊 FULL ANALYSIS OUTPUT:")
                print("=" * 60)
                print(response_text)
                print("=" * 60)
                
                results.append((scenario['name'], True, api_time))
                
            except Exception as e:
                print(f"❌ {scenario['name']} failed: {e}")
                print(f"❌ Error details: {str(e)}")
                results.append((scenario['name'], False, 0))
        
        # Summary
        print("\n📊 REUSE AGENTS DEMO RESULTS")
        print("=" * 80)
        
        passed = sum(1 for _, success, _ in results if success)
        total = len(results)
        
        print(f"Total Scenarios: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {passed/total:.0%}")
        print(f"Total API Time: {total_api_time:.2f} seconds")
        print(f"Average API Time: {total_api_time/passed:.2f} seconds" if passed > 0 else "No successful API calls")
        
        print(f"\n📋 DETAILED RESULTS:")
        for scenario_name, success, api_time in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   • {scenario_name}: {status} ({api_time:.2f}s)")
        
        if passed == total:
            print(f"\n🎉 ALL SCENARIOS PASSED!")
            print(f"✅ Existing agents are working perfectly!")
            print(f"✅ Real API calls are being made!")
            print(f"✅ No agent recreation needed!")
            print(f"✅ Full outputs are displayed!")
            print(f"✅ Average API response time: {total_api_time/passed:.2f}s")
            
            print(f"\n🚀 FOR YOUR DEMO:")
            print(f"   • Reusing existing agents efficiently")
            print(f"   • Real Gemini API calls are being made")
            print(f"   • Complete analysis outputs shown")
            print(f"   • Check Google Cloud dashboard for API usage")
            print(f"   • Clean, efficient demo ready!")
            
        elif passed >= total * 0.8:
            print(f"\n⚠️  MOSTLY WORKING ({passed}/{total})")
            print(f"✅ Core functionality available")
            
        else:
            print(f"\n❌ NEEDS ATTENTION ({passed}/{total})")
            print(f"❌ Some scenarios need fixes")
        
        print(f"\n🔗 USEFUL LINKS:")
        print(f"   • Google Cloud Console: https://console.cloud.google.com/apis/api/generativeai.googleapis.com")
        print(f"   • API Usage Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
        print(f"   • You should see {passed} API calls in your dashboard!")
        
        return passed == total
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_reuse_agents()
    sys.exit(0 if success else 1) 