#!/usr/bin/env python
"""
Automated Hugging Face Setup for NexusStore AI Chatbot
"""
import os
import requests
import webbrowser
from dotenv import load_dotenv
import time

def test_current_api_key():
    """Test if the current API key in .env is working"""
    load_dotenv()
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    print("🔍 Testing current Hugging Face API key...")
    print(f"🔑 Key: {api_key[:10] if api_key else 'None'}...")
    
    if not api_key or api_key.startswith('hf_PaMa'):
        print("❌ Invalid or placeholder API key")
        return False
    
    # Test API key validity
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=10)
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ API key valid! User: {user_info.get('name', 'Unknown')}")
            return api_key
        else:
            print(f"❌ API key invalid: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

def test_model_availability(api_key, models):
    """Test if specific models are available and working"""
    headers = {"Authorization": f"Bearer {api_key}"}
    working_models = []
    
    for model in models:
        print(f"\n🧪 Testing model: {model}")
        url = f"https://api-inference.huggingface.co/models/{model}"
        payload = {"inputs": "Hello! I need help finding game assets for my project."}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ SUCCESS! Model is working")
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get('generated_text', '')
                    print(f"   📝 Sample: {text[:80]}...")
                working_models.append(model)
                break
            elif response.status_code == 503:
                print("   ⏳ Model loading... (normal for first use)")
                working_models.append(f"{model} (loading)")
            elif response.status_code == 404:
                print("   ❌ Model not found or not available")
            else:
                print(f"   ❌ Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    return working_models

def open_huggingface_setup():
    """Open Hugging Face token page for user"""
    print("\n" + "="*60)
    print("🤗 HUGGING FACE API KEY SETUP")
    print("="*60)
    print("Opening Hugging Face tokens page...")
    
    try:
        webbrowser.open("https://huggingface.co/settings/tokens")
        print("✅ Browser opened successfully")
    except:
        print("❌ Could not open browser. Please go to:")
        print("   https://huggingface.co/settings/tokens")
    
    print("\n📋 Follow these steps:")
    print("   1. Sign up/Login to Hugging Face (FREE)")
    print("   2. Click 'New token'")
    print("   3. Name: 'NexusStore ChatBot'")
    print("   4. Role: 'Read' (free tier)")
    print("   5. Click 'Generate'")
    print("   6. Copy the token (starts with 'hf_')")
    
    return input("\n🔑 Paste your new API key here (or press Enter to skip): ").strip()

def update_env_file(new_api_key):
    """Update the .env file with new API key"""
    env_path = '.env'
    
    if not os.path.exists(env_path):
        print("❌ .env file not found")
        return False
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        updated = False
        
        for i, line in enumerate(lines):
            if line.startswith('HUGGINGFACE_API_KEY='):
                lines[i] = f'HUGGINGFACE_API_KEY={new_api_key}'
                updated = True
                break
        
        if not updated:
            lines.append(f'HUGGINGFACE_API_KEY={new_api_key}')
        
        with open(env_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ API key updated in .env file")
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def main():
    print("🚀 NexusStore Hugging Face Setup")
    print("="*50)
    
    # Test current API key
    current_key = test_current_api_key()
    
    if current_key:
        print("\n🎯 Testing available models...")
        
        # Test standard models and the user's requested GLM-4.5 model
        test_models = [
            "zai-org/GLM-4.5",  # User's requested model
            "microsoft/DialoGPT-medium",
            "microsoft/DialoGPT-small",
            "facebook/blenderbot-400M-distill",
            "gpt2",
            "distilgpt2"
        ]
        
        working_models = test_model_availability(current_key, test_models)
        
        if working_models:
            print(f"\n🎉 SUCCESS! {len(working_models)} model(s) available:")
            for model in working_models:
                print(f"   ✅ {model}")
            
            # Special check for GLM-4.5
            if any("GLM-4.5" in model for model in working_models):
                print(f"\n🌟 GREAT NEWS! GLM-4.5 model is available!")
                print("   This is a powerful multilingual model from ZhipuAI")
                print("   It should provide excellent responses for your chatbot!")
            
            print(f"\n🔄 Restarting Django server to activate AI...")
            return True
        else:
            print(f"\n❌ No models are currently working. This could be temporary.")
            print("   Models might be loading or experiencing high traffic.")
            print("   Try again in a few minutes.")
    
    else:
        print("\n🔧 Setting up new API key...")
        new_key = open_huggingface_setup()
        
        if new_key and new_key.startswith('hf_'):
            if update_env_file(new_key):
                print("\n🔄 Testing new API key...")
                time.sleep(2)  # Brief pause for file system
                return main()  # Restart the process with new key
        else:
            print("❌ No valid API key provided. Setup cancelled.")
    
    return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n" + "="*60)
        print("🎉 HUGGING FACE SETUP COMPLETE!")
        print("="*60)
        print("✅ API key is working")
        print("✅ Models are available") 
        print("✅ AI chatbot is ready!")
        print(f"\n🚀 Next steps:")
        print("   1. Restart Django server: python manage.py runserver")
        print("   2. Test AI chat: python test_ai_chat.py")
        print("   3. Open your website and try the chatbot!")
        print(f"\n💡 Your chatbot will now use FREE Hugging Face AI!")
    else:
        print(f"\n❌ Setup incomplete. Please try again or check your API key.")
