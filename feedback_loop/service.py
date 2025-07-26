import asyncio
import time
from datetime import datetime
from typing import Dict, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
sys.path.append('../')
from libs.common import create_agent_app, get_logger, redis_manager

# Request models
class FeedbackRequest(BaseModel):
    action_id: str
    effectiveness_score: float  # 0-1
    implementation_time: float  # seconds
    actual_impact: str
    notes: str = ""

class ActionTrackingRequest(BaseModel):
    action_id: str
    segment_id: str
    status: str  # implemented, failed, pending

# Global instances
redis = None
logger = get_logger("feedback_service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis
    logger.info("Starting Feedback Loop Service...")
    redis = redis_manager
    logger.info("Feedback Loop Service started successfully")
    yield
    logger.info("Shutting down Feedback Loop Service...")

# Create FastAPI app
app = create_agent_app("Feedback Loop")
app.router.lifespan_context = lifespan

@app.post("/track-action")
async def track_action_implementation(request: ActionTrackingRequest):
    """Track when an action is implemented"""
    global redis
    if not redis:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        tracking_data = {
            "action_id": request.action_id,
            "segment_id": request.segment_id,
            "status": request.status,
            "timestamp": time.time()
        }
        
        redis.set_with_expiry(f"action_tracking:{request.action_id}", tracking_data, 86400)  # 24 hours
        
        return {
            "message": "Action tracking recorded",
            "action_id": request.action_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error tracking action: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def record_feedback(request: FeedbackRequest):
    """Record feedback on action effectiveness"""
    global redis
    if not redis:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        feedback_data = {
            "action_id": request.action_id,
            "effectiveness_score": request.effectiveness_score,
            "implementation_time": request.implementation_time,
            "actual_impact": request.actual_impact,
            "notes": request.notes,
            "timestamp": time.time()
        }
        
        redis.set_with_expiry(f"feedback:{request.action_id}", feedback_data, 86400 * 7)  # 7 days
        
        return {
            "message": "Feedback recorded successfully",
            "action_id": request.action_id,
            "effectiveness_score": request.effectiveness_score,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error recording feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_feedback_analytics():
    """Get analytics on action effectiveness"""
    global redis
    if not redis:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        redis_client = redis.get_client()
        feedback_keys = redis_client.keys("feedback:*")
        
        total_actions = len(feedback_keys)
        effectiveness_scores = []
        
        for key in feedback_keys:
            feedback_data = redis.get_json(key)
            if feedback_data:
                effectiveness_scores.append(feedback_data.get("effectiveness_score", 0))
        
        avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0
        
        return {
            "total_actions_tracked": total_actions,
            "average_effectiveness": avg_effectiveness,
            "effectiveness_distribution": {
                "high": len([s for s in effectiveness_scores if s > 0.7]),
                "medium": len([s for s in effectiveness_scores if 0.3 <= s <= 0.7]),
                "low": len([s for s in effectiveness_scores if s < 0.3])
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 