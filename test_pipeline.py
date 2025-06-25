# test_pipeline.py
import asyncio
import json
from workflows.content_pipeline import ContentPipeline

async def test_content_creation():
    """Test the content creation pipeline"""
    
    pipeline = ContentPipeline()
    
    # Test cases
    test_cases = [
        {
            "topic": "The future of artificial intelligence in 2025",
            "platforms": ["twitter"],
            "content_type": "educational"
        },
        {
            "topic": "Remote work productivity tips",
            "platforms": ["twitter", "linkedin"],
            "content_type": "educational"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"TEST CASE {i}")
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
    print("🚀 Testing AI Social Media Content Engine")
    asyncio.run(test_content_creation())