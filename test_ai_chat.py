"""
Test script for AI Chat functionality
"""
import requests
import json

def test_chatbot_api():
    """Test the chatbot API endpoint"""
    url = "http://127.0.0.1:8000/api/chatbot/"
    
    # Test data
    test_messages = [
        {
            "message": "Hello! I need some 3D character models for my game",
            "conversation_history": [],
            "request_id": "test-1"
        },
        {
            "message": "Show me 2D art assets",
            "conversation_history": [
                {"role": "user", "content": "Hello! I need some 3D character models for my game"},
                {"role": "assistant", "content": "Great! I can help you find 3D character models."}
            ],
            "request_id": "test-2"
        },
        {
            "message": "What audio assets do you have?",
            "conversation_history": [],
            "request_id": "test-3"
        }
    ]
    
    print("🧪 Testing NexusStore AI Chat API")
    print("=" * 50)
    
    for i, test_data in enumerate(test_messages, 1):
        print(f"\n🔍 Test {i}: {test_data['message']}")
        
        try:
            response = requests.post(
                url,
                data=json.dumps(test_data),
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"📝 Response: {data.get('response', 'No response')[:100]}...")
                print(f"🎯 Actions: {len(data.get('actions', []))} action(s)")
                print(f"⚡ Quick Actions: {len(data.get('quick_actions', []))} quick action(s)")
                print(f"🤖 AI Powered: {data.get('is_ai_powered', False)}")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"📝 Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure Django server is running")
        except requests.exceptions.Timeout:
            print("⏱️ Timeout: Request took too long")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("\n💡 Note: AI features require OPENAI_API_KEY in .env file")
    print("   Without API key, system uses fallback responses")

if __name__ == "__main__":
    test_chatbot_api()
