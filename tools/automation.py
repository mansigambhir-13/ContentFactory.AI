# tools/free_automation.py
import requests
import json
from typing import Dict, Optional
from datetime import datetime
import os

class FreeAutomationTools:
    """Free alternatives for automation and posting"""
    
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")  # Free Discord webhook
        self.zapier_webhook = os.getenv("ZAPIER_WEBHOOK_URL")  # Free Zapier webhook
    
    def send_to_discord(self, content: Dict, topic: str) -> bool:
        """Send generated content to Discord channel via webhook (FREE)"""
        if not self.webhook_url:
            print("💡 Set DISCORD_WEBHOOK_URL in .env to auto-send content to Discord")
            return False
        
        twitter_content = content.get('twitter', 'Not generated')
        linkedin_content = content.get('linkedin', 'Not generated')
        
        discord_message = {
            "embeds": [{
                "title": f"📝 New Content Generated: {topic}",
                "color": 3447003,  # Blue color
                "fields": [
                    {
                        "name": "🐦 Twitter",
                        "value": f"```{twitter_content}```",
                        "inline": False
                    },
                    {
                        "name": "💼 LinkedIn", 
                        "value": f"```{linkedin_content[:500]}{'...' if len(linkedin_content) > 500 else ''}```",
                        "inline": False
                    },
                    {
                        "name": "📋 Next Steps",
                        "value": "1. Copy content above\n2. Go to social platform\n3. Paste and post!\n4. Track engagement",
                        "inline": False
                    }
                ],
                "timestamp": datetime.now().isoformat()
            }]
        }
        
        try:
            response = requests.post(self.webhook_url, json=discord_message)
            if response.status_code == 204:
                print("✅ Content sent to Discord!")
                return True
            else:
                print(f"❌ Discord webhook failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Discord error: {str(e)}")
            return False
    
    def send_to_zapier(self, content: Dict, topic: str) -> bool:
        """Send to Zapier webhook for further automation (FREE tier available)"""
        if not self.zapier_webhook:
            print("💡 Set ZAPIER_WEBHOOK_URL in .env to trigger Zapier automations")
            return False
        
        payload = {
            "topic": topic,
            "twitter_content": content.get('twitter', ''),
            "linkedin_content": content.get('linkedin', ''),
            "generated_at": datetime.now().isoformat(),
            "hashtags": content.get('hashtags', [])
        }
        
        try:
            response = requests.post(self.zapier_webhook, json=payload)
            if response.status_code == 200:
                print("✅ Content sent to Zapier!")
                return True
            else:
                print(f"❌ Zapier webhook failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Zapier error: {str(e)}")
            return False
    
    def create_ifttt_format(self, content: Dict, topic: str) -> str:
        """Create IFTTT-compatible JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_content/ifttt_trigger_{timestamp}.json"
        
        ifttt_data = {
            "trigger_event": "content_generated",
            "topic": topic,
            "twitter_content": content.get('twitter', ''),
            "linkedin_content": content.get('linkedin', ''),
            "timestamp": datetime.now().isoformat()
        }
        
        os.makedirs("generated_content", exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(ifttt_data, f, indent=2)
        
        print(f"📄 IFTTT trigger file created: {filename}")
        return filename
    
    def send_email_summary(self, content: Dict, topic: str, email: Optional[str] = None) -> str:
        """Generate email-ready summary"""
        email_body = f"""
Subject: 📝 New Social Media Content Generated: {topic}

Hi there!

Your AI Content Engine has generated new social media content:

🐦 TWITTER CONTENT:
{content.get('twitter', 'Not generated')}

💼 LINKEDIN CONTENT:
{content.get('linkedin', 'Not generated')}

📋 NEXT STEPS:
1. Copy the content above
2. Go to your social media platforms
3. Paste and post!
4. Track engagement and performance

📊 HASHTAGS: {', '.join(content.get('hashtags', []))}

Generated on: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

Happy posting! 🚀
        """
        
        # Save email to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_content/email_summary_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(email_body)
        
        print(f"📧 Email summary saved: {filename}")
        return filename