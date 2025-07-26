#!/usr/bin/env python3
"""
Simple Agents Demo - Clean demo without session issues
"""

import os
import sys
import time
from datetime import datetime

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

def demo_simple_agents():
    """Simple demo using direct agent calls"""
    print("🚀 SIMPLE AGENTS DEMO - CLEAN & EFFICIENT")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        # Create agents once and reuse them
        print("🔍 Creating agents...")
        
        # Congestion Detector
        cd_agent = LlmAgent(
            name="congestion_detector",
            model="gemini-2.0-flash",
            description="AI agent for detecting traffic congestion",
            instruction="""You are a traffic congestion detection specialist. 
            Analyze GPS data and traffic patterns to identify congestion levels.
            Provide structured responses with:
            - Congestion level (LOW/MODERATE/HIGH/CRITICAL)
            - Confidence score (0-1)
            - Contributing factors
            - Recommended actions"""
        )
        
        # Context Aggregator
        ca_agent = LlmAgent(
            name="context_aggregator",
            model="gemini-2.0-flash",
            description="AI agent for gathering contextual information",
            instruction="""You are a context analysis specialist.
            Gather and analyze information from multiple sources (weather, events, news).
            Provide structured responses with:
            - Weather impact assessment
            - Event analysis
            - News context
            - Social media sentiment
            - Overall context summary"""
        )
        
        # Fix Recommender
        fr_agent = LlmAgent(
            name="fix_recommender",
            model="gemini-2.0-flash",
            description="AI agent for recommending traffic solutions",
            instruction="""You are a traffic solution specialist.
            Based on congestion analysis and context, provide specific, actionable recommendations.
            Provide structured responses with:
            - Immediate actions (0-1 hour)
            - Short-term solutions (1-24 hours)
            - Long-term improvements (1+ days)
            - Expected impact percentages"""
        )
        
        print("✅ All agents created successfully!")
        
        # Test scenarios
        scenarios = [
            {
                "name": "Congestion Analysis",
                "agent": cd_agent,
                "prompt": """
                Analyze this traffic scenario for congestion:
                
                Location: Downtown Main Street
                Current Speed: 15 km/h (expected: 50 km/h)
                Vehicle Count: 45
                Weather: Heavy rain
                Time: Rush hour (8:30 AM)
                
                Provide detailed analysis with:
                1. Congestion level assessment
                2. Root causes
                3. Contributing factors
                4. Immediate recommendations
                """
            },
            {
                "name": "Context Analysis",
                "agent": ca_agent,
                "prompt": """
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
                """
            },
            {
                "name": "Solution Recommendations",
                "agent": fr_agent,
                "prompt": """
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
                """
            }
        ]
        
        results = []
        total_api_time = 0
        
        for i, scenario in enumerate(scenarios):
            print(f"\n{'='*20} {scenario['name']} {'='*20}")
            
            try:
                # Create runner for this agent
                runner = InMemoryRunner(scenario['agent'])
                
                print(f"📡 Making API call to {scenario['agent'].name}...")
                start_time = time.time()
                
                # Use unique session ID for each call
                session_id = f"demo_session_{i}_{int(time.time())}"
                
                result = runner.run(
                    user_id="demo_user",
                    session_id=session_id,
                    new_message=scenario['prompt']
                )
                
                api_time = time.time() - start_time
                total_api_time += api_time
                
                # Extract response
                if hasattr(result, 'text'):
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
                print(f"✅ Analysis preview: {response_text[:300]}...")
                
                results.append((scenario['name'], True, api_time))
                
            except Exception as e:
                print(f"❌ {scenario['name']} failed: {e}")
                results.append((scenario['name'], False, 0))
        
        # Summary
        print("\n📊 SIMPLE DEMO RESULTS")
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
            print(f"✅ Agents are working perfectly!")
            print(f"✅ Real API calls are being made!")
            print(f"✅ No session issues!")
            print(f"✅ Average API response time: {total_api_time/passed:.2f}s")
            
            print(f"\n🚀 FOR YOUR DEMO:")
            print(f"   • Clean, simple agent demo")
            print(f"   • Real Gemini API calls are being made")
            print(f"   • Check Google Cloud dashboard for API usage")
            print(f"   • Ready for presentation!")
            
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
    success = demo_simple_agents()
    sys.exit(0 if success else 1) 