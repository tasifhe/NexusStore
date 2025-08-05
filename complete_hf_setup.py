#!/usr/bin/env python
"""
Complete Hugging Face Setup Guide
"""
import webbrowser
import os
import requests
from dotenv import load_dotenv

def open_huggingface_signup():
    """Open Hugging Face signup/token page"""
    print("🤗 HUGGING FACE SETUP - Step by Step")
    print("="*60)
    
    print("Opening Hugging Face in your browser...")
    try:
        webbrowser.open("https://huggingface.co/join")
        print("✅ Opened signup page")
    except:
        print("❌ Could not open browser")
    
    print("\n📋 STEP 1: Create Account (if you don't have one)")
    print("   • Go to: https://huggingface.co/join")
    print("   • Sign up with email (it's FREE!)")
    print("   • Verify your email")
    
    input("\n⏸️  Press ENTER when you've created your account...")
    
    print("\n📋 STEP 2: Get API Token")
    try:
        webbrowser.open("https://huggingface.co/settings/tokens")
        print("✅ Opened tokens page")
    except:
        print("❌ Could not open tokens page")
        print("   Go to: https://huggingface.co/settings/tokens")
    
    print("\n🔧 On the tokens page:")
    print("   1. Click 'New token'")
    print("   2. Name: 'NexusStore AI Chatbot'")
    print("   3. Role: 'Read' (this is FREE)")
    print("   4. Click 'Generate'")
    print("   5. COPY the token (starts with 'hf_')")
    print("   6. ⚠️  Save it somewhere safe!")
    
    token = input("\n🔑 Paste your NEW token here: ").strip()
    
    if not token:
        print("❌ No token provided")
        return None
    
    if not token.startswith('hf_'):
        print("❌ Invalid token format. Should start with 'hf_'")
        return None
    
    return token

def test_token(token):
    """Test if the token works"""
    print(f"\n🧪 Testing token: {token[:10]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ Token WORKS! User: {user_info.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ Token invalid: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def update_env_file(token):
    """Update .env file with working token"""
    env_path = '.env'
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Replace the line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('HUGGINGFACE_API_KEY='):
                lines[i] = f'HUGGINGFACE_API_KEY={token}'
                break
        
        with open(env_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Token saved to .env file")
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env: {e}")
        return False

def main():
    print("🚀 COMPLETE HUGGING FACE SETUP")
    print("="*50)
    
    # Check current token first
    load_dotenv()
    current_token = os.getenv('HUGGINGFACE_API_KEY')
    
    if current_token and len(current_token) > 10:
        print(f"🔍 Testing current token: {current_token[:10]}...")
        if test_token(current_token):
            print("🎉 Your current token works! No setup needed.")
            return True
    
    print("❌ Current token doesn't work. Let's get a new one!")
    
    # Get new token
    token = open_huggingface_signup()
    
    if not token:
        print("❌ Setup cancelled")
        return False
    
    # Test new token
    if test_token(token):
        # Update .env file
        if update_env_file(token):
            print("\n🎉 SETUP COMPLETE!")
            print("✅ Valid Hugging Face token installed")
            print("✅ .env file updated")
            print("\n🚀 Next steps:")
            print("   1. Run: python test_ai_chat.py")
            print("   2. Start Django: python manage.py runserver")
            print("   3. Test your AI chatbot!")
            return True
    
    print("❌ Token validation failed")
    return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n💡 MANUAL SETUP:")
        print("   1. Go to: https://huggingface.co/settings/tokens")
        print("   2. Create a 'Read' token")
        print("   3. Update your .env file manually")
        print("   4. Token should start with 'hf_'")
