from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from assets.models import Asset, Category
from accounts.models import User

def home(request):
    """Home page view"""
    featured_assets = {
        'limited_free': Asset.objects.filter(
            status='approved', is_featured=True, is_active=True, is_free=True
        ).select_related('owner', 'category')[:6],
        'on_sale': Asset.objects.filter(
            status='approved', is_featured=True, is_active=True
        ).exclude(is_free=True).order_by('price')[:6],
        'recent': Asset.objects.filter(
            status='approved', is_active=True
        ).order_by('-created_at')[:6],
    }

    categories = Category.objects.filter(is_active=True)
    recent_assets = Asset.objects.filter(
        status='approved',
        is_active=True
    ).select_related('owner', 'category')[:8]

    top_sellers = User.objects.filter(
        is_seller=True,
        assets__status='approved'
    ).distinct()[:6]

    context = {
        'featured_assets': featured_assets,
        'categories': categories,
        'recent_assets': recent_assets,
        'top_sellers': top_sellers,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    return render(request, 'core/about.html')

def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            try:
                # In a real application, you would send an email here
                # For now, we'll just show a success message
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('core:contact')
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'core/contact.html')

@login_required
def dashboard(request):
    """User dashboard view"""
    if request.user.is_seller:
        # Seller dashboard
        user_assets = Asset.objects.filter(owner=request.user)
        stats = request.user.get_seller_stats()
        
        context = {
            'user_assets': user_assets,
            'stats': stats,
            'is_seller': True,
        }
    else:
        # Buyer dashboard
        purchased_assets = Asset.objects.filter(
            purchases__user=request.user
        ).distinct()
        
        wishlist_assets = Asset.objects.filter(
            wishlisted_by__user=request.user
        ).distinct()
        
        context = {
            'purchased_assets': purchased_assets,
            'wishlist_assets': wishlist_assets,
            'is_seller': False,
        }
    
    return render(request, 'core/dashboard.html', context)

def search(request):
    """Search assets view"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    asset_type = request.GET.get('type')
    price_filter = request.GET.get('price')
    
    assets = Asset.objects.filter(status='approved', is_active=True)
    
    if query:
        assets = assets.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    
    if category_id:
        assets = assets.filter(category_id=category_id)
    
    if asset_type:
        assets = assets.filter(asset_type=asset_type)
    
    if price_filter:
        if price_filter == 'free':
            assets = assets.filter(is_free=True)
        elif price_filter == 'paid':
            assets = assets.filter(is_free=False)
    
    # Pagination
    paginator = Paginator(assets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'selected_category': category_id,
        'selected_type': asset_type,
        'selected_price': price_filter,
    }
    
    return render(request, 'core/search.html', context)
