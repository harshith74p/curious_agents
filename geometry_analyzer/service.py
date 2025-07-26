import asyncio
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
from agent import GeometryAnalyzer

# Request/Response models
class NetworkAnalysisRequest(BaseModel):
    latitude: float
    longitude: float
    radius_m: float = 2000

class RouteRequest(BaseModel):
    origin_latitude: float
    origin_longitude: float
    destination_latitude: float
    destination_longitude: float
    avoid_segments: Optional[List[str]] = None

# Global analyzer instance
analyzer = None
logger = get_logger("geometry_service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the FastAPI app"""
    global analyzer
    logger.info("Starting Geometry Analyzer Service...")
    
    # Initialize analyzer
    analyzer = GeometryAnalyzer()
    
    logger.info("Geometry Analyzer Service started successfully")
    yield
    
    logger.info("Shutting down Geometry Analyzer Service...")

# Create FastAPI app
app = create_agent_app("Geometry Analyzer")
app.router.lifespan_context = lifespan

@app.post("/analyze-network")
async def analyze_network_capacity(request: NetworkAnalysisRequest):
    """Analyze road network capacity for a location"""
    global analyzer
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")
    
    try:
        analysis = await analyzer.analyze_network_capacity(
            request.latitude, 
            request.longitude, 
            request.radius_m
        )
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing network capacity: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/find-routes")
async def find_optimal_routes(request: RouteRequest):
    """Find optimal routes between two points"""
    global analyzer
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")
    
    try:
        routes = await analyzer.find_optimal_routes(
            request.origin_latitude,
            request.origin_longitude,
            request.destination_latitude,
            request.destination_longitude,
            request.avoid_segments
        )
        
        return routes
        
    except Exception as e:
        logger.error(f"Error finding optimal routes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/segment/{segment_id}/geometry")
async def get_segment_geometry(segment_id: str):
    """Get geometric properties of a traffic segment"""
    global analyzer
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")
    
    try:
        geometry = await analyzer.get_segment_geometry(segment_id)
        
        if geometry:
            return geometry
        else:
            raise HTTPException(status_code=404, detail="Segment geometry not found")
            
    except Exception as e:
        logger.error(f"Error getting segment geometry: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/network/{latitude}/{longitude}/bottlenecks")
async def get_network_bottlenecks(latitude: float, longitude: float, radius_m: int = Query(2000)):
    """Get network bottlenecks for a location"""
    global analyzer
    if not analyzer:
        raise HTTPException(status_code=503, detail="Analyzer not initialized")
    
    try:
        # Get network analysis
        analysis = await analyzer.analyze_network_capacity(latitude, longitude, radius_m)
        
        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "bottlenecks": analysis.get("bottlenecks", []),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting network bottlenecks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 