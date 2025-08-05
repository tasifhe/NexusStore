"""
AI Service for Chatbot functionality using multiple AI providers
Supports: OpenAI, Hugging Face, Google Gemini (all with free tiers)
"""
import openai
import requests
import json
from django.conf import settings
from django.core.cache import cache
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class AIService:
    """Service class for handling AI chat interactions with multiple providers"""
    
    def __init__(self):
        self.openai_client = None
        self.providers = []
        
        # Initialize OpenAI if available
        if getattr(settings, 'OPENAI_API_KEY', None):
            try:
                self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                self.providers.append('openai')
            except Exception as e:
                logger.warning(f"OpenAI initialization failed: {e}")
        
        # Check other providers
        if getattr(settings, 'HUGGINGFACE_API_KEY', None):
            self.providers.append('huggingface')
        
        if getattr(settings, 'GEMINI_API_KEY', None):
            self.providers.append('gemini')
    
    def is_available(self) -> bool:
        """Check if any AI service is available"""
        return len(self.providers) > 0
    
    def generate_chat_response(self, user_message: str, conversation_history: List[Dict] = None, asset_context: str = "") -> Dict:
        """
        Generate AI-powered chat response using available providers
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            asset_context: Context about available assets
            
        Returns:
            Dict with response, actions, and quick_actions
        """
        if not self.is_available():
            return self._fallback_response(user_message)
        
        # Try providers in order of preference
        for provider in self.providers:
            try:
                if provider == 'huggingface':
                    return self._generate_huggingface_response(user_message, conversation_history, asset_context)
                elif provider == 'openai':
                    return self._generate_openai_response(user_message, conversation_history, asset_context)
                elif provider == 'gemini':
                    return self._generate_gemini_response(user_message, conversation_history, asset_context)
            except Exception as e:
                logger.warning(f"{provider} failed: {e}")
                continue
        
        # If all providers fail, use fallback
        return self._fallback_response(user_message)
    
    def _generate_huggingface_response(self, user_message: str, conversation_history: List[Dict] = None, asset_context: str = "") -> Dict:
        """Generate response using Hugging Face Inference API (FREE)"""
        api_key = getattr(settings, 'HUGGINGFACE_API_KEY', None)
        if not api_key:
            raise Exception("Hugging Face API key not available")
        
        # Build context
        system_prompt = self._build_system_prompt(asset_context)
        
        # Create a more compatible prompt format
        messages = []
        if conversation_history:
            for msg in conversation_history[-3:]:  # Keep last 3 messages
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                messages.append(f"{role.title()}: {content}")
        
        # Build full conversation
        conversation_text = f"{system_prompt}\n\n"
        if messages:
            conversation_text += "\n".join(messages) + "\n"
        conversation_text += f"User: {user_message}\nAssistant:"
        
        # Call Hugging Face API with retry logic
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Try multiple models for better success rate, including GLM-4.5
        models = [
            "zai-org/GLM-4.5",  # Advanced multilingual model (user requested)
            "microsoft/DialoGPT-medium",  # Good for conversation
            "facebook/blenderbot-400M-distill",  # Conversational AI
            "microsoft/DialoGPT-small",  # Faster fallback
            "gpt2",  # Reliable fallback
            "distilgpt2"  # Fastest fallback
        ]
        
        for model in models:
            try:
                api_url = f"https://api-inference.huggingface.co/models/{model}"
                
                payload = {
                    "inputs": conversation_text,
                    "parameters": {
                        "max_new_tokens": 150,
                        "temperature": 0.7,
                        "do_sample": True,
                        "return_full_text": False,
                        "pad_token_id": 50256  # For GPT-based models
                    },
                    "options": {
                        "wait_for_model": True,  # Wait for model to load
                        "use_cache": False
                    }
                }
                
                response = requests.post(api_url, headers=headers, json=payload, timeout=45)
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        ai_response = result[0].get('generated_text', '').strip()
                        
                        # Clean up the response
                        if ai_response.startswith('Assistant:'):
                            ai_response = ai_response[10:].strip()
                        
                        # Filter out repetitive or low-quality responses
                        if len(ai_response) > 10 and not ai_response.lower().startswith('user:'):
                            # Generate contextual actions
                            actions, quick_actions = self._generate_contextual_actions(user_message, ai_response)
                            
                            return {
                                'response': ai_response,
                                'actions': actions,
                                'quick_actions': quick_actions,
                                'is_ai_powered': True,
                                'provider': f'Hugging Face ({model.split("/")[-1]})'
                            }
                
                elif response.status_code == 503:
                    # Model is loading, try next model
                    continue
                    
            except Exception as e:
                logger.warning(f"Hugging Face model {model} failed: {e}")
                continue
        
        raise Exception("All Hugging Face models failed or are loading")
    
    def _generate_openai_response(self, user_message: str, conversation_history: List[Dict] = None, asset_context: str = "") -> Dict:
        """Generate response using OpenAI API"""
        if not self.openai_client:
            raise Exception("OpenAI client not available")
        
        # Build context for the AI
        system_prompt = self._build_system_prompt(asset_context)
        
        # Prepare messages for OpenAI
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-6:]:  # Keep last 6 messages for context
                messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Generate response using OpenAI
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
            presence_penalty=0.1,
            frequency_penalty=0.1
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Generate contextual actions based on the response
        actions, quick_actions = self._generate_contextual_actions(user_message, ai_response)
        
        return {
            'response': ai_response,
            'actions': actions,
            'quick_actions': quick_actions,
            'is_ai_powered': True,
            'provider': 'OpenAI'
        }
    
    def _generate_gemini_response(self, user_message: str, conversation_history: List[Dict] = None, asset_context: str = "") -> Dict:
        """Generate response using Google Gemini API (FREE tier available)"""
        api_key = getattr(settings, 'GEMINI_API_KEY', None) 
        if not api_key:
            raise Exception("Gemini API key not available")
        
        # Build context
        system_prompt = self._build_system_prompt(asset_context)
        
        # Try multiple Gemini models (from fastest to most capable)
        models = [
            "models/gemini-1.5-flash",  # Fastest free model
            "models/gemini-1.5-flash-8b",  # Very fast
            "models/gemini-1.5-pro",  # Most capable but slower
        ]
        
        for model in models:
            try:
                # Prepare request for Gemini
                url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={api_key}"
                
                prompt = f"{system_prompt}\n\nUser: {user_message}\n\nPlease respond as the NexusBot assistant:"
                
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 250
                    }
                }
                
                response = requests.post(url, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'candidates' in result and len(result['candidates']) > 0:
                        ai_response = result['candidates'][0]['content']['parts'][0]['text'].strip()
                        
                        # Generate contextual actions
                        actions, quick_actions = self._generate_contextual_actions(user_message, ai_response)
                        
                        return {
                            'response': ai_response,
                            'actions': actions,
                            'quick_actions': quick_actions,
                            'is_ai_powered': True,
                            'provider': f'Google Gemini ({model.split("/")[-1]})'
                        }
                elif response.status_code == 429:
                    # Rate limit - try next model
                    logger.warning(f"Gemini {model} rate limited, trying next model")
                    continue
                else:
                    logger.warning(f"Gemini {model} error {response.status_code}, trying next model")
                    continue
                    
            except Exception as e:
                logger.warning(f"Gemini {model} failed: {e}")
                continue
        
        raise Exception("All Gemini models failed or rate limited")
    
    def _build_system_prompt(self, asset_context: str) -> str:
        """Build system prompt for the AI assistant"""
        return f"""You are NexusBot, a helpful AI assistant for Nexus Store - a platform for free game development assets.

Your role:
- Help users find the perfect game development assets
- Provide friendly, enthusiastic, and professional assistance
- Keep responses concise but informative (max 200 words)
- Use relevant emojis to make responses engaging
- Focus on game development topics and asset recommendations

Key information about Nexus Store:
- All assets are FREE for educational use
- Categories include: 3D Models, 2D Art, Audio, Scripts, Textures
- Users need to be logged in to download
- Community-driven platform with user uploads
- Supports Unity, Unreal Engine, Blender, and other tools

Current asset context: {asset_context}

Guidelines:
- If users ask about specific asset types, provide helpful suggestions
- For technical questions, give practical game development advice  
- If asked about pricing, emphasize that everything is free for education
- Encourage users to explore different categories
- Be enthusiastic about game development and creativity
- If you don't know something specific, be honest but still helpful

Remember: You're here to make game development more accessible and fun!"""

    def _generate_contextual_actions(self, user_message: str, ai_response: str) -> tuple:
        """Generate contextual action buttons based on the conversation"""
        actions = []
        quick_actions = []
        
        # Analyze user message for context
        message_lower = user_message.lower()
        
        # Asset type specific actions
        if any(word in message_lower for word in ['3d', 'model', 'character', 'mesh']):
            actions = [
                {'label': 'Browse 3D Models', 'text': 'Show me 3D models'},
                {'label': '3D Characters', 'text': 'Show me 3D characters'},
                {'label': '3D Environments', 'text': 'Show me 3D environments'}
            ]
            quick_actions = [
                {'icon': '👤', 'label': 'Characters', 'text': 'Show me 3D characters'},
                {'icon': '🏰', 'label': 'Buildings', 'text': 'Show me 3D buildings'},
                {'icon': '🚗', 'label': 'Vehicles', 'text': 'Show me 3D vehicles'},
                {'icon': '⚔️', 'label': 'Weapons', 'text': 'Show me 3D weapons'}
            ]
        elif any(word in message_lower for word in ['2d', 'sprite', 'art', 'pixel']):
            actions = [
                {'label': 'Browse 2D Art', 'text': 'Show me 2D art'},
                {'label': 'Character Sprites', 'text': 'Show me character sprites'},
                {'label': 'Pixel Art', 'text': 'Show me pixel art'}
            ]
            quick_actions = [
                {'icon': '🧙', 'label': 'Characters', 'text': 'Show me 2D characters'},
                {'icon': '🏞️', 'label': 'Backgrounds', 'text': 'Show me 2D backgrounds'},
                {'icon': '🔳', 'label': 'Pixel Art', 'text': 'Show me pixel art'},
                {'icon': '🎭', 'label': 'Icons', 'text': 'Show me 2D icons'}
            ]
        elif any(word in message_lower for word in ['audio', 'sound', 'music']):
            actions = [
                {'label': 'Browse Audio', 'text': 'Show me audio assets'},
                {'label': 'Background Music', 'text': 'Show me background music'},
                {'label': 'Sound Effects', 'text': 'Show me sound effects'}
            ]
            quick_actions = [
                {'icon': '🎼', 'label': 'Music', 'text': 'Show me background music'},
                {'icon': '💥', 'label': 'SFX', 'text': 'Show me sound effects'},
                {'icon': '🌊', 'label': 'Ambient', 'text': 'Show me ambient sounds'},
                {'icon': '🎸', 'label': 'Loops', 'text': 'Show me music loops'}
            ]
        else:
            # General actions
            actions = [
                {'label': 'Browse Assets', 'text': 'Show me popular assets'},
                {'label': 'Get Started', 'text': 'How do I get started?'},
                {'label': 'Upload Assets', 'text': 'How do I upload my assets?'}
            ]
            quick_actions = [
                {'icon': '🎮', 'label': '3D Models', 'text': 'Show me 3D models'},
                {'icon': '🎨', 'label': '2D Art', 'text': 'Show me 2D art'},
                {'icon': '🎵', 'label': 'Audio', 'text': 'Show me audio assets'},
                {'icon': '🔥', 'label': 'Popular', 'text': 'Show me popular assets'}
            ]
        
        return actions, quick_actions
    
    def _fallback_response(self, user_message: str) -> Dict:
        """Fallback response when AI is not available"""
        return {
            'response': "I'm currently running in basic mode. For AI-powered responses, please configure a free API key from Hugging Face, Google Gemini, or OpenAI. I can still help you find assets though! What type of game assets are you looking for?",
            'actions': [
                {'label': '3D Models', 'text': 'Show me 3D models'},
                {'label': '2D Art', 'text': 'Show me 2D art'},
                {'label': 'Audio', 'text': 'Show me audio assets'}
            ],
            'quick_actions': [
                {'icon': '🎮', 'label': '3D Models', 'text': 'Show me 3D models'},
                {'icon': '🎨', 'label': '2D Art', 'text': 'Show me 2D art'},
                {'icon': '🎵', 'label': 'Audio', 'text': 'Show me audio assets'},
                {'icon': '🔥', 'label': 'Popular', 'text': 'Show me popular assets'}
            ],
            'is_ai_powered': False,
            'provider': 'Enhanced Fallback'
        }

# Global instance
ai_service = AIService()
