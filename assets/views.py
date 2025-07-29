
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
    """Show assets added to the user's library"""
    user_profile = request.user.userprofile
    assets = user_profile.library.select_related('creator', 'category').order_by('-created_at')
    paginator = Paginator(assets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'assets': page_obj,
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
import json
import os
from django.contrib.auth.decorators import login_required

def home(request):
    """Home page with categories and recent assets"""
    categories = Category.objects.all()
    recent_assets = Asset.objects.select_related('creator', 'category').order_by('-created_at')[:6]
    
    context = {
        'categories': categories,
        'recent_assets': recent_assets,
    }
    return render(request, 'assets/home.html', context)

def asset_list(request):
    """List all assets with pagination"""
    assets = Asset.objects.select_related('creator', 'category').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(assets, 12)  # Show 12 assets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'assets': page_obj,
    }
    return render(request, 'assets/asset_list.html', context)

def asset_detail(request, asset_id):
    """Asset detail page"""
    asset = get_object_or_404(Asset, id=asset_id)
    related_assets = Asset.objects.filter(category=asset.category).exclude(id=asset.id)[:4]
    
    context = {
        'asset': asset,
        'related_assets': related_assets,
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
    """Search assets"""
    query = request.GET.get('q', '')
    assets = Asset.objects.select_related('creator', 'category').order_by('-created_at')
    
    if query:
        assets = assets.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(creator__username__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(assets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'assets': page_obj,
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
    """Simple chatbot API for asset recommendations"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower()
            
            # Simple keyword-based responses
            response = generate_chatbot_response(user_message)
            
            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def generate_chatbot_response(message):
    """Generate chatbot response based on keywords"""
    message = message.lower()
    
    # Asset type recommendations
    if any(word in message for word in ['3d', 'model', 'character', 'object']):
        assets = Asset.objects.filter(category__name__icontains='3D').order_by('-created_at')[:3]
        if assets:
            asset_list = ', '.join([asset.title for asset in assets])
            return f"I found some great 3D models for you: {asset_list}. You can find more in our 3D Models category!"
        return "Check out our 3D Models category for characters, objects, and environments!"
    
    elif any(word in message for word in ['2d', 'sprite', 'art', 'drawing']):
        assets = Asset.objects.filter(category__name__icontains='2D').order_by('-created_at')[:3]
        if assets:
            asset_list = ', '.join([asset.title for asset in assets])
            return f"Here are some amazing 2D art assets: {asset_list}. Browse our 2D Art category for more!"
        return "Our 2D Art category has sprites, backgrounds, and illustrations perfect for your game!"
    
    elif any(word in message for word in ['audio', 'sound', 'music', 'sfx']):
        assets = Asset.objects.filter(category__name__icontains='Audio').order_by('-created_at')[:3]
        if assets:
            asset_list = ', '.join([asset.title for asset in assets])
            return f"I found these audio assets: {asset_list}. Check our Audio category for more sounds!"
        return "Visit our Audio category for music tracks, sound effects, and ambient sounds!"
    
    elif any(word in message for word in ['texture', 'material']):
        assets = Asset.objects.filter(category__name__icontains='Texture').order_by('-created_at')[:3]
        if assets:
            asset_list = ', '.join([asset.title for asset in assets])
            return f"Here are some texture assets: {asset_list}. Find more in our Textures category!"
        return "Our Textures category has materials for walls, floors, and surfaces!"
    
    elif any(word in message for word in ['script', 'code', 'programming']):
        assets = Asset.objects.filter(category__name__icontains='Script').order_by('-created_at')[:3]
        if assets:
            asset_list = ', '.join([asset.title for asset in assets])
            return f"Check out these scripts: {asset_list}. More available in our Scripts category!"
        return "Browse our Scripts category for useful code snippets and tools!"
    
    elif any(word in message for word in ['ui', 'interface', 'button', 'menu']):
        assets = Asset.objects.filter(category__name__icontains='UI').order_by('-created_at')[:3]
        if assets:
            asset_list = ', '.join([asset.title for asset in assets])
            return f"Here are some UI elements: {asset_list}. Find more in our UI Elements category!"
        return "Our UI Elements category has buttons, menus, and interface components!"
    
    elif any(word in message for word in ['animation', 'animate']):
        assets = Asset.objects.filter(category__name__icontains='Animation').order_by('-created_at')[:3]
        if assets:
            asset_list = ', '.join([asset.title for asset in assets])
            return f"I found these animations: {asset_list}. Browse our Animations category for more!"
        return "Check out our Animations category for character and object animations!"
    
    elif any(word in message for word in ['environment', 'level', 'scene']):
        assets = Asset.objects.filter(category__name__icontains='Environment').order_by('-created_at')[:3]
        if assets:
            asset_list = ', '.join([asset.title for asset in assets])
            return f"Here are some environments: {asset_list}. More available in our Environments category!"
        return "Our Environments category has complete scenes and level assets!"
    
    elif any(word in message for word in ['help', 'how', 'what']):
        return "I can help you find assets! Try asking about 3D models, 2D art, audio, textures, scripts, UI elements, animations, or environments. You can also browse by category or use the search bar!"
    
    elif any(word in message for word in ['download', 'free']):
        return "All assets on our platform are free for educational use! Just click on any asset and hit the download button. You'll need to be logged in to download."
    
    elif any(word in message for word in ['upload', 'share']):
        return "To upload assets, you need to be a verified user. Register an account and contact the administrator to get verified. Then you can share your creations with the community!"
    
    else:
        # Default response with recent assets
        recent_assets = Asset.objects.order_by('-created_at')[:3]
        if recent_assets:
            asset_list = ', '.join([asset.title for asset in recent_assets])
            return f"Here are some of our latest assets: {asset_list}. What type of assets are you looking for? I can help you find 3D models, 2D art, audio, textures, and more!"
        return "Welcome to GameAsset Store! I can help you find the perfect assets for your game. What are you working on? Try asking about 3D models, 2D art, audio, or any other type of asset!"

