#!/usr/bin/env python
"""
Test Hugging Face API key and endpoint
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('HUGGINGFACE_API_KEY')
if not api_key:
    print("❌ No Hugging Face API key found")
    exit(1)

print(f"🔑 Using API key: {api_key[:10]}...")

# Test API key with whoami endpoint
print("\n🔍 Testing API key validity...")
headers = {"Authorization": f"Bearer {api_key}"}

try:
    response = requests.get("https://huggingface.co/api/whoami", headers=headers)
    print(f"📊 Whoami Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API key valid! User: {data.get('name', 'Unknown')}")
    else:
        print(f"❌ API key invalid: {response.text}")
        exit(1)
except Exception as e:
    print(f"❌ Error testing API key: {e}")
    exit(1)

# Test simple model listing
print("\n🔍 Testing model availability...")
try:
    response = requests.get("https://api-inference.huggingface.co/models", headers=headers)
    print(f"📊 Models endpoint status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Models endpoint accessible")
    else:
        print(f"❌ Models endpoint error: {response.text}")
except Exception as e:
    print(f"❌ Error accessing models: {e}")

# Try a very simple text generation request
print("\n🔍 Testing text generation with gpt2...")
url = "https://api-inference.huggingface.co/models/gpt2"
payload = {"inputs": "The tower is 324 meters"}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"📊 GPT-2 Status: {response.status_code}")
    print(f"📝 Response: {response.text}")
    
    if response.status_code == 503:
        print("⏳ Model is loading, this is normal for the first request")
    
except Exception as e:
    print(f"❌ Exception: {e}")

print("\n" + "=" * 50)
