#!/usr/bin/env python3
"""
Debug Version of CuriousAgents with Real Gemini API
Enhanced with detailed logging to track agent status and API calls
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any

# Set up environment for Gemini API
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

class DebugTrafficAgent:
    """Debug Traffic Agent with Real Gemini API Integration and Detailed Logging"""
    
    def __init__(self, agent_name="TrafficAgent"):
        self.agent_name = agent_name
        self.api_calls_made = 0
        self.total_response_time = 0
        self.setup_gemini_api()
        
    def setup_gemini_api(self):
        """Initialize real Gemini API connection with debug logging"""
        print(f"[DEBUG] {self.agent_name}: Starting Gemini API setup...")
        try:
            import google.generativeai as genai
            print(f"[DEBUG] {self.agent_name}: Importing google.generativeai...")
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            print(f"[DEBUG] {self.agent_name}: Configuring API with key: {os.environ['GOOGLE_API_KEY'][:20]}...")
            
            print(f"[DEBUG] {self.agent_name}: Creating Gemini model...")
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            print(f"[DEBUG] {self.agent_name}: ✅ Real Gemini API initialized successfully")
            return True
        except Exception as e:
            print(f"[DEBUG] {self.agent_name}: ❌ Failed to initialize Gemini API: {e}")
            self.model = None
            return False
    
    def analyze_traffic(self, traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze traffic using real Gemini API with detailed logging"""
        
        print(f"\n[DEBUG] {self.agent_name}: Starting traffic analysis...")
        print(f"[DEBUG] {self.agent_name}: Input data: {json.dumps(traffic_data, indent=2)}")
        
        if not self.model:
            print(f"[DEBUG] {self.agent_name}: ⚠️  No model available, using fallback")
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
        
        print(f"[DEBUG] {self.agent_name}: 📡 Making Gemini API call...")
        print(f"[DEBUG] {self.agent_name}: Target location: {traffic_data.get('location', 'Unknown')}")
        
        start_time = time.time()
        try:
            print(f"[DEBUG] {self.agent_name}: ⏳ Waiting for API response...")
            response = self.model.generate_content(prompt)
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"[DEBUG] {self.agent_name}: ✅ API call successful!")
            print(f"[DEBUG] {self.agent_name}: ⏱️  Response time: {response_time:.2f} seconds")
            print(f"[DEBUG] {self.agent_name}: 📝 Response length: {len(response.text)} characters")
            
            # Track API usage
            self.api_calls_made += 1
            self.total_response_time += response_time
            
            # Parse the response
            analysis = self._parse_gemini_response(response.text, traffic_data, response_time)
            print(f"[DEBUG] {self.agent_name}: 📊 Analysis complete - Severity: {analysis.get('severity', 'Unknown')}")
            return analysis
            
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            print(f"[DEBUG] {self.agent_name}: ❌ Gemini API call failed after {response_time:.2f}s: {e}")
            return self._fallback_analysis(traffic_data)
    
    def _parse_gemini_response(self, response_text: str, traffic_data: Dict, response_time: float) -> Dict[str, Any]:
        """Parse Gemini response into structured data with debug logging"""
        
        print(f"[DEBUG] {self.agent_name}: 🔍 Parsing API response...")
        
        lines = response_text.split('\n')
        analysis = {
            'raw_response': response_text,
            'api_used': 'gemini-2.0-flash',
            'timestamp': datetime.now().isoformat(),
            'response_time_seconds': response_time,
            'location': traffic_data.get('location'),
            'speed_kmph': traffic_data.get('speed_kmph'),
            'congestion_level': self._calculate_congestion(traffic_data)
        }
        
        # Extract structured data from response
        for line in lines:
            line = line.strip()
            if line.startswith('SEVERITY:'):
                analysis['severity'] = line.replace('SEVERITY:', '').strip()
                print(f"[DEBUG] {self.agent_name}: 📊 Extracted severity: {analysis['severity']}")
            elif line.startswith('ROOT_CAUSES:'):
                analysis['root_causes'] = line.replace('ROOT_CAUSES:', '').strip()
                print(f"[DEBUG] {self.agent_name}: 🔍 Extracted root causes: {analysis['root_causes'][:50]}...")
            elif line.startswith('RECOMMENDATIONS:'):
                analysis['recommendations'] = line.replace('RECOMMENDATIONS:', '').strip()
                print(f"[DEBUG] {self.agent_name}: 💡 Extracted recommendations: {analysis['recommendations'][:50]}...")
        
        print(f"[DEBUG] {self.agent_name}: ✅ Response parsing complete")
        return analysis
    
    def _calculate_congestion(self, traffic_data: Dict) -> float:
        """Calculate congestion level with debug logging"""
        speed_kmph = traffic_data.get('speed_kmph', 50)
        expected_speed = traffic_data.get('expected_speed', 50)
        vehicle_count = traffic_data.get('vehicle_count', 10)
        
        speed_factor = max(0, 1.0 - (speed_kmph / expected_speed))
        density_factor = min(0.5, vehicle_count / 60.0)
        congestion = min(1.0, speed_factor + density_factor)
        
        print(f"[DEBUG] {self.agent_name}: 🧮 Congestion calculation:")
        print(f"[DEBUG] {self.agent_name}:   Speed factor: {speed_factor:.2f}")
        print(f"[DEBUG] {self.agent_name}:   Density factor: {density_factor:.2f}")
        print(f"[DEBUG] {self.agent_name}:   Total congestion: {congestion:.2f}")
        
        return congestion
    
    def _fallback_analysis(self, traffic_data: Dict) -> Dict[str, Any]:
        """Fallback analysis when API unavailable with debug logging"""
        print(f"[DEBUG] {self.agent_name}: 🔄 Using fallback analysis")
        
        congestion = self._calculate_congestion(traffic_data)
        
        analysis = {
            'severity': 'HIGH' if congestion > 0.6 else 'MODERATE' if congestion > 0.3 else 'LOW',
            'congestion_level': congestion,
            'root_causes': 'Local analysis - API unavailable',
            'recommendations': 'Standard traffic management',
            'api_used': 'fallback_local',
            'timestamp': datetime.now().isoformat(),
            'location': traffic_data.get('location'),
            'speed_kmph': traffic_data.get('speed_kmph'),
            'response_time_seconds': 0.0
        }
        
        print(f"[DEBUG] {self.agent_name}: ✅ Fallback analysis complete")
        return analysis
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        avg_response_time = self.total_response_time / self.api_calls_made if self.api_calls_made > 0 else 0
        return {
            'agent_name': self.agent_name,
            'api_calls_made': self.api_calls_made,
            'total_response_time': self.total_response_time,
            'average_response_time': avg_response_time,
            'success_rate': 1.0 if self.api_calls_made > 0 else 0.0
        }

