# test_gemini.py
import asyncio
import json
from workflows.content_pipeline import GeminiContentPipeline

async def test_gemini_content_creation():
    """Test the Gemini content creation pipeline"""
    
    pipeline = GeminiContentPipeline()
    
    # Test case
    test_case = {
        "topic": "The future of artificial intelligence in 2025",
        "platforms": ["twitter"],
        "content_type": "educational"
    }
    
    print(f"\n{'='*50}")
    print(f"GEMINI TEST")
    print(f"{'='*50}")
    
    result = await pipeline.create_content(**test_case)
    
    print(f"\n📊 RESULTS:")
    print(f"Status: {result.get('status')}")
    print(f"Topic: {result.get('topic')}")
    
    if result.get('errors'):
        print(f"❌ Errors: {result['errors']}")
    
    if result.get('key_insights'):
        print(f"\n🔍 Key Insights:")
        for insight in result['key_insights']:
            print(f"  • {insight}")
    
    if result.get('final_twitter'):
        print(f"\n🐦 Twitter Content:")
        print(f"  {result['final_twitter']}")
        print(f"  Length: {len(result['final_twitter'])} characters")
    
    if result.get('final_linkedin'):
        print(f"\n💼 LinkedIn Content:")
        print(f"  {result['final_linkedin']}")
        print(f"  Length: {len(result['final_linkedin'])} characters")
    
    print(f"\n📈 Hashtags: {result.get('hashtags', [])}")

if __name__ == "__main__":
    print("🤖 Testing AI Social Media Content Engine with Gemini")
    asyncio.run(test_gemini_content_creation())