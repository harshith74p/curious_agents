# 🚀 How to Run CuriousAgents Traffic Management System

## 📋 **What You Have Right Now**

✅ **Complete working system** - All code is ready  
✅ **Demo already works** - You've seen it in action  
✅ **Production-ready** - Just needs Docker for full deployment  

---

## 🏃‍♂️ **Option 1: Full System (Recommended)**

### Step 1: Install Docker Desktop
1. **Download**: https://docs.docker.com/desktop/install/windows/
2. **Install** and restart your computer
3. **Verify**: Open PowerShell and run `docker --version`

### Step 2: Start Your System
```powershell
# In your current directory (C:\Users\harsh\curious-agents)

# Start all services (6 agents + infrastructure)
docker compose up --build -d

# Check if all services are running
docker compose ps

# View logs
docker compose logs -f
```

### Step 3: Test Everything Works
```powershell
# Run the comprehensive test suite
python test_system.py

# Expected: All ✅ green checkmarks!
```

### Step 4: Explore Your System
- **API Documentation**: http://localhost:8001/docs
- **All Services**: Ports 8001-8006 (each has `/docs`)
- **Health Checks**: http://localhost:8001/health

### Step 5: Send Test Traffic Data
```powershell
# Test congestion detection
curl -X POST http://localhost:8001/analyze `
  -H "Content-Type: application/json" `
  -d '{
    "segment_id": "SEG001",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "speed_kmph": 15.3,
    "vehicle_count": 42
  }'

# Get smart recommendations
curl -X POST http://localhost:8005/recommend `
  -H "Content-Type: application/json" `
  -d '{
    "segment_id": "SEG001",
    "congestion_level": 0.8,
    "avg_speed": 12.5,
    "expected_speed": 50.0,
    "factors": ["accident_nearby", "rush_hour"]
  }'
```

---

## 💻 **Option 2: Run Locally (What You Can Do Right Now)**

### A. Run the Demo Again
```powershell
# See the intelligent agents in action
python demo_local.py
```

### B. Test Individual Components
```powershell
# Install minimal dependencies
pip install fastapi uvicorn

# Run a single agent locally
cd congestion_detector
python -c "
import sys
sys.path.append('../')
from agent import CongestionDetector
print('Congestion Detector imported successfully!')
"
```

### C. Modify and Experiment
```powershell
# Edit the demo to test your own scenarios
notepad demo_local.py

# Change the GPS data in the scenarios:
# - Try different speed values
# - Modify vehicle counts  
# - Test different times of day
```

---

## 🔧 **Option 3: Development Mode**

### Run Single Services Locally
```powershell
# Terminal 1: Start Redis (if you have it)
redis-server

# Terminal 2: Start a single agent
cd congestion_detector
pip install -r requirements.txt
python service.py

# Terminal 3: Test the agent
curl http://localhost:8000/health
```

---

## 🎯 **Quick Start Commands**

### If you have Docker:
```powershell
docker compose up -d && python test_system.py
```

### If you don't have Docker:
```powershell
python demo_local.py
```

### To stop everything:
```powershell
docker compose down
```

---

## 🐛 **Troubleshooting**

### Docker Issues
```powershell
# Docker not found
# → Install Docker Desktop from link above

# Services won't start  
docker compose logs

# Port conflicts
docker compose down && docker compose up -d

# Clean restart
docker compose down -v && docker compose up --build -d
```

### Python Issues
```powershell
# Missing dependencies
pip install httpx

# Permission errors
# → Run PowerShell as Administrator
```

---

## 🌟 **What Each Option Gives You**

| Feature | Demo | Local Agent | Full Docker |
|---------|------|-------------|-------------|
| See system logic | ✅ | ✅ | ✅ |
| Test agents | ✅ | ✅ | ✅ |
| Real APIs | ❌ | ⚠️ | ✅ |
| Full distribution | ❌ | ❌ | ✅ |
| External data | ❌ | ❌ | ✅ |
| Production ready | ❌ | ❌ | ✅ |

---

## 🎉 **Next Steps After Running**

1. **Explore the APIs** - Each service has interactive docs
2. **Add your own data** - Modify the sample data files
3. **Create custom agents** - Follow the agent template
4. **Integrate with external systems** - Use the REST endpoints
5. **Scale to production** - Deploy with Kubernetes

---

## 💡 **Pro Tips**

- **Start with the demo** to understand the logic
- **Use Docker** for the full experience  
- **Check logs** if something doesn't work: `docker compose logs -f`
- **Modify sample data** in `sample_data/` to test different scenarios
- **Add API keys** in `.env` for external data sources

**Your system is ready to go! Choose the option that fits your setup.** 🚀 