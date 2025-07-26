import asyncio
import threading
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import json

# Import from shared libraries
import sys
sys.path.append('../')
from libs.common import create_agent_app, get_logger
from agent import ContextAggregator

# Request/Response models
class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    radius_km: float = 5.0

class ContextResponse(BaseModel):
    location: Dict
    timestamp: str
    news_articles: List[Dict]
    events: List[Dict]
    weather_conditions: Dict
    social_mentions: List[Dict]
    traffic_alerts: List[Dict]
    ai_analysis: str

# Global aggregator instance
aggregator = None
logger = get_logger("context_service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the FastAPI app"""
    global aggregator
    logger.info("Starting Context Aggregator Service...")
    
    # Initialize aggregator
    aggregator = ContextAggregator()
    
    # Start background tasks
    def run_alert_processor():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(aggregator.process_congestion_alerts())
    
    def run_context_refresher():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(aggregator.refresh_context_periodically())
    
    alert_thread = threading.Thread(target=run_alert_processor, daemon=True)
    refresh_thread = threading.Thread(target=run_context_refresher, daemon=True)
    
    alert_thread.start()
    refresh_thread.start()
    
    logger.info("Context Aggregator Service started successfully")
    yield
    
    logger.info("Shutting down Context Aggregator Service...")

# Create FastAPI app
app = create_agent_app("Context Aggregator")
app.router.lifespan_context = lifespan

@app.post("/analyze", response_model=ContextResponse)
async def analyze_location_context(request: LocationRequest):
    """Analyze and gather context for a specific location"""
    global aggregator
    if not aggregator:
        raise HTTPException(status_code=503, detail="Aggregator not initialized")
    
    try:
        context = await aggregator.gather_context_for_location(
            request.latitude, 
            request.longitude, 
            request.radius_km
        )
        
        return ContextResponse(**context)
        
    except Exception as e:
        logger.error(f"Error analyzing location context: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/context/{latitude}/{longitude}")
async def get_cached_context(latitude: float, longitude: float):
    """Get cached context for a location"""
    global aggregator
    if not aggregator:
        raise HTTPException(status_code=503, detail="Aggregator not initialized")
    
    try:
        context = await aggregator.get_cached_context(latitude, longitude)
        
        if context:
            return context
        else:
            raise HTTPException(status_code=404, detail="No cached context found")
            
    except Exception as e:
        logger.error(f"Error getting cached context: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news")
async def get_traffic_news(limit: int = Query(10, ge=1, le=50)):
    """Get recent traffic-related news"""
    global aggregator
    if not aggregator:
        raise HTTPException(status_code=503, detail="Aggregator not initialized")
    
    try:
        # Get news for a general location (SF Bay Area)
        news_articles = await aggregator._fetch_news_context(37.7749, -122.4194, 50.0)
        
        return {
            "articles": news_articles[:limit],
            "timestamp": datetime.now().isoformat(),
            "total_found": len(news_articles)
        }
        
    except Exception as e:
        logger.error(f"Error getting traffic news: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/{latitude}/{longitude}")
async def get_weather_context(latitude: float, longitude: float):
    """Get weather context for a location"""
    global aggregator
    if not aggregator:
        raise HTTPException(status_code=503, detail="Aggregator not initialized")
    
    try:
        weather = await aggregator._fetch_weather_context(latitude, longitude)
        return weather
        
    except Exception as e:
        logger.error(f"Error getting weather context: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events/{latitude}/{longitude}")
async def get_events_context(latitude: float, longitude: float, radius_km: float = 5.0):
    """Get events context for a location"""
    global aggregator
    if not aggregator:
        raise HTTPException(status_code=503, detail="Aggregator not initialized")
    
    try:
        events = await aggregator._fetch_events_context(latitude, longitude, radius_km)
        return {
            "events": events,
            "location": {"latitude": latitude, "longitude": longitude},
            "radius_km": radius_km,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting events context: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refresh")
async def force_context_refresh(request: LocationRequest):
    """Force refresh context for a location"""
    global aggregator
    if not aggregator:
        raise HTTPException(status_code=503, detail="Aggregator not initialized")
    
    try:
        context = await aggregator.gather_context_for_location(
            request.latitude, 
            request.longitude, 
            request.radius_km
        )
        
        return {
            "message": "Context refreshed successfully",
            "location": {"latitude": request.latitude, "longitude": request.longitude},
            "timestamp": datetime.now().isoformat(),
            "context_summary": {
                "news_articles_found": len(context.get("news_articles", [])),
                "events_found": len(context.get("events", [])),
                "traffic_alerts_found": len(context.get("traffic_alerts", [])),
                "has_weather_data": bool(context.get("weather_conditions")),
                "ai_analysis_length": len(context.get("ai_analysis", ""))
            }
        }
        
    except Exception as e:
        logger.error(f"Error refreshing context: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 