from django.contrib import admin
from django.utils.html import format_html

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
    list_display = ['title', 'creator', 'category', 'is_featured', 'is_free', 'is_new', 'created_at']
    list_filter = ['category', 'is_featured', 'created_at', 'creator']
    search_fields = ['title', 'description', 'creator__username']
    readonly_fields = ['created_at', 'updated_at', 'is_new']
    list_editable = ['is_featured']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'creator', 'category')
        }),
        ('Files', {
            'fields': ('asset_file', 'thumbnail')
        }),
        ('Settings', {
            'fields': ('price', 'is_featured'),
            'description': 'Pricing and featured status'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_free(self, obj):
        return obj.is_free
    is_free.boolean = True
    is_free.short_description = 'Free'
    
    def is_new(self, obj):
        return obj.is_new
    is_new.boolean = True
    is_new.short_description = 'New'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified', 'library_count']
    list_filter = ['is_verified']
    search_fields = ['user__username', 'user__email']
    
    def library_count(self, obj):
        return obj.library.count()
    library_count.short_description = 'Library Assets'

