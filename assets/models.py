from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

# A model to categorize assets (e.g., 2D Art, 3D Models, Audio)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="A short, URL-friendly version of the name.")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# Extends the built-in User model to add a verification status
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_verified = models.BooleanField(default=False, help_text="Designates whether the user is verified to upload assets.")
    library = models.ManyToManyField('Asset', related_name='in_libraries', blank=True, help_text="Assets added to the user's library.")

    def __str__(self):
        return self.user.username

# These functions ensure a UserProfile is created automatically for each new User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# The main model for the assets
class Asset(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assets")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # File fields for the actual asset and its preview image
    asset_file = models.FileField(upload_to='asset_files/', help_text="The main downloadable asset file.")
    thumbnail = models.ImageField(upload_to='thumbnails/', help_text="A preview image for the asset.")
    
    # Optional pricing field (if 0 or None, asset is free)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00, help_text="Price in USD. Leave 0 for free assets.")
    
    # Feature flags
    is_featured = models.BooleanField(default=False, help_text="Mark this asset as featured.")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_free(self):
        """Check if the asset is free"""
        return self.price is None or self.price == 0

    @property
    def is_new(self):
        """Check if the asset was created within the last 7 days"""
        return self.created_at >= timezone.now() - timedelta(days=7)

    @property
    def download_count(self):
        """Return the number of times this asset has been downloaded"""
        # For now, return a placeholder. In the future, this could be tracked with a separate model
        return 0

    @property
    def downloads(self):
        """Alias for download_count for template compatibility"""
        return self.download_count

    @property
    def favorite_count(self):
        """Return the number of users who favorited this asset"""
        # For now, return a placeholder. In the future, this could be calculated from user libraries
        return self.in_libraries.count()

    @property
    def file_size(self):
        """Return a human-readable file size"""
        if self.asset_file:
            try:
                size = self.asset_file.size
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size // 1024} KB"
                elif size < 1024 * 1024 * 1024:
                    return f"{size // (1024 * 1024)} MB"
                else:
                    return f"{size // (1024 * 1024 * 1024)} GB"
            except (ValueError, OSError):
                return "Unknown"
        return "No file"

    @property
    def rating(self):
        """Return average rating for this asset"""
        # Placeholder for future rating system
        return 4.5

    @property
    def rating_count(self):
        """Return number of ratings for this asset"""
        # Placeholder for future rating system
        return 23
        return 0

    @property
    def view_count(self):
        """Return the number of times this asset has been viewed"""
        # For now, return a placeholder. In the future, this could be tracked with a separate model
        return 0

    @property
    def rating(self):
        """Return the average rating for this asset"""
        # For now, return a placeholder. In the future, this could be calculated from a Rating model
        return None

    @property
    def rating_count(self):
        """Return the number of ratings for this asset"""
        # For now, return a placeholder. In the future, this could be calculated from a Rating model
        return 0

    def __str__(self):
        return f'"{self.title}" by {self.creator.username}'

