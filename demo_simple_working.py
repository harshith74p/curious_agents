#!/usr/bin/env python3
"""
Simple Working Demo - Direct Gemini API calls without complex dependencies
"""

import os
import sys
import time
import json
import re
from datetime import datetime

# Set up environment
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

def create_simple_agent(name, description, instruction):
    """Create a simple agent using direct Gemini API"""
    try:
        import google.generativeai as genai
        
        # Configure the API
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        
        # Create the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        return {
            "name": name,
            "description": description,
            "instruction": instruction,
            "model": model
        }
    except Exception as e:
        print(f"❌ Failed to create agent {name}: {e}")
        return None

def extract_confidence_and_top_action(response_text):
    """Extract confidence score and top action item from response"""
    confidence = "N/A"
    top_action = "N/A"
    
    # Extract confidence score
    confidence_patterns = [
        r"confidence.*?(\d+\.?\d*)",
        r"confidence.*?(\d+)%",
        r"score.*?(\d+\.?\d*)",
        r"(\d+\.?\d*).*?confidence"
    ]
    
    for pattern in confidence_patterns:
        match = re.search(pattern, response_text.lower())
        if match:
            confidence = match.group(1)
            break
    
    # Extract top action item
    action_patterns = [
        r"immediate.*?action.*?[:|-](.*?)(?:\n|\.)",
        r"top.*?priority.*?[:|-](.*?)(?:\n|\.)",
        r"recommended.*?action.*?[:|-](.*?)(?:\n|\.)",
        r"primary.*?action.*?[:|-](.*?)(?:\n|\.)"
    ]
    
    for pattern in action_patterns:
        match = re.search(pattern, response_text.lower())
        if match:
            top_action = match.group(1).strip()
            break
    
    # If no specific action found, try to extract first bullet point
    if top_action == "N/A":
        bullet_match = re.search(r"•\s*(.*?)(?:\n|\.)", response_text)
        if bullet_match:
            top_action = bullet_match.group(1).strip()
    
    return confidence, top_action

def run_agent(agent, prompt):
    """Run an agent with a prompt"""
    try:
        if not agent:
            return {"error": "Agent not available"}
        
        # Create the full prompt with instruction
        full_prompt = f"""
{agent['instruction']}

{prompt}

Please provide a detailed analysis with clear sections and actionable insights.
IMPORTANT: Include a confidence score (0-1) and clearly identify the top priority action.
"""
        
        print(f"📡 Making API call to {agent['name']}...")
        start_time = time.time()
        
        # Generate response
        response = agent['model'].generate_content(full_prompt)
        
        api_time = time.time() - start_time
        
        print(f"✅ {agent['name']} complete in {api_time:.2f}s!")
        
        # Extract confidence and top action
        confidence, top_action = extract_confidence_and_top_action(response.text)
        
        return {
            "success": True,
            "response": response.text,
            "api_time": api_time,
            "confidence": confidence,
            "top_action": top_action
        }
        
    except Exception as e:
        print(f"❌ {agent['name']} failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "api_time": 0,
            "confidence": "N/A",
            "top_action": "N/A"
        }

