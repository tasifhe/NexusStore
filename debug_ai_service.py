#!/usr/bin/env python
"""
Direct test of AI service with current configuration
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from assets.ai_service import ai_service
from django.conf import settings

print("🔍 AI Service Debug Test")
print("="*50)

# Check environment variables
print("🔧 Environment Check:")
print(f"   OPENAI_API_KEY: {'✅' if getattr(settings, 'OPENAI_API_KEY', None) else '❌'}")
print(f"   HUGGINGFACE_API_KEY: {'✅' if getattr(settings, 'HUGGINGFACE_API_KEY', None) else '❌'}")
print(f"   GEMINI_API_KEY: {'✅' if getattr(settings, 'GEMINI_API_KEY', None) else '❌'}")

# Check AI service
print(f"\n🤖 AI Service Status:")
print(f"   is_available(): {ai_service.is_available()}")
print(f"   providers: {ai_service.providers}")

# Test response generation
print(f"\n🧪 Testing response generation...")
try:
    response = ai_service.generate_chat_response("Hello, I need 3D models for my game")
    print(f"✅ Response generated!")
    print(f"📝 Response: {response.get('response', '')[:100]}...")
    print(f"🤖 AI Powered: {response.get('is_ai_powered', False)}")
    print(f"🏷️  Provider: {response.get('provider', 'Unknown')}")
    print(f"🎯 Actions: {len(response.get('actions', []))}")
    print(f"⚡ Quick Actions: {len(response.get('quick_actions', []))}")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("="*50)
