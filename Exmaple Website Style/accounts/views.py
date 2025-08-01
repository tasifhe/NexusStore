from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import User
from assets.models import Asset

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            # Log in the user
            user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            if user:
                login(request, user)
                return redirect('core:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """User profile view"""
    user_assets = Asset.objects.filter(owner=request.user)
    purchased_assets = Asset.objects.filter(purchases__user=request.user)
    wishlist_assets = Asset.objects.filter(wishlisted_by__user=request.user)
    
    context = {
        'user_assets': user_assets,
        'purchased_assets': purchased_assets,
        'wishlist_assets': wishlist_assets,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile view"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def become_seller(request):
    """Become a seller view"""
    if request.method == 'POST':
        request.user.is_seller = True
        request.user.save()
        messages.success(request, 'Congratulations! You are now a seller!')
        return redirect('core:dashboard')
    
    return render(request, 'accounts/become_seller.html')

def seller_profile(request, username):
    """Public seller profile view"""
    seller = get_object_or_404(User, username=username, is_seller=True)
    assets = Asset.objects.filter(
        owner=seller,
        status='approved',
        is_active=True
    ).select_related('category')
    
    stats = seller.get_seller_stats()
    
    context = {
        'seller': seller,
        'assets': assets,
        'stats': stats,
    }
    return render(request, 'accounts/seller_profile.html', context)
