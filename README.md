# 🚦 CuriousAgents: AI-Powered Traffic Management System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **An intelligent, multi-agent system for traffic congestion analysis that goes beyond simple detection to provide contextual understanding and actionable solutions.**

## 🎯 **What Makes This Different**

**Traditional systems**: _"Traffic detected on Highway 101"_  
**CuriousAgents**: _"Stadium event + rain causing 73% probability event-traffic on SEG001. **Recommend**: Open HOV lanes (5 min implementation), deploy officers to Exit 7 (15 min), update dynamic signs (immediate). Expected 45min duration based on historical patterns."_

## ⚡ **Quick Demo**

```bash
# Clone and run the demo (no setup required!)
git clone https://github.com/YOUR_USERNAME/curious-agents.git
cd curious-agents
python demo_local.py
```

**Output**: Watch 6 AI agents work together to analyze traffic and provide intelligent solutions!

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Congestion      │    │ Context         │    │ Fix             │
│ Detector        │───▶│ Aggregator      │───▶│ Recommender     │
│ (ML + Rules)    │    │ (LLM + APIs)    │    │ (AI + Rules)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Kafka + Redis                                │
│               (Real-time Data Flow)                            │
└─────────────────────────────────────────────────────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Data Ingestion  │    │ Geometry        │    │ Feedback Loop   │
│ (GPS, Weather)  │    │ Analyzer        │    │ (Learning)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 **Core Agents**

| Agent | Purpose | Technology | Output |
|-------|---------|------------|---------|
| **🔍 Congestion Detector** | ML-powered anomaly detection | RandomForest + Rules | Congestion alerts with confidence |
| **🧠 Context Aggregator** | Multi-source intelligence | LLM + RSS + APIs | "Why" analysis with context |
| **💡 Fix Recommender** | Actionable solutions | AI + Rules Engine | Priority-ranked actions |
| **🗺️ Geometry Analyzer** | Network analysis | OSMnx + NetworkX | Alternative routes |
| **📊 Root Cause Scorer** | Pattern recognition | ML Classification | Probable causes |
| **🔄 Feedback Loop** | Continuous learning | Redis Streams | Effectiveness tracking |

## 🚀 **Quick Start**

### Option 1: Full System (Recommended)
```bash
# Prerequisites: Docker Desktop
docker compose up --build -d
python test_system.py  # Should show all ✅ green!

# Explore APIs
curl http://localhost:8001/docs
```

### Option 2: Local Demo
```bash
# No dependencies required
python demo_local.py
```

### Option 3: Test Individual Components
```bash
python validate_code.py  # Validates all components
```

## 📊 **Live Demo Results**

When you run the demo, you'll see real agent interactions:

```
🚨 CONGESTION DETECTED!
   Level: 75% (Confidence: 95%)
   Speed: 12.3 km/h (Expected: 50.0)

🧠 CONTEXT ANALYSIS:
   📰 "Giants Game Tonight - Heavy Traffic Expected" 
   🌤️ Weather: Rain, visibility 5.1km
   🎯 Events: Baseball game nearby

💡 SMART RECOMMENDATIONS:
   1. [CRITICAL] Emergency signal timing (25-40% improvement, 5-15 min)
   2. [HIGH] Immediate reroute alerts (30-50% volume reduction, immediate)
   3. [HIGH] Deploy traffic officers (20-35% improvement, 15-30 min)

📈 System Statistics:
   📤 Kafka Messages: 9
   💾 Redis Cache Entries: 4  
   🤖 Agents Coordinated: 3
   ⏱️ Response Time: <30 seconds
```

## 🛠️ **Technology Stack**

- **🐍 Python 3.11+** - Core development
- **⚡ FastAPI** - REST APIs with auto-documentation  
- **🔄 Apache Kafka** - Real-time agent communication
- **💾 Redis** - Caching and streaming
- **🐳 Docker** - Containerized deployment
- **🤖 AI/ML**: Scikit-learn, Google Gemini, OpenAI
- **🗺️ Geospatial**: OSMnx, NetworkX, GeoPandas
- **📊 Data**: Pandas, NumPy

## 📡 **API Examples**

### Analyze Traffic Congestion
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

### Get Smart Recommendations
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

### Stream Real-time Alerts
```bash
curl -N http://localhost:8001/stream/alerts
```

## 📈 **Extensibility**

### Add Your Own Agent
1. **Copy agent template**: Follow the pattern in any agent directory
2. **Implement logic**: Add your custom analysis
3. **Add to Docker**: Update `docker-compose.yml`
4. **Connect via Kafka**: Subscribe to relevant topics

### Add New Data Sources
1. **Create producer**: Follow `ingestion/` patterns  
2. **Define Kafka topic**: Add to `libs/common.py`
3. **Process in agents**: Subscribe and analyze

## 🔧 **Configuration**

### Environment Variables
Create `.env` file:
```bash
# AI Services (optional but recommended)
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# External Data Sources  
WEATHER_API_KEY=your_weather_api_key
TWITTER_BEARER_TOKEN=your_twitter_token

# Infrastructure (defaults work locally)
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
REDIS_URL=redis://redis:6379/0
```

## 📚 **Documentation**

- **[🚀 Setup Guide](SETUP_GUIDE.md)** - Multiple ways to run the system
- **[🔄 System Flow](SYSTEM_FLOW.md)** - Detailed architecture explanation  
- **[⚡ Quick Start](QUICK_START.md)** - Get running in 5 minutes
- **[🔧 Git Setup](GIT_SETUP.md)** - Repository management

## 🧪 **Testing**

```bash
# Comprehensive system test
python test_system.py

# Code structure validation  
python validate_code.py

# Interactive demo
python demo_local.py
```

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Areas for Enhancement
- 🌐 **New data sources** (social media, city APIs)
- 🤖 **Advanced ML models** (deep learning, time series)
- 📱 **Mobile dashboard** (React Native, Flutter)
- 🚀 **Cloud deployment** (Kubernetes, AWS/GCP)
- 🔌 **External integrations** (traffic management systems)

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- OpenStreetMap for road network data
- Traffic engineering best practices
- Open source ML/AI community
- Real-world traffic management insights

## 📞 **Support**

- 🐛 **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/curious-agents/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/curious-agents/discussions)
- 📧 **Email**: [your.email@example.com](mailto:your.email@example.com)

---

<div align="center">

**🌟 Star this repo if you find it useful! 🌟**

**Built with ❤️ for intelligent traffic management**

[⭐ Star](https://github.com/YOUR_USERNAME/curious-agents) · [🍴 Fork](https://github.com/YOUR_USERNAME/curious-agents/fork) · [📝 Report Bug](https://github.com/YOUR_USERNAME/curious-agents/issues) · [💡 Request Feature](https://github.com/YOUR_USERNAME/curious-agents/issues)

</div> 