def main():
    """Main demo function with detailed debug logging"""
    print("🔍 DEBUG GEMINI AGENT DEMO")
    print("=" * 60)
    print("Testing real Gemini API integration with detailed logging...")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize agent
    print("[DEBUG] MAIN: Initializing TrafficAgent...")
    agent = DebugTrafficAgent("TrafficAgent")
    
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
        },
        {
            "location": "Bridge District",
            "speed_kmph": 8.5,
            "expected_speed": 35.0,
            "vehicle_count": 58,
            "weather": "Fog",
            "events": "Morning rush hour + accident"
        }
    ]
    
    print(f"[DEBUG] MAIN: Processing {len(scenarios)} scenarios...")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*20} SCENARIO {i}: {scenario['location']} {'='*20}")
        
        # Show scenario details
        congestion = agent._calculate_congestion(scenario)
        print(f"[DEBUG] MAIN: Scenario {i} details:")
        print(f"  Speed: {scenario['speed_kmph']} km/h")
        print(f"  Expected: {scenario['expected_speed']} km/h")
        print(f"  Congestion: {congestion:.0%}")
        
        # Analyze with Gemini
        print(f"\n[DEBUG] MAIN: Starting analysis for scenario {i}...")
        analysis = agent.analyze_traffic(scenario)
        
        # Show results
        print(f"\n[DEBUG] MAIN: Analysis results for scenario {i}:")
        print(f"  Severity: {analysis.get('severity', 'Unknown')}")
        print(f"  API Used: {analysis.get('api_used', 'Unknown')}")
        print(f"  Response Time: {analysis.get('response_time_seconds', 0):.2f}s")
        
        if analysis.get('api_used') == 'gemini-2.0-flash':
            print(f"  ✅ Real Gemini API used!")
        else:
            print(f"  ⚠️  Used fallback analysis")
        
        print()
    
    # Get final statistics
    stats = agent.get_stats()
    print("📊 FINAL STATISTICS")
    print("=" * 60)
    print(f"Agent: {stats['agent_name']}")
    print(f"API Calls Made: {stats['api_calls_made']}")
    print(f"Total Response Time: {stats['total_response_time']:.2f}s")
    print(f"Average Response Time: {stats['average_response_time']:.2f}s")
    print(f"Success Rate: {stats['success_rate']:.0%}")
    
    if stats['api_calls_made'] > 0:
        print(f"\n🎉 SUCCESS! Real Gemini API integration working!")
        print(f"Check your Google Cloud dashboard for API usage!")
        print(f"Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
    else:
        print(f"\n⚠️  No successful API calls - check your API key")
    
    print(f"\n[DEBUG] MAIN: Demo complete!")

if __name__ == "__main__":
    main() 