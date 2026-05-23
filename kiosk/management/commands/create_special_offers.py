from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from kiosk.models import SpecialOffer, Product, Category
import random


class Command(BaseCommand):
    help = 'Create sample special offers for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample special offers...')
        
        # Clear existing special offers
        SpecialOffer.objects.all().delete()
        
        # Get some products and categories
        products = list(Product.objects.all()[:5])
        categories = list(Category.objects.all()[:3])
        
        # Create special offers
        special_offers = [
            {
                'title': '🌟 Weekend Special - 20% Off All Flower',
                'description': 'Get 20% off all flower products this weekend! Perfect time to try our premium strains.',
                'discount_type': 'Percentage',
                'discount_value': 20.00,
                'start_date': timezone.now() - timedelta(days=1),
                'end_date': timezone.now() + timedelta(days=2),
                'applicable_categories': [cat for cat in categories if 'flower' in cat.name.lower()][:1],
                'minimum_spend': None,
            },
            {
                'title': '🔥 Flash Sale - $15 Off Orders Over $100',
                'description': 'Limited time offer! Save $15 on any order over $100. No code needed.',
                'discount_type': 'Fixed Amount Off Total',
                'discount_value': 15.00,
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(hours=6),
                'applicable_categories': [],
                'minimum_spend': 100.00,
            },
            {
                'title': '🌿 New Customer Special - $10 Off First Purchase',
                'description': 'Welcome to Ocean City Hemp! Enjoy $10 off your first purchase with us.',
                'discount_type': 'Fixed Amount Off Total',
                'discount_value': 10.00,
                'start_date': timezone.now() - timedelta(days=7),
                'end_date': timezone.now() + timedelta(days=30),
                'applicable_categories': [],
                'minimum_spend': 50.00,
            },
            {
                'title': '💎 Premium Product Discount - 15% Off Select Items',
                'description': 'Save 15% on our premium selection of top-shelf products.',
                'discount_type': 'Percentage',
                'discount_value': 15.00,
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=7),
                'applicable_products': products[:3] if products else [],
                'minimum_spend': None,
            },
            {
                'title': '🎉 Happy Hour - 25% Off Edibles (3-6 PM)',
                'description': 'Join us for happy hour! Get 25% off all edibles between 3 PM and 6 PM daily.',
                'discount_type': 'Percentage',
                'discount_value': 25.00,
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=14),
                'applicable_categories': [cat for cat in categories if 'edible' in cat.name.lower()][:1],
                'minimum_spend': None,
            },
        ]
        
        created_count = 0
        for offer_data in special_offers:
            # Extract many-to-many fields
            applicable_products = offer_data.pop('applicable_products', [])
            applicable_categories = offer_data.pop('applicable_categories', [])
            
            # Create the offer
            offer = SpecialOffer.objects.create(**offer_data)
            
            # Set many-to-many relationships
            if applicable_products:
                offer.applicable_products.set(applicable_products)
            if applicable_categories:
                offer.applicable_categories.set(applicable_categories)
            
            created_count += 1
            self.stdout.write(f'✔ Created special offer: {offer.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} special offers!')
        )
        
        # Show active offers
        active_offers = SpecialOffer.objects.filter(is_active=True)
        currently_active = [offer for offer in active_offers if offer.is_currently_active()]
        
        self.stdout.write(f'\n📊 Status:')
        self.stdout.write(f'   Total offers: {active_offers.count()}')
        self.stdout.write(f'   Currently active: {len(currently_active)}')
        self.stdout.write(f'   Available for display: {len(currently_active)}')
