#!/usr/bin/env python
"""
Direct AI Service Test - Testing AI service instantiation and availability
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from assets.ai_service import ai_service

print("🔍 Direct AI Service Test")
print("=" * 50)

print(f"🤖 AI Service is_available(): {ai_service.is_available()}")
print(f"📋 Available providers: {ai_service.providers}")

# Test environment variables in this context
from django.conf import settings
print(f"⚙️  OPENAI_API_KEY exists: {bool(getattr(settings, 'OPENAI_API_KEY', None))}")
print(f"⚙️  HUGGINGFACE_API_KEY exists: {bool(getattr(settings, 'HUGGINGFACE_API_KEY', None))}")
print(f"⚙️  GEMINI_API_KEY exists: {bool(getattr(settings, 'GEMINI_API_KEY', None))}")

# Test response generation
print("\n🧪 Testing response generation...")
try:
    response = ai_service.generate_chat_response("Hello, I need 3D models for my game")
    print(f"✅ Response generated successfully")
    print(f"📝 Response length: {len(response.get('response', ''))}")
    print(f"🎯 Actions: {len(response.get('actions', []))}")
    print(f"⚡ Quick actions: {len(response.get('quick_actions', []))}")
    print(f"🤖 AI powered in response: {response.get('ai_powered', False)}")
except Exception as e:
    print(f"❌ Error generating response: {e}")

print("=" * 50)
