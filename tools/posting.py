# tools/alternative_posting.py
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import qrcode
from io import BytesIO
import base64

class AlternativePostingManager:
    """Free alternatives for social media posting"""
    
    def __init__(self):
        self.output_dir = "generated_content"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save_content_to_file(self, content: Dict, topic: str) -> str:
        """Save generated content to structured files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/content_{timestamp}_{topic.replace(' ', '_')[:20]}.json"
        
        content_data = {
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "content": content,
            "posting_instructions": {
                "twitter": "Copy the Twitter content and paste directly to twitter.com",
                "linkedin": "Copy the LinkedIn content and paste to linkedin.com/feed",
                "optimal_times": "Best posting times: 9AM, 1PM, 5PM in your timezone"
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content_data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def create_content_card(self, content: Dict, topic: str) -> str:
        """Create a visual content card as HTML for easy sharing"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/content_card_{timestamp}.html"
        
        twitter_content = content.get('twitter', 'Not generated')
        linkedin_content = content.get('linkedin', 'Not generated')
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Content for: {topic}</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 20px 0; }}
                .twitter {{ border-left: 4px solid #1DA1F2; }}
                .linkedin {{ border-left: 4px solid #0077B5; }}
                .copy-btn {{ background: #007bff; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }}
                .topic {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="topic">
                <h1>📝 Generated Content</h1>
                <h2>Topic: {topic}</h2>
                <p>Generated on: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
            </div>
            
            <div class="card twitter">
                <h3>🐦 Twitter Content</h3>
                <div id="twitter-content">{twitter_content}</div>
                <br>
                <button class="copy-btn" onclick="copyToClipboard('twitter-content')">Copy Twitter Content</button>
                <p><small>Character count: {len(twitter_content)}/280</small></p>
            </div>
            
            <div class="card linkedin">
                <h3>💼 LinkedIn Content</h3>
                <div id="linkedin-content" style="white-space: pre-line;">{linkedin_content}</div>
                <br>
                <button class="copy-btn" onclick="copyToClipboard('linkedin-content')">Copy LinkedIn Content</button>
                <p><small>Character count: {len(linkedin_content)}</small></p>
            </div>
            
            <div class="card">
                <h3>📋 Posting Instructions</h3>
                <ol>
                    <li>Click the copy button above for your preferred platform</li>
                    <li>Go to <a href="https://twitter.com" target="_blank">Twitter</a> or <a href="https://linkedin.com/feed" target="_blank">LinkedIn</a></li>
                    <li>Paste the content and post!</li>
                    <li>Best posting times: 9AM, 1PM, or 5PM in your timezone</li>
                </ol>
            </div>
            
            <script>
                function copyToClipboard(elementId) {{
                    const element = document.getElementById(elementId);
                    const text = element.innerText;
                    navigator.clipboard.writeText(text).then(() => {{
                        alert('Content copied to clipboard!');
                    }});
                }}
            </script>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
    
    def schedule_content(self, content: Dict, topic: str, schedule_times: List[str]) -> str:
        """Create a content schedule file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/schedule_{timestamp}.json"
        
        schedule_data = {
            "topic": topic,
            "content": content,
            "schedule": [
                {
                    "platform": platform,
                    "content": content.get(platform, ""),
                    "suggested_times": schedule_times,
                    "status": "pending"
                }
                for platform in content.keys()
            ],
            "created_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, indent=2, ensure_ascii=False)
        
        return filename