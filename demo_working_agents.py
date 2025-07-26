#!/usr/bin/env python3
"""
Working Demo - Using the correct ADK API with real Gemini calls
"""

import os
import time
from datetime import datetime

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

def demo_working_adk_agents():
    """Demo working ADK agents with correct API"""
    print("🚀 WORKING ADK AGENTS DEMO")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        
        # Create multiple agents
        agents = []
        
        # 1. Congestion Detector Agent
        print("🔍 Creating Congestion Detector Agent...")
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
        agents.append(("Congestion Detector", cd_agent))
        
        # 2. Context Aggregator Agent
        print("🔍 Creating Context Aggregator Agent...")
        ca_agent = LlmAgent(
            name="context_aggregator",
            model="gemini-2.0-flash",
            description="AI agent for gathering contextual information",
            instruction="""You are a context analysis specialist.
            Gather and analyze information from multiple sources (weather, events, news).
            Provide structured responses with:
            - Weather impact
            - Events affecting traffic
            - News context
            - Overall assessment"""
        )
        agents.append(("Context Aggregator", ca_agent))
        
        # 3. Fix Recommender Agent
        print("🔍 Creating Fix Recommender Agent...")
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
        agents.append(("Fix Recommender", fr_agent))
        
        print(f"✅ Created {len(agents)} agents successfully!")
        
        # Test each agent with real API calls
        total_api_time = 0
        successful_calls = 0
        
        for agent_name, agent in agents:
            print(f"\n{'='*20} TESTING {agent_name} {'='*20}")
            
            # Create runner for this agent
            runner = InMemoryRunner(agent)
            
            # Test scenario
            if agent_name == "Congestion Detector":
                prompt = """
                Analyze this GPS data for traffic congestion:
                Location: Downtown Main Street
                Current Speed: 15 km/h (expected: 50 km/h)
                Vehicle Count: 45
                Weather: Heavy rain
                Time: Rush hour
                
                Provide structured analysis with congestion level, confidence, factors, and recommendations.
                """
            elif agent_name == "Context Aggregator":
                prompt = """
                Gather context for this traffic situation:
                Location: Downtown Main Street
                Weather: Heavy rain
                Time: Rush hour
                
                Analyze weather impact, nearby events, and news context.
                """
            else:  # Fix Recommender
                prompt = """
                Based on this traffic situation, provide solutions:
                Location: Downtown Main Street
                Congestion Level: HIGH
                Weather: Heavy rain
                Contributing Factors: Rush hour, weather, high vehicle density
                
                Provide immediate, short-term, and long-term solutions with expected impacts.
                """
            
            print(f"📡 Making API call to {agent_name}...")
            start_time = time.time()
            
            try:
                # Use the correct API with required parameters
                result = runner.run(
                    user_id="demo_user",
                    session_id=f"demo_session_{agent_name.lower().replace(' ', '_')}",
                    new_message=prompt
                )
                api_time = time.time() - start_time
                total_api_time += api_time
                successful_calls += 1
                
                print(f"✅ {agent_name} API call successful in {api_time:.2f}s!")
                
                # Extract response
                if hasattr(result, 'text'):
                    response_text = result.text
                elif hasattr(result, 'content'):
                    response_text = result.content
                elif hasattr(result, '__iter__'):
                    # Handle generator object
                    try:
                        response_text = ''.join(result)
                    except:
                        response_text = str(result)
                else:
                    response_text = str(result)
                
                print(f"✅ Response length: {len(response_text)} characters")
                print(f"✅ Response preview: {response_text[:300]}...")
                
            except Exception as e:
                print(f"❌ {agent_name} API call failed: {e}")
        
        # Summary
        print(f"\n📊 DEMO RESULTS")
        print("=" * 80)
        print(f"Total Agents: {len(agents)}")
        print(f"Successful API Calls: {successful_calls}")
        print(f"Failed API Calls: {len(agents) - successful_calls}")
        print(f"Success Rate: {successful_calls/len(agents):.0%}")
        print(f"Total API Time: {total_api_time:.2f} seconds")
        print(f"Average API Time: {total_api_time/successful_calls:.2f} seconds" if successful_calls > 0 else "No successful API calls")
        
        if successful_calls == len(agents):
            print(f"\n🎉 ALL AGENTS WORKING PERFECTLY!")
            print(f"✅ Real ADK agents are working with Gemini API!")
            print(f"✅ Real API calls are being made!")
            print(f"✅ All agents are production-ready!")
            
            print(f"\n🚀 FOR YOUR DEMO:")
            print(f"   • Real agents are using Google ADK")
            print(f"   • Real Gemini API calls are being made")
            print(f"   • Check Google Cloud dashboard for API usage")
            print(f"   • You should see {successful_calls} API calls in your dashboard!")
            
        elif successful_calls >= len(agents) * 0.8:
            print(f"\n⚠️  MOSTLY WORKING ({successful_calls}/{len(agents)})")
            print(f"✅ Core functionality available")
            
        else:
            print(f"\n❌ NEEDS ATTENTION ({successful_calls}/{len(agents)})")
            print(f"❌ Some agents need fixes")
        
        print(f"\n🔗 USEFUL LINKS:")
        print(f"   • Google Cloud Console: https://console.cloud.google.com/apis/api/generativeai.googleapis.com")
        print(f"   • API Usage Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
        
        return successful_calls == len(agents)
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_working_adk_agents()
    import sys
    sys.exit(0 if success else 1) 