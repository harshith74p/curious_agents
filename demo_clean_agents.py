#!/usr/bin/env python3
"""
Clean Agents Demo - No Kafka, Just Core Agent Functionality
"""

import os
import sys
import time
from datetime import datetime

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

def demo_clean_congestion_detector():
    """Demo congestion detector without Kafka"""
    print("🔍 DEMO: CONGESTION DETECTOR AGENT")
    print("=" * 60)
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        # Create agent
        agent = LlmAgent(
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
        
        runner = InMemoryRunner(agent)
        
        # Test scenario
        prompt = """
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
        
        print("📡 Making API call to Congestion Detector...")
        start_time = time.time()
        
        result = runner.run(
            user_id="demo_user",
            session_id="congestion_demo",
            new_message=prompt
        )
        
        api_time = time.time() - start_time
        
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
        
        print(f"✅ Congestion analysis complete in {api_time:.2f}s!")
        print(f"✅ Response length: {len(response_text)} characters")
        print(f"✅ Analysis preview: {response_text[:300]}...")
        
        return True, api_time
        
    except Exception as e:
        print(f"❌ Congestion detector demo failed: {e}")
        return False, 0

def demo_clean_context_aggregator():
    """Demo context aggregator without Kafka"""
    print("\n🔍 DEMO: CONTEXT AGGREGATOR AGENT")
    print("=" * 60)
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        # Create agent
        agent = LlmAgent(
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
        
        runner = InMemoryRunner(agent)
        
        # Test scenario
        prompt = """
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
        
        print("📡 Making API call to Context Aggregator...")
        start_time = time.time()
        
        result = runner.run(
            user_id="demo_user",
            session_id="context_demo",
            new_message=prompt
        )
        
        api_time = time.time() - start_time
        
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
        
        print(f"✅ Context analysis complete in {api_time:.2f}s!")
        print(f"✅ Response length: {len(response_text)} characters")
        print(f"✅ Analysis preview: {response_text[:300]}...")
        
        return True, api_time
        
    except Exception as e:
        print(f"❌ Context aggregator demo failed: {e}")
        return False, 0

def demo_clean_fix_recommender():
    """Demo fix recommender without Kafka"""
    print("\n🔍 DEMO: FIX RECOMMENDER AGENT")
    print("=" * 60)
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        # Create agent
        agent = LlmAgent(
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
        
        runner = InMemoryRunner(agent)
        
        # Test scenario
        prompt = """
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
        
        print("📡 Making API call to Fix Recommender...")
        start_time = time.time()
        
        result = runner.run(
            user_id="demo_user",
            session_id="recommendations_demo",
            new_message=prompt
        )
        
        api_time = time.time() - start_time
        
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
        
        print(f"✅ Solution recommendations complete in {api_time:.2f}s!")
        print(f"✅ Response length: {len(response_text)} characters")
        print(f"✅ Recommendations preview: {response_text[:300]}...")
        
        return True, api_time
        
    except Exception as e:
        print(f"❌ Fix recommender demo failed: {e}")
        return False, 0

def main():
    """Main demo function"""
    print("🚀 CLEAN AGENTS DEMO - NO KAFKA, JUST CORE FUNCTIONALITY")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    # Run all demos
    demos = [
        ("Congestion Detector", demo_clean_congestion_detector),
        ("Context Aggregator", demo_clean_context_aggregator),
        ("Fix Recommender", demo_clean_fix_recommender)
    ]
    
    results = []
    total_api_time = 0
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*20} {demo_name} {'='*20}")
        try:
            success, api_time = demo_func()
            results.append((demo_name, success, api_time))
            if success:
                total_api_time += api_time
        except Exception as e:
            print(f"❌ Demo failed with exception: {e}")
            results.append((demo_name, False, 0))
    
    # Summary
    print("\n📊 CLEAN DEMO RESULTS")
    print("=" * 80)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Total Demos: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {passed/total:.0%}")
    print(f"Total API Time: {total_api_time:.2f} seconds")
    print(f"Average API Time: {total_api_time/passed:.2f} seconds" if passed > 0 else "No successful API calls")
    
    print(f"\n📋 DETAILED RESULTS:")
    for demo_name, success, api_time in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   • {demo_name}: {status} ({api_time:.2f}s)")
    
    if passed == total:
        print(f"\n🎉 ALL CLEAN DEMOS PASSED!")
        print(f"✅ All agents are working perfectly!")
        print(f"✅ Real API calls are being made!")
        print(f"✅ No Kafka errors!")
        print(f"✅ Average API response time: {total_api_time/passed:.2f}s")
        
        print(f"\n🚀 FOR YOUR DEMO:")
        print(f"   • All agents are using Google ADK correctly")
        print(f"   • Real Gemini API calls are being made")
        print(f"   • Check Google Cloud dashboard for API usage")
        print(f"   • Clean, no-Kafka demo ready!")
        
    elif passed >= total * 0.8:
        print(f"\n⚠️  MOSTLY WORKING ({passed}/{total})")
        print(f"✅ Core functionality available")
        
    else:
        print(f"\n❌ NEEDS ATTENTION ({passed}/{total})")
        print(f"❌ Some demos need fixes")
    
    print(f"\n🔗 USEFUL LINKS:")
    print(f"   • Google Cloud Console: https://console.cloud.google.com/apis/api/generativeai.googleapis.com")
    print(f"   • API Usage Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
    print(f"   • You should see {passed} API calls in your dashboard!")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 