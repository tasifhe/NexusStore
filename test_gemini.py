#!/usr/bin/env python
"""
Test Google Gemini API to see if it's working
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')
print(f"🔍 Gemini API Key: {'✅ Found' if gemini_key else '❌ Not found'}")

if gemini_key:
    print(f"🔑 Using key: {gemini_key[:10]}...")
    
    # Test Gemini API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello, I need 3D models for my game. Can you help me find assets?"
            }]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"📊 Gemini Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Gemini working!")
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"📝 Response: {text[:100]}...")
            else:
                print(f"📝 Raw result: {result}")
        else:
            print(f"❌ Gemini Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        
else:
    print("❌ No Gemini API key found in environment")

print("\n" + "=" * 50)
