from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.urls import reverse
from .models import Asset, Category, Review, Purchase, Wishlist
from .forms import AssetForm, ReviewForm
from accounts.models import User

def asset_list(request):
    """List all assets"""
    assets = Asset.objects.filter(status='approved', is_active=True).select_related('owner', 'category')
    
    # Search and filtering
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    asset_type = request.GET.get('type')
    price_filter = request.GET.get('price')
    
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
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'selected_type': asset_type,
        'selected_price': price_filter,
    }
    
    return render(request, 'assets/asset_list.html', context)

def asset_detail(request, pk):
    """Asset detail view"""
    asset = get_object_or_404(Asset, pk=pk, status='approved', is_active=True)
    reviews = Review.objects.filter(asset=asset).select_related('user')
    
    # Check if user has purchased/downloaded this asset
    has_access = False
    in_wishlist = False
    
    if request.user.is_authenticated:
        has_access = (
            asset.is_free or 
            Purchase.objects.filter(user=request.user, asset=asset).exists()
        )
        in_wishlist = Wishlist.objects.filter(user=request.user, asset=asset).exists()
    
    # Related assets
    related_assets = Asset.objects.filter(
        category=asset.category,
        status='approved',
        is_active=True
    ).exclude(pk=asset.pk)[:4]
    
    context = {
        'asset': asset,
        'reviews': reviews,
        'has_access': has_access,
        'in_wishlist': in_wishlist,
        'related_assets': related_assets,
    }
    
    return render(request, 'assets/asset_detail.html', context)

@login_required
def create_asset(request):
    """Create new asset"""
    if not request.user.is_seller:
        messages.error(request, 'You need to become a seller first!')
        return redirect('accounts:become_seller')
    
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.owner = request.user
            asset.save()
            messages.success(request, 'Asset created successfully!')
            return redirect('assets:asset_detail', pk=asset.pk)
    else:
        form = AssetForm()
    
    return render(request, 'assets/create_asset.html', {'form': form})

@login_required
def edit_asset(request, pk):
    """Edit asset"""
    asset = get_object_or_404(Asset, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset updated successfully!')
            return redirect('assets:asset_detail', pk=asset.pk)
    else:
        form = AssetForm(instance=asset)
    
    return render(request, 'assets/edit_asset.html', {'form': form, 'asset': asset})

@login_required
def delete_asset(request, pk):
    """Delete asset"""
    asset = get_object_or_404(Asset, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        asset.delete()
        messages.success(request, 'Asset deleted successfully!')
        return redirect('core:dashboard')
    
    return render(request, 'assets/delete_asset.html', {'asset': asset})

@login_required
def download_asset(request, pk):
    """Download asset"""
    asset = get_object_or_404(Asset, pk=pk, status='approved', is_active=True)
    
    # Check if user has access
    has_access = (
        asset.is_free or 
        Purchase.objects.filter(user=request.user, asset=asset).exists()
    )
    
    if not has_access:
        messages.error(request, 'You need to purchase this asset first!')
        return redirect('assets:asset_detail', pk=asset.pk)
    
    # Increment download count
    asset.download_count += 1
    asset.save()
    
    if asset.asset_file:
        response = HttpResponse(
            asset.asset_file.read(),
            content_type='application/force-download'
        )
        response['Content-Disposition'] = f'attachment; filename={asset.asset_file.name}'
        return response
    else:
        messages.error(request, 'Asset file not found!')
        return redirect('assets:asset_detail', pk=asset.pk)

@login_required
def add_to_wishlist(request, pk):
    """Add asset to wishlist"""
    asset = get_object_or_404(Asset, pk=pk, status='approved', is_active=True)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        asset=asset
    )
    
    if created:
        messages.success(request, 'Asset added to wishlist!')
    else:
        messages.info(request, 'Asset already in wishlist!')
    
    return redirect('assets:asset_detail', pk=asset.pk)

@login_required
def remove_from_wishlist(request, pk):
    """Remove asset from wishlist"""
    asset = get_object_or_404(Asset, pk=pk)
    
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, asset=asset)
        wishlist_item.delete()
        messages.success(request, 'Asset removed from wishlist!')
    except Wishlist.DoesNotExist:
        messages.error(request, 'Asset not in wishlist!')
    
    return redirect('assets:asset_detail', pk=asset.pk)

@login_required
def purchase_asset(request, pk):
    """Purchase asset"""
    asset = get_object_or_404(Asset, pk=pk, status='approved', is_active=True)
    
    if asset.is_free:
        messages.error(request, 'This asset is free!')
        return redirect('assets:asset_detail', pk=asset.pk)
    
    # Check if already purchased
    if Purchase.objects.filter(user=request.user, asset=asset).exists():
        messages.info(request, 'You already own this asset!')
        return redirect('assets:asset_detail', pk=asset.pk)
    
    if request.method == 'POST':
        # Create purchase record
        Purchase.objects.create(
            user=request.user,
            asset=asset,
            price_paid=asset.price
        )
        messages.success(request, 'Asset purchased successfully!')
        return redirect('assets:download_asset', pk=asset.pk)
    
    return render(request, 'assets/purchase_asset.html', {'asset': asset})

@login_required
def add_review(request, pk):
    """Add review to asset"""
    asset = get_object_or_404(Asset, pk=pk, status='approved', is_active=True)
    
    # Check if user has purchased/downloaded this asset
    has_access = (
        asset.is_free or 
        Purchase.objects.filter(user=request.user, asset=asset).exists()
    )
    
    if not has_access:
        messages.error(request, 'You need to purchase this asset first!')
        return redirect('assets:asset_detail', pk=asset.pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.asset = asset
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('assets:asset_detail', pk=asset.pk)
    else:
        form = ReviewForm()
    
    return render(request, 'assets/add_review.html', {'form': form, 'asset': asset})

def category_detail(request, slug):
    """Category detail view"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    assets = Asset.objects.filter(
        category=category,
        status='approved',
        is_active=True
    ).select_related('owner')
    
    # Pagination
    paginator = Paginator(assets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'assets/category_detail.html', context)

def category_list(request):
    """List all categories"""
    categories = Category.objects.filter(is_active=True).prefetch_related('assets')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'assets/category_list.html', context)
