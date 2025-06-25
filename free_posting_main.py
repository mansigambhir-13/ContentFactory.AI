# free_posting_main.py
"""
Complete FREE social media posting solution
No API keys required for posting!
"""
import asyncio
import os
from workflows.content_pipeline import ContentPipeline
from tools.alternative_posting import AlternativePostingManager
from tools.free_automation import FreeAutomationTools
from tools.browser_automation import BrowserPoster

class FreeSocialMediaEngine:
    """Complete free social media content and posting engine"""
    
    def __init__(self):
        self.pipeline = ContentPipeline()
        self.posting_manager = AlternativePostingManager()
        self.automation_tools = FreeAutomationTools()
        self.browser_poster = BrowserPoster()
    
    async def create_and_handle_content(self, topic: str, platforms: list = ["twitter"], posting_method: str = "manual"):
        """Create content and handle posting via free methods"""
        
        print(f"🚀 Creating content for: {topic}")
        print(f"📱 Platforms: {', '.join(platforms)}")
        print(f"📤 Posting method: {posting_method}")
        
        # Generate content
        result = await self.pipeline.create_content(topic, platforms)
        
        if result.get("status") == "error":
            print("❌ Content generation failed!")
            return result
        
        # Prepare content
        content = {}
        if result.get("final_twitter"):
            content["twitter"] = result["final_twitter"]
        if result.get("final_linkedin"):
            content["final_linkedin"] = result["final_linkedin"]
        content["hashtags"] = result.get("hashtags", [])
        
        # Handle posting based on method
        await self._handle_posting(content, topic, posting_method)
        
        return result
    
    async def _handle_posting(self, content: dict, topic: str, method: str):
        """Handle different posting methods"""
        
        if method == "manual":
            # Create files for manual posting
            json_file = self.posting_manager.save_content_to_file(content, topic)
            html_file = self.posting_manager.create_content_card(content, topic)
            print(f"\n✅ Content ready for manual posting!")
            print(f"📄 JSON file: {json_file}")
            print(f"🎨 Visual card: {html_file}")
            print(f"💡 Open {html_file} in your browser for easy copy-paste!")
            
        elif method == "guided":
            # Guided posting with prompts
            self.browser_poster.guided_posting(content)
            
        elif method == "browser":
            # Automated browser posting
            print("\n🤖 Starting browser automation...")
            print("⚠️  You'll need to log in manually the first time")
            
            if content.get("twitter"):
                success = self.browser_poster.post_to_twitter(content["twitter"])
                if success:
                    print("✅ Twitter posting completed!")
                else:
                    print("❌ Twitter posting failed, falling back to manual")
                    self.browser_poster.guided_posting({"twitter": content["twitter"]})
            
            if content.get("linkedin"):
                success = self.browser_poster.post_to_linkedin(content["linkedin"])
                if success:
                    print("✅ LinkedIn posting completed!")
                else:
                    print("❌ LinkedIn posting failed, falling back to manual")
                    self.browser_poster.guided_posting({"linkedin": content["linkedin"]})
            
            self.browser_poster.close()
            
        elif method == "webhook":
            # Send to webhooks (Discord, Zapier, etc.)
            discord_sent = self.automation_tools.send_to_discord(content, topic)
            zapier_sent = self.automation_tools.send_to_zapier(content, topic)
            
            if not discord_sent and not zapier_sent:
                print("💡 Set DISCORD_WEBHOOK_URL or ZAPIER_WEBHOOK_URL in .env for webhook posting")
                # Fallback to manual
                await self._handle_posting(content, topic, "manual")
        
        # Always create email summary
        email_file = self.automation_tools.send_email_summary(content, topic)
        print(f"📧 Email summary: {email_file}")

async def main():
    """Interactive main function"""
    engine = FreeSocialMediaEngine()
    
    print("🎯 AI Social Media Content Engine (FREE VERSION)")
    print("=" * 50)
    
    # Get user input
    topic = input("📝 Enter your topic: ").strip()
    if not topic:
        topic = "The future of AI in 2025"
        print(f"Using default topic: {topic}")
    
    # Platform selection
    print("\n📱 Select platforms:")
    print("1. Twitter only")
    print("2. LinkedIn only") 
    print("3. Both Twitter and LinkedIn")
    
    platform_choice = input("Choose (1-3): ").strip()
    if platform_choice == "2":
        platforms = ["linkedin"]
    elif platform_choice == "3":
        platforms = ["twitter", "linkedin"]
    else:
        platforms = ["twitter"]
    
    # Posting method selection
    print("\n📤 Select posting method:")
    print("1. Manual (files + copy-paste) - RECOMMENDED")
    print("2. Guided (step-by-step prompts)")
    print("3. Browser automation (requires setup)")
    print("4. Webhooks (Discord/Zapier)")
    
    method_choice = input("Choose (1-4): ").strip()
    methods = {
        "1": "manual",
        "2": "guided", 
        "3": "browser",
        "4": "webhook"
    }
    posting_method = methods.get(method_choice, "manual")
    
    # Create and post content
    print(f"\n🚀 Starting content creation...")
    await engine.create_and_handle_content(topic, platforms, posting_method)
    
    print(f"\n🎉 Process completed!")
    print(f"💡 Check the 'generated_content' folder for all output files")

if __name__ == "__main__":
    asyncio.run(main())