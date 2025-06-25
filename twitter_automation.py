# safe_auto_twitter.py - Safe automated posting with content filtering
import asyncio
import re
from workflows.content_pipeline import GeminiContentPipeline
from tools.automation import RobustTwitterPoster

class SafeTwitterAutomation:
    """Safe Twitter automation with content filtering and validation"""
    
    def __init__(self):
        self.pipeline = GeminiContentPipeline()
        self.poster = RobustTwitterPoster(headless=False)
        
        # Content safety filters
        self.banned_keywords = [
            "crash", "died", "dead", "killed", "tragedy", "disaster", 
            "accident", "explosion", "terrorist", "attack", "bomb",
            "murder", "suicide", "death", "funeral", "shooting"
        ]
        
        # Preferred safe topics
        self.safe_topics = [
            "productivity tips",
            "technology trends", 
            "AI innovations",
            "remote work advice",
            "social media marketing",
            "digital tools review",
            "business insights",
            "learning resources",
            "career development",
            "startup advice"
        ]
    
    def validate_content(self, content: str) -> tuple[bool, str]:
        """Validate content for safety and quality"""
        
        # Check for banned keywords
        content_lower = content.lower()
        for keyword in self.banned_keywords:
            if keyword in content_lower:
                return False, f"Contains sensitive keyword: {keyword}"
        
        # Check for potential fake news patterns
        fake_news_patterns = [
            r'\d+\s+(dead|died|killed)',  # "279 dead"
            r'(breaking|urgent).*crash',
            r'astrologer.*predict',
            r'investigation.*death'
        ]
        
        for pattern in fake_news_patterns:
            if re.search(pattern, content_lower):
                return False, f"Matches fake news pattern: {pattern}"
        
        # Check length
        if len(content) > 280:
            return False, f"Too long: {len(content)} characters"
        
        if len(content) < 10:
            return False, "Too short"
        
        # Check for proper hashtags
        hashtags = re.findall(r'#\w+', content)
        if len(hashtags) > 5:
            return False, "Too many hashtags"
        
        return True, "Content is safe"
    
    async def generate_safe_content(self, topic: str, max_attempts: int = 3) -> dict:
        """Generate safe content with multiple attempts"""
        
        for attempt in range(max_attempts):
            print(f"🔄 Attempt {attempt + 1}: Generating content for '{topic}'")
            
            # Add safety instructions to the topic
            safe_topic = f"Write positive, educational content about {topic}. Focus on helpful tips, insights, or trends. Avoid any negative, tragic, or controversial content."
            
            result = await self.pipeline.create_content(safe_topic, ["twitter"])
            
            if result.get("status") == "error":
                print(f"❌ Generation failed: {result.get('errors')}")
                continue
            
            content = result.get("final_twitter", "")
            
            if not content:
                print("❌ No content generated")
                continue
            
            # Validate content
            is_safe, reason = self.validate_content(content)
            
            if is_safe:
                print(f"✅ Safe content generated: {content}")
                return result
            else:
                print(f"⚠️ Content rejected: {reason}")
                print(f"📝 Rejected content: {content}")
                continue
        
        print("❌ Failed to generate safe content after all attempts")
        return None
    
    async def auto_post_safe_content(self):
        """Main function for safe automated posting"""
        
        print("🛡️ Safe Twitter Auto-Poster Starting...")
        
        # Get topic from user or use safe default
        topic = input("📝 Enter topic (or press Enter for random safe topic): ").strip()
        
        if not topic:
            import random
            topic = random.choice(self.safe_topics)
            print(f"Using safe topic: {topic}")
        
        # Generate safe content
        result = await self.generate_safe_content(topic)
        
        if not result:
            print("❌ Could not generate safe content. Please try a different topic.")
            return
        
        content = result["final_twitter"]
        
        # Show content for approval
        print(f"\n✅ Generated safe content:")
        print(f"📝 Tweet: {content}")
        print(f"📏 Length: {len(content)} characters")
        print(f"🏷️ Hashtags: {result.get('hashtags', [])}")
        
        # Get user approval
        choice = input(f"\n🤔 Post this to Twitter? (y/n): ").strip().lower()
        
        if choice != 'y':
            print("👍 Content saved to files. You can copy-paste manually!")
            return
        
        # Attempt automated posting
        print("\n🤖 Attempting automated posting...")
        success = self.poster.post_to_twitter(content)
        
        if success:
            print("🎉 SUCCESS! Posted to Twitter automatically!")
        else:
            print("🎯 Automated posting failed. Switching to guided mode...")
            self.poster.guided_posting_mode(content)
        
        self.poster.close()

# Batch safe content generator
async def generate_safe_content_batch():
    """Generate multiple safe posts for content planning"""
    
    automation = SafeTwitterAutomation()
    safe_topics = automation.safe_topics
    
    print("📅 Generating content batch for content planning...")
    
    generated_content = []
    
    for i, topic in enumerate(safe_topics[:5], 1):
        print(f"\n📝 {i}/5: Generating content for '{topic}'")
        result = await automation.generate_safe_content(topic)
        
        if result:
            generated_content.append({
                "topic": topic,
                "content": result["final_twitter"],
                "hashtags": result.get("hashtags", [])
            })
    
    # Save batch to file
    import json
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_content/content_batch_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(generated_content, f, indent=2)
    
    print(f"\n📄 Batch content saved to: {filename}")
    print("💡 Review and schedule these posts throughout the week!")

if __name__ == "__main__":
    print("🛡️ Safe Twitter Automation Options:")
    print("1. Generate and post single safe content")
    print("2. Generate batch content for planning")
    print("3. Test Twitter automation only")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "1":
        automation = SafeTwitterAutomation()
        asyncio.run(automation.auto_post_safe_content())
    elif choice == "2":
        asyncio.run(generate_safe_content_batch())
    elif choice == "3":
        poster = RobustTwitterPoster()
        test_content = "Testing my AI automation! 🤖 #AI #Test #Automation"
        poster.post_to_twitter(test_content)
        poster.close()
    else:
        print("Running safe auto-posting...")
        automation = SafeTwitterAutomation()
        asyncio.run(automation.auto_post_safe_content())