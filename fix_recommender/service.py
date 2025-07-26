import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

# Import from shared libraries
import sys
sys.path.append('../')
from libs.common import create_agent_app, get_logger
from agent import FixRecommender

# Request/Response models
class RecommendationRequest(BaseModel):
    segment_id: str
    congestion_level: float
    avg_speed: float
    expected_speed: float
    factors: List[str] = []
    context_data: Optional[Dict] = None

class RecommendationResponse(BaseModel):
    action_id: str
    action_type: str
    description: str
    affected_segments: List[str]
    priority: str
    estimated_impact: str
    implementation_time: str
    timestamp: float

# Global recommender instance
recommender = None
logger = get_logger("fix_recommender_service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the FastAPI app"""
    global recommender
    logger.info("Starting Fix Recommender Service...")
    
    # Initialize recommender
    recommender = FixRecommender()
    
    logger.info("Fix Recommender Service started successfully")
    yield
    
    logger.info("Shutting down Fix Recommender Service...")

# Create FastAPI app
app = create_agent_app("Fix Recommender")
app.router.lifespan_context = lifespan

@app.post("/recommend", response_model=List[RecommendationResponse])
async def generate_recommendations(request: RecommendationRequest):
    """Generate actionable recommendations for congestion"""
    global recommender
    if not recommender:
        raise HTTPException(status_code=503, detail="Recommender not initialized")
    
    try:
        # Prepare congestion data
        congestion_data = {
            "segment_id": request.segment_id,
            "congestion_level": request.congestion_level,
            "avg_speed": request.avg_speed,
            "expected_speed": request.expected_speed,
            "factors": request.factors
        }
        
        # Generate recommendations
        recommendations = await recommender.generate_recommendations(
            congestion_data, 
            request.context_data
        )
        
        # Convert to response format
        response = []
        for rec in recommendations:
            response.append(RecommendationResponse(
                action_id=rec.action_id,
                action_type=rec.action_type,
                description=rec.description,
                affected_segments=rec.affected_segments,
                priority=rec.priority,
                estimated_impact=rec.estimated_impact,
                implementation_time=rec.implementation_time,
                timestamp=rec.timestamp
            ))
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/segment/{segment_id}/recommendations")
async def get_cached_recommendations(segment_id: str):
    """Get cached recommendations for a segment"""
    global recommender
    if not recommender:
        raise HTTPException(status_code=503, detail="Recommender not initialized")
    
    try:
        recommendations = await recommender.get_cached_recommendations(segment_id)
        
        if recommendations:
            return {
                "segment_id": segment_id,
                "recommendations": recommendations,
                "cached_at": datetime.now().isoformat(),
                "count": len(recommendations)
            }
        else:
            raise HTTPException(status_code=404, detail="No recommendations found")
            
    except Exception as e:
        logger.error(f"Error getting cached recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/strategies")
async def get_available_strategies():
    """Get available fix strategies"""
    global recommender
    if not recommender:
        raise HTTPException(status_code=503, detail="Recommender not initialized")
    
    return {
        "strategies": recommender.fix_strategies,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 