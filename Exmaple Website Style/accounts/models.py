from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_seller = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize profile picture if it exists
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.profile_picture.path)
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def get_seller_stats(self):
        """Get seller statistics"""
        if not self.is_seller:
            return None
        
        from assets.models import Asset
        assets = Asset.objects.filter(owner=self, is_active=True)
        
        return {
            'total_assets': assets.count(),
            'total_downloads': sum(asset.download_count for asset in assets),
            'total_revenue': sum(asset.price * asset.download_count for asset in assets),
            'average_rating': assets.aggregate(models.Avg('rating'))['rating__avg'] or 0
        }
