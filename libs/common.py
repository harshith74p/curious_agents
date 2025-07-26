"""
CuriousAgents: Common utilities and data models for the traffic management system
Built with Google Agent Development Kit (ADK)
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
import httpx
import math
from kafka import KafkaProducer, KafkaConsumer
import redis
from google.adk.agents import LlmAgent, BaseAgent
from google.adk.tools import FunctionTool
from google.adk.memory import InMemoryMemoryService
import pandas as pd

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Logging setup
def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, LOG_LEVEL))
    return logger

# Data Models
@dataclass
class GPSPoint:
    segment_id: str
    latitude: float
    longitude: float
    speed_kmph: float
    vehicle_count: int
    timestamp: datetime
    
    def to_dict(self):
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class WeatherData:
    latitude: float
    longitude: float
    temperature: float
    humidity: float
    wind_speed: float
    precipitation: float
    visibility: float
    timestamp: datetime
    
    def to_dict(self):
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class TrafficEvent:
    event_id: str
    event_type: str  # accident, construction, weather, special_event
    latitude: float
    longitude: float
    severity: float  # 0.0 to 1.0
    description: str
    start_time: datetime
    end_time: Optional[datetime]
    affected_segments: List[str]
    
    def to_dict(self):
        return {
            **asdict(self),
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None
        }

@dataclass
class CongestionAlert:
    segment_id: str
    congestion_level: float  # 0.0 to 1.0
    congestion_score: float
    avg_speed: float
    expected_speed: float
    vehicle_density: float
    confidence: float
    factors: List[str]
    timestamp: datetime
    location: Dict[str, float]  # lat, lng
    
    def to_dict(self):
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class ContextData:
    location: Dict[str, float]
    news_items: List[Dict]
    weather_conditions: Dict
    events_nearby: List[Dict]
    social_mentions: List[Dict]
    analysis_summary: str
    confidence: float
    timestamp: datetime
    
    def to_dict(self):
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class RecommendedAction:
    action_id: str
    segment_id: str
    action_type: str
    title: str
    description: str
    priority: str  # critical, high, medium, low
    estimated_impact: float  # 0.0 to 1.0
    implementation_time: str
    cost_estimate: str
    requirements: List[str]
    timestamp: datetime
    
    def to_dict(self):
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat()
        }

# Kafka Topics
class Topics:
    GPS_DATA = "gps_data"
    WEATHER_DATA = "weather_data"
    TRAFFIC_EVENTS = "traffic_events"
    CONGESTION_ALERTS = "congestion_alerts"
    CONTEXT_DATA = "context_data"
    ROOT_CAUSE = "root_cause"
    RECOMMENDATIONS = "recommendations"

# Redis Keys
class RedisKeys:
    CONGESTION_PREFIX = "congestion:"
    CONTEXT_PREFIX = "context:"
    RECOMMENDATIONS_PREFIX = "recommendations:"
    CACHE_PREFIX = "cache:"

# Google ADK Agent Factory
def create_adk_agent(
    name: str,
    description: str,
    instruction: str,
    tools: List[FunctionTool] = None,
    model: str = None,
    memory_service = None
) -> LlmAgent:
    """Create a Google ADK LLM Agent with proper configuration"""
    
    if not tools:
        tools = []
    
    if not model:
        model = DEFAULT_MODEL
    
    if not memory_service:
        memory_service = InMemoryMemoryService()
    
    agent = LlmAgent(
        name=name,
        model=model,
        description=description,
        instruction=instruction,
        tools=tools,
        memory_service=memory_service
    )
    
    return agent

# ADK Function Tool Helpers
def create_function_tool(func, name: str = None, description: str = None):
    """Create a Google ADK Function Tool from a Python function"""
    # The correct way to create a FunctionTool is to use it as a decorator
    # or create it directly with the function
    from google.adk.tools import FunctionTool
    
    # Create the tool directly with the function
    tool = FunctionTool(func)
    
    # Set name and description if provided
    if name:
        tool.name = name
    if description:
        tool.description = description
    
    return tool

# Kafka Manager
class KafkaManager:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS.split(',')
    
    def get_producer(self) -> KafkaProducer:
        return KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
    
    def get_consumer(self, topic: str, group_id: str) -> KafkaConsumer:
        return KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            auto_offset_reset='latest',
            enable_auto_commit=True
        )
    
    def send_message(self, topic: str, message: Dict, key: str = None):
        producer = self.get_producer()
        try:
            future = producer.send(topic, value=message, key=key)
            producer.flush()
            self.logger.info(f"Message sent to {topic}: {key}")
            return future
        except Exception as e:
            self.logger.error(f"Failed to send message to {topic}: {e}")
            raise
        finally:
            producer.close()

# Redis Manager
class RedisManager:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.redis_url = REDIS_URL
        self._client = None
    
    def get_client(self):
        if not self._client:
            self._client = redis.from_url(self.redis_url, decode_responses=True)
        return self._client
    
    def set_with_expiry(self, key: str, value: Any, expiry: int = 3600):
        client = self.get_client()
        if isinstance(value, dict):
            value = json.dumps(value, default=str)
        client.setex(key, expiry, value)
    
    def get_json(self, key: str) -> Optional[Dict]:
        client = self.get_client()
        value = client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return {"raw_value": value}
        return None
    
    def add_to_stream(self, stream: str, data: Dict):
        client = self.get_client()
        client.xadd(stream, data)

# Utility Functions
async def fetch_external_data(url: str, headers: Dict = None, timeout: int = 30) -> Optional[Dict]:
    """Fetch data from external API with error handling"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        get_logger(__name__).error(f"Failed to fetch from {url}: {e}")
        return None

def dataclass_to_dict(obj) -> Dict:
    """Convert dataclass to dictionary with proper serialization"""
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    return asdict(obj)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def normalize_score(value: float, min_val: float, max_val: float) -> float:
    """Normalize a value to 0-1 range"""
    if max_val == min_val:
        return 0.5
    return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))

# ADK Agent Communication Helper
class AgentCommunication:
    """Helper class for agent-to-agent communication via Kafka and Redis"""
    
    def __init__(self):
        self.kafka = KafkaManager()
        self.redis = RedisManager()
        self.logger = get_logger(__name__)
    
    def publish_agent_result(self, agent_name: str, result: Dict, topic: str):
        """Publish agent result to Kafka topic"""
        message = {
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        self.kafka.send_message(topic, message, key=agent_name)
    
    def cache_agent_result(self, agent_name: str, result: Dict, cache_key: str, expiry: int = 3600):
        """Cache agent result in Redis"""
        cache_data = {
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        self.redis.set_with_expiry(cache_key, cache_data, expiry)
    
    def get_cached_result(self, cache_key: str) -> Optional[Dict]:
        """Get cached result from Redis"""
        return self.redis.get_json(cache_key)

# Export all important classes and functions
__all__ = [
    'GPSPoint', 'WeatherData', 'TrafficEvent', 'CongestionAlert', 
    'ContextData', 'RecommendedAction', 'Topics', 'RedisKeys',
    'KafkaManager', 'RedisManager', 'AgentCommunication',
    'create_adk_agent', 'create_function_tool', 'get_logger',
    'fetch_external_data', 'dataclass_to_dict', 'calculate_distance', 
    'normalize_score'
] 