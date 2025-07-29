from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from assets.models import Category, Asset, UserProfile
from django.core.files.base import ContentFile
import os

class Command(BaseCommand):
    help = 'Populate the database with initial categories and sample data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': '2D Art', 'slug': '2d-art'},
            {'name': '3D Models', 'slug': '3d-models'},
            {'name': 'Audio', 'slug': 'audio'},
            {'name': 'Textures', 'slug': 'textures'},
            {'name': 'Scripts', 'slug': 'scripts'},
            {'name': 'Animations', 'slug': 'animations'},
            {'name': 'UI Elements', 'slug': 'ui-elements'},
            {'name': 'Environments', 'slug': 'environments'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'slug': cat_data['slug']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create some sample users
        sample_users = [
            {'username': 'artist1', 'email': 'artist1@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'developer1', 'email': 'dev1@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'designer1', 'email': 'designer1@example.com', 'first_name': 'Mike', 'last_name': 'Johnson'},
        ]

        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                # Mark some users as verified
                if user.username in ['artist1', 'developer1']:
                    user.userprofile.is_verified = True
                    user.userprofile.save()
                self.stdout.write(f'Created user: {user.username}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with initial data'))