def demo_simple_agents():
    """Demo using simple agents with direct Gemini API calls"""
    print("🚀 SIMPLE WORKING AGENTS DEMO")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
    print()
    
    try:
        # Create simple agents
        print("🔍 Creating simple agents...")
        
        congestion_agent = create_simple_agent(
            name="Congestion Detector",
            description="AI agent for detecting traffic congestion patterns",
            instruction="""You are a traffic congestion detection specialist. Your role is to:
            1. Analyze GPS data and traffic patterns to identify congestion levels
            2. Detect patterns in vehicle speed, density, and flow
            3. Identify contributing factors to congestion
            4. Provide real-time congestion assessments
            5. Generate alerts for severe congestion situations
            
            Always provide structured responses with:
            - Congestion level (LOW/MODERATE/HIGH/CRITICAL)
            - Confidence score (0-1)
            - Contributing factors
            - Recommended actions
            - TOP PRIORITY ACTION (clearly marked)"""
        )
        
        context_agent = create_simple_agent(
            name="Context Aggregator",
            description="AI agent for gathering and analyzing contextual information",
            instruction="""You are a context analysis specialist. Your role is to:
            1. Gather information from multiple sources (weather, events, news, social media)
            2. Analyze how external factors affect traffic patterns
            3. Provide comprehensive context analysis
            4. Identify correlations between events and traffic conditions
            5. Generate contextual insights for traffic management
            
            Always provide structured responses with:
            - Weather impact assessment
            - Event analysis
            - News context
            - Social media sentiment
            - Overall context summary
            - TOP PRIORITY INSIGHT (clearly marked)"""
        )
        
        fix_agent = create_simple_agent(
            name="Fix Recommender",
            description="AI agent for recommending traffic solutions",
            instruction="""You are a traffic solution specialist. Your role is to:
            1. Analyze congestion problems and their root causes
            2. Generate specific, actionable recommendations
            3. Provide implementation timelines and cost estimates
            4. Assess expected impact and improvement percentages
            5. Prioritize solutions based on urgency and effectiveness
            
            Always provide structured responses with:
            - Immediate actions (0-1 hour)
            - Short-term solutions (1-24 hours)
            - Long-term improvements (1+ days)
            - Expected impact percentages
            - Implementation requirements
            - TOP PRIORITY ACTION (clearly marked)"""
        )
        
        agents = [congestion_agent, context_agent, fix_agent]
        valid_agents = [a for a in agents if a is not None]
        
        print(f"✅ Successfully created {len(valid_agents)} agents!")
        for agent in valid_agents:
            print(f"   • {agent['name']}")
        
        # Test scenarios
        scenarios = [
            {
                "name": "Congestion Analysis",
                "agent": congestion_agent,
                "prompt": """
                Analyze this traffic scenario for congestion:
                
                Location: Downtown Main Street, NYC
                Current Speed: 15 km/h (expected: 50 km/h)
                Vehicle Count: 45
                Weather: Heavy rain, 18°C, 75% humidity
                Time: Rush hour (8:30 AM)
                Events: Football game at stadium (50,000 attendees)
                
                Provide detailed analysis with:
                1. Congestion level assessment
                2. Root causes
                3. Contributing factors
                4. Immediate recommendations
                5. TOP PRIORITY ACTION (most critical action needed)
                """
            },
            {
                "name": "Context Analysis",
                "agent": context_agent,
                "prompt": """
                Analyze this traffic context:
                
                Location: Downtown Main Street, NYC
                Weather: Heavy rain, 18°C, 75% humidity
                Events: Football game at stadium (50,000 attendees)
                News: Major construction project announced
                Time: Rush hour (8:30 AM)
                
                Provide comprehensive context analysis including:
                1. Weather impact on traffic
                2. Event-related traffic patterns
                3. News context affecting traffic
                4. Overall traffic context assessment
                5. TOP PRIORITY INSIGHT (most critical factor)
                """
            },
            {
                "name": "Solution Recommendations",
                "agent": fix_agent,
                "prompt": """
                Based on this traffic situation, provide solutions:
                
                Location: Downtown Main Street, NYC
                Congestion Level: HIGH
                Weather: Heavy rain
                Contributing Factors: Rush hour, weather, high vehicle density, football game
                Context: Major construction project announced
                
                Provide comprehensive recommendations including:
                1. Immediate actions (0-1 hour) with expected impact
                2. Short-term solutions (1-24 hours) with implementation steps
                3. Long-term improvements (1+ days) with cost estimates
                4. Priority ranking and expected improvement percentages
                5. TOP PRIORITY ACTION (most critical solution)
                """
            }
        ]
        
        results = []
        total_api_time = 0
        
        for scenario in scenarios:
            print(f"\n{'='*20} {scenario['name']} {'='*20}")
            
            if not scenario['agent']:
                print(f"❌ {scenario['name']} skipped - agent not available")
                results.append((scenario['name'], False, 0, "N/A", "N/A"))
                continue
            
            result = run_agent(scenario['agent'], scenario['prompt'])
            
            if result['success']:
                print(f"✅ Response length: {len(result['response'])} characters")
                print(f"✅ Processing time: {result['api_time']:.2f}s")
                
                # Highlight confidence and top action
                print(f"\n🎯 KEY INSIGHTS:")
                print(f"   • Confidence Score: {result['confidence']}")
                print(f"   • Top Priority Action: {result['top_action']}")
                
                print(f"\n📊 FULL ANALYSIS OUTPUT:")
                print("=" * 60)
                print(result['response'])
                print("=" * 60)
                
                results.append((scenario['name'], True, result['api_time'], result['confidence'], result['top_action']))
                total_api_time += result['api_time']
            else:
                print(f"❌ Error: {result['error']}")
                results.append((scenario['name'], False, 0, "N/A", "N/A"))
        
        # Summary
        print("\n📊 SIMPLE DEMO RESULTS")
        print("=" * 80)
        
        passed = sum(1 for _, success, _, _, _ in results if success)
        total = len(results)
        
        print(f"Total Scenarios: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {passed/total:.0%}")
        print(f"Total API Time: {total_api_time:.2f} seconds")
        print(f"Average API Time: {total_api_time/passed:.2f} seconds" if passed > 0 else "No successful API calls")
        
        print(f"\n📋 DETAILED RESULTS:")
        for scenario_name, success, api_time, confidence, top_action in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   • {scenario_name}: {status} ({api_time:.2f}s)")
            if success:
                print(f"     - Confidence: {confidence}")
                print(f"     - Top Action: {top_action}")
        
        if passed == total:
            print(f"\n🎉 ALL SCENARIOS PASSED!")
            print(f"✅ Simple agents are working perfectly!")
            print(f"✅ Real Gemini API calls are being made!")
            print(f"✅ Confidence scores and top actions highlighted!")
            print(f"✅ Average API response time: {total_api_time/passed:.2f}s")
            
            print(f"\n🚀 FOR YOUR DEMO:")
            print(f"   • Simple, reliable agent implementation")
            print(f"   • Direct Gemini API integration")
            print(f"   • Confidence scores and priority actions")
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
        print(f"❌ Simple demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_simple_agents()
    sys.exit(0 if success else 1) 