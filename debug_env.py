#!/usr/bin/env python
"""
Debug script to check if environment variables are loading correctly
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append('f:/WEB/NexusStore')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def debug_env():
    """Debug environment variable loading"""
    print("🔍 Environment Variables Debug")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = 'f:/WEB/NexusStore/.env'
    if os.path.exists(env_file):
        print("✅ .env file exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content:
                print("✅ OPENAI_API_KEY found in .env file")
            if 'HUGGINGFACE_API_KEY' in content and 'hf_' in content:
                print("✅ HUGGINGFACE_API_KEY found in .env file")
            else:
                print("❌ HUGGINGFACE_API_KEY not found or invalid in .env file")
    else:
        print("❌ .env file does not exist")
    
    # Check Django settings
    try:
        api_key = settings.OPENAI_API_KEY
        if api_key:
            print(f"✅ Django settings.OPENAI_API_KEY: {api_key[:20]}...")
        else:
            print("❌ Django settings.OPENAI_API_KEY is empty")
    except AttributeError:
        print("❌ OPENAI_API_KEY not defined in Django settings")
    
    # Check Hugging Face key
    try:
        hf_key = settings.HUGGINGFACE_API_KEY
        if hf_key and hf_key.startswith('hf_'):
            print(f"✅ Django settings.HUGGINGFACE_API_KEY: {hf_key[:20]}...")
        else:
            print("❌ Django settings.HUGGINGFACE_API_KEY is empty or invalid")
    except AttributeError:
        print("❌ HUGGINGFACE_API_KEY not defined in Django settings")
    
    # Check os.environ directly
    env_key = os.environ.get('OPENAI_API_KEY', '')
    if env_key:
        print(f"✅ os.environ OPENAI_API_KEY: {env_key[:20]}...")
    else:
        print("❌ os.environ OPENAI_API_KEY is empty")
        
    # Check Hugging Face in os.environ
    hf_env_key = os.environ.get('HUGGINGFACE_API_KEY', '')
    if hf_env_key and hf_env_key.startswith('hf_'):
        print(f"✅ os.environ HUGGINGFACE_API_KEY: {hf_env_key[:20]}...")
    else:
        print("❌ os.environ HUGGINGFACE_API_KEY is empty or invalid")
    
    # Test AI service
    try:
        from assets.ai_service import ai_service
        if ai_service.is_available():
            print("✅ AI Service is available")
        else:
            print("❌ AI Service is not available")
    except Exception as e:
        print(f"❌ Error loading AI service: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    debug_env()
