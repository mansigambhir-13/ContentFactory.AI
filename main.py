# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from datetime import datetime

from workflows.content_pipeline import ContentPipeline
from workflows.state import PostRequest, PostResponse

app = FastAPI(
    title="AI Social Media Content Engine",
    description="Create engaging social media content using AI agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the content pipeline
pipeline = ContentPipeline()

@app.get("/")
async def root():
    return {
        "message": "AI Social Media Content Engine",
        "status": "running",
        "endpoints": {
            "create_content": "/create-content",
            "health": "/health"
        }
    }

@app.post("/create-content", response_model=PostResponse)
async def create_content(request: PostRequest):
    """Create social media content for given topic"""
    
    try:
        print(f"📝 Received request: {request.topic} for {request.platforms}")
        
        # Run the content creation pipeline
        result = await pipeline.create_content(
            topic=request.topic,
            platforms=request.platforms,
            content_type=request.content_type
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Content creation failed",
                    "errors": result.get("errors", [])
                }
            )
        
        # Format response
        content = {}
        if result.get("final_twitter"):
            content["twitter"] = result["final_twitter"]
        if result.get("final_linkedin"):
            content["linkedin"] = result["final_linkedin"]
        
        return PostResponse(
            success=True,
            message="Content created successfully!",
            content=content
        )
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Test endpoint
@app.post("/test")
async def test_pipeline(topic: str = "artificial intelligence"):
    """Test the pipeline with a simple topic"""
    try:
        result = await pipeline.create_content(
            topic=topic,
            platforms=["twitter"],
            content_type="educational"
        )
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)