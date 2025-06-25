# agents/researcher_gemini.py
import google.generativeai as genai
from langchain_community.tools import DuckDuckGoSearchRun
from typing import Dict, Any, List

import json
from datetime import datetime
from config.settings import settings

class GeminiResearchAgent:
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.search_tool = DuckDuckGoSearchRun()
    
    def research_topic(self, topic: str) -> Dict[str, Any]:
        """Research a topic using Gemini and return structured insights"""
        
        # Search for current information
        search_results = self.search_tool.run(f"{topic} 2024 2025 latest trends")
        
        # Use Gemini to analyze and structure the research
        research_prompt = f"""
        You are a research specialist. Analyze the following search results about "{topic}" and provide:
        
        1. Key insights (3-5 bullet points)
        2. Current trends or developments
        3. Interesting angles for social media content
        4. Potential controversies or debates
        5. Actionable advice or tips
        
        Search Results:
        {search_results}
        
        Return your analysis in JSON format with keys: insights, trends, content_angles, debates, tips
        Make sure the JSON is valid and properly formatted.
        """
        
        try:
            response = self.model.generate_content(research_prompt)
            
            # Try to parse as JSON, fallback to structured text
            try:
                # Extract JSON from response if it's wrapped in markdown
                content = response.text
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                
                research_data = json.loads(content.strip())
            except (json.JSONDecodeError, AttributeError):
                # Fallback structure
                research_data = {
                    "insights": [response.text],
                    "trends": [],
                    "content_angles": [],
                    "debates": [],
                    "tips": []
                }
        
        except Exception as e:
            print(f"⚠️ Gemini API error: {str(e)}")
            research_data = {
                "insights": [f"Research topic: {topic}"],
                "trends": ["AI and technology advancement"],
                "content_angles": ["Educational content"],
                "debates": [],
                "tips": ["Stay updated with latest trends"]
            }
        
        return {
            "research_data": research_data,
            "raw_search": search_results,
            "researched_at": datetime.now().isoformat()
        }
    
    def extract_key_insights(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract the most important insights for content creation"""
        insights = research_data.get("research_data", {}).get("insights", [])
        tips = research_data.get("research_data", {}).get("tips", [])
        
        # Combine and prioritize
        all_insights = insights + tips
        return all_insights[:5]  # Return top 5

# LangGraph node function for Gemini
def gemini_research_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node for research phase using Gemini"""
    researcher = GeminiResearchAgent()
    
    topic = state["topic"]
    print(f"🔍 Researching topic with Gemini: {topic}")
    
    try:
        research_results = researcher.research_topic(topic)
        key_insights = researcher.extract_key_insights(research_results)
        
        return {
            **state,
            "research_data": research_results,
            "key_insights": key_insights,
            "status": "researched"
        }
    except Exception as e:
        return {
            **state,
            "errors": state.get("errors", []) + [f"Research error: {str(e)}"],
            "status": "error"
        }