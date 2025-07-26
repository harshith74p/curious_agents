#!/usr/bin/env python3
"""
Direct Gemini API Demo - Bypass ADK runner issues
"""

import os
import sys
import time
from datetime import datetime

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

def demo_direct_gemini():
    """Demo using direct Gemini API calls"""
    print("🚀 DIRECT GEMINI API DEMO - CLEAN & RELIABLE")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        
        # Create model
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("✅ Gemini model created successfully!")
        
        # Test scenarios
        scenarios = [
            {
                "name": "Congestion Analysis",
                "prompt": """
                You are a traffic congestion detection specialist. 
                Analyze this traffic scenario for congestion:
                
                Location: Downtown Main Street
                Current Speed: 15 km/h (expected: 50 km/h)
                Vehicle Count: 45
                Weather: Heavy rain
                Time: Rush hour (8:30 AM)
                
                Provide detailed analysis with:
                1. Congestion level assessment (LOW/MODERATE/HIGH/CRITICAL)
                2. Root causes
                3. Contributing factors
                4. Immediate recommendations
                5. Confidence score (0-1)
                """
            },
            {
                "name": "Context Analysis",
                "prompt": """
                You are a context analysis specialist for traffic management.
                Analyze this traffic context:
                
                Location: Downtown Main Street
                Weather: Heavy rain, 18°C, 75% humidity
                Events: Football game at stadium (50,000 attendees)
                News: Major construction project announced
                Time: Rush hour (8:30 AM)
                
                Provide comprehensive context analysis including:
                1. Weather impact on traffic
                2. Event-related traffic patterns
                3. News context affecting traffic
                4. Overall traffic context assessment
                5. Impact severity (LOW/MEDIUM/HIGH)
                """
            },
            {
                "name": "Solution Recommendations",
                "prompt": """
                You are a traffic solution specialist.
                Based on this traffic situation, provide solutions:
                
                Location: Downtown Main Street
                Congestion Level: HIGH
                Weather: Heavy rain
                Contributing Factors: Rush hour, weather, high vehicle density, football game
                Context: Major construction project announced
                
                Provide comprehensive recommendations including:
                1. Immediate actions (0-1 hour) with expected impact
                2. Short-term solutions (1-24 hours) with implementation steps
                3. Long-term improvements (1+ days) with cost estimates
                4. Priority ranking and expected improvement percentages
                5. Risk assessment for each recommendation
                """
            }
        ]
        
        results = []
        total_api_time = 0
        
        for scenario in scenarios:
            print(f"\n{'='*20} {scenario['name']} {'='*20}")
            
            try:
                print(f"📡 Making direct Gemini API call...")
                start_time = time.time()
                
                response = model.generate_content(scenario['prompt'])
                
                api_time = time.time() - start_time
                total_api_time += api_time
                
                print(f"✅ {scenario['name']} complete in {api_time:.2f}s!")
                print(f"✅ Response length: {len(response.text)} characters")
                print(f"✅ Analysis preview: {response.text[:300]}...")
                
                results.append((scenario['name'], True, api_time))
                
            except Exception as e:
                print(f"❌ {scenario['name']} failed: {e}")
                results.append((scenario['name'], False, 0))
        
        # Summary
        print("\n📊 DIRECT GEMINI DEMO RESULTS")
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
            print(f"✅ Direct Gemini API calls working perfectly!")
            print(f"✅ Real API calls are being made!")
            print(f"✅ No ADK runner issues!")
            print(f"✅ Average API response time: {total_api_time/passed:.2f}s")
            
            print(f"\n🚀 FOR YOUR DEMO:")
            print(f"   • Direct Gemini API integration")
            print(f"   • Real API calls are being made")
            print(f"   • Check Google Cloud dashboard for API usage")
            print(f"   • Clean, reliable demo ready!")
            
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
    success = demo_direct_gemini()
    sys.exit(0 if success else 1) 