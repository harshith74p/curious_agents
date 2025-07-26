#!/usr/bin/env python3
"""
Debug Version of Google ADK Agent
Enhanced with detailed logging to track agent status and API calls
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any

# Set up environment
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

class DebugADKAgent:
    """Debug ADK Agent with Real Gemini API Integration and Detailed Logging"""
    
    def __init__(self, agent_name="ADKAgent"):
        self.agent_name = agent_name
        self.api_calls_made = 0
        self.total_response_time = 0
        self.setup_adk_agent()
        
    def setup_adk_agent(self):
        """Initialize ADK agent with debug logging"""
        print(f"[DEBUG] {self.agent_name}: Starting ADK agent setup...")
        try:
            print(f"[DEBUG] {self.agent_name}: Importing Google ADK...")
            from google.adk.agents import LlmAgent
            from google.adk.runners import InMemoryRunner
            
            print(f"[DEBUG] {self.agent_name}: Creating LlmAgent...")
            self.agent = LlmAgent(
                name=self.agent_name,
                model="gemini-2.0-flash",
                description="Debug traffic management agent",
                instruction="You are a traffic management AI expert. Analyze traffic scenarios and provide specific recommendations."
            )
            
            print(f"[DEBUG] {self.agent_name}: Creating InMemoryRunner...")
            self.runner = InMemoryRunner()
            
            print(f"[DEBUG] {self.agent_name}: ✅ ADK agent initialized successfully")
            print(f"[DEBUG] {self.agent_name}: Agent name: {self.agent.name}")
            print(f"[DEBUG] {self.agent_name}: Model: {self.agent.model}")
            return True
            
        except Exception as e:
            print(f"[DEBUG] {self.agent_name}: ❌ Failed to initialize ADK agent: {e}")
            self.agent = None
            self.runner = None
            return False
    
    def analyze_traffic_with_adk(self, traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze traffic using ADK agent with detailed logging"""
        
        print(f"\n[DEBUG] {self.agent_name}: Starting ADK traffic analysis...")
        print(f"[DEBUG] {self.agent_name}: Input data: {json.dumps(traffic_data, indent=2)}")
        
        if not self.agent or not self.runner:
            print(f"[DEBUG] {self.agent_name}: ⚠️  No ADK agent available, using fallback")
            return self._fallback_analysis(traffic_data)
        
        # Create prompt for ADK agent
        prompt = f"""
        Analyze this traffic scenario and provide specific recommendations:

        TRAFFIC DATA:
        - Location: {traffic_data.get('location', 'Unknown')}
        - Current Speed: {traffic_data.get('speed_kmph', 0)} km/h
        - Expected Speed: {traffic_data.get('expected_speed', 50)} km/h
        - Vehicle Count: {traffic_data.get('vehicle_count', 0)}
        - Weather: {traffic_data.get('weather', 'Clear')}
        - Events: {traffic_data.get('events', 'None')}

        Provide analysis in this format:
        SEVERITY: [CRITICAL/HIGH/MODERATE/LOW]
        ROOT_CAUSES: [List main causes]
        RECOMMENDATIONS: [List 2-3 actions]
        """
        
        print(f"[DEBUG] {self.agent_name}: 📡 Making ADK API call...")
        print(f"[DEBUG] {self.agent_name}: Target location: {traffic_data.get('location', 'Unknown')}")
        
        start_time = time.time()
        try:
            print(f"[DEBUG] {self.agent_name}: ⏳ Waiting for ADK response...")
            
            # Run the agent with the prompt
            result = self.runner.run(self.agent, prompt)
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"[DEBUG] {self.agent_name}: ✅ ADK call successful!")
            print(f"[DEBUG] {self.agent_name}: ⏱️  Response time: {response_time:.2f} seconds")
            
            # Extract response text
            if hasattr(result, 'text'):
                response_text = result.text
            elif hasattr(result, 'content'):
                response_text = result.content
            else:
                response_text = str(result)
            
            print(f"[DEBUG] {self.agent_name}: 📝 Response length: {len(response_text)} characters")
            
            # Track API usage
            self.api_calls_made += 1
            self.total_response_time += response_time
            
            # Parse the response
            analysis = self._parse_adk_response(response_text, traffic_data, response_time)
            print(f"[DEBUG] {self.agent_name}: 📊 Analysis complete - Severity: {analysis.get('severity', 'Unknown')}")
            return analysis
            
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            print(f"[DEBUG] {self.agent_name}: ❌ ADK call failed after {response_time:.2f}s: {e}")
            return self._fallback_analysis(traffic_data)
    
    def _parse_adk_response(self, response_text: str, traffic_data: Dict, response_time: float) -> Dict[str, Any]:
        """Parse ADK response into structured data with debug logging"""
        
        print(f"[DEBUG] {self.agent_name}: 🔍 Parsing ADK response...")
        
        lines = response_text.split('\n')
        analysis = {
            'raw_response': response_text,
            'api_used': 'google-adk-gemini',
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
        
        print(f"[DEBUG] {self.agent_name}: ✅ ADK response parsing complete")
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
        """Fallback analysis when ADK unavailable with debug logging"""
        print(f"[DEBUG] {self.agent_name}: 🔄 Using fallback analysis")
        
        congestion = self._calculate_congestion(traffic_data)
        
        analysis = {
            'severity': 'HIGH' if congestion > 0.6 else 'MODERATE' if congestion > 0.3 else 'LOW',
            'congestion_level': congestion,
            'root_causes': 'Local analysis - ADK unavailable',
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
    print("🔍 DEBUG ADK AGENT DEMO")
    print("=" * 60)
    print("Testing Google ADK integration with detailed logging...")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize agent
    print("[DEBUG] MAIN: Initializing ADK Agent...")
    agent = DebugADKAgent("ADKAgent")
    
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
    
    print(f"[DEBUG] MAIN: Processing {len(scenarios)} scenarios...")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*20} SCENARIO {i}: {scenario['location']} {'='*20}")
        
        # Show scenario details
        congestion = agent._calculate_congestion(scenario)
        print(f"[DEBUG] MAIN: Scenario {i} details:")
        print(f"  Speed: {scenario['speed_kmph']} km/h")
        print(f"  Expected: {scenario['expected_speed']} km/h")
        print(f"  Congestion: {congestion:.0%}")
        
        # Analyze with ADK
        print(f"\n[DEBUG] MAIN: Starting ADK analysis for scenario {i}...")
        analysis = agent.analyze_traffic_with_adk(scenario)
        
        # Show results
        print(f"\n[DEBUG] MAIN: Analysis results for scenario {i}:")
        print(f"  Severity: {analysis.get('severity', 'Unknown')}")
        print(f"  API Used: {analysis.get('api_used', 'Unknown')}")
        print(f"  Response Time: {analysis.get('response_time_seconds', 0):.2f}s")
        
        if analysis.get('api_used') == 'google-adk-gemini':
            print(f"  ✅ Real ADK API used!")
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
        print(f"\n🎉 SUCCESS! Real ADK integration working!")
        print(f"Check your Google Cloud dashboard for API usage!")
        print(f"Dashboard: https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas")
    else:
        print(f"\n⚠️  No successful API calls - check your API key")
    
    print(f"\n[DEBUG] MAIN: Demo complete!")

if __name__ == "__main__":
    main() 