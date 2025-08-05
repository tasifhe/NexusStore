#!/usr/bin/env python
"""
Test Hugging Face API directly
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

# Test with popular, available models
models_to_test = [
    "gpt2",
    "distilgpt2", 
    "microsoft/DialoGPT-medium",
    "google/flan-t5-small"
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

for model in models_to_test:
    print(f"\n🧪 Testing model: {model}")
    
    url = f"https://api-inference.huggingface.co/models/{model}"
    
    # Try different payload formats
    payloads = [
        {
            "inputs": "Hello, I need 3D models for my game",
            "options": {"wait_for_model": True}
        },
        {
            "inputs": "Hello, I need 3D models for my game"
        },
        "Hello, I need 3D models for my game"
    ]
    
    for i, payload in enumerate(payloads):
        print(f"  📋 Trying payload format {i+1}")
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            print(f"  📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Success!")
                print(f"  📝 Result: {result}")
                break
            elif response.status_code == 503:
                print(f"  ⏳ Model loading, please wait...")
            else:
                print(f"  ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
    
    # If we got a successful response, break
    if response.status_code == 200:
        break

print("\n" + "=" * 50)
