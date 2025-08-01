from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from assets.models import Category, Asset
from chatbot.models import ChatbotKnowledge

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for GameAssetHub'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'name': 'Characters & Creatures', 'description': 'Heroes, monsters, NPCs and more', 'icon': '🦸', 'slug': 'characters-creatures'},
            {'name': 'Environments', 'description': 'Landscapes, buildings, and scenes', 'icon': '🏞️', 'slug': 'environments'},
            {'name': 'Weapons & Items', 'description': 'Swords, guns, tools, and props', 'icon': '⚔️', 'slug': 'weapons-items'},
            {'name': 'Textures & Materials', 'description': 'PBR textures and materials', 'icon': '🎨', 'slug': 'textures-materials'},
            {'name': 'Audio', 'description': 'Sound effects and music', 'icon': '🎵', 'slug': 'audio'},
        ]

        for cat_data in categories:
            Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )

        self.stdout.write(self.style.SUCCESS('Categories created successfully!'))

        # Create a test seller
        seller, created = User.objects.get_or_create(
            username='testseller',
            defaults={
                'email': 'seller@example.com',
                'is_seller': True,
                'first_name': 'Test',
                'last_name': 'Seller',
                'bio': 'Professional game asset creator with 5+ years of experience.'
            }
        )

        if created:
            seller.set_password('password123')
            seller.save()

        # Create some sample assets
        category = Category.objects.first()
        if category:
            Asset.objects.get_or_create(
                title='Medieval Knight Character',
                defaults={
                    'description': 'A fully rigged and animated medieval knight character perfect for RPG games.',
                    'category': category,
                    'owner': seller,
                    'price': 29.99,
                    'status': 'approved',
                    'is_featured': True,
                    'tags': 'medieval, knight, character, rigged, animated',
                    'version': '1.0'
                }
            )

            Asset.objects.get_or_create(
                title='Free Sword Pack',
                defaults={
                    'description': 'A collection of 10 high-quality sword models for your fantasy games.',
                    'category': category,
                    'owner': seller,
                    'price': 0,
                    'is_free': True,
                    'status': 'approved',
                    'is_featured': True,
                    'tags': 'sword, weapon, fantasy, free, pack',
                    'version': '1.0'
                }
            )

        self.stdout.write(self.style.SUCCESS('Sample assets created successfully!'))

        # Create chatbot knowledge
        knowledge_items = [
            {
                'knowledge_type': 'faq',
                'question': 'How do I download assets?',
                'answer': 'To download assets: 1) Browse our asset library 2) Click on an asset you like 3) For free assets, click Download 4) For paid assets, click Purchase then Download 5) Access your downloads from your dashboard',
                'keywords': 'download, how to download, get assets, purchase'
            },
            {
                'knowledge_type': 'faq',
                'question': 'How do I become a seller?',
                'answer': 'To become a seller: 1) Create an account or log in 2) Go to your profile 3) Click Become a Seller 4) Start uploading your assets 5) Set prices and descriptions 6) Submit for review',
                'keywords': 'seller, become seller, sell assets, upload'
            },
            {
                'knowledge_type': 'general',
                'question': 'What file formats do you support?',
                'answer': 'We support various file formats including: 3D Models (.fbx, .obj, .blend), Textures (.png, .jpg, .tga), Audio (.mp3, .wav, .ogg), and more. Check our guidelines for complete format list.',
                'keywords': 'formats, file types, supported formats, fbx, obj, png'
            }
        ]

        for item in knowledge_items:
            ChatbotKnowledge.objects.get_or_create(
                question=item['question'],
                defaults=item
            )

        self.stdout.write(self.style.SUCCESS('Chatbot knowledge created successfully!'))
        self.stdout.write(self.style.SUCCESS('Setup complete!'))