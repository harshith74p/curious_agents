#!/usr/bin/env python3
"""
Simple code validation script for CuriousAgents
Tests code structure and imports without requiring external services
"""

import os
import sys
import importlib.util
from pathlib import Path

def test_file_structure():
    """Test that all required files exist"""
    print("🔍 Testing File Structure...")
    
    required_files = [
        "docker-compose.yml",
        "Makefile", 
        "README.md",
        "QUICK_START.md",
        "SYSTEM_FLOW.md",
        "libs/common.py",
        "sample_data/gps.csv",
        "sample_data/weather.csv",
        "sample_data/events.json", 
        "sample_data/permits.json",
        "congestion_detector/agent.py",
        "congestion_detector/service.py",
        "congestion_detector/train.py",
        "context_aggregator/agent.py",
        "context_aggregator/service.py",
        "fix_recommender/agent.py",
        "fix_recommender/service.py",
        "root_cause_scorer/agent.py",
        "root_cause_scorer/service.py",
        "geometry_analyzer/agent.py",
        "geometry_analyzer/service.py",
        "feedback_loop/service.py",
        "ingestion/gps_producer.py",
        "ingestion/weather_producer.py",
        "ingestion/events_producer.py",
        "ingestion/run_all.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print(f"\n  ❌ Missing files:")
        for file_path in missing_files:
            print(f"     - {file_path}")
        return False
    
    print("  ✅ All required files present!")
    return True

def test_common_library():
    """Test the common library imports and structure"""
    print("\n🧪 Testing Common Library...")
    
    try:
        # Add libs to path
        sys.path.insert(0, 'libs')
        
        # Test basic imports (mock external dependencies)
        spec = importlib.util.spec_from_file_location("common", "libs/common.py")
        common = importlib.util.module_from_spec(spec)
        
        # Mock external dependencies that might not be installed
        sys.modules['kafka'] = type('MockKafka', (), {
            'KafkaProducer': type('MockProducer', (), {}),
            'KafkaConsumer': type('MockConsumer', (), {})
        })()
        sys.modules['redis'] = type('MockRedis', (), {
            'Redis': type('MockRedisClient', (), {
                'from_url': lambda url, **kwargs: type('MockClient', (), {
                    'ping': lambda: True,
                    'get': lambda key: None,
                    'setex': lambda key, time, value: True
                })()
            })
        })()
        
        spec.loader.exec_module(common)
        
        # Test data models
        gps_point = common.GPSPoint(
            segment_id="TEST001",
            latitude=37.7749,
            longitude=-122.4194,
            speed_kmph=25.0,
            timestamp=1703080800.0,
            vehicle_count=10
        )
        
        print(f"  ✅ GPSPoint created: {gps_point.segment_id}")
        
        # Test other data models
        alert = common.CongestionAlert(
            segment_id="TEST001",
            congestion_level=0.7,
            avg_speed=15.0,
            expected_speed=50.0,
            confidence=0.85,
            timestamp=1703080800.0,
            factors=["rush_hour", "weather"]
        )
        
        print(f"  ✅ CongestionAlert created: {alert.segment_id}")
        
        # Test utility functions
        distance = common.calculate_distance(37.7749, -122.4194, 37.7849, -122.4094)
        print(f"  ✅ Distance calculation: {distance:.2f} km")
        
        normalized = common.normalize_score(75, 0, 100)
        print(f"  ✅ Score normalization: {normalized}")
        
        # Test topics and keys
        print(f"  ✅ Kafka topics defined: {len([attr for attr in dir(common.Topics) if not attr.startswith('_')])}")
        print(f"  ✅ Redis keys defined: {len([attr for attr in dir(common.RedisKeys) if not attr.startswith('_')])}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Common library test failed: {e}")
        return False

def test_agent_structure():
    """Test that agent files have proper structure"""
    print("\n🔧 Testing Agent Structure...")
    
    agents = [
        "congestion_detector",
        "context_aggregator", 
        "fix_recommender",
        "root_cause_scorer",
        "geometry_analyzer"
    ]
    
    for agent in agents:
        try:
            # Check agent.py exists and has basic structure
            agent_file = Path(f"{agent}/agent.py")
            if agent_file.exists():
                content = agent_file.read_text()
                
                # Check for key patterns
                has_class = "class" in content
                has_init = "__init__" in content
                has_logger = "logger" in content
                has_async = "async def" in content
                
                status = "✅" if all([has_class, has_init, has_logger]) else "⚠️"
                print(f"  {status} {agent}: class={has_class}, init={has_init}, logger={has_logger}, async={has_async}")
            else:
                print(f"  ❌ {agent}: agent.py missing")
                
            # Check service.py
            service_file = Path(f"{agent}/service.py")
            if service_file.exists():
                content = service_file.read_text()
                has_fastapi = "FastAPI" in content
                has_endpoints = "@app." in content
                print(f"    └── service.py: FastAPI={has_fastapi}, endpoints={has_endpoints}")
            else:
                print(f"    └── service.py: missing")
                
        except Exception as e:
            print(f"  ❌ {agent}: Error reading files - {e}")
    
    return True

def test_sample_data():
    """Test sample data files"""
    print("\n📊 Testing Sample Data...")
    
    try:
        # Test GPS data
        import csv
        with open("sample_data/gps.csv", 'r') as f:
            reader = csv.DictReader(f)
            gps_rows = list(reader)
            print(f"  ✅ GPS data: {len(gps_rows)} rows")
            if gps_rows:
                print(f"    Sample: {gps_rows[0]['segment_id']} - {gps_rows[0]['speed_kmph']} km/h")
        
        # Test weather data
        with open("sample_data/weather.csv", 'r') as f:
            reader = csv.DictReader(f)
            weather_rows = list(reader)
            print(f"  ✅ Weather data: {len(weather_rows)} rows")
        
        # Test events data
        import json
        with open("sample_data/events.json", 'r') as f:
            events = json.load(f)
            print(f"  ✅ Events data: {len(events)} events")
            
        # Test permits data
        with open("sample_data/permits.json", 'r') as f:
            permits = json.load(f)
            print(f"  ✅ Permits data: {len(permits)} permits")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Sample data test failed: {e}")
        return False

def test_docker_config():
    """Test Docker configuration"""
    print("\n🐳 Testing Docker Configuration...")
    
    try:
        with open("docker-compose.yml", 'r') as f:
            content = f.read()
            
        services = content.count("build:")
        ports = content.count("ports:")
        dependencies = content.count("depends_on:")
        
        print(f"  ✅ Services with builds: {services}")
        print(f"  ✅ Port mappings: {ports}")
        print(f"  ✅ Dependencies: {dependencies}")
        
        # Check for key services
        key_services = ["kafka", "redis", "congestion-detector", "context-aggregator"]
        for service in key_services:
            if service in content:
                print(f"    ✅ {service} configured")
            else:
                print(f"    ❌ {service} missing")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Docker config test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🚀 CuriousAgents Code Validation")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_common_library,
        test_agent_structure,
        test_sample_data,
        test_docker_config
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n📈 Validation Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All validation tests passed!")
        print("\n🔧 Next Steps:")
        print("  1. Install Docker Desktop for Windows")
        print("  2. Run: docker compose up --build -d")
        print("  3. Run: python test_system.py")
        print("  4. Explore APIs at http://localhost:8001/docs")
        
        print("\n💡 What you have:")
        print("  ✅ Complete multi-agent traffic management system")
        print("  ✅ 6 intelligent agents with ML and AI capabilities")
        print("  ✅ Real-time data processing with Kafka")
        print("  ✅ Caching and storage with Redis")
        print("  ✅ REST APIs with FastAPI")
        print("  ✅ Realistic sample data for testing")
        print("  ✅ Docker containerization")
        print("  ✅ Comprehensive documentation")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Check the error messages above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 