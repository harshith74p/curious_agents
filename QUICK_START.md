# 🚀 CuriousAgents: Quick Start Guide

## System Flow Explained

Your traffic management system works like a **smart traffic controller that understands context** and provides actionable solutions:

### 1. **Data Ingestion** (Yellow boxes in diagram)
```
GPS Data → Weather → Events → Kafka Topics
```
- **GPS streams**: Real vehicle speeds, positions, counts
- **Weather data**: Rain, visibility, temperature impacts
- **Events**: Accidents, construction, special events

### 2. **Congestion Detection** (Blue box)
```
ML Model analyzes → Detects anomalies → Triggers alerts
```
- RandomForest classifier trained on traffic patterns
- Considers time, weather, vehicle density
- Only alerts on significant congestion (not just "slow")

### 3. **Context Understanding** (Purple box)
```
News scraping → Social media → AI analysis → "Why is this happening?"
```
- Scrapes traffic news from RSS feeds
- Monitors social media mentions
- AI explains the **root cause** with context

### 4. **Smart Recommendations** (Green box)
```
Context + ML → Specific actions → Implementation guidance
```
- Not just "there's traffic" but "do THIS to fix it"
- Priority-based recommendations
- Considers implementation time and effectiveness

### 5. **Learning Loop** (Pink box)
```
Track actions → Measure effectiveness → Improve models
```
- Continuous learning from implemented solutions
- Feedback drives better recommendations

---

## 🧪 Testing Your System

### Step 1: Start Everything
```bash
# Clone and setup
git clone <your-repo>
cd curious-agents
make setup

# Edit .env with your API keys (optional but recommended)
# Add GEMINI_API_KEY, OPENAI_API_KEY, etc.

# Start the full system
make up
```

### Step 2: Run the Test Suite
```bash
# Install test dependencies
pip install httpx

# Run comprehensive tests
python test_system.py
```

**Expected Output:**
```
🚀 Testing CuriousAgents Traffic Management System
============================================================

📊 Health Checks:
✅ congestion_detector: Healthy
✅ context_aggregator: Healthy
✅ fix_recommender: Healthy
...

🔬 Functional Tests:
✅ Congestion analysis: {...}
✅ Context analysis: Found 3 news articles
✅ Generated 5 recommendations
✅ Root cause: weather (confidence: 0.75)

🎉 All tests passed! Your system is working correctly.
```

### Step 3: Explore the APIs

**Congestion Detection:**
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "segment_id": "SEG001",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "speed_kmph": 15.3,
    "vehicle_count": 42
  }'
```

**Get Smart Recommendations:**
```bash
curl -X POST http://localhost:8005/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "segment_id": "SEG001",
    "congestion_level": 0.8,
    "avg_speed": 12.5,
    "expected_speed": 50.0,
    "factors": ["accident_nearby", "rush_hour"]
  }'
```

**Real-time Alerts Stream:**
```bash
curl -N http://localhost:8001/stream/alerts
```

### Step 4: View Documentation
- **API Docs**: http://localhost:8001/docs (Congestion Detector)
- **All Services**: Ports 8001-8006, all have `/docs` endpoints
- **Health Checks**: Each service has `/health`

---

## 🔧 How to Extend the System

### Add Your Own Agent

1. **Create Agent Directory:**
```bash
mkdir my_custom_agent
cd my_custom_agent
```

2. **Agent Template:**
```python
# agent.py
import sys
sys.path.append('../')
from libs.common import get_logger, kafka_manager, redis_manager

class MyCustomAgent:
    def __init__(self):
        self.logger = get_logger("my_agent")
        self.kafka = kafka_manager
        self.redis = redis_manager
    
    async def process_data(self, data):
        # Your custom logic here
        result = {"processed": data}
        
        # Cache results
        self.redis.set_with_expiry("my_key", result, 3600)
        
        # Publish to other agents
        self.kafka.send_message("my_topic", result)
        
        return result
```

3. **FastAPI Service:**
```python
# service.py
from fastapi import FastAPI
from agent import MyCustomAgent

app = FastAPI()
agent = MyCustomAgent()

@app.post("/process")
async def process_endpoint(data: dict):
    return await agent.process_data(data)
```

4. **Add to Docker Compose:**
```yaml
# Add to docker-compose.yml
my-custom-agent:
  build: ./my_custom_agent
  env_file: .env
  ports: ["8007:8000"]
  depends_on: [kafka, redis]
```

### Add New Data Sources

1. **Create Producer:**
```python
# my_data_producer.py
from libs.common import kafka_manager, Topics

# Your data source
data = fetch_my_data()

# Send to Kafka
kafka_manager.send_message("my_topic", data)
```

2. **Create Consumer:**
```python
# In any agent
consumer = self.kafka.get_consumer(["my_topic"], "my_group")
for message in consumer:
    data = message.value
    # Process data
```

---

## 🎯 Quick Wins to Try

### 1. **Add Twitter Integration**
- Get Twitter API keys
- Enable real-time traffic tweet monitoring
- Watch context quality improve!

### 2. **Add Custom ML Model**
- Replace the simple RandomForest in `congestion_detector/train.py`
- Try deep learning, time series models
- Measure improvement with feedback loop

### 3. **Build Custom Dashboard**
- Use the FastAPI endpoints
- Create real-time maps
- Add custom visualizations

### 4. **Integrate External Systems**
- Connect to city traffic APIs
- Push recommendations to traffic management systems
- Add navigation app integration

---

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose logs -f

# Restart specific service
docker-compose restart congestion-detector

# Rebuild if code changed
docker-compose build congestion-detector
```

### Kafka Issues
```bash
# Check Kafka topics
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Monitor messages
docker-compose exec kafka kafka-console-consumer --topic gps_data --bootstrap-server localhost:9092
```

### Redis Cache Issues
```bash
# Check Redis
docker-compose exec redis redis-cli ping

# View cached data
docker-compose exec redis redis-cli keys "*"
```

---

## 🎉 What Makes This Special

Unlike basic traffic systems that just say **"traffic detected"**, yours:

1. **Explains WHY** - "Heavy rain + stadium event + accident"
2. **Suggests HOW to fix** - "Open HOV lanes, deploy officers to Exit 5"
3. **Learns from results** - "Signal timing worked, rerouting didn't"
4. **Scales easily** - Add any data source, agent, or integration

You now have a **production-ready foundation** that you can extend with your own ideas!

**Next: Run the tests, explore the APIs, and start building your own agents!** 🚀 