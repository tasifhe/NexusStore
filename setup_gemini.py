#!/usr/bin/env python
"""
Setup Google Gemini API as FREE alternative
"""
import webbrowser
import os
import requests
from dotenv import load_dotenv

def setup_gemini():
    print("🌟 GOOGLE GEMINI API SETUP (100% FREE)")
    print("="*60)
    print("Gemini offers 15 requests per minute - completely FREE!")
    print("No credit card required!")
    
    print("\n📋 STEP 1: Get Gemini API Key")
    try:
        webbrowser.open("https://makersuite.google.com/app/apikey")
        print("✅ Opened Google AI Studio")
    except:
        print("❌ Could not open browser")
        print("   Go to: https://makersuite.google.com/app/apikey")
    
    print("\n🔧 On the Google AI Studio page:")
    print("   1. Sign in with your Google account")
    print("   2. Click 'Create API Key'")
    print("   3. Select 'Create API key in new project'")
    print("   4. COPY the API key")
    print("   5. ⚠️  Save it somewhere safe!")
    
    api_key = input("\n🔑 Paste your Gemini API key here: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return None
    
    return api_key

def test_gemini(api_key):
    print(f"\n🧪 Testing Gemini API key...")
    
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
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Gemini API WORKS!")
            
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"📝 Sample response: {text[:100]}...")
            else:
                print(f"📝 Raw result: {result}")
            
            return True
        else:
            print(f"❌ Gemini error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def update_env_with_gemini(api_key):
    """Update .env file with Gemini API key"""
    env_path = '.env'
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        updated = False
        
        for i, line in enumerate(lines):
            if line.startswith('GEMINI_API_KEY='):
                lines[i] = f'GEMINI_API_KEY={api_key}'
                updated = True
                break
        
        if not updated:
            # Add before the last line
            lines.insert(-1, f'GEMINI_API_KEY={api_key}')
        
        with open(env_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Gemini API key saved to .env file")
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env: {e}")
        return False

def main():
    print("🚀 ALTERNATIVE: GOOGLE GEMINI SETUP")
    print("="*50)
    print("Since Hugging Face tokens aren't working,")
    print("let's use Google Gemini - it's also FREE!")
    
    # Get Gemini API key
    api_key = setup_gemini()
    
    if not api_key:
        print("❌ Setup cancelled")
        return False
    
    # Test Gemini API
    if test_gemini(api_key):
        # Update .env file
        if update_env_with_gemini(api_key):
            print("\n🎉 GEMINI SETUP COMPLETE!")
            print("✅ Valid Gemini API key installed")
            print("✅ .env file updated")
            print("✅ Your AI chatbot will use Google Gemini!")
            print("\n🚀 Next steps:")
            print("   1. Restart Django: python manage.py runserver")
            print("   2. Run test: python test_ai_chat.py")
            print("   3. Your chatbot now has AI powers!")
            return True
    
    print("❌ Gemini validation failed")
    return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n💡 You can also try these FREE alternatives:")
        print("   • Cohere API: https://dashboard.cohere.ai/api-keys")
        print("   • Anthropic Claude (limited free): https://console.anthropic.com/")
        print("   • Or keep trying Hugging Face: https://huggingface.co/settings/tokens")
