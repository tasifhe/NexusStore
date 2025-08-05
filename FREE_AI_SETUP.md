# 🆓 FREE AI API Setup Guide

## Quick Setup for FREE AI Chat

Choose any of these **completely free** options:

### 🤗 **Option 1: Hugging Face (Recommended)**
**Why**: 30,000 characters/month free, reliable, good quality

1. **Get API Key**:
   - Go to: https://huggingface.co/settings/tokens
   - Sign up/login (free)
   - Click "New token" → "Read" access
   - Copy your token

2. **Add to .env**:
   ```
   HUGGINGFACE_API_KEY=hf_your_token_here
   ```

3. **Restart server**: `python manage.py runserver`

### 🔷 **Option 2: Google Gemini** 
**Why**: 15 requests/minute free, excellent quality

1. **Get API Key**:
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy your key

2. **Add to .env**:
   ```
   GEMINI_API_KEY=your_gemini_key_here
   ```

3. **Restart server**: `python manage.py runserver`

### 🌊 **Option 3: Cohere**
**Why**: 1000 API calls/month free

1. **Get API Key**:
   - Go to: https://dashboard.cohere.ai/api-keys
   - Sign up (free)
   - Copy your API key

2. **Add to .env**:
   ```
   COHERE_API_KEY=your_cohere_key_here
   ```

## 🚀 **Test Your Setup**

After adding any API key:

1. **Restart Django**:
   ```bash
   python manage.py runserver
   ```

2. **Test AI Chat**:
   ```bash
   python test_ai_chat.py
   ```

3. **Look for**: `🤖 AI Powered: True`

## 🎯 **Recommended Setup Order**

1. **Try Hugging Face first** (most generous free tier)
2. **Fallback to Gemini** if you need higher quality
3. **Keep your enhanced fallback** as backup (always works)

## 💡 **Pro Tips**

- **Multiple APIs**: You can add multiple keys - the system will try them in order
- **Zero Cost**: All these options are completely free to start
- **Automatic Fallback**: If one API fails, it tries the next one
- **Enhanced Mode**: Even without API keys, your chatbot works great!

## 🔧 **Current Status Check**

Run this to see what's available:
```bash
python debug_env.py
```

## 🎉 **Your Chatbot Will**:

- ✅ **Use AI when available** (with any of the free APIs)
- ✅ **Fallback gracefully** when APIs are down
- ✅ **Provide great responses** in all modes
- ✅ **Cost nothing** with free tiers
- ✅ **Work reliably** for your users

**Choose any option above and enjoy AI-powered chat in minutes!** 🚀
