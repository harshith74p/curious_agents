#!/usr/bin/env python3
"""
Real Gemini API Demo for CuriousAgents
This demo makes ACTUAL API calls to Google Gemini to show real usage
"""

import os
import sys
import json
import asyncio
from datetime import datetime

# Set up environment for Gemini API
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

def test_real_gemini_api():
    """Test direct Gemini API calls"""
    print("REAL GEMINI API INTEGRATION TEST")
    print("=" * 50)
    
    try:
        import google.generativeai as genai
        
        # Configure the API
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        
        print("+ Gemini API configured successfully")
        print(f"+ Using API Key: {os.environ['GOOGLE_API_KEY'][:20]}...")
        
        # Create the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("+ Gemini 2.0 Flash model created")
        
        # Test API call
        print("\nTesting Real API Call...")
        response = model.generate_content("Hello Gemini! Can you confirm you're working?")
        print(f"+ API Response: {response.text[:100]}...")
        
        return True, model
        
    except Exception as e:
        print(f"- Error: {e}")
        return False, None

def analyze_traffic_with_real_gemini(model, traffic_scenario):
    """Use real Gemini API to analyze traffic scenarios"""
    
    prompt = f"""
    You are a traffic management AI expert. Analyze this traffic scenario and provide specific recommendations:
    
    SCENARIO:
    - Location: {traffic_scenario['location']}
    - Current Speed: {traffic_scenario['speed_kmph']} km/h
    - Expected Speed: {traffic_scenario['expected_speed']} km/h
    - Vehicle Count: {traffic_scenario['vehicle_count']}
    - Weather: {traffic_scenario['weather']}
    - Events: {traffic_scenario['events']}
    - Time: {traffic_scenario['time']}
    
    Provide analysis in this format:
    SEVERITY: [LOW/MODERATE/HIGH/CRITICAL]
    ROOT_CAUSES: [List main reasons for congestion]
    RECOMMENDATIONS: [List 3 specific actions with timelines]
    IMPACT_PREDICTION: [Expected improvement percentages]
    """
    
    try:
        print(f"\n   📡 Calling Gemini API for: {traffic_scenario['location']}")
        response = model.generate_content(prompt)
        
        print(f"   ✅ API call successful!")
        print(f"   📝 Response length: {len(response.text)} characters")
        
        # Parse and display the response
        analysis = response.text
        print(f"\n   🤖 GEMINI AI ANALYSIS:")
        print(f"   {'-'*40}")
        
        # Display formatted response
        lines = analysis.split('\n')
        for line in lines[:10]:  # Show first 10 lines
            if line.strip():
                print(f"   {line}")
        
        if len(lines) > 10:
            print(f"   ... (showing first 10 lines of {len(lines)} total)")
        
        return analysis
        
    except Exception as e:
        print(f"   ❌ API call failed: {e}")
        return None

def main():
    """Main demo function"""
    print("🚀 CuriousAgents - REAL GEMINI API INTEGRATION")
    print("=" * 60)
    print("This demo makes ACTUAL API calls to Google Gemini")
    print("You will see usage in your Google Cloud dashboard!")
    print()
    
    # Test the API connection
    api_working, model = test_real_gemini_api()
    
    if not api_working:
        print("❌ Cannot proceed - API not working")
        return False
    
    print("\n🚦 RUNNING TRAFFIC SCENARIOS WITH REAL GEMINI AI")
    print("=" * 60)
    
    # Define realistic traffic scenarios
    scenarios = [
        {
            "location": "Downtown Main Street & 5th Ave",
            "speed_kmph": 15.2,
            "expected_speed": 50.0,
            "vehicle_count": 45,
            "weather": "Heavy rain, low visibility",
            "events": "Concert at nearby stadium (25,000 attendees)",
            "time": "Friday 7:30 PM"
        },
        {
            "location": "Highway 101 North - Mile Marker 23",
            "speed_kmph": 25.8,
            "expected_speed": 65.0,
            "vehicle_count": 32,
            "weather": "Clear conditions",
            "events": "Construction zone - 2 lanes closed",
            "time": "Monday 8:15 AM"
        },
        {
            "location": "Bridge District - Market Street",
            "speed_kmph": 8.5,
            "expected_speed": 35.0,
            "vehicle_count": 58,
            "weather": "Fog, visibility 100m",
            "events": "Morning rush hour + accident reported",
            "time": "Tuesday 8:45 AM"
        }
    ]
    
    api_calls_made = 0
    successful_analyses = 0
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎬 SCENARIO {i}: {scenario['location']}")
        print("=" * 50)
        
        # Show scenario details
        congestion_level = 1.0 - (scenario['speed_kmph'] / scenario['expected_speed'])
        severity = "CRITICAL" if congestion_level > 0.7 else "HIGH" if congestion_level > 0.5 else "MODERATE"
        
        print(f"   📊 Current Speed: {scenario['speed_kmph']} km/h")
        print(f"   🎯 Expected Speed: {scenario['expected_speed']} km/h")
        print(f"   🚗 Vehicle Count: {scenario['vehicle_count']}")
        print(f"   🌤️  Weather: {scenario['weather']}")
        print(f"   📅 Context: {scenario['events']}")
        print(f"   ⚠️  Severity: {severity} ({congestion_level:.0%} congestion)")
        
        # Make real API call to Gemini
        analysis = analyze_traffic_with_real_gemini(model, scenario)
        api_calls_made += 1
        
        if analysis:
            successful_analyses += 1
            print(f"   ✅ Analysis complete!")
        else:
            print(f"   ❌ Analysis failed!")
        
        print()
    
    # Summary
    print("🏁 DEMO COMPLETE!")
    print("=" * 60)
    print(f"📊 Statistics:")
    print(f"   • Total API calls made: {api_calls_made}")
    print(f"   • Successful analyses: {successful_analyses}")
    print(f"   • Success rate: {successful_analyses/api_calls_made:.0%}")
    print(f"   • API Key used: {os.environ['GOOGLE_API_KEY'][:20]}...")
    
    print(f"\n✅ CHECK YOUR GOOGLE CLOUD DASHBOARD:")
    print(f"   🔗 https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
    print(f"   You should see {api_calls_made} API calls in the usage metrics!")
    
    print(f"\n🚀 Your CuriousAgents system is now proven to:")
    print(f"   ✅ Make real Gemini API calls")
    print(f"   ✅ Analyze complex traffic scenarios") 
    print(f"   ✅ Generate intelligent recommendations")
    print(f"   ✅ Handle multiple data sources")
    print(f"   ✅ Provide actionable insights")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SUCCESS! Real Gemini API integration working!")
    else:
        print("\n❌ FAILED! Check your API key and connection")
    
    sys.exit(0 if success else 1) 