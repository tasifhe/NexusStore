
from django.contrib.auth.decorators import login_required

# ...existing code...

@login_required
def profile(request):
    """Show the user's profile page"""
    user_profile = request.user.userprofile
    return render(request, 'assets/profile.html', {'user_profile': user_profile})

# ...existing imports...

from django.contrib.auth.decorators import login_required

# ...existing code...

@login_required
def my_library(request):
    """Show assets added to the user's library with enhanced features"""
    user_profile = request.user.userprofile
    assets = user_profile.library.select_related('creator', 'category').order_by('-created_at')
    
    # Calculate additional stats
    total_size = "0 MB"  # Placeholder for now
    categories_count = assets.values('category').distinct().count() if assets.exists() else 0
    total_downloads = sum(asset.downloads for asset in assets if hasattr(asset, 'downloads'))
    
    # Pagination
    paginator = Paginator(assets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'assets': page_obj,
        'total_size': total_size,
        'categories_count': categories_count,
        'total_downloads': total_downloads,
    }
    return render(request, 'assets/my_library.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Asset, Category, UserProfile
from .forms import AssetUploadForm, UserRegistrationForm
from .ai_service import ai_service
import json
import os
from django.contrib.auth.decorators import login_required

def home(request):
    """Home page with categories and recent assets"""
    categories = Category.objects.all()
    recent_assets = Asset.objects.select_related('creator', 'category').order_by('-created_at')[:12]
    
    # Get featured asset (first featured asset or most recent if none)
    featured_asset = Asset.objects.filter(is_featured=True).select_related('creator', 'category').first()
    if not featured_asset:
        featured_asset = Asset.objects.select_related('creator', 'category').order_by('-created_at').first()
    
    context = {
        'categories': categories,
        'recent_assets': recent_assets,
        'featured_asset': featured_asset,
    }
    return render(request, 'assets/home.html', context)

def asset_list(request):
    """Enhanced list all assets with pagination and stats"""
    assets = Asset.objects.select_related('creator', 'category').order_by('-created_at')
    
    # Get filter and sort parameters
    filter_type = request.GET.get('filter', 'all')
    sort_by = request.GET.get('sort', 'recent')
    
    # Apply filters
    if filter_type == 'featured':
        assets = assets.filter(is_featured=True)
    elif filter_type == 'recent':
        from datetime import datetime, timedelta
        recent_date = datetime.now() - timedelta(days=30)
        assets = assets.filter(created_at__gte=recent_date)
    elif filter_type == 'free':
        assets = assets.filter(price=0)
    elif filter_type == 'popular':
        # Assuming you have a download_count field, otherwise use created_at
        assets = assets.order_by('-created_at')  # Placeholder for popularity
    
    # Apply sorting
    if sort_by == 'name':
        assets = assets.order_by('title')
    elif sort_by == 'category':
        assets = assets.order_by('category__name', 'title')
    elif sort_by == 'popular':
        assets = assets.order_by('-created_at')  # Placeholder for popularity
    else:  # 'recent' or default
        assets = assets.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(assets, 12)  # Show 12 assets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get stats for the header
    from django.db.models import Count
    total_assets = Asset.objects.count()
    total_categories = Asset.objects.values('category').distinct().count()
    total_creators = Asset.objects.values('creator').distinct().count()
    
    context = {
        'page_obj': page_obj,
        'assets': page_obj,
        'total_assets': total_assets,
        'total_categories': total_categories,
        'total_creators': total_creators,
        'current_filter': filter_type,
        'current_sort': sort_by,
    }
    return render(request, 'assets/asset_list.html', context)

def asset_detail(request, asset_id):
    """Enhanced asset detail page with additional context"""
    asset = get_object_or_404(Asset, id=asset_id)
    related_assets = Asset.objects.filter(category=asset.category).exclude(id=asset.id)[:4]
    
    # Check if asset is in user's library
    is_in_library = False
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
            is_in_library = asset in user_profile.library.all()
        except:
            is_in_library = False
    
    # Get additional context
    context = {
        'asset': asset,
        'related_assets': related_assets,
        'asset_creator_total': asset.creator.assets.count(),
        'similar_assets_count': Asset.objects.filter(category=asset.category).count() - 1,
        'is_in_library': is_in_library,
    }
    return render(request, 'assets/asset_detail.html', context)

def download_asset(request, asset_id):
    """Handle asset download"""
    asset = get_object_or_404(Asset, id=asset_id)
    
    # Check if user is authenticated (optional for educational use)
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to download assets.')
        return redirect('assets:login')
    
    # Serve the file
    if asset.asset_file:
        response = HttpResponse(asset.asset_file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(asset.asset_file.name)}"'
        return response
    else:
        raise Http404("Asset file not found")

def category_assets(request, category_slug):
    """Assets filtered by category"""
    category = get_object_or_404(Category, slug=category_slug)
    assets = Asset.objects.filter(category=category).select_related('creator').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(assets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'assets': page_obj,
    }
    return render(request, 'assets/category_assets.html', context)

def search_assets(request):
    """Enhanced search assets with filtering and sorting"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    price_range = request.GET.get('price_range')
    file_type = request.GET.get('file_type')
    sort = request.GET.get('sort', '')
    
    # Start with all assets
    assets = Asset.objects.select_related('creator', 'category').all()
    
    # Apply search query filter
    if query:
        assets = assets.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(creator__username__icontains=query) |
            Q(creator__first_name__icontains=query) |
            Q(creator__last_name__icontains=query)
        )
    
    # Apply category filter
    if category_id:
        try:
            assets = assets.filter(category_id=int(category_id))
        except (ValueError, TypeError):
            pass
    
    # Apply price range filter
    if price_range:
        if price_range == 'free':
            assets = assets.filter(price=0)
        elif price_range == '0-10':
            assets = assets.filter(price__gt=0, price__lte=10)
        elif price_range == '10-50':
            assets = assets.filter(price__gt=10, price__lte=50)
        elif price_range == '50-100':
            assets = assets.filter(price__gt=50, price__lte=100)
        elif price_range == '100+':
            assets = assets.filter(price__gt=100)
    
    # Apply file type filter (basic implementation)
    if file_type:
        if file_type == 'image':
            assets = assets.filter(
                Q(file__icontains='.jpg') | Q(file__icontains='.jpeg') |
                Q(file__icontains='.png') | Q(file__icontains='.gif') |
                Q(file__icontains='.bmp') | Q(file__icontains='.tiff')
            )
        elif file_type == '3d':
            assets = assets.filter(
                Q(file__icontains='.obj') | Q(file__icontains='.fbx') |
                Q(file__icontains='.blend') | Q(file__icontains='.3ds') |
                Q(file__icontains='.dae') | Q(file__icontains='.max')
            )
        elif file_type == 'audio':
            assets = assets.filter(
                Q(file__icontains='.mp3') | Q(file__icontains='.wav') |
                Q(file__icontains='.ogg') | Q(file__icontains='.flac') |
                Q(file__icontains='.m4a')
            )
        elif file_type == 'video':
            assets = assets.filter(
                Q(file__icontains='.mp4') | Q(file__icontains='.avi') |
                Q(file__icontains='.mov') | Q(file__icontains='.wmv') |
                Q(file__icontains='.flv') | Q(file__icontains='.webm')
            )
        elif file_type == 'script':
            assets = assets.filter(
                Q(file__icontains='.py') | Q(file__icontains='.js') |
                Q(file__icontains='.cs') | Q(file__icontains='.cpp') |
                Q(file__icontains='.c') | Q(file__icontains='.java')
            )
    
    # Apply sorting
    if sort == 'newest':
        assets = assets.order_by('-created_at')
    elif sort == 'oldest':
        assets = assets.order_by('created_at')  
    elif sort == 'price_low':
        assets = assets.order_by('price', '-created_at')
    elif sort == 'price_high':
        assets = assets.order_by('-price', '-created_at')
    elif sort == 'name':
        assets = assets.order_by('title')
    else:
        # Default ordering - featured first, then by relevance/date
        if query:
            # For search results, order by relevance (basic implementation)
            assets = assets.order_by('-is_featured', '-created_at')
        else:
            assets = assets.order_by('-is_featured', '-created_at')
    
    # Pagination
    paginator = Paginator(assets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter dropdown
    categories = Category.objects.all().order_by('name')
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'assets': page_obj,
        'categories': categories,
        'current_filters': {
            'category': category_id,
            'price_range': price_range,
            'file_type': file_type,
            'sort': sort,
        }
    }
    return render(request, 'assets/search_results.html', context)

@login_required
def upload_asset(request):
    """Upload new asset (verified users only)"""
    if not request.user.userprofile.is_verified:
        messages.error(request, 'You need to be verified to upload assets. Please contact the administrator.')
        return redirect('assets:home')
    
    if request.method == 'POST':
        form = AssetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.creator = request.user
            asset.save()
            messages.success(request, 'Asset uploaded successfully!')
            return redirect('assets:asset_detail', asset_id=asset.id)
    else:
        form = AssetUploadForm()
    
    context = {
        'form': form,
    }
    return render(request, 'assets/upload_asset.html', context)

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('assets:login')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'assets/register.html', context)

def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'assets:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'assets/login.html')

def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('assets:home')

@csrf_exempt
def chatbot_api(request):
    """Enhanced AI chatbot API for asset recommendations"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            conversation_history = data.get('conversation_history', [])
            request_id = data.get('request_id', '')
            
            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            # Get asset context for AI
            asset_context = _build_asset_context()
            
            # Try AI-powered response first
            if ai_service.is_available():
                response_data = ai_service.generate_chat_response(
                    user_message, 
                    conversation_history, 
                    asset_context
                )
            else:
                # Fallback to enhanced rule-based response
                response_data = generate_enhanced_chatbot_response(user_message, conversation_history)
            
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def _build_asset_context():
    """Build context about available assets for AI"""
    try:
        # Get statistics about assets
        total_assets = Asset.objects.count()
        categories = Category.objects.all()
        recent_assets = Asset.objects.order_by('-created_at')[:5]
        featured_assets = Asset.objects.filter(is_featured=True)[:3]
        
        context_parts = [
            f"Total assets available: {total_assets}",
            f"Categories: {', '.join([cat.name for cat in categories])}",
        ]
        
        if recent_assets.exists():
            recent_titles = [asset.title for asset in recent_assets]
            context_parts.append(f"Recent assets: {', '.join(recent_titles)}")
        
        if featured_assets.exists():
            featured_titles = [asset.title for asset in featured_assets]
            context_parts.append(f"Featured assets: {', '.join(featured_titles)}")
        
        return " | ".join(context_parts)
    except Exception:
        return "Game development assets platform with 3D models, 2D art, audio, and more."

def generate_enhanced_chatbot_response(message, conversation_history=None):
    """Generate enhanced chatbot response with actions and context awareness"""
    message = message.lower().strip()
    
    # Context from conversation history
    has_context = conversation_history and len(conversation_history) > 0
    
    # Greeting responses
    if any(word in message for word in ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon']):
        return {
            'response': "Hello! 👋 Welcome to Nexus Store! I'm here to help you find amazing game development assets. What type of project are you working on?",
            'actions': [
                {'label': '3D Game', 'text': 'I need 3D assets'},
                {'label': '2D Game', 'text': 'I need 2D assets'},
                {'label': 'Just Browsing', 'text': 'Show me popular assets'}
            ],
            'quick_actions': [
                {'icon': '🎮', 'label': '3D Models', 'text': 'Show me 3D models'},
                {'icon': '🎨', 'label': '2D Art', 'text': 'Show me 2D art'},
                {'icon': '🎵', 'label': 'Audio', 'text': 'Show me audio assets'},
                {'icon': '🔥', 'label': 'Popular', 'text': 'Show me popular assets'}
            ]
        }
    
    # Asset type specific searches with enhanced responses
    if any(word in message for word in ['3d', 'model', 'character', 'object', 'mesh']):
        assets = Asset.objects.filter(category__name__icontains='3D').order_by('-created_at')[:5]
        if assets:
            asset_names = [asset.title for asset in assets]
            asset_list = ', '.join(asset_names[:3])
            count = assets.count()
            
            response = f"🎮 Great choice! I found {count}+ 3D models including: **{asset_list}**"
            if count > 3:
                response += f" and {count-3} more!"
            response += "\n\nThese are perfect for characters, environments, and game objects. Would you like to see a specific type?"
            
            return {
                'response': response,
                'actions': [
                    {'label': 'Characters', 'text': 'Show me 3D characters'},
                    {'label': 'Environments', 'text': 'Show me 3D environments'},
                    {'label': 'Browse All', 'text': 'Browse all 3D models'}
                ],
                'quick_actions': [
                    {'icon': '👤', 'label': 'Characters', 'text': 'Show me 3D characters'},
                    {'icon': '🏰', 'label': 'Buildings', 'text': 'Show me 3D buildings'},
                    {'icon': '🚗', 'label': 'Vehicles', 'text': 'Show me 3D vehicles'},
                    {'icon': '⚔️', 'label': 'Weapons', 'text': 'Show me 3D weapons'}
                ]
            }
        return {
            'response': "🎮 Our 3D Models category has characters, environments, props, and more! Perfect for Unity, Unreal Engine, and Blender projects. What specific type of 3D asset are you looking for?",
            'actions': [
                {'label': 'Browse 3D', 'text': 'Browse all 3D models'},
                {'label': 'Characters', 'text': 'Show me 3D characters'},
                {'label': 'Environments', 'text': 'Show me 3D environments'}
            ]
        }
    
    elif any(word in message for word in ['2d', 'sprite', 'art', 'drawing', 'pixel']):
        assets = Asset.objects.filter(category__name__icontains='2D').order_by('-created_at')[:5]
        if assets:
            asset_names = [asset.title for asset in assets]
            asset_list = ', '.join(asset_names[:3])
            count = assets.count()
            
            response = f"🎨 Perfect! I found {count}+ 2D art assets including: **{asset_list}**"
            if count > 3:
                response += f" and {count-3} more!"
            response += "\n\nThese include sprites, backgrounds, UI elements, and pixel art. What style are you looking for?"
            
            return {
                'response': response,
                'actions': [
                    {'label': 'Sprites', 'text': 'Show me character sprites'},
                    {'label': 'Backgrounds', 'text': 'Show me 2D backgrounds'},
                    {'label': 'Browse All', 'text': 'Browse all 2D art'}
                ],
                'quick_actions': [
                    {'icon': '🧙', 'label': 'Characters', 'text': 'Show me 2D characters'},
                    {'icon': '🏞️', 'label': 'Backgrounds', 'text': 'Show me 2D backgrounds'},
                    {'icon': '🔳', 'label': 'Pixel Art', 'text': 'Show me pixel art'},
                    {'icon': '🎭', 'label': 'Icons', 'text': 'Show me 2D icons'}
                ]
            }
        return {
            'response': "🎨 Our 2D Art collection includes sprites, backgrounds, pixel art, and illustrations! Great for indie games, mobile games, and retro-style projects. What kind of 2D assets do you need?",
            'actions': [
                {'label': 'Browse 2D', 'text': 'Browse all 2D art'},
                {'label': 'Pixel Art', 'text': 'Show me pixel art'},
                {'label': 'Sprites', 'text': 'Show me character sprites'}
            ]
        }
    
    elif any(word in message for word in ['audio', 'sound', 'music', 'sfx', 'soundtrack']):
        assets = Asset.objects.filter(category__name__icontains='Audio').order_by('-created_at')[:5]
        if assets:
            asset_names = [asset.title for asset in assets]
            asset_list = ', '.join(asset_names[:3])
            count = assets.count()
            
            response = f"🎵 Awesome! I found {count}+ audio assets including: **{asset_list}**"
            if count > 3:
                response += f" and {count-3} more!"
            response += "\n\nWe have background music, sound effects, and ambient sounds. What type of audio do you need?"
            
            return {
                'response': response,
                'actions': [
                    {'label': 'Music', 'text': 'Show me background music'},
                    {'label': 'Sound Effects', 'text': 'Show me sound effects'},
                    {'label': 'Browse All', 'text': 'Browse all audio'}
                ],
                'quick_actions': [
                    {'icon': '🎼', 'label': 'Music', 'text': 'Show me background music'},
                    {'icon': '💥', 'label': 'SFX', 'text': 'Show me sound effects'},
                    {'icon': '🌊', 'label': 'Ambient', 'text': 'Show me ambient sounds'},
                    {'icon': '🎸', 'label': 'Loops', 'text': 'Show me music loops'}
                ]
            }
        return {
            'response': "🎵 Our Audio collection includes background music, sound effects, ambient sounds, and voice clips! Perfect for creating immersive game experiences. What type of audio are you looking for?",
            'actions': [
                {'label': 'Browse Audio', 'text': 'Browse all audio'},
                {'label': 'Background Music', 'text': 'Show me background music'},
                {'label': 'Sound Effects', 'text': 'Show me sound effects'}
            ]
        }
    
    # Popular/trending assets
    elif any(word in message for word in ['popular', 'trending', 'best', 'top', 'featured']):
        featured_assets = Asset.objects.filter(is_featured=True).order_by('-created_at')[:4]
        if featured_assets:
            asset_list = ', '.join([asset.title for asset in featured_assets[:3]])
            response = f"🔥 Here are our most popular assets right now: **{asset_list}**"
            if len(featured_assets) > 3:
                response += f" and more!"
            response += f"\n\nThese have been downloaded by hundreds of developers. Check them out!"
            
            return {
                'response': response,
                'actions': [
                    {'label': 'View Featured', 'text': 'Show me all featured assets'},
                    {'label': 'Most Downloaded', 'text': 'Show me most downloaded'},
                    {'label': 'Recent Popular', 'text': 'Show me recent popular assets'}
                ]
            }
        return {
            'response': "🔥 Our featured assets are the community favorites! These are high-quality, well-reviewed assets that developers love. Want to see what's trending?",
            'actions': [
                {'label': 'View Featured', 'text': 'Show me featured assets'},
                {'label': 'Browse All', 'text': 'Browse all assets'}
            ]
        }
    
    # Latest/new assets
    elif any(word in message for word in ['latest', 'new', 'recent', 'newest']):
        recent_assets = Asset.objects.order_by('-created_at')[:4]
        if recent_assets:
            asset_list = ', '.join([asset.title for asset in recent_assets[:3]])
            response = f"🆕 Fresh additions to our collection: **{asset_list}**"
            if len(recent_assets) > 3:
                response += " and more!"
            response += "\n\nThese were just added by our amazing community of creators!"
            
            return {
                'response': response,
                'actions': [
                    {'label': 'View All New', 'text': 'Show me all new assets'},
                    {'label': 'This Week', 'text': 'Show me assets from this week'},
                    {'label': 'Subscribe', 'text': 'How do I get notified of new assets?'}
                ]
            }
        return {
            'response': "🆕 We're constantly adding new assets to our collection! Our creators upload fresh content regularly. Want to see the latest additions?",
            'actions': [
                {'label': 'View Latest', 'text': 'Show me latest assets'},
                {'label': 'Browse All', 'text': 'Browse all assets'}
            ]
        }
    
    # Help and guidance
    elif any(word in message for word in ['help', 'how', 'guide', 'tutorial', 'explain']):
        return {
            'response': "🤝 I'm here to help! I can assist you with:\n\n• **Finding Assets**: Tell me what type of assets you need\n• **Categories**: Browse our organized collections\n• **Downloads**: Learn how to download and use assets\n• **Uploads**: Information about sharing your creations\n\nWhat would you like to know more about?",
            'actions': [
                {'label': 'Finding Assets', 'text': 'How do I find the right assets?'},
                {'label': 'Downloads', 'text': 'How do I download assets?'},
                {'label': 'Upload Guide', 'text': 'How do I upload my assets?'}
            ],
            'quick_actions': [
                {'icon': '📁', 'label': 'Categories', 'text': 'Show me all categories'},
                {'icon': '⬇️', 'label': 'Download Help', 'text': 'How do I download assets?'},
                {'icon': '⬆️', 'label': 'Upload Help', 'text': 'How do I upload assets?'},
                {'icon': '🔍', 'label': 'Search Tips', 'text': 'Give me search tips'}
            ]
        }
    
    # Download information
    elif any(word in message for word in ['download', 'free', 'cost', 'price']):
        return {
            'response': "💰 All assets on Nexus Store are **completely free** for educational use! 🎉\n\n**To download:**\n1. Browse or search for assets\n2. Click on any asset you like\n3. Hit the download button\n4. Enjoy creating!\n\n*Note: You'll need to be logged in to download assets.*",
            'actions': [
                {'label': 'Sign Up', 'text': 'How do I create an account?'},
                {'label': 'Browse Assets', 'text': 'Show me assets to download'},
                {'label': 'License Info', 'text': 'Tell me about licenses'}
            ]
        }
    
    # Upload information
    elif any(word in message for word in ['upload', 'share', 'publish', 'contribute']):
        return {
            'response': "🎨 Love creating? We'd love to have your assets in our community!\n\n**To become a publisher:**\n1. Create an account\n2. Get verified by our team\n3. Upload your amazing creations\n4. Share with the community!\n\nContact our administrators to get verified and start sharing your work!",
            'actions': [
                {'label': 'Contact Admin', 'text': 'How do I contact administrators?'},
                {'label': 'Learn More', 'text': 'Tell me more about publishing'},
                {'label': 'Guidelines', 'text': 'What are the upload guidelines?'}
            ]
        }
    
    else:
        # Context-aware default response
        recent_assets = Asset.objects.order_by('-created_at')[:3]
        if recent_assets:
            asset_list = ', '.join([asset.title for asset in recent_assets])
            response = f"I'm not sure I understood that, but here are some of our latest assets: **{asset_list}**\n\nI can help you find specific types of assets! Try asking about:"
        else:
            response = "I'm not sure I understood that, but I'm here to help you find amazing game development assets!\n\nI can help you find:"
        
        return {
            'response': response,
            'actions': [
                {'label': '3D Models', 'text': 'Show me 3D models'},
                {'label': '2D Art', 'text': 'Show me 2D art'},
                {'label': 'Audio Assets', 'text': 'Show me audio assets'}
            ],
            'quick_actions': [
                {'icon': '🎮', 'label': '3D Models', 'text': 'Show me 3D models'},
                {'icon': '🎨', 'label': '2D Art', 'text': 'Show me 2D art'},
                {'icon': '🎵', 'label': 'Audio', 'text': 'Show me audio assets'},
                {'icon': '🏠', 'label': 'Home', 'text': 'Take me to the homepage'}
            ]
        }


# Enhanced Library Management Views

@login_required
def add_to_library(request, asset_id):
    """Add an asset to user's library"""
    if request.method == 'POST':
        try:
            asset = get_object_or_404(Asset, id=asset_id)
            user_profile = request.user.userprofile
            
            if asset not in user_profile.library.all():
                user_profile.library.add(asset)
                return JsonResponse({
                    'success': True,
                    'message': f'{asset.title} added to your library!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Asset is already in your library.'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Failed to add asset to library.'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
def remove_from_library(request, asset_id):
    """Remove an asset from user's library"""
    if request.method == 'POST':
        try:
            asset = get_object_or_404(Asset, id=asset_id)
            user_profile = request.user.userprofile
            
            if asset in user_profile.library.all():
                user_profile.library.remove(asset)
                return JsonResponse({
                    'success': True,
                    'message': f'{asset.title} removed from your library!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Asset is not in your library.'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Failed to remove asset from library.'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def asset_preview_api(request, asset_id):
    """API endpoint for asset quick preview"""
    try:
        asset = get_object_or_404(Asset, id=asset_id)
        data = {
            'id': asset.id,
            'title': asset.title,
            'description': asset.description,
            'creator': asset.creator.get_full_name() or asset.creator.username,
            'category': asset.category.name if asset.category else 'Uncategorized',
            'price': float(asset.price) if asset.price else 0,
            'is_free': asset.is_free,
            'is_featured': asset.is_featured,
            'is_new': asset.is_new,
            'download_count': asset.download_count,
            'created_at': asset.created_at.strftime('%B %d, %Y'),
            'thumbnail_url': asset.thumbnail.url if asset.thumbnail else None,
        }
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': 'Asset not found or error occurred'
        }, status=404)

