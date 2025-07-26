import asyncio
import threading
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

# Import from shared libraries
import sys
sys.path.append('../')
from libs.common import create_agent_app, get_logger
from agent import CongestionDetector

# Request/Response models
class SegmentStatusRequest(BaseModel):
    segment_id: str

class CongestionPredictionRequest(BaseModel):
    segment_id: str
    latitude: float
    longitude: float
    speed_kmph: float
    vehicle_count: int
    timestamp: Optional[float] = None

class CongestionResponse(BaseModel):
    segment_id: str
    congestion_level: float
    congestion_level_name: str
    confidence: float
    factors: List[str]
    timestamp: float

# Global detector instance
detector = None
logger = get_logger("congestion_service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the FastAPI app"""
    global detector
    logger.info("Starting Congestion Detector Service...")
    
    # Initialize detector
    detector = CongestionDetector()
    
    # Start Kafka message processing in background
    def run_kafka_consumer():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(detector.process_kafka_messages())
    
    kafka_thread = threading.Thread(target=run_kafka_consumer, daemon=True)
    kafka_thread.start()
    
    logger.info("Congestion Detector Service started successfully")
    yield
    
    logger.info("Shutting down Congestion Detector Service...")

# Create FastAPI app
app = create_agent_app("Congestion Detector")
app.router.lifespan_context = lifespan

@app.post("/analyze", response_model=Optional[CongestionResponse])
async def analyze_congestion(request: CongestionPredictionRequest):
    """Analyze traffic data and detect congestion"""
    global detector
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    try:
        # Prepare GPS data
        gps_data = {
            "segment_id": request.segment_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "speed_kmph": request.speed_kmph,
            "vehicle_count": request.vehicle_count,
            "timestamp": request.timestamp or datetime.now().timestamp()
        }
        
        # Analyze congestion
        alert = await detector.analyze_gps_data(gps_data)
        
        if alert:
            return CongestionResponse(
                segment_id=alert.segment_id,
                congestion_level=alert.congestion_level,
                congestion_level_name=_get_level_name(alert.congestion_level),
                confidence=alert.confidence,
                factors=alert.factors or [],
                timestamp=alert.timestamp
            )
        
        return None
        
    except Exception as e:
        logger.error(f"Error in congestion analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/segment/{segment_id}")
async def get_segment_status(segment_id: str):
    """Get current status of a specific segment"""
    global detector
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    try:
        status = await detector.get_segment_status(segment_id)
        return status
    except Exception as e:
        logger.error(f"Error getting segment status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/overview")
async def get_system_overview():
    """Get system-wide congestion overview"""
    global detector
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    try:
        overview = await detector.get_system_overview()
        return overview
    except Exception as e:
        logger.error(f"Error getting system overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/segments")
async def list_all_segments():
    """List all monitored segments"""
    global detector
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    try:
        redis_client = detector.redis.get_client()
        segment_keys = redis_client.keys("segment:*")
        
        segments = []
        for key in segment_keys:
            segment_id = key.split(":")[-1]
            status = await detector.get_segment_status(segment_id)
            segments.append(status)
        
        return {
            "total_segments": len(segments),
            "segments": segments,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error listing segments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stream/alerts")
async def stream_congestion_alerts():
    """Stream real-time congestion alerts (SSE)"""
    async def event_stream():
        global detector
        if not detector:
            yield "data: {\"error\": \"Detector not initialized\"}\n\n"
            return
        
        redis_client = detector.redis.get_client()
        
        while True:
            try:
                # Get all current congestion alerts
                alert_keys = redis_client.keys("congestion:*")
                alerts = []
                
                for key in alert_keys:
                    alert_data = detector.redis.get_json(key)
                    if alert_data:
                        alerts.append(alert_data)
                
                # Send alerts as SSE
                event_data = {
                    "timestamp": datetime.now().isoformat(),
                    "alerts": alerts,
                    "count": len(alerts)
                }
                
                yield f"data: {json.dumps(event_data)}\n\n"
                
                # Wait before next update
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Error in alert stream: {e}")
                yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
                await asyncio.sleep(10)
    
    return StreamingResponse(
        event_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache"}
    )

@app.post("/train")
async def retrain_model(background_tasks: BackgroundTasks):
    """Retrain the congestion detection model"""
    global detector
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    def train_in_background():
        try:
            logger.info("Starting model retraining...")
            detector.model_trainer.train_models()
            detector.model_trainer.save_models()
            logger.info("Model retraining completed")
        except Exception as e:
            logger.error(f"Error during model retraining: {e}")
    
    background_tasks.add_task(train_in_background)
    
    return {
        "message": "Model retraining started in background",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model/info")
async def get_model_info():
    """Get information about the current model"""
    global detector
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    try:
        # Try to load metadata
        from pathlib import Path
        import json
        
        metadata_path = Path("./models/metadata.json")
        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            return metadata
        else:
            return {"message": "Model metadata not available"}
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def _get_level_name(level: float) -> str:
    """Convert congestion level to human-readable name"""
    if level < 0.25:
        return "Free Flow"
    elif level < 0.5:
        return "Moderate"
    elif level < 0.75:
        return "Heavy"
    else:
        return "Severe"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 