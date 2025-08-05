#!/usr/bin/env python
"""
Test the current Gemini API key
"""
import os
import requests
from dotenv import load_dotenv

def test_gemini_key():
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    print("🌟 Testing Google Gemini API Key")
    print("="*50)
    print(f"🔑 API Key: {api_key[:20] if api_key else 'None'}...")
    
    if not api_key or api_key.startswith('your-'):
        print("❌ No valid API key found")
        return False
    
    # Test Gemini API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello! I'm looking for 3D character models for my indie game. Can you help me find some good game assets?"
            }]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        print("\n🧪 Testing Gemini API...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ GEMINI API WORKS!")
            
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"📝 Sample response: {text[:150]}...")
                print(f"📏 Full response length: {len(text)} characters")
                return True
            else:
                print(f"📝 Raw result: {result}")
                return True
                
        elif response.status_code == 400:
            error_data = response.json()
            print(f"❌ Gemini API Error: {error_data}")
            if "API key not valid" in str(error_data):
                print("💡 The API key appears to be invalid or expired")
            return False
            
        else:
            print(f"❌ Unexpected error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_ai_service_with_gemini():
    """Test if our Django AI service detects Gemini"""
    print(f"\n🔍 Testing Django AI Service Detection")
    print("-"*40)
    
    import django
    import sys
    import os
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    
    from assets.ai_service import ai_service
    
    print(f"🤖 AI Service available: {ai_service.is_available()}")
    print(f"📋 Available providers: {ai_service.providers}")
    
    # Test response generation
    try:
        print(f"\n🧪 Testing AI response generation...")
        response = ai_service.generate_chat_response("Hello, I need 3D models for my game")
        print(f"✅ Response generated!")
        print(f"📝 Response: {response.get('response', '')[:100]}...")
        print(f"🤖 AI Powered: {response.get('is_ai_powered', False)}")
        print(f"🏷️  Provider: {response.get('provider', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ AI service error: {e}")
        return False

def main():
    # Test Gemini API directly
    gemini_works = test_gemini_key()
    
    if gemini_works:
        print(f"\n🎉 GEMINI API IS WORKING!")
        
        # Test Django integration
        django_works = test_ai_service_with_gemini()
        
        if django_works:
            print(f"\n🚀 COMPLETE SUCCESS!")
            print("✅ Gemini API working")
            print("✅ Django integration working") 
            print("✅ AI chatbot is now POWERED!")
            
        else:
            print(f"\n⚠️  Gemini works but Django integration needs restart")
            print("🔄 Restart your Django server to activate AI!")
            
    else:
        print(f"\n❌ Gemini API key is not working")
        print("💡 You may need to get a new API key from:")
        print("   https://makersuite.google.com/app/apikey")

if __name__ == "__main__":
    main()
