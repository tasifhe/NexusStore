#!/usr/bin/env python
"""
Test the AI service directly via Django
"""
import os
import sys
import django
import requests
import json

# Add the project directory to Python path
sys.path.append('f:/WEB/NexusStore')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def test_ai_service_direct():
    """Test AI service directly"""
    print("🧪 Testing AI Service Directly")
    print("=" * 50)
    
    try:
        from django.conf import settings
        from assets.ai_service import ai_service
        
        print(f"✅ OPENAI_API_KEY in settings: {bool(settings.OPENAI_API_KEY)}")
        print(f"✅ AI Service available: {ai_service.is_available()}")
        
        if ai_service.is_available():
            # Test direct AI call
            response = ai_service.generate_chat_response(
                "Hello, I need 3D character models",
                [],
                "Total assets: 50, Categories: 3D Models, 2D Art, Audio"
            )
            print(f"✅ AI Response received: {response.get('is_ai_powered', False)}")
            print(f"📝 Response preview: {response.get('response', '')[:100]}...")
        else:
            print("❌ AI Service not available - checking why...")
            print(f"   Settings API Key: {settings.OPENAI_API_KEY[:20] if settings.OPENAI_API_KEY else 'Empty'}...")
            print(f"   Client initialized: {ai_service.client is not None}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_via_api():
    """Test via HTTP API"""
    print("\n🌐 Testing via HTTP API")
    print("=" * 30)
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/chatbot/',
            json={
                'message': 'Hello, test AI functionality',
                'conversation_history': [],
                'request_id': 'test-direct'
            },
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {response.status_code}")
            print(f"🤖 AI Powered: {data.get('is_ai_powered', False)}")
            print(f"📝 Response: {data.get('response', '')[:100]}...")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"📝 Error: {response.text}")
            
    except Exception as e:
        print(f"❌ HTTP Error: {e}")

if __name__ == "__main__":
    test_ai_service_direct()
    test_via_api()
