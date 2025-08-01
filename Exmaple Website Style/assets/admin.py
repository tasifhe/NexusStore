from django.contrib import admin
from .models import Category, Asset, Review, Purchase, Wishlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'price', 'is_free', 'status', 'download_count', 'created_at']
    list_filter = ['category', 'asset_type', 'status', 'is_free', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'owner__username', 'tags']
    readonly_fields = ['download_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'asset_type', 'owner')
        }),
        ('Files', {
            'fields': ('preview_image', 'asset_file')
        }),
        ('Pricing', {
            'fields': ('price', 'is_free')
        }),
        ('Metadata', {
            'fields': ('tags', 'version', 'file_size')
        }),
        ('Status', {
            'fields': ('status', 'is_active', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('download_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['asset', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['asset__title', 'user__username', 'comment']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'asset', 'price_paid', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'asset__title']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'asset', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'asset__title']
