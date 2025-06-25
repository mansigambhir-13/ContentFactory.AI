# agents/writer_gemini.py
import google.generativeai as genai
from typing import Dict, Any, List
import re
from config.settings import settings

class GeminiContentWriter:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def write_twitter_content(self, topic: str, insights: List[str], content_type: str = "educational") -> Dict[str, Any]:
        """Write Twitter-specific content using Gemini"""
        
        insights_text = "\n".join([f"• {insight}" for insight in insights[:3]])
        
        twitter_prompt = f"""
        Write engaging Twitter content about "{topic}".
        
        Key insights to include:
        {insights_text}
        
        Content type: {content_type}
        
        Requirements:
        - Maximum 280 characters
        - Engaging hook in first line
        - Include 2-3 relevant hashtags
        - Call to action or question at the end
        - Professional but conversational tone
        
        Return ONLY the tweet text, nothing else.
        """
        
        try:
            response = self.model.generate_content(twitter_prompt)
            tweet = response.text.strip()
            
            # Extract hashtags
            hashtags = re.findall(r'#\w+', tweet)
            
            return {
                "content": tweet,
                "hashtags": hashtags,
                "character_count": len(tweet),
                "platform": "twitter"
            }
        except Exception as e:
            print(f"⚠️ Gemini Twitter writing error: {str(e)}")
            # Fallback content
            return {
                "content": f"Exploring {topic} - fascinating insights ahead! What are your thoughts? #AI #Tech #Innovation",
                "hashtags": ["#AI", "#Tech", "#Innovation"],
                "character_count": 80,
                "platform": "twitter"
            }
    
    def write_linkedin_content(self, topic: str, insights: List[str], content_type: str = "educational") -> Dict[str, Any]:
        """Write LinkedIn-specific content using Gemini"""
        
        insights_text = "\n".join([f"• {insight}" for insight in insights])
        
        linkedin_prompt = f"""
        Write professional LinkedIn content about "{topic}".
        
        Key insights to include:
        {insights_text}
        
        Content type: {content_type}
        
        Requirements:
        - 500-1500 characters (LinkedIn sweet spot)
        - Professional tone but accessible
        - Strong opening hook
        - Bullet points or numbered lists when appropriate
        - Call to action encouraging engagement
        - 3-5 relevant hashtags at the end
        - Include a thought-provoking question
        
        Structure:
        1. Hook/Opening statement
        2. Main insights (use bullet points)
        3. Personal take or conclusion
        4. Call to action question
        5. Hashtags
        """
        
        try:
            response = self.model.generate_content(linkedin_prompt)
            post = response.text.strip()
            
            # Extract hashtags
            hashtags = re.findall(r'#\w+', post)
            
            return {
                "content": post,
                "hashtags": hashtags,
                "character_count": len(post),
                "platform": "linkedin"
            }
        except Exception as e:
            print(f"⚠️ Gemini LinkedIn writing error: {str(e)}")
            # Fallback content
            return {
                "content": f"Diving deep into {topic} today.\n\nKey takeaway: The landscape is evolving rapidly, and staying informed is crucial.\n\nWhat's your experience with this? Share your thoughts below!\n\n#Professional #Innovation #Technology",
                "hashtags": ["#Professional", "#Innovation", "#Technology"],
                "character_count": 200,
                "platform": "linkedin"
            }

# LangGraph node functions for Gemini
def gemini_write_twitter_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node for Twitter content creation using Gemini"""
    writer = GeminiContentWriter()
    
    topic = state["topic"]
    insights = state.get("key_insights", [])
    content_type = state.get("content_type", "educational")
    
    print(f"✍️ Writing Twitter content with Gemini for: {topic}")
    
    try:
        twitter_result = writer.write_twitter_content(topic, insights, content_type)
        
        return {
            **state,
            "twitter_content": twitter_result["content"],
            "hashtags": twitter_result["hashtags"],
            "status": "twitter_written"
        }
    except Exception as e:
        return {
            **state,
            "errors": state.get("errors", []) + [f"Twitter writing error: {str(e)}"],
            "status": "error"
        }

def gemini_write_linkedin_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node for LinkedIn content creation using Gemini"""
    writer = GeminiContentWriter()
    
    topic = state["topic"]
    insights = state.get("key_insights", [])
    content_type = state.get("content_type", "educational")
    
    print(f"✍️ Writing LinkedIn content with Gemini for: {topic}")
    
    try:
        linkedin_result = writer.write_linkedin_content(topic, insights, content_type)
        
        return {
            **state,
            "linkedin_content": linkedin_result["content"],
            "status": "linkedin_written"
        }
    except Exception as e:
        return {
            **state,
            "errors": state.get("errors", []) + [f"LinkedIn writing error: {str(e)}"],
            "status": "error"
        }