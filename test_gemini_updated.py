#!/usr/bin/env python
"""
Test Gemini API with updated endpoints
"""
import os
import requests
from dotenv import load_dotenv

def test_gemini_models():
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    print("🌟 Testing Google Gemini API (Updated)")
    print("="*50)
    print(f"🔑 API Key: {api_key[:20] if api_key else 'None'}...")
    
    if not api_key:
        print("❌ No API key found")
        return False
    
    # First, list available models
    print("\n🔍 Checking available models...")
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(list_url, timeout=10)
        print(f"📊 Models list status: {response.status_code}")
        
        if response.status_code == 200:
            models_data = response.json()
            available_models = []
            
            if 'models' in models_data:
                for model in models_data['models']:
                    model_name = model.get('name', '')
                    if 'generateContent' in model.get('supportedGenerationMethods', []):
                        available_models.append(model_name)
                        print(f"✅ Available: {model_name}")
            
            if available_models:
                # Test with first available model
                test_model = available_models[0]
                return test_gemini_generation(api_key, test_model)
            else:
                print("❌ No models support generateContent")
                return False
                
        else:
            print(f"❌ Models list error: {response.text}")
            # Try with common model names
            return test_common_models(api_key)
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return test_common_models(api_key)

def test_common_models(api_key):
    """Test common Gemini model names"""
    print(f"\n🧪 Testing common model names...")
    
    common_models = [
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro", 
        "models/gemini-pro",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro"
    ]
    
    for model in common_models:
        print(f"\n🔍 Trying model: {model}")
        result = test_gemini_generation(api_key, model)
        if result:
            return True
    
    return False

def test_gemini_generation(api_key, model_name):
    """Test content generation with specific model"""
    
    # Clean model name for URL
    if not model_name.startswith('models/'):
        model_name = f"models/{model_name}"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    
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
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS with {model_name}!")
            
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"   📝 Response: {text[:100]}...")
                print(f"\n🎉 GEMINI IS WORKING!")
                print(f"🏷️  Working model: {model_name}")
                return model_name
            else:
                print(f"   📝 Raw result: {result}")
                return model_name
                
        elif response.status_code == 400:
            error_data = response.json()
            print(f"   ❌ Error 400: {error_data}")
            return False
            
        elif response.status_code == 404:
            print(f"   ❌ Model not found")
            return False
            
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

if __name__ == "__main__":
    working_model = test_gemini_models()
    
    if working_model:
        print(f"\n" + "="*60)
        print("🎉 GEMINI API SETUP SUCCESSFUL!")
        print("="*60)
        print(f"✅ API key is valid")
        print(f"✅ Working model: {working_model}")
        print(f"✅ Ready for AI chatbot integration!")
        
        print(f"\n🚀 Next steps:")
        print("   1. The model will be integrated automatically")
        print("   2. Restart Django server")  
        print("   3. Test with: python test_ai_chat.py")
        
    else:
        print(f"\n❌ Gemini API not working with current key")
        print("💡 Try getting a new API key from:")
        print("   https://makersuite.google.com/app/apikey")
