from django.contrib import admin

# Custom admin branding
admin.site.site_header = "GameAsset Store Admin"
admin.site.site_title = "GameAsset Store Admin Portal"
admin.site.index_title = "Welcome to the GameAsset Store Admin"
from .models import Category, Asset, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'created_at']
    list_filter = ['category', 'created_at', 'creator']
    search_fields = ['title', 'description', 'creator__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['user__username', 'user__email']

