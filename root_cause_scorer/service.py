import asyncio
from datetime import datetime
from typing import Dict, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

# Import from shared libraries
import sys
sys.path.append('../')
from libs.common import create_agent_app, get_logger
from agent import RootCauseScorer

# Request/Response models
class RootCauseRequest(BaseModel):
    congestion_data: Dict
    context_data: Optional[Dict] = None

class RootCauseResponse(BaseModel):
    root_cause: str
    probabilities: Dict[str, float]
    features: Dict[str, float]

# Global scorer instance
scorer = None
logger = get_logger("root_cause_service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global scorer
    logger.info("Starting Root Cause Scorer Service...")
    scorer = RootCauseScorer()
    # Start Kafka consumer in background
    def run_consumer():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(scorer.process_congestion_alerts())
    import threading
    consumer_thread = threading.Thread(target=run_consumer, daemon=True)
    consumer_thread.start()
    logger.info("Root Cause Scorer Service started successfully")
    yield
    logger.info("Shutting down Root Cause Scorer Service...")

# Create FastAPI app
app = create_agent_app("Root Cause Scorer")
app.router.lifespan_context = lifespan

@app.post("/score", response_model=RootCauseResponse)
async def score_root_cause(request: RootCauseRequest):
    global scorer
    if not scorer:
        raise HTTPException(status_code=503, detail="Scorer not initialized")
    try:
        result = scorer.score_from_api(request.congestion_data, request.context_data)
        return RootCauseResponse(**result)
    except Exception as e:
        logger.error(f"Error scoring root cause: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "root_cause_scorer", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 