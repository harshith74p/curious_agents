#!/usr/bin/env python3
"""
Simple test script to validate the traffic management system
"""

import asyncio
import httpx
import json
import time
from datetime import datetime

# Test configuration
BASE_URLS = {
    "congestion_detector": "http://localhost:8001",
    "context_aggregator": "http://localhost:8002", 
    "geometry_analyzer": "http://localhost:8003",
    "root_cause_scorer": "http://localhost:8004",
    "fix_recommender": "http://localhost:8005",
    "feedback_loop": "http://localhost:8006"
}

async def test_service_health(service_name: str, url: str):
    """Test if a service is healthy"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}/health", timeout=5.0)
            if response.status_code == 200:
                print(f"✅ {service_name}: Healthy")
                return True
            else:
                print(f"❌ {service_name}: Unhealthy (status: {response.status_code})")
                return False
    except Exception as e:
        print(f"❌ {service_name}: Failed to connect ({e})")
        return False

async def test_congestion_detection():
    """Test congestion detection"""
    print("\n🧪 Testing Congestion Detection...")
    
    try:
        async with httpx.AsyncClient() as client:
            # Test analyze endpoint
            test_data = {
                "segment_id": "SEG001",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "speed_kmph": 15.3,
                "vehicle_count": 42
            }
            
            response = await client.post(
                f"{BASE_URLS['congestion_detector']}/analyze",
                json=test_data,
                timeout=10.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Congestion analysis: {result}")
                return True
            else:
                print(f"❌ Congestion analysis failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Congestion detection test failed: {e}")
        return False

async def test_context_aggregation():
    """Test context aggregation"""
    print("\n🧪 Testing Context Aggregation...")
    
    try:
        async with httpx.AsyncClient() as client:
            test_data = {
                "latitude": 37.7749,
                "longitude": -122.4194,
                "radius_km": 2.0
            }
            
            response = await client.post(
                f"{BASE_URLS['context_aggregator']}/analyze",
                json=test_data,
                timeout=15.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Context analysis: Found {len(result.get('news_articles', []))} news articles")
                return True
            else:
                print(f"❌ Context analysis failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Context aggregation test failed: {e}")
        return False

async def test_fix_recommendation():
    """Test fix recommendation"""
    print("\n🧪 Testing Fix Recommendations...")
    
    try:
        async with httpx.AsyncClient() as client:
            test_data = {
                "segment_id": "SEG001",
                "congestion_level": 0.8,
                "avg_speed": 12.5,
                "expected_speed": 50.0,
                "factors": ["accident_nearby", "rush_hour"]
            }
            
            response = await client.post(
                f"{BASE_URLS['fix_recommender']}/recommend",
                json=test_data,
                timeout=15.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Generated {len(result)} recommendations")
                for rec in result[:2]:  # Show first 2
                    print(f"   - {rec['action_type']}: {rec['description'][:50]}...")
                return True
            else:
                print(f"❌ Fix recommendation failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Fix recommendation test failed: {e}")
        return False

async def test_root_cause_scoring():
    """Test root cause scoring"""
    print("\n🧪 Testing Root Cause Scoring...")
    
    try:
        async with httpx.AsyncClient() as client:
            test_data = {
                "congestion_data": {
                    "avg_speed": 15.0,
                    "vehicle_count": 45,
                    "hour": 8,
                    "day_of_week": 1,
                    "is_rush_hour": 1
                },
                "context_data": {
                    "weather_conditions": {
                        "precipitation": 2.5,
                        "visibility": 5.0
                    },
                    "traffic_alerts": [
                        {"type": "accident"}
                    ]
                }
            }
            
            response = await client.post(
                f"{BASE_URLS['root_cause_scorer']}/score",
                json=test_data,
                timeout=10.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Root cause: {result['root_cause']} (confidence: {max(result['probabilities'].values()):.2f})")
                return True
            else:
                print(f"❌ Root cause scoring failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Root cause scoring test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Testing CuriousAgents Traffic Management System")
    print("=" * 60)
    
    # Test service health
    print("\n📊 Health Checks:")
    health_results = []
    for service, url in BASE_URLS.items():
        result = await test_service_health(service, url)
        health_results.append(result)
    
    healthy_services = sum(health_results)
    print(f"\n📈 Health Summary: {healthy_services}/{len(BASE_URLS)} services healthy")
    
    if healthy_services < len(BASE_URLS):
        print("\n⚠️  Some services are not healthy. Check docker-compose logs.")
        print("   Run: docker-compose logs -f")
        return
    
    # Test functionality
    print("\n🔬 Functional Tests:")
    
    tests = [
        test_congestion_detection(),
        test_context_aggregation(), 
        test_fix_recommendation(),
        test_root_cause_scoring()
    ]
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    passed_tests = sum(1 for r in results if r is True)
    print(f"\n📈 Test Summary: {passed_tests}/{len(tests)} tests passed")
    
    if passed_tests == len(tests):
        print("\n🎉 All tests passed! Your system is working correctly.")
        print("\n🔧 Next steps:")
        print("   1. Check the dashboard at http://localhost:3000")
        print("   2. View API docs at http://localhost:8001/docs")
        print("   3. Monitor with: docker-compose logs -f")
        print("   4. Add your own agents and data sources!")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main()) 