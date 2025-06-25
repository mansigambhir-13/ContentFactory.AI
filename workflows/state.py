# workflows/state.py
from typing import TypedDict, List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class ContentState(TypedDict):
    """State that flows through our LangGraph workflow"""
    
    # Input
    topic: str
    target_platforms: List[str]  # ["twitter", "linkedin"]
    content_type: Optional[str]  # "educational", "entertaining", "promotional"
    
    # Research phase
    research_data: Optional[Dict[str, Any]]
    key_insights: Optional[List[str]]
    trending_info: Optional[Dict[str, Any]]
    
    # Content creation
    twitter_content: Optional[str]
    linkedin_content: Optional[str]
    hashtags: Optional[List[str]]
    
    # Review & editing
    content_feedback: Optional[str]
    final_twitter: Optional[str]
    final_linkedin: Optional[str]
    
    # Scheduling
    suggested_post_times: Optional[Dict[str, datetime]]
    scheduled: Optional[bool]
    
    # Metadata
    created_at: datetime
    status: str  # "researching", "writing", "reviewing", "scheduled", "posted"
    errors: Optional[List[str]]

class PostRequest(BaseModel):
    """API request model"""
    topic: str
    platforms: List[str] = ["twitter"]
    content_type: str = "educational"
    schedule_immediately: bool = False
    
class PostResponse(BaseModel):
    """API response model"""
    success: bool
    message: str
    content: Optional[Dict[str, str]] = None
    post_urls: Optional[Dict[str, str]] = None