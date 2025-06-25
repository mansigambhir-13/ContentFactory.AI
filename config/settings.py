# config/settings.py - Updated for Gemini support
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # AI Provider Selection
    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")  # "openai" or "gemini"
    
    # OpenAI (Optional)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Gemini (Google AI) - Make sure this is loaded
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Twitter (Optional)
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Content Settings
    MAX_TWITTER_LENGTH = 280
    MAX_LINKEDIN_LENGTH = 3000
    
    # Model Settings
    DEFAULT_MODEL = "gemini-1.5-flash"  # Updated model name
    RESEARCH_MODEL = "gemini-1.5-flash"  # Updated model name
    
    def __init__(self):
        # Debug: Check if API key is loaded
        if not self.GEMINI_API_KEY:
            print("⚠️ Warning: GEMINI_API_KEY not found in environment variables")
            print("💡 Make sure your .env file contains: GEMINI_API_KEY=your_key_here")

settings = Settings()
