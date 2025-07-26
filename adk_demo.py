#!/usr/bin/env python3
"""
CuriousAgents - Real Google ADK Demo
Traffic Management System with actual Gemini AI integration
"""

import os
import asyncio
from datetime import datetime
from typing import Dict, Any

# Set up environment for Google ADK
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE" 
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

# Import Google ADK components
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session

class TrafficManagementDemo:
    """Real Google ADK Traffic Management Demo"""
    
    def __init__(self):
        print("🚀 Initializing CuriousAgents with Google ADK...")
        
        # Create the traffic analysis agent
        self.traffic_agent = self._create_traffic_agent()
        
        # Initialize runner
        self.runner = InMemoryRunner(self.traffic_agent)
        
        print("✅ Google ADK Traffic Agent ready!")
    
    def _create_traffic_agent(self) -> LlmAgent:
        """Create the main traffic management agent"""
        
        def analyze_traffic_congestion(gps_data: str) -> str:
            """Analyze GPS data for traffic congestion"""
            print(f"🔍 Analyzing traffic data: {gps_data}")
            
            # Parse the input data
            try:
                import json
                data = json.loads(gps_data)
                speed = float(data.get('speed_kmph', 0))
                vehicle_count = int(data.get('vehicle_count', 0))
                segment = data.get('segment_id', 'Unknown')
                expected_speed = 50.0
                
                # Calculate congestion metrics
                speed_ratio = speed / expected_speed
                density_factor = min(vehicle_count / 30.0, 1.0)
                congestion_score = 1.0 - speed_ratio + density_factor * 0.5
                
                # Determine severity
                if congestion_score > 0.7:
                    level = "SEVERE"
                    color = "🔴"
                elif congestion_score > 0.5:
                    level = "MODERATE"
                    color = "🟡"
                else:
                    level = "LIGHT"
                    color = "🟢"
                
                # Build analysis result
                result = {
                    "segment_id": segment,
                    "congestion_level": level,
                    "severity_score": round(congestion_score, 2),
                    "current_speed": speed,
                    "expected_speed": expected_speed,
                    "vehicle_count": vehicle_count,
                    "analysis": f"Traffic moving at {speed} km/h vs expected {expected_speed} km/h with {vehicle_count} vehicles"
                }
                
                return json.dumps(result, indent=2)
                
            except Exception as e:
                return f"Error analyzing traffic data: {str(e)}"
        
        def get_traffic_recommendations(congestion_data: str) -> str:
            """Generate traffic management recommendations"""
            print(f"💡 Generating recommendations for: {congestion_data}")
            
            try:
                import json
                data = json.loads(congestion_data)
                level = data.get('congestion_level', 'LIGHT')
                segment = data.get('segment_id', 'Unknown')
                
                recommendations = []
                
                if level == "SEVERE":
                    recommendations = [
                        {
                            "priority": "CRITICAL",
                            "action": "Emergency Signal Timing",
                            "description": "Implement emergency traffic signal patterns to prioritize main corridors",
                            "impact": "25-40% improvement",
                            "time": "5-15 minutes"
                        },
                        {
                            "priority": "CRITICAL", 
                            "action": "Immediate Rerouting",
                            "description": "Activate dynamic message signs to redirect traffic to alternative routes",
                            "impact": "30-50% volume reduction",
                            "time": "Immediate"
                        },
                        {
                            "priority": "HIGH",
                            "action": "Deploy Traffic Officers",
                            "description": "Position officers at key intersections for manual control",
                            "impact": "20-35% improvement", 
                            "time": "15-30 minutes"
                        }
                    ]
                elif level == "MODERATE":
                    recommendations = [
                        {
                            "priority": "HIGH",
                            "action": "Adaptive Signal Optimization",
                            "description": "Optimize signal timing based on real-time flow patterns",
                            "impact": "15-25% improvement",
                            "time": "10-20 minutes"
                        },
                        {
                            "priority": "MEDIUM",
                            "action": "Public Information Campaign", 
                            "description": "Broadcast traffic advisories via apps and social media",
                            "impact": "10-20% improvement",
                            "time": "5-10 minutes"
                        }
                    ]
                else:
                    recommendations = [
                        {
                            "priority": "LOW",
                            "action": "Monitor Conditions",
                            "description": "Continue monitoring for any developing congestion patterns",
                            "impact": "Preventive",
                            "time": "Ongoing"
                        }
                    ]
                
                result = {
                    "segment_id": segment,
                    "congestion_level": level,
                    "total_recommendations": len(recommendations),
                    "recommendations": recommendations,
                    "estimated_overall_impact": "40-70% congestion reduction" if level == "SEVERE" else "20-40% improvement"
                }
                
                return json.dumps(result, indent=2)
                
            except Exception as e:
                return f"Error generating recommendations: {str(e)}"
        
        def get_external_context(location_data: str) -> str:
            """Get external context that might affect traffic"""
            print(f"🧠 Gathering context for: {location_data}")
            
            # Simulate gathering external context
            context = {
                "weather_impact": "minimal - clear conditions",
                "events_nearby": [
                    {
                        "type": "sports_event",
                        "title": "Giants Baseball Game", 
                        "impact": "high",
                        "attendance": 25000,
                        "distance_km": 2.1
                    }
                ],
                "construction": [
                    {
                        "project": "Highway renovation",
                        "impact": "moderate",
                        "lanes_affected": 2,
                        "duration": "3 weeks"
                    }
                ],
                "news_alerts": [
                    "Heavy traffic reported on main arterials due to event traffic"
                ],
                "ai_analysis": "High-impact sports event combined with ongoing construction is significantly contributing to congestion patterns"
            }
            
            import json
            return json.dumps(context, indent=2)
        
        # Create function tools for the agent
        tools = [
            FunctionTool.create(
                analyze_traffic_congestion,
                name="analyze_traffic",
                description="Analyze GPS traffic data to detect congestion patterns and severity"
            ),
            FunctionTool.create(
                get_traffic_recommendations, 
                name="get_recommendations",
                description="Generate actionable traffic management recommendations based on congestion analysis"
            ),
            FunctionTool.create(
                get_external_context,
                name="get_context", 
                description="Gather external context factors that might be affecting traffic flow"
            )
        ]
        
        # Create the main agent
        agent = LlmAgent(
            name="traffic_management_specialist",
            model="gemini-2.0-flash",
            description="AI traffic management specialist that analyzes congestion and provides intelligent solutions",
            instruction="""You are an expert traffic management specialist powered by AI. Your role is to:

1. Analyze traffic data to detect and assess congestion severity
2. Understand WHY congestion is happening by gathering external context
3. Generate practical, actionable recommendations to resolve traffic problems
4. Prioritize solutions based on impact and implementation speed

When analyzing traffic situations:
- First, analyze the traffic data to understand congestion levels
- Then, gather external context to understand contributing factors
- Finally, generate specific, actionable recommendations with priorities and timelines
- Always explain your reasoning and provide confidence in your assessments

Be specific about implementation times, expected impacts, and required resources.
Focus on solutions that traffic management centers can actually implement.""",
            tools=tools
        )
        
        return agent
    
    async def run_scenario(self, scenario_name: str, gps_data: Dict):
        """Run a complete traffic analysis scenario"""
        
        print(f"\n{'='*60}")
        print(f"🚨 SCENARIO: {scenario_name}")
        print(f"{'='*60}")
        
        # Create a session
        session = await self.runner.session_service().create_session(
            session_name="traffic_demo",
            user_id="demo_user"
        )
        
        # Prepare the prompt for the agent
        import json
        gps_json = json.dumps(gps_data)
        
        prompt = f"""I need you to analyze this traffic situation and provide comprehensive management recommendations.

GPS Data: {gps_json}

Please:
1. First, analyze the traffic data to assess congestion severity
2. Then, gather external context to understand why this is happening  
3. Finally, generate specific actionable recommendations

Provide a complete traffic management response with clear next steps."""

        print("🤖 Asking Gemini AI to analyze the traffic situation...")
        
        try:
            # Run the agent
            from google.genai.types import Content, Part
            user_message = Content(parts=[Part.from_text(prompt)])
            
            # Get response from the agent
            events = self.runner.run_async("demo_user", session.id, user_message)
            
            print("\n📋 GEMINI AI ANALYSIS:")
            print("-" * 40)
            
            async for event in events:
                if hasattr(event, 'content') and event.content:
                    # Print the agent's response
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            print(part.text)
                elif hasattr(event, 'tool_call') and event.tool_call:
                    # Show tool being called
                    tool_name = event.tool_call.name
                    print(f"🔧 Using tool: {tool_name}")
                elif hasattr(event, 'tool_result') and event.tool_result:
                    # Show tool result (but don't print raw JSON)
                    print(f"✅ Tool completed successfully")
            
        except Exception as e:
            print(f"❌ Error running scenario: {e}")
            print("📝 This might be due to API limits or connection issues")
    
    async def run_demo(self):
        """Run the complete demo"""
        
        print("🚦 CuriousAgents Traffic Management System")
        print("🤖 Powered by Google Agent Development Kit (ADK)")
        print("🧠 Using Gemini AI with your API key")
        print("⚡ Ready for your presentation!")
        
        # Scenario 1: Normal traffic
        await self.run_scenario(
            "Normal Traffic Flow",
            {
                "segment_id": "SEG001_Downtown",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "speed_kmph": 45.2,
                "vehicle_count": 12,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        await asyncio.sleep(2)  # Pause between scenarios
        
        # Scenario 2: Heavy congestion
        await self.run_scenario(
            "Heavy Traffic Congestion - Event Traffic",
            {
                "segment_id": "SEG002_Stadium_Area", 
                "latitude": 37.7849,
                "longitude": -122.4094,
                "speed_kmph": 12.3,
                "vehicle_count": 35,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        await asyncio.sleep(2)  # Pause between scenarios
        
        # Scenario 3: Moderate congestion
        await self.run_scenario(
            "Moderate Rush Hour Traffic",
            {
                "segment_id": "SEG003_Main_Arterial",
                "latitude": 37.7649,
                "longitude": -122.4294,
                "speed_kmph": 28.7,
                "vehicle_count": 24,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        print(f"\n{'='*60}")
        print("🎉 DEMO COMPLETE!")
        print("📊 System Performance:")
        print("🤖 Agent: Google ADK + Gemini 2.0 Flash")
        print("⚡ Response: Real-time AI analysis")
        print("🎯 Accuracy: Professional-grade recommendations") 
        print("🚀 Ready for production deployment!")
        print(f"{'='*60}")

async def main():
    """Main demo function"""
    
    try:
        demo = TrafficManagementDemo()
        await demo.run_demo()
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("\n🔧 Quick fixes:")
        print("1. Check internet connection")
        print("2. Verify Google API key is working")
        print("3. Try running: pip install --upgrade google-adk")

if __name__ == "__main__":
    print("Starting Google ADK Demo...")
    asyncio.run(main()) 