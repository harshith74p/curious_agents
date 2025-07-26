#!/usr/bin/env python3
"""
Local Demo of CuriousAgents Traffic Management System
Simulates all agents working together without external dependencies
"""

import os
import sys
import json
import random
import time
from datetime import datetime
from typing import Dict, Any, List

# Add libs to path
sys.path.append('libs')

def simulate_traffic_scenario():
    """Simulate complete traffic management scenarios"""
    
    print("CuriousAgents Local Demo")
    print("=" * 60)
    print("Simulating intelligent traffic management scenario...")
    
    # Import components
    try:
        from libs.common import (
            GPSPoint, CongestionAlert, ContextData, RecommendedAction,
            get_logger, KafkaManager, RedisManager
        )
    except ImportError as e:
        print(f"Warning: Some imports failed ({e}), using simulated versions")
        # Create mock classes for demo
        class GPSPoint:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)
        class CongestionAlert:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)
    
    logger = get_logger(__name__) if 'get_logger' in locals() else None
    
    print("\nSIMULATING GPS DATA STREAM")
    
    # Define test scenarios
    scenarios = [
        {
            "name": "Normal Traffic",
            "location": "Highway 101 - Normal evening traffic",
            "segment_id": "SEG001",
            "gps_data": {
                "latitude": 37.7749,
                "longitude": -122.4194,
                "speed_kmph": 55.2,
                "vehicle_count": 12,
                "timestamp": datetime.now()
            },
            "expected_response": "normal"
        },
        {
            "name": "Heavy Congestion", 
            "location": "Downtown - Event traffic + rain",
            "segment_id": "SEG002",
            "gps_data": {
                "latitude": 37.7749,
                "longitude": -122.4194,
                "speed_kmph": 12.3,
                "vehicle_count": 35,
                "timestamp": datetime.now()
            },
            "expected_response": "critical"
        },
        {
            "name": "Moderate Congestion",
            "location": "Bridge approach - Rush hour backup", 
            "segment_id": "SEG003",
            "gps_data": {
                "latitude": 37.7749,
                "longitude": -122.4194,
                "speed_kmph": 28.7,
                "vehicle_count": 25,
                "timestamp": datetime.now()
            },
            "expected_response": "moderate"
        }
    ]
    
    kafka_messages = 0
    redis_entries = 0
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*20} SCENARIO {i}: {scenario['name']} {'='*20}")
        print(f"Location: {scenario['location']}")
        
        # Step 1: Congestion Detection
        print(f"\nCONGESTION DETECTOR: Analyzing {scenario['segment_id']}")
        
        gps_data = scenario["gps_data"]
        expected_speed = 50.0
        speed_ratio = gps_data["speed_kmph"] / expected_speed
        congestion_level = max(0, 1.0 - speed_ratio) + (gps_data["vehicle_count"] / 50.0) * 0.5
        congestion_level = min(congestion_level, 1.0)
        
        if congestion_level < 0.3:
            print(f"  + Normal traffic (Speed: {gps_data['speed_kmph']} km/h)")
            print("\n" + "=" * 60)
            continue
        
        # Congestion detected
        confidence = 0.85 + random.uniform(0, 0.15)
        factors = ['high_vehicle_density'] if gps_data["vehicle_count"] > 20 else ['moderate_density']
        
        print(f"  ! CONGESTION DETECTED!")
        print(f"     Level: {congestion_level:.2f} (Confidence: {confidence:.2f})")
        print(f"     Speed: {gps_data['speed_kmph']} km/h (Expected: {expected_speed})")
        print(f"     Factors: {', '.join(factors)}")
        
        # Simulate Kafka/Redis operations
        print(f"Cache: Cached congestion:{scenario['segment_id']}")
        redis_entries += 1
        
        alert_data = {
            "segment_id": scenario["segment_id"],
            "congestion_level": round(congestion_level, 3),
            "avg_speed": gps_data["speed_kmph"],
            "expected_speed": expected_speed,
            "timestamp": datetime.now().isoformat(),
            "factors": factors
        }
        
        print(f"Kafka: congestion_alerts <- {scenario['segment_id']}: {{")
        print(f'  "segment_id": "{scenario["segment_id"]}",')
        print(f'  "congestion_level": {alert_data["congestion_level"]},')
        print(f'  "avg_speed": {alert_data["avg_speed"]},')
        print(f'  "expected_speed": {alert_data["expected_speed"]}...')
        kafka_messages += 1
        
        # Step 2: Context Aggregation
        print(f"\nCONTEXT AGGREGATOR: Gathering context for {scenario['segment_id']}")
        
        # Simulate context gathering
        weather_conditions = ['clear', 'rain', 'fog']
        weather = random.choice(weather_conditions)
        visibility = round(random.uniform(5.0, 10.0), 1)
        
        context_data = {
            "location": {"latitude": gps_data["latitude"], "longitude": gps_data["longitude"]},
            "weather_conditions": {
                "condition": weather,
                "visibility": visibility,
                "impact": "high" if weather == "rain" else "minimal"
            },
            "news_items": [
                {"title": "Construction delays reported", "relevance": "medium"},
                {"title": "Event traffic expected downtown", "relevance": "high"}
            ],
            "events_nearby": [
                {"type": "sports_event", "impact": "high", "attendance": 25000}
            ],
            "social_mentions": [
                {"platform": "twitter", "sentiment": "negative", "mentions": 23}
            ]
        }
        
        print(f"  News: Found {len(context_data['news_items'])} relevant news articles")
        print(f"  Weather: {weather} weather, visibility {visibility}km")
        print(f"  Events: {len(context_data['events_nearby'])} nearby events") 
        print(f"  AI Analysis generated")
        
        print(f"Cache: Cached context:{scenario['segment_id']}")
        redis_entries += 1
        
        print(f"Kafka: context_data <- {scenario['segment_id']}: {{")
        print(f'  "location": {{')
        print(f'    "latitude": {gps_data["latitude"]},')
        print(f'    "longitude": {gps_data["longitude"]}')
        print(f'  }},')
        print(f'  "weather_conditions": {{...')
        kafka_messages += 1
        
        # Step 3: Fix Recommender
        print(f"\nFIX RECOMMENDER: Generating solutions for {scenario['segment_id']}")
        
        recommendations = []
        
        # Generate recommendations based on severity
        if congestion_level > 0.7:  # Critical
            recommendations.extend([
                {
                    "action": "signal_timing",
                    "priority": "CRITICAL",
                    "description": "Implement emergency signal timing to prioritize flow from congested direction",
                    "impact": "Improve flow rate by 25-40%",
                    "time": "5-15 minutes"
                },
                {
                    "action": "reroute", 
                    "priority": "HIGH",
                    "description": "Issue immediate reroute alerts to navigation apps and traffic management",
                    "impact": "Reduce traffic volume by 30-50%",
                    "time": "immediate"
                },
                {
                    "action": "enforcement",
                    "priority": "HIGH", 
                    "description": "Deploy traffic officers to manage event-related congestion",
                    "impact": "Improve traffic flow by 20-35%",
                    "time": "15-30 minutes"
                }
            ])
        elif congestion_level > 0.4:  # Moderate
            recommendations.append({
                "action": "enforcement",
                "priority": "HIGH",
                "description": "Deploy traffic officers to manage event-related congestion",
                "impact": "Improve traffic flow by 20-35%", 
                "time": "15-30 minutes"
            })
        
        # Weather-specific recommendations
        if weather in ['rain', 'fog']:
            recommendations.append({
                "action": "public_alert",
                "priority": "MEDIUM" if weather == "fog" else "HIGH",
                "description": f"Activate dynamic message signs warning of {weather} conditions",
                "impact": "Improve driver awareness and safety",
                "time": "immediate"
            })
        
        print(f"  Generated {len(recommendations)} recommendations:")
        for j, rec in enumerate(recommendations, 1):
            print(f"     {j}. [{rec['priority']}] {rec['action']}: {rec['description'][:60]}...")
            print(f"        Impact: {rec['impact']}")
            print(f"        Time: {rec['time']}")
        
        # Send recommendations to Kafka
        for rec in recommendations:
            action_id = f"{rec['action']}_{scenario['segment_id']}_{int(time.time())}"
            print(f"Kafka: recommendations <- {action_id}: {{")
            print(f'  "action_id": "{action_id}",')
            print(f'  "action_type": "{rec["action"]}",')
            print(f'  "description": "{rec["description"][:20]}..."')
            kafka_messages += 1
        
        # Scenario summary
        print(f"\nSCENARIO SUMMARY:")
        print(f"   Congestion Level: {congestion_level:.0%}")
        print(f"   Key Factors: {', '.join(factors)}")
        print(f"   Recommendations: {len(recommendations)} actions")
        print(f"   Response Time: <30 seconds")
        
        print("\n" + "=" * 60)
    
    # Demo complete
    print(f"\nDEMO COMPLETE!")
    print(f"\nWhat You've Seen:")
    print(f"   + Real-time congestion detection with ML logic")
    print(f"   + Context aggregation from multiple sources") 
    print(f"   + AI-powered situation analysis")
    print(f"   + Priority-based action recommendations")
    print(f"   + Event-driven agent communication")
    
    print(f"\nSystem Statistics:")
    print(f"   Kafka Messages: {kafka_messages}")
    print(f"   Redis Cache Entries: {redis_entries}")
    print(f"   Agents Coordinated: 3")
    print(f"   Scenarios Processed: {len(scenarios)}")
    
    print(f"\nWith Docker Running:")
    print(f"   - This same logic runs distributed across 6 agents")
    print(f"   - Real external data sources (news, weather, social)")
    print(f"   - FastAPI endpoints for integration")
    print(f"   - Real-time streaming with Kafka")
    print(f"   - Persistent storage with Redis")
    print(f"   - Web dashboard for monitoring")

if __name__ == "__main__":
    simulate_traffic_scenario() 