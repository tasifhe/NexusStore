#!/usr/bin/env python
"""
Quick setup script for FREE Hugging Face AI
"""
import webbrowser
import time

def setup_huggingface():
    """Guide user through Hugging Face setup"""
    print("🤗 Setting up FREE Hugging Face AI")
    print("=" * 40)
    print()
    print("Follow these steps:")
    print()
    print("1. 🌐 Opening Hugging Face in your browser...")
    
    # Open Hugging Face token page
    webbrowser.open("https://huggingface.co/settings/tokens")
    
    print("2. 📝 On the webpage:")
    print("   • Sign up/login (it's free!)")
    print("   • Click 'New token'")
    print("   • Choose 'Read' access")
    print("   • Copy your token")
    print()
    print("3. 📋 Paste your token here (or press Enter to skip):")
    
    token = input("Token: ").strip()
    
    if token:
        # Update .env file
        env_path = "f:/WEB/NexusStore/.env"
        try:
            with open(env_path, 'r') as f:
                content = f.read()
            
            # Replace the token line
            if 'HUGGINGFACE_API_KEY=your-huggingface-token-here' in content:
                content = content.replace(
                    'HUGGINGFACE_API_KEY=your-huggingface-token-here',
                    f'HUGGINGFACE_API_KEY={token}'
                )
            else:
                content += f'\nHUGGINGFACE_API_KEY={token}\n'
            
            with open(env_path, 'w') as f:
                f.write(content)
            
            print("✅ Token saved to .env file!")
            print()
            print("4. 🚀 Restart your Django server:")
            print("   • Stop current server (Ctrl+C)")
            print("   • Run: python manage.py runserver")
            print()
            print("5. 🧪 Test your AI:")
            print("   • Run: python test_ai_chat.py")
            print("   • Look for '🤖 AI Powered: True'")
            print()
            print("🎉 Your FREE AI chatbot is ready!")
            
        except Exception as e:
            print(f"❌ Error saving token: {e}")
            print(f"💡 Manually add this line to your .env file:")
            print(f"   HUGGINGFACE_API_KEY={token}")
    else:
        print("⏭️  Skipped token setup.")
        print("💡 You can set it up later by adding to .env:")
        print("   HUGGINGFACE_API_KEY=your_token_here")
    
    print()
    print("📚 Need help? Check FREE_AI_SETUP.md")

if __name__ == "__main__":
    setup_huggingface()
