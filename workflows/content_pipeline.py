# workflows/content_pipeline_gemini.py
from langgraph.graph import StateGraph, END
from typing import Dict, Any, List
from datetime import datetime

# FIXED: Import from the correct Gemini files
from agents.researcher import gemini_research_node
from agents.writer import gemini_write_twitter_node, gemini_write_linkedin_node
from workflows.state import ContentState

class GeminiContentPipeline:
    def __init__(self):
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the main content creation workflow using Gemini"""
        
        # Initialize the state graph
        workflow = StateGraph(ContentState)
        
        # Add nodes
        workflow.add_node("research", gemini_research_node)
        workflow.add_node("write_twitter", gemini_write_twitter_node)
        workflow.add_node("write_linkedin", gemini_write_linkedin_node)
        workflow.add_node("finalize", self._finalize_content)
        
        # Define the flow
        workflow.set_entry_point("research")
        
        # After research, decide which platforms to write for
        workflow.add_conditional_edges(
            "research",
            self._decide_platforms,
            {
                "twitter_only": "write_twitter",
                "linkedin_only": "write_linkedin", 
                "both_twitter_first": "write_twitter",
                "error": END
            }
        )
        
        # From Twitter, either go to LinkedIn or finalize
        workflow.add_conditional_edges(
            "write_twitter",
            self._after_twitter,
            {
                "linkedin_next": "write_linkedin",
                "finalize": "finalize",
                "error": END
            }
        )
        
        # From LinkedIn, finalize
        workflow.add_edge("write_linkedin", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    def _decide_platforms(self, state: Dict[str, Any]) -> str:
        """Decide which platforms to create content for"""
        if state.get("status") == "error":
            return "error"
            
        platforms = state.get("target_platforms", ["twitter"])
        
        if "twitter" in platforms and "linkedin" in platforms:
            return "both_twitter_first"
        elif "twitter" in platforms:
            return "twitter_only"
        elif "linkedin" in platforms:
            return "linkedin_only"
        else:
            return "twitter_only"  # Default
    
    def _after_twitter(self, state: Dict[str, Any]) -> str:
        """Decide what to do after Twitter content is created"""
        if state.get("status") == "error":
            return "error"
            
        platforms = state.get("target_platforms", ["twitter"])
        
        if "linkedin" in platforms and not state.get("linkedin_content"):
            return "linkedin_next"
        else:
            return "finalize"
    
    def _finalize_content(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize the content creation process"""
        print("✅ Finalizing content...")
        
        # FIXED: Import from correct file paths
        from tools.posting import AlternativePostingManager
        from tools.automation import FreeAutomationTools
        
        # Prepare content for output
        content = {}
        if state.get("twitter_content"):
            content["twitter"] = state["twitter_content"]
        if state.get("linkedin_content"):
            content["linkedin"] = state["linkedin_content"]
        
        content["hashtags"] = state.get("hashtags", [])
        
        # Save content using free alternatives
        posting_manager = AlternativePostingManager()
        automation_tools = FreeAutomationTools()
        
        # Save to files
        json_file = posting_manager.save_content_to_file(content, state["topic"])
        html_file = posting_manager.create_content_card(content, state["topic"])
        
        # Try to send to Discord/Zapier if configured
        automation_tools.send_to_discord(content, state["topic"])
        automation_tools.send_to_zapier(content, state["topic"])
        
        print(f"📄 Content saved to: {json_file}")
        print(f"🎨 Visual card created: {html_file}")
        print("💡 Open the HTML file in your browser for easy copy-paste!")
        
        return {
            **state,
            "final_twitter": state.get("twitter_content"),
            "final_linkedin": state.get("linkedin_content"),
            "content_files": {
                "json": json_file,
                "html": html_file
            },
            "status": "completed",
            "completed_at": datetime.now().isoformat()
        }
    
    async def create_content(self, topic: str, platforms: List[str] = ["twitter"], content_type: str = "educational") -> Dict[str, Any]:
        """Main method to create content using Gemini"""
        
        initial_state = {
            "topic": topic,
            "target_platforms": platforms,
            "content_type": content_type,
            "created_at": datetime.now(),
            "status": "starting",
            "errors": []
        }
        
        print(f"🚀 Starting content creation with Gemini for: {topic}")
        print(f"📱 Target platforms: {', '.join(platforms)}")
        
        try:
            # Run the workflow
            result = self.workflow.invoke(initial_state)
            return result
        except Exception as e:
            print(f"❌ Workflow error: {str(e)}")
            return {
                **initial_state,
                "status": "error",
                "errors": [f"Workflow error: {str(e)}"]
            }

# Helper function for direct usage
async def create_gemini_content_pipeline(topic: str, platforms: List[str] = ["twitter"], content_type: str = "educational") -> Dict[str, Any]:
    """Helper function to create content using Gemini"""
    pipeline = GeminiContentPipeline()
    return await pipeline.create_content(topic, platforms, content_type)