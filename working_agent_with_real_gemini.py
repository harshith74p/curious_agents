#!/usr/bin/env python3
"""
Working CuriousAgents with Real Gemini API Integration
This demonstrates how to integrate real Gemini API calls into the agent architecture
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List

# Set up environment for Gemini API
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

# Add libs to path
sys.path.append('libs')

class TrafficAnalysisAgent:
    """Enhanced Traffic Analysis Agent with Real Gemini API Integration"""
    
    def __init__(self):
        self.setup_gemini_api()
        
    def setup_gemini_api(self):
        """Initialize real Gemini API connection"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            print("+ Real Gemini API initialized successfully")
        except Exception as e:
            print(f"- Failed to initialize Gemini API: {e}")
            self.model = None
    
    def analyze_congestion_with_gemini(self, traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use real Gemini API to analyze traffic congestion"""
        
        if not self.model:
            return self._fallback_analysis(traffic_data)
        
        # Create detailed prompt for Gemini
        prompt = f"""
        You are an expert traffic management AI. Analyze this traffic scenario and provide specific actionable recommendations:

        TRAFFIC DATA:
        - Location: {traffic_data.get('location', 'Unknown')}
        - Current Speed: {traffic_data.get('speed_kmph', 0)} km/h
        - Expected Speed: {traffic_data.get('expected_speed', 50)} km/h
        - Vehicle Count: {traffic_data.get('vehicle_count', 0)}
        - Time: {traffic_data.get('timestamp', datetime.now())}
        - Weather: {traffic_data.get('weather', 'Clear')}
        - Special Events: {traffic_data.get('events', 'None')}

        Provide analysis in this exact format:
        SEVERITY: [CRITICAL/HIGH/MODERATE/LOW]
        CONGESTION_SCORE: [0.0-1.0]
        ROOT_CAUSES: [List 2-3 main causes]
        IMMEDIATE_ACTIONS: [List 2-3 actions with timelines]
        EXPECTED_IMPROVEMENT: [Percentage improvement expected]
        RESPONSE_PRIORITY: [1-5 priority level]
        """
        
        try:
            print(f"   Making Gemini API call for {traffic_data.get('location', 'Unknown location')}...")
            response = self.model.generate_content(prompt)
            
            # Parse the response
            analysis = self._parse_gemini_response(response.text, traffic_data)
            print(f"   + Gemini API analysis complete!")
            return analysis
            
        except Exception as e:
            print(f"   - Gemini API call failed: {e}")
            return self._fallback_analysis(traffic_data)
    
    def _parse_gemini_response(self, response_text: str, traffic_data: Dict) -> Dict[str, Any]:
        """Parse Gemini response into structured data"""
        
        lines = response_text.split('\n')
        analysis = {
            'raw_response': response_text,
            'api_used': 'gemini-2.0-flash',
            'timestamp': datetime.now().isoformat()
        }
        
        # Extract structured data from response
        for line in lines:
            line = line.strip()
            if line.startswith('SEVERITY:'):
                analysis['severity'] = line.replace('SEVERITY:', '').strip()
            elif line.startswith('CONGESTION_SCORE:'):
                try:
                    score_text = line.replace('CONGESTION_SCORE:', '').strip()
                    analysis['congestion_score'] = float(score_text)
                except:
                    analysis['congestion_score'] = self._calculate_congestion_score(traffic_data)
            elif line.startswith('ROOT_CAUSES:'):
                analysis['root_causes'] = line.replace('ROOT_CAUSES:', '').strip()
            elif line.startswith('IMMEDIATE_ACTIONS:'):
                analysis['immediate_actions'] = line.replace('IMMEDIATE_ACTIONS:', '').strip()
            elif line.startswith('EXPECTED_IMPROVEMENT:'):
                analysis['expected_improvement'] = line.replace('EXPECTED_IMPROVEMENT:', '').strip()
            elif line.startswith('RESPONSE_PRIORITY:'):
                try:
                    priority_text = line.replace('RESPONSE_PRIORITY:', '').strip()
                    analysis['response_priority'] = int(priority_text)
                except:
                    analysis['response_priority'] = 3
        
        # Ensure we have all required fields
        if 'congestion_score' not in analysis:
            analysis['congestion_score'] = self._calculate_congestion_score(traffic_data)
        if 'severity' not in analysis:
            score = analysis['congestion_score']
            if score > 0.8:
                analysis['severity'] = 'CRITICAL'
            elif score > 0.6:
                analysis['severity'] = 'HIGH'
            elif score > 0.3:
                analysis['severity'] = 'MODERATE'
            else:
                analysis['severity'] = 'LOW'
        
        return analysis
    
    def _calculate_congestion_score(self, traffic_data: Dict) -> float:
        """Calculate congestion score from traffic data"""
        speed_kmph = traffic_data.get('speed_kmph', 50)
        expected_speed = traffic_data.get('expected_speed', 50)
        vehicle_count = traffic_data.get('vehicle_count', 10)
        
        # Speed factor (0-1, higher = more congested)
        speed_factor = max(0, 1.0 - (speed_kmph / expected_speed))
        
        # Density factor (0-0.5, higher = more congested)
        density_factor = min(0.5, vehicle_count / 60.0)
        
        return min(1.0, speed_factor + density_factor)
    
    def _fallback_analysis(self, traffic_data: Dict) -> Dict[str, Any]:
        """Fallback analysis when Gemini API is unavailable"""
        score = self._calculate_congestion_score(traffic_data)
        
        return {
            'severity': 'HIGH' if score > 0.6 else 'MODERATE' if score > 0.3 else 'LOW',
            'congestion_score': score,
            'root_causes': 'Local traffic analysis - API unavailable',
            'immediate_actions': 'Standard traffic management protocols',
            'expected_improvement': '15-25% with standard measures',
            'response_priority': 3,
            'api_used': 'fallback_local',
            'timestamp': datetime.now().isoformat()
        }

def demo_real_gemini_agents():
    """Demonstrate real Gemini API integration with traffic agents"""
    
    print("CURIOUSAGENTS - REAL GEMINI API INTEGRATION DEMO")
    print("=" * 60)
    print("This demo shows agents using REAL Gemini API calls")
    print("Check your Google Cloud dashboard for API usage!")
    print()
    
    # Initialize the agent
    agent = TrafficAnalysisAgent()
    
    # Define test scenarios with real traffic data
    scenarios = [
        {
            "name": "Highway Accident During Rush Hour",
            "location": "I-280 South near Daly City",
            "speed_kmph": 8.2,
            "expected_speed": 65.0,
            "vehicle_count": 67,
            "weather": "Clear conditions",
            "events": "Multi-car accident blocking 2 lanes",
            "timestamp": "Monday 8:30 AM"
        },
        {
            "name": "Stadium Event Traffic",
            "location": "Downtown near Sports Arena",
            "speed_kmph": 18.5,
            "expected_speed": 45.0,
            "vehicle_count": 52,
            "weather": "Light rain",
            "events": "Basketball game - 20,000 attendees expected",
            "timestamp": "Friday 6:45 PM"
        },
        {
            "name": "Construction Zone Backup",
            "location": "Highway 101 North - San Mateo",
            "speed_kmph": 25.3,
            "expected_speed": 70.0,
            "vehicle_count": 35,
            "weather": "Fog, visibility 200m",
            "events": "Lane closure for bridge maintenance",
            "timestamp": "Tuesday 7:15 AM"
        }
    ]
    
    api_calls_made = 0
    successful_analyses = 0
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nSCENARIO {i}: {scenario['name']}")
        print("=" * 50)
        
        # Show traffic data
        congestion_pct = (1.0 - scenario['speed_kmph'] / scenario['expected_speed']) * 100
        print(f"Location: {scenario['location']}")
        print(f"Current Speed: {scenario['speed_kmph']} km/h")
        print(f"Expected Speed: {scenario['expected_speed']} km/h")
        print(f"Congestion Level: {congestion_pct:.0f}%")
        print(f"Vehicle Count: {scenario['vehicle_count']}")
        print(f"Conditions: {scenario['weather']}")
        print(f"Context: {scenario['events']}")
        
        # Analyze with real Gemini API
        print(f"\nCalling Real Gemini API...")
        analysis = agent.analyze_congestion_with_gemini(scenario)
        api_calls_made += 1
        
        if analysis and 'api_used' in analysis and analysis['api_used'] == 'gemini-2.0-flash':
            successful_analyses += 1
            print(f"\nGEMINI AI ANALYSIS:")
            print(f"- Severity: {analysis.get('severity', 'UNKNOWN')}")
            print(f"- Congestion Score: {analysis.get('congestion_score', 0):.2f}")
            print(f"- Root Causes: {analysis.get('root_causes', 'Not provided')}")
            print(f"- Actions: {analysis.get('immediate_actions', 'Not provided')}")
            print(f"- Expected Improvement: {analysis.get('expected_improvement', 'Not provided')}")
            print(f"- Priority Level: {analysis.get('response_priority', 'Unknown')}")
        else:
            print(f"+ Used fallback analysis (API unavailable)")
        
        print()
    
    # Summary
    print("DEMO RESULTS")
    print("=" * 60)
    print(f"Total Scenarios: {len(scenarios)}")
    print(f"API Calls Made: {api_calls_made}")
    print(f"Successful Gemini Analyses: {successful_analyses}")
    print(f"Success Rate: {successful_analyses/api_calls_made:.0%}")
    
    if successful_analyses > 0:
        print(f"\n+ SUCCESS! Your agents are using REAL Gemini API!")
        print(f"+ Check your Google Cloud Console for API usage")
        print(f"+ Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com")
    else:
        print(f"\n- Warning: No successful API calls made")
        print(f"- Check your API key and internet connection")
    
    print(f"\nYour CuriousAgents system now demonstrates:")
    print(f"+ Real AI integration with Google Gemini")
    print(f"+ Intelligent traffic scenario analysis")
    print(f"+ Actionable recommendations with priorities")
    print(f"+ Production-ready agent architecture")

if __name__ == "__main__":
    demo_real_gemini_agents() 