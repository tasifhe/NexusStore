#!/usr/bin/env python
"""
Test Hugging Face API key and GLM-4.5 model
"""
import os
import requests
from dotenv import load_dotenv

def test_api_key():
    load_dotenv()
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    print("🔍 Testing Hugging Face Setup")
    print("="*50)
    print(f"🔑 API Key: {api_key[:10] if api_key else 'None'}...")
    
    if not api_key:
        print("❌ No API key found")
        return False
    
    # Test API key validity
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        print("\n🧪 Testing API key authentication...")
        response = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ API key VALID! User: {user_info.get('name', 'Unknown')}")
            return api_key
        else:
            print(f"❌ API key INVALID: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_glm_model(api_key):
    print(f"\n🌟 Testing GLM-4.5 Model (https://huggingface.co/zai-org/GLM-4.5)")
    print("-"*60)
    
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api-inference.huggingface.co/models/zai-org/GLM-4.5"
    
    # Test if model exists and is accessible
    payload = {
        "inputs": "Hello! I'm looking for 3D character models for my indie game. Can you help me find some good assets?",
        "options": {"wait_for_model": True}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ GLM-4.5 is WORKING!")
            print(f"📝 Response: {result}")
            return True
            
        elif response.status_code == 503:
            print("⏳ GLM-4.5 is loading (this can take 1-2 minutes for large models)")
            print("   Try again in a few minutes - this is normal!")
            return "loading"
            
        elif response.status_code == 404:
            print("❌ GLM-4.5 model not found or not available via Inference API")
            return False
            
        elif response.status_code == 403:
            print("❌ GLM-4.5 access denied - might require paid plan or special permissions")
            return False
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_fallback_models(api_key):
    print(f"\n🔧 Testing Fallback Models")
    print("-"*40)
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Simple, reliable models for free tier
    fallback_models = [
        "microsoft/DialoGPT-medium",
        "microsoft/DialoGPT-small", 
        "gpt2",
        "distilgpt2"
    ]
    
    working_models = []
    
    for model in fallback_models:
        print(f"\n🧪 Testing: {model}")
        url = f"https://api-inference.huggingface.co/models/{model}"
        payload = {"inputs": "Hello, I need game assets"}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                print(f"   ✅ Working!")
                working_models.append(model)
            elif response.status_code == 503:
                print(f"   ⏳ Loading...")
                working_models.append(f"{model} (loading)")
            else:
                print(f"   ❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return working_models

def main():
    # Test API key
    api_key = test_api_key()
    if not api_key:
        print(f"\n❌ Please get a valid Hugging Face API key from:")
        print("   https://huggingface.co/settings/tokens")
        return
    
    # Test GLM-4.5 model
    glm_result = test_glm_model(api_key)
    
    # Test fallback models
    fallback_models = test_fallback_models(api_key)
    
    # Summary
    print(f"\n" + "="*60)
    print("📋 SUMMARY")
    print("="*60)
    
    if glm_result == True:
        print("🌟 GLM-4.5: ✅ AVAILABLE AND WORKING!")
        print("   This is an excellent multilingual model!")
    elif glm_result == "loading":
        print("🌟 GLM-4.5: ⏳ AVAILABLE BUT LOADING")
        print("   Wait 1-2 minutes and try again")
    else:
        print("🌟 GLM-4.5: ❌ NOT AVAILABLE")
        print("   This model might require paid access or not support Inference API")
    
    if fallback_models:
        print(f"\n✅ {len(fallback_models)} fallback models available:")
        for model in fallback_models:
            print(f"   • {model}")
    else:
        print(f"\n❌ No fallback models working")
    
    if glm_result or fallback_models:
        print(f"\n🎉 AI CHATBOT IS READY!")
        print("🚀 Next: Restart Django server and test!")
    else:
        print(f"\n❌ No models are working. Try again later.")

if __name__ == "__main__":
    main()
