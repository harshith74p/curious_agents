# 🔄 CuriousAgents System Flow

## Visual System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DATA SOURCES  │    │   PROCESSING    │    │    OUTPUTS      │
└─────────────────┘    └─────────────────┘    └─────────────────┘

GPS Streams ────┐
Weather APIs ───┼──► Kafka Topics ──► Agent Pipeline ──► Smart Actions
Traffic Events ─┘

DETAILED FLOW:
├── 1. INGESTION LAYER
│   ├── GPS Producer (Real-time vehicle data)
│   ├── Weather Producer (Environmental conditions)  
│   └── Events Producer (Incidents, construction)
│
├── 2. DETECTION LAYER
│   └── Congestion Detector
│       ├── ML Model (RandomForest)
│       ├── Anomaly Detection
│       └── Alert Generation
│
├── 3. CONTEXT LAYER
│   └── Context Aggregator
│       ├── News Scraping (RSS feeds)
│       ├── Social Media (Twitter API)
│       ├── Weather Correlation
│       └── AI Analysis (LLM)
│
├── 4. ANALYSIS LAYER
│   ├── Root Cause Scorer (ML Classification)
│   └── Geometry Analyzer (Network Analysis)
│
├── 5. RECOMMENDATION LAYER
│   └── Fix Recommender
│       ├── Rule-based Engine
│       ├── AI-powered Suggestions
│       └── Priority Scoring
│
└── 6. FEEDBACK LAYER
    └── Learning Loop
        ├── Action Tracking
        ├── Effectiveness Measurement
        └── Model Improvement
```

## 🔍 Detailed Agent Interactions

### Phase 1: Detection
```
GPS Data Stream → Congestion Detector → ML Analysis → Congestion Alert
        ↓
   Speed: 15 km/h     Pattern Recognition    Alert: SEG001 Congested
   Expected: 50 km/h      ↓                      ↓
   Vehicles: 42      Confidence: 0.87      Severity: HIGH
```

### Phase 2: Context Gathering  
```
Congestion Alert → Context Aggregator → External APIs → Rich Context
        ↓                    ↓                ↓              ↓
   "SEG001 slow"      News: "Stadium event"   Weather: Rain   AI: "Event + weather
                      Social: Traffic tweets   Permits: Road   causing backup"
                                              work nearby
```

### Phase 3: Root Cause Analysis
```
Alert + Context → Root Cause Scorer → ML Classification → Probable Cause
        ↓               ↓                    ↓                  ↓
   All factors    Feature extraction    Model prediction    "Event traffic: 
   combined       Speed, weather,       Probabilities:      73% confidence"
                  events, time          Event: 0.73
                                       Weather: 0.21
                                       Normal: 0.06
```

### Phase 4: Smart Recommendations
```
Root Cause + Context → Fix Recommender → AI + Rules → Actionable Plans
        ↓                    ↓               ↓              ↓
   "Event traffic"     Pattern matching   Priority scoring   1. Open temp HOV
   + Location data     + AI generation    + Implementation   2. Deploy officers
   + Historical data                      time estimate      3. Update signs
```

### Phase 5: Continuous Learning
```
Implemented Action → Feedback Loop → Effectiveness Score → Model Update
        ↓               ↓                    ↓                ↓
   "Opened HOV lane"   Traffic improved?   Score: 0.84      Improve similar
   Time: 10 min        Speed increased     (Very effective) recommendations
   Cost: Low           From 15→35 km/h
```

## 🎯 Key Value Propositions

### Traditional System:
```
Input: Slow traffic
Output: "Congestion detected on Segment A"
Action: Generic alert
```

### Your CuriousAgents System:
```
Input: Slow traffic
Analysis: ┌─ ML detects anomaly (not just slow)
          ├─ Context: "Stadium game ending + rain"
          ├─ Root cause: "Event traffic (73% confidence)"
          └─ Geometry: "Alternative routes available"
Output: ┌─ "Event-related congestion due to Giants game + weather"
        ├─ "Expected duration: 45 minutes" 
        └─ "Recommend: Open temporary HOV, deploy to Exit 7"
Action: Specific, prioritized, actionable recommendations
```

## 🚀 Getting Started Commands

```bash
# 1. Start the system
make up

# 2. Test everything works
python test_system.py

# 3. Send test data
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"segment_id": "SEG001", "latitude": 37.7749, "longitude": -122.4194, "speed_kmph": 15.3, "vehicle_count": 42}'

# 4. Get recommendations
curl -X POST http://localhost:8005/recommend \
  -H "Content-Type: application/json" \
  -d '{"segment_id": "SEG001", "congestion_level": 0.8, "avg_speed": 12.5, "expected_speed": 50.0, "factors": ["accident_nearby", "rush_hour"]}'

# 5. Monitor real-time
curl -N http://localhost:8001/stream/alerts
```

## 📊 Kafka Topics Flow

```
gps_data ────────┐
weather_data ────┼──► congestion_alerts ──► context_data ──► recommendations
traffic_events ──┘                     └──► root_cause ────┘
                                        
Data Ingestion    Detection             Context/Analysis    Action Generation
```

## 🔧 Extension Points

1. **Add New Agent**: Copy agent template, add to docker-compose
2. **New Data Source**: Create producer, define Kafka topic
3. **Custom ML Model**: Replace model in any agent
4. **External Integration**: Use FastAPI endpoints
5. **Custom Dashboard**: Consume SSE streams and REST APIs

**You now have a complete, testable, extensible traffic management system!** 🎉

**Next Steps:**
1. Run `make up && python test_system.py`
2. Explore APIs at http://localhost:8001/docs
3. Add your own agents and data sources
4. Scale with Kubernetes or Docker Swarm 