from django.core.management.base import BaseCommand
from kiosk.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate the database with sample categories and products'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample categories and products...')

        # Create Categories
        categories_data = [
            {
                'name': 'Flower',
                'description': 'Premium cannabis flower in various strains and potencies'
            },
            {
                'name': 'Edibles',
                'description': 'Delicious cannabis-infused edibles including gummies, chocolates, and more'
            },
            {
                'name': 'Concentrates',
                'description': 'High-potency cannabis concentrates and extracts'
            },
            {
                'name': 'Vapes',
                'description': 'Convenient vape cartridges and disposables'
            },
            {
                'name': 'Topicals',
                'description': 'Cannabis-infused creams, balms, and lotions'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description']
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create Products
        products_data = [
            # Flower
            {
                'name': 'Purple Haze',
                'category': 'Flower',
                'description': 'Classic Sativa strain with uplifting effects and berry flavors',
                'price': Decimal('45.00'),
                'thc_content': Decimal('22.5'),
                'cbd_content': Decimal('0.8'),
                'flower_type': 'Sativa'
            },
            {
                'name': 'OG Kush',
                'category': 'Flower',
                'description': 'Legendary Indica-dominant hybrid with earthy pine aromas',
                'price': Decimal('50.00'),
                'thc_content': Decimal('24.2'),
                'cbd_content': Decimal('0.5'),
                'flower_type': 'Hybrid'
            },
            {
                'name': 'Granddaddy Purple',
                'category': 'Flower',
                'description': 'Heavy Indica strain perfect for relaxation and sleep',
                'price': Decimal('48.00'),
                'thc_content': Decimal('20.8'),
                'cbd_content': Decimal('0.3'),
                'flower_type': 'Indica'
            },
            {
                'name': 'ACDC',
                'category': 'Flower',
                'description': 'High-CBD strain with minimal psychoactive effects',
                'price': Decimal('40.00'),
                'thc_content': Decimal('1.2'),
                'cbd_content': Decimal('18.5'),
                'flower_type': 'High CBD'
            },

            # Edibles
            {
                'name': 'Mixed Berry Gummies',
                'category': 'Edibles',
                'description': 'Delicious fruit gummies with 10mg THC each, 10-pack',
                'price': Decimal('25.00'),
                'thc_content': Decimal('10.0'),
                'cbd_content': Decimal('0.0'),
                'flower_type': None
            },
            {
                'name': 'Dark Chocolate Bar',
                'category': 'Edibles',
                'description': 'Premium Belgian chocolate infused with 100mg THC',
                'price': Decimal('30.00'),
                'thc_content': Decimal('100.0'),
                'cbd_content': Decimal('0.0'),
                'flower_type': None
            },
            {
                'name': 'CBD Sleep Gummies',
                'category': 'Edibles',
                'description': 'Melatonin and CBD gummies for better sleep, 5mg CBD each',
                'price': Decimal('28.00'),
                'thc_content': Decimal('0.0'),
                'cbd_content': Decimal('5.0'),
                'flower_type': None
            },

            # Concentrates
            {
                'name': 'Live Resin - Gelato',
                'category': 'Concentrates',
                'description': 'Premium live resin with incredible flavor and potency',
                'price': Decimal('65.00'),
                'thc_content': Decimal('78.5'),
                'cbd_content': Decimal('0.2'),
                'flower_type': 'Hybrid'
            },
            {
                'name': 'Shatter - Blue Dream',
                'category': 'Concentrates',
                'description': 'High-quality shatter with smooth, clear consistency',
                'price': Decimal('55.00'),
                'thc_content': Decimal('82.3'),
                'cbd_content': Decimal('0.1'),
                'flower_type': 'Hybrid'
            },

            # Vapes
            {
                'name': 'Sativa Blend Cart',
                'category': 'Vapes',
                'description': 'Energizing sativa blend in a 1g cartridge',
                'price': Decimal('60.00'),
                'thc_content': Decimal('85.2'),
                'cbd_content': Decimal('1.5'),
                'flower_type': 'Sativa'
            },
            {
                'name': 'Indica Disposable',
                'category': 'Vapes',
                'description': 'Convenient disposable vape pen, 0.5g capacity',
                'price': Decimal('35.00'),
                'thc_content': Decimal('80.8'),
                'cbd_content': Decimal('2.1'),
                'flower_type': 'Indica'
            },

            # Topicals
            {
                'name': 'Pain Relief Balm',
                'category': 'Topicals',
                'description': 'Soothing balm with 200mg CBD for localized relief',
                'price': Decimal('42.00'),
                'thc_content': Decimal('0.0'),
                'cbd_content': Decimal('200.0'),
                'flower_type': None
            },
            {
                'name': 'Recovery Cream',
                'category': 'Topicals',
                'description': 'Full-spectrum cream with THC and CBD for muscle recovery',
                'price': Decimal('38.00'),
                'thc_content': Decimal('50.0'),
                'cbd_content': Decimal('150.0'),
                'flower_type': None
            }
        ]

        for product_data in products_data:
            category = categories[product_data['category']]
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'category': category,
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'thc_content': product_data['thc_content'],
                    'cbd_content': product_data['cbd_content'],
                    'flower_type': product_data['flower_type']
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {Category.objects.count()} categories and {Product.objects.count()} products'
            )
        )
