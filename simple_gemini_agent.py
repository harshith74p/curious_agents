#!/usr/bin/env python3
"""
Simple Working Agent with Real Gemini API
No external dependencies - just pure Gemini API integration
"""

import os
import json
from datetime import datetime
from typing import Dict, Any

# Set up environment for Gemini API
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

class SimpleTrafficAgent:
    """Simple Traffic Agent with Real Gemini API Integration"""
    
    def __init__(self):
        self.setup_gemini_api()
        
    def setup_gemini_api(self):
        """Initialize real Gemini API connection"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            print("+ Real Gemini API initialized successfully")
            return True
        except Exception as e:
            print(f"- Failed to initialize Gemini API: {e}")
            self.model = None
            return False
    
    def analyze_traffic(self, traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze traffic using real Gemini API"""
        
        if not self.model:
            return self._fallback_analysis(traffic_data)
        
        # Create prompt for Gemini
        prompt = f"""
        Analyze this traffic scenario and provide recommendations:

        Location: {traffic_data.get('location', 'Unknown')}
        Current Speed: {traffic_data.get('speed_kmph', 0)} km/h
        Expected Speed: {traffic_data.get('expected_speed', 50)} km/h
        Vehicle Count: {traffic_data.get('vehicle_count', 0)}
        Weather: {traffic_data.get('weather', 'Clear')}
        Events: {traffic_data.get('events', 'None')}

        Provide analysis in this format:
        SEVERITY: [CRITICAL/HIGH/MODERATE/LOW]
        ROOT_CAUSES: [List main causes]
        RECOMMENDATIONS: [List 2-3 actions]
        """
        
        try:
            print(f"   Calling Gemini API for {traffic_data.get('location', 'Unknown')}...")
            response = self.model.generate_content(prompt)
            
            analysis = {
                'raw_response': response.text,
                'api_used': 'gemini-2.0-flash',
                'timestamp': datetime.now().isoformat(),
                'location': traffic_data.get('location'),
                'speed_kmph': traffic_data.get('speed_kmph'),
                'congestion_level': self._calculate_congestion(traffic_data)
            }
            
            print(f"   + Gemini API analysis complete!")
            return analysis
            
        except Exception as e:
            print(f"   - Gemini API call failed: {e}")
            return self._fallback_analysis(traffic_data)
    
    def _calculate_congestion(self, traffic_data: Dict) -> float:
        """Calculate congestion level"""
        speed_kmph = traffic_data.get('speed_kmph', 50)
        expected_speed = traffic_data.get('expected_speed', 50)
        vehicle_count = traffic_data.get('vehicle_count', 10)
        
        speed_factor = max(0, 1.0 - (speed_kmph / expected_speed))
        density_factor = min(0.5, vehicle_count / 60.0)
        
        return min(1.0, speed_factor + density_factor)
    
    def _fallback_analysis(self, traffic_data: Dict) -> Dict[str, Any]:
        """Fallback analysis when API unavailable"""
        congestion = self._calculate_congestion(traffic_data)
        
        return {
            'severity': 'HIGH' if congestion > 0.6 else 'MODERATE' if congestion > 0.3 else 'LOW',
            'congestion_level': congestion,
            'root_causes': 'Local analysis - API unavailable',
            'recommendations': 'Standard traffic management',
            'api_used': 'fallback_local',
            'timestamp': datetime.now().isoformat(),
            'location': traffic_data.get('location'),
            'speed_kmph': traffic_data.get('speed_kmph')
        }

def main():
    """Main demo function"""
    print("SIMPLE GEMINI AGENT DEMO")
    print("=" * 50)
    print("Testing real Gemini API integration...")
    print()
    
    # Initialize agent
    agent = SimpleTrafficAgent()
    
    # Test scenarios
    scenarios = [
        {
            "location": "Downtown Main Street",
            "speed_kmph": 15.2,
            "expected_speed": 50.0,
            "vehicle_count": 45,
            "weather": "Heavy rain",
            "events": "Concert nearby"
        },
        {
            "location": "Highway 101 North",
            "speed_kmph": 25.8,
            "expected_speed": 65.0,
            "vehicle_count": 32,
            "weather": "Clear",
            "events": "Construction zone"
        }
    ]
    
    api_calls = 0
    successful = 0
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nSCENARIO {i}: {scenario['location']}")
        print("-" * 40)
        
        # Show scenario details
        congestion = agent._calculate_congestion(scenario)
        print(f"Speed: {scenario['speed_kmph']} km/h")
        print(f"Expected: {scenario['expected_speed']} km/h")
        print(f"Congestion: {congestion:.0%}")
        
        # Analyze with Gemini
        analysis = agent.analyze_traffic(scenario)
        api_calls += 1
        
        if analysis.get('api_used') == 'gemini-2.0-flash':
            successful += 1
            print(f"✅ Real Gemini API used!")
        else:
            print(f"⚠️  Used fallback analysis")
        
        # Show results
        print(f"Severity: {analysis.get('severity', 'Unknown')}")
        print(f"API Used: {analysis.get('api_used', 'Unknown')}")
        print()
    
    # Summary
    print("DEMO RESULTS")
    print("=" * 50)
    print(f"Total Scenarios: {len(scenarios)}")
    print(f"API Calls Made: {api_calls}")
    print(f"Successful Gemini Calls: {successful}")
    print(f"Success Rate: {successful/api_calls:.0%}")
    
    if successful > 0:
        print(f"\n🎉 SUCCESS! Real Gemini API integration working!")
        print(f"Check your Google Cloud dashboard for API usage!")
    else:
        print(f"\n⚠️  No successful API calls - check your API key")

if __name__ == "__main__":
    main() 