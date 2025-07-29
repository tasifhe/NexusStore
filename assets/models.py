from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'"{self.title}" by {self.creator.username}'

