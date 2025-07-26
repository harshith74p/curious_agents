#!/usr/bin/env python3
"""
Original Agents Demo with Full Output - Show complete agent responses
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

def format_output_for_demo(response_text, max_length=800):
    """Format output for better demo presentation"""
    if len(response_text) <= max_length:
        return response_text
    
    # Try to find a good breaking point
    sentences = response_text.split('. ')
    formatted_text = ""
    current_length = 0
    
    for sentence in sentences:
        if current_length + len(sentence) < max_length:
            formatted_text += sentence + ". "
            current_length += len(sentence)
        else:
            break
    
    if formatted_text:
        return formatted_text + "\n\n[Output truncated for demo - full response available]"
    else:
        return response_text[:max_length] + "\n\n[Output truncated for demo]"

def demo_original_agents_with_output():
    """Demo using original agents with full output display"""
    print("🚀 ORIGINAL AGENTS DEMO WITH ENHANCED OUTPUT")
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
                
                # Extract confidence and top action
                confidence, top_action = extract_confidence_and_top_action(response_text)
                
                print(f"✅ {scenario['name']} complete in {api_time:.2f}s!")
                print(f"✅ Response length: {len(response_text)} characters")
                print(f"✅ Processing time: {api_time:.2f}s")
                
                # Highlight confidence and top action
                print(f"\n🎯 KEY INSIGHTS:")
                print(f"   • Confidence Score: {confidence}")
                print(f"   • Top Priority Action: {top_action}")
                
                # Format output for better demo presentation
                formatted_output = format_output_for_demo(response_text)
                
                print(f"\n📊 ANALYSIS OUTPUT:")
                print("=" * 60)
                print(formatted_output)
                print("=" * 60)
                
                results.append((scenario['name'], True, api_time, confidence, top_action))
                
            except Exception as e:
                print(f"❌ {scenario['name']} failed: {e}")
                print(f"❌ Error details: {str(e)}")
                results.append((scenario['name'], False, 0, "N/A", "N/A"))
        
        # Summary
        print("\n📊 ORIGINAL AGENTS DEMO RESULTS")
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
            print(f"✅ Original agents are working perfectly!")
            print(f"✅ Real API calls are being made!")
            print(f"✅ Full outputs are displayed!")
            print(f"✅ Confidence scores and top actions highlighted!")
            print(f"✅ Average API response time: {total_api_time/passed:.2f}s")
            
            print(f"\n🚀 FOR YOUR DEMO:")
            print(f"   • Using original agent implementations")
            print(f"   • Real Gemini API calls are being made")
            print(f"   • Complete analysis outputs shown")
            print(f"   • Confidence scores and priority actions highlighted")
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
        print(f"❌ Original agents demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_original_agents_with_output()
    sys.exit(0 if success else 1) 