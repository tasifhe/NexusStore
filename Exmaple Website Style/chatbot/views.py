from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import json
import re
from .models import ChatSession, ChatMessage, ChatbotKnowledge
from assets.models import Asset, Category
from accounts.models import User

def chat_interface(request):
    """Chat interface view"""
    return render(request, 'chatbot/chat_interface.html')

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Send message to chatbot"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get or create session
        session = get_chat_session(request, session_id)
        
        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=message
        )
        
        # Generate bot response
        bot_response = generate_bot_response(message, session)
        
        # Save bot response
        bot_message = ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content=bot_response
        )
        
        return JsonResponse({
            'success': True,
            'response': bot_response,
            'session_id': str(session.id)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET", "POST"])
def get_or_create_session(request):
    """Get or create chat session"""
    session = get_chat_session(request)
    
    return JsonResponse({
        'session_id': str(session.id),
        'success': True
    })

def get_chat_history(request, session_id):
    """Get chat history for a session"""
    try:
        session = ChatSession.objects.get(id=session_id)
        
        # Check if user has access to this session
        if request.user.is_authenticated:
            if session.user != request.user:
                return JsonResponse({'error': 'Access denied'}, status=403)
        else:
            if session.session_key != request.session.session_key:
                return JsonResponse({'error': 'Access denied'}, status=403)
        
        messages = ChatMessage.objects.filter(session=session).order_by('created_at')
        
        history = []
        for msg in messages:
            history.append({
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.created_at.isoformat()
            })
        
        return JsonResponse({
            'history': history,
            'success': True
        })
        
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_chat_session(request, session_id=None):
    """Get or create chat session"""
    if session_id:
        try:
            session = ChatSession.objects.get(id=session_id)
            return session
        except ChatSession.DoesNotExist:
            pass
    
    # Create new session
    session = ChatSession.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key if not request.user.is_authenticated else None
    )
    
    return session

def generate_bot_response(message, session):
    """Generate bot response based on message"""
    message_lower = message.lower()
    
    # Greeting responses
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm your GameAssetHub assistant. I can help you find assets, answer questions about our platform, and suggest the best assets for your projects. What can I help you with today?"
    
    # Asset search queries
    if any(word in message_lower for word in ['find', 'search', 'looking for', 'need', 'want']):
        return handle_asset_search(message_lower)
    
    # Category queries
    if any(word in message_lower for word in ['category', 'categories', 'type', 'types']):
        return handle_category_query(message_lower)
    
    # Help queries
    if any(word in message_lower for word in ['help', 'how to', 'how do', 'guide']):
        return handle_help_query(message_lower)
    
    # Pricing queries
    if any(word in message_lower for word in ['price', 'cost', 'free', 'paid', 'money']):
        return handle_pricing_query(message_lower)
    
    # Check knowledge base
    knowledge_response = check_knowledge_base(message_lower)
    if knowledge_response:
        return knowledge_response
    
    # Default response
    return "I'm here to help you with GameAssetHub! You can ask me about:\n\n• Finding specific assets\n• Asset categories\n• Pricing information\n• How to use the platform\n• Publishing your assets\n\nWhat would you like to know more about?"

def handle_asset_search(message):
    """Handle asset search queries"""
    # Extract potential keywords
    keywords = []
    
    # Common asset types
    asset_types = ['3d model', 'texture', 'material', 'animation', 'sound', 'music', 'tool', 'template']
    for asset_type in asset_types:
        if asset_type in message:
            keywords.append(asset_type)
    
    # Common themes
    themes = ['character', 'building', 'environment', 'weapon', 'vehicle', 'nature', 'fantasy', 'sci-fi']
    for theme in themes:
        if theme in message:
            keywords.append(theme)
    
    if keywords:
        # Search for assets with these keywords
        assets = Asset.objects.filter(
            Q(title__icontains=keywords[0]) | 
            Q(description__icontains=keywords[0]) |
            Q(tags__icontains=keywords[0]),
            status='approved',
            is_active=True
        )[:3]
        
        if assets:
            response = f"I found some great {keywords[0]} assets for you:\n\n"
            for asset in assets:
                response += f"• **{asset.title}** by {asset.owner.username}\n"
                response += f"  {'Free' if asset.is_free else f'${asset.price}'} | {asset.category.name}\n"
                response += f"  {asset.description[:100]}...\n\n"
            
            response += "Would you like me to help you find something more specific?"
            return response
    
    return "I can help you find assets! Could you be more specific about what you're looking for? For example:\n\n• 3D character models\n• Environment textures\n• Sound effects\n• Animation tools\n\nWhat type of asset are you interested in?"

def handle_category_query(message):
    """Handle category queries"""
    categories = Category.objects.filter(is_active=True)
    
    response = "Here are our main asset categories:\n\n"
    for category in categories:
        asset_count = Asset.objects.filter(category=category, status='approved', is_active=True).count()
        response += f"{category.icon} **{category.name}** ({asset_count} assets)\n"
        response += f"  {category.description}\n\n"
    
    response += "Which category interests you the most?"
    return response

def handle_help_query(message):
    """Handle help queries"""
    if 'upload' in message or 'publish' in message or 'sell' in message:
        return "To publish assets on GameAssetHub:\n\n1. **Become a Seller** - Click 'Become a Seller' in your profile\n2. **Upload Your Asset** - Use the 'Create Asset' button\n3. **Add Details** - Title, description, category, and tags\n4. **Set Price** - Choose free or paid\n5. **Submit for Review** - Our team will review your asset\n\nOnce approved, your asset will be available for download!"
    
    if 'download' in message or 'buy' in message:
        return "To download assets:\n\n1. **Browse Assets** - Use search or browse categories\n2. **Free Assets** - Click 'Download' immediately\n3. **Paid Assets** - Click 'Purchase' then 'Download'\n4. **Access Your Assets** - View in your dashboard\n\nAll purchases are instant and you get lifetime access!"
    
    return "I can help you with:\n\n• **Publishing Assets** - How to upload and sell your work\n• **Downloading Assets** - How to purchase and download\n• **Platform Features** - Search, categories, reviews\n• **Account Management** - Profile, seller status\n\nWhat would you like help with?"

def handle_pricing_query(message):
    """Handle pricing queries"""
    free_count = Asset.objects.filter(is_free=True, status='approved', is_active=True).count()
    paid_count = Asset.objects.filter(is_free=False, status='approved', is_active=True).count()
    
    return f"GameAssetHub pricing:\n\n• **Free Assets**: {free_count} available - Download immediately\n• **Paid Assets**: {paid_count} available - One-time purchase\n• **No Subscriptions** - Pay once, own forever\n• **Seller Revenue** - Keep 70% of sales\n• **Safe Payments** - Secure payment processing\n\nFree assets are great for getting started, while paid assets often offer higher quality and more features!"

def check_knowledge_base(message):
    """Check knowledge base for relevant information"""
    knowledge_items = ChatbotKnowledge.objects.filter(is_active=True)
    
    for item in knowledge_items:
        keywords = item.get_keywords_list()
        if any(keyword in message for keyword in keywords):
            return item.answer
    
    return None
