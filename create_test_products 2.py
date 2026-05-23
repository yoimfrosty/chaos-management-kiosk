#!/usr/bin/env python3
"""
Ocean City Hemp Kiosk - Test Data Creator
Creates realistic cannabis dispensary products and categories for testing
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Category, Product, SpecialOffer

def create_categories():
    """Create product categories"""
    categories_data = [
        {
            'name': 'Flower',
            'emoji': '🌿',
            'description': 'Premium cannabis flower products including indica, sativa, and hybrid strains.'
        },
        {
            'name': 'Edibles',
            'emoji': '🍫',
            'description': 'Cannabis-infused edibles including gummies, chocolates, and baked goods.'
        },
        {
            'name': 'Pre-rolls',
            'emoji': '🚬',
            'description': 'Pre-rolled joints and blunts ready to enjoy.'
        },
        {
            'name': 'Concentrates',
            'emoji': '💎',
            'description': 'High-potency cannabis concentrates, wax, shatter, and oils.'
        },
        {
            'name': 'Accessories',
            'emoji': '🔥',
            'description': 'Cannabis accessories including pipes, papers, lighters, and storage.'
        },
        {
            'name': 'Vapes',
            'emoji': '💨',
            'description': 'Vape cartridges, disposables, and vaping devices.'
        },
    ]
    
    created_categories = {}
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'emoji': cat_data['emoji'],
                'description': cat_data['description']
            }
        )
        created_categories[cat_data['name']] = category
        print(f"{'✅ Created' if created else '📋 Found'} category: {category.name} {category.emoji}")
    
    return created_categories

def create_flower_products(flower_category):
    """Create flower products"""
    flower_products = [
        {
            'name': 'Ocean City OG',
            'description': 'A classic OG strain with earthy pine flavors and relaxing effects. Perfect for evening use.',
            'price': Decimal('45.00'),
            'thc_content': Decimal('24.5'),
            'cbd_content': Decimal('0.8'),
            'flower_type': 'Indica'
        },
        {
            'name': 'Sunset Sherbet',
            'description': 'Sweet and fruity hybrid with beautiful purple hues. Balanced effects for any time of day.',
            'price': Decimal('48.00'),
            'thc_content': Decimal('22.3'),
            'cbd_content': Decimal('1.2'),
            'flower_type': 'Hybrid'
        },
        {
            'name': 'Green Crack',
            'description': 'Energizing sativa perfect for daytime use. Citrusy aroma with uplifting effects.',
            'price': Decimal('42.00'),
            'thc_content': Decimal('21.8'),
            'cbd_content': Decimal('0.5'),
            'flower_type': 'Sativa'
        },
        {
            'name': 'Purple Punch',
            'description': 'Indica-dominant strain with grape and berry flavors. Great for relaxation and sleep.',
            'price': Decimal('46.00'),
            'thc_content': Decimal('23.7'),
            'cbd_content': Decimal('0.9'),
            'flower_type': 'Indica'
        },
        {
            'name': 'Jack Herer',
            'description': 'Classic sativa named after the cannabis activist. Clear-headed and creative effects.',
            'price': Decimal('44.00'),
            'thc_content': Decimal('20.5'),
            'cbd_content': Decimal('0.7'),
            'flower_type': 'Sativa'
        },
        {
            'name': 'Wedding Cake',
            'description': 'Popular hybrid with vanilla and cake-like flavors. Relaxing but not overwhelming.',
            'price': Decimal('50.00'),
            'thc_content': Decimal('25.2'),
            'cbd_content': Decimal('1.1'),
            'flower_type': 'Hybrid'
        },
        {
            'name': 'Blue Dream',
            'description': 'Well-balanced hybrid perfect for beginners. Sweet berry aroma with gentle effects.',
            'price': Decimal('40.00'),
            'thc_content': Decimal('19.8'),
            'cbd_content': Decimal('1.5'),
            'flower_type': 'Hybrid'
        },
        {
            'name': 'Charlotte\'s Web',
            'description': 'High-CBD strain with minimal psychoactive effects. Great for therapeutic use.',
            'price': Decimal('38.00'),
            'thc_content': Decimal('0.9'),
            'cbd_content': Decimal('18.5'),
            'flower_type': 'High CBD'
        }
    ]
    
    created_products = []
    for product_data in flower_products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': flower_category,
                'description': product_data['description'],
                'price': product_data['price'],
                'thc_content': product_data['thc_content'],
                'cbd_content': product_data['cbd_content'],
                'flower_type': product_data['flower_type'],
                'is_available': True
            }
        )
        created_products.append(product)
        print(f"{'✅ Created' if created else '📋 Found'} flower: {product.name} ({product.flower_type}) - ${product.price}")
    
    return created_products

def create_edible_products(edibles_category):
    """Create edible products"""
    edible_products = [
        {
            'name': 'Mixed Berry Gummies - 10mg',
            'description': 'Delicious mixed berry gummies with 10mg THC each. Perfect for microdosing.',
            'price': Decimal('25.00'),
            'thc_content': Decimal('10.0'),
            'cbd_content': Decimal('0.0')
        },
        {
            'name': 'Dark Chocolate Bar - 100mg',
            'description': 'Premium dark chocolate infused with 100mg THC. Break into 10mg pieces.',
            'price': Decimal('35.00'),
            'thc_content': Decimal('100.0'),
            'cbd_content': Decimal('0.0')
        },
        {
            'name': 'Peach Rings - 5mg',
            'description': 'Sweet peach ring gummies with 5mg THC each. Great for beginners.',
            'price': Decimal('20.00'),
            'thc_content': Decimal('5.0'),
            'cbd_content': Decimal('0.0')
        },
        {
            'name': 'CBD:THC Gummies 1:1 - 10mg',
            'description': 'Balanced CBD and THC gummies with 10mg of each cannabinoid.',
            'price': Decimal('30.00'),
            'thc_content': Decimal('10.0'),
            'cbd_content': Decimal('10.0')
        },
        {
            'name': 'Brownies - 25mg',
            'description': 'Classic cannabis brownies with 25mg THC each. Rich chocolate flavor.',
            'price': Decimal('15.00'),
            'thc_content': Decimal('25.0'),
            'cbd_content': Decimal('0.0')
        },
        {
            'name': 'Sour Worms - 10mg',
            'description': 'Sour gummy worms with 10mg THC each. Tropical fruit flavors.',
            'price': Decimal('28.00'),
            'thc_content': Decimal('10.0'),
            'cbd_content': Decimal('0.0')
        }
    ]
    
    created_products = []
    for product_data in edible_products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': edibles_category,
                'description': product_data['description'],
                'price': product_data['price'],
                'thc_content': product_data['thc_content'],
                'cbd_content': product_data['cbd_content'],
                'is_available': True
            }
        )
        created_products.append(product)
        print(f"{'✅ Created' if created else '📋 Found'} edible: {product.name} - ${product.price}")
    
    return created_products

def create_preroll_products(prerolls_category):
    """Create pre-roll products"""
    preroll_products = [
        {
            'name': 'Ocean OG Pre-roll - 1g',
            'description': 'Single gram pre-roll of our signature Ocean OG strain.',
            'price': Decimal('12.00'),
            'thc_content': Decimal('24.5'),
            'cbd_content': Decimal('0.8'),
            'flower_type': 'Indica'
        },
        {
            'name': 'Sativa Blend 3-Pack',
            'description': 'Three 0.5g pre-rolls of premium sativa strains.',
            'price': Decimal('25.00'),
            'thc_content': Decimal('21.0'),
            'cbd_content': Decimal('0.6'),
            'flower_type': 'Sativa'
        },
        {
            'name': 'Hybrid Mix 5-Pack',
            'description': 'Five 0.5g pre-rolls featuring different hybrid strains.',
            'price': Decimal('40.00'),
            'thc_content': Decimal('22.5'),
            'cbd_content': Decimal('1.0'),
            'flower_type': 'Hybrid'
        },
        {
            'name': 'Infused Blunt - Wedding Cake',
            'description': 'Premium blunt infused with kief and concentrate. 2g total.',
            'price': Decimal('35.00'),
            'thc_content': Decimal('35.8'),
            'cbd_content': Decimal('1.2'),
            'flower_type': 'Hybrid'
        }
    ]
    
    created_products = []
    for product_data in preroll_products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': prerolls_category,
                'description': product_data['description'],
                'price': product_data['price'],
                'thc_content': product_data['thc_content'],
                'cbd_content': product_data['cbd_content'],
                'flower_type': product_data['flower_type'],
                'is_available': True
            }
        )
        created_products.append(product)
        print(f"{'✅ Created' if created else '📋 Found'} pre-roll: {product.name} - ${product.price}")
    
    return created_products

def create_concentrate_products(concentrates_category):
    """Create concentrate products"""
    concentrate_products = [
        {
            'name': 'Live Resin - Blue Dream',
            'description': 'Premium live resin with full terpene profile. 1g container.',
            'price': Decimal('60.00'),
            'thc_content': Decimal('78.5'),
            'cbd_content': Decimal('1.2'),
            'flower_type': 'Hybrid'
        },
        {
            'name': 'Shatter - Green Crack',
            'description': 'Glass-like shatter concentrate. Easy to handle and dose.',
            'price': Decimal('45.00'),
            'thc_content': Decimal('82.3'),
            'cbd_content': Decimal('0.5'),
            'flower_type': 'Sativa'
        },
        {
            'name': 'Rosin - Purple Punch',
            'description': 'Solventless rosin extracted using heat and pressure.',
            'price': Decimal('70.00'),
            'thc_content': Decimal('75.8'),
            'cbd_content': Decimal('1.8'),
            'flower_type': 'Indica'
        },
        {
            'name': 'Hash - Traditional Moroccan',
            'description': 'Traditional hash made from premium flower. Rich flavor.',
            'price': Decimal('55.00'),
            'thc_content': Decimal('65.2'),
            'cbd_content': Decimal('2.1'),
            'flower_type': 'Hybrid'
        }
    ]
    
    created_products = []
    for product_data in concentrate_products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': concentrates_category,
                'description': product_data['description'],
                'price': product_data['price'],
                'thc_content': product_data['thc_content'],
                'cbd_content': product_data['cbd_content'],
                'flower_type': product_data['flower_type'],
                'is_available': True
            }
        )
        created_products.append(product)
        print(f"{'✅ Created' if created else '📋 Found'} concentrate: {product.name} - ${product.price}")
    
    return created_products

def create_vape_products(vapes_category):
    """Create vape products"""
    vape_products = [
        {
            'name': 'Sativa Cart - Jack Herer',
            'description': '0.5g vape cartridge with Jack Herer distillate and natural terpenes.',
            'price': Decimal('35.00'),
            'thc_content': Decimal('88.5'),
            'cbd_content': Decimal('0.3'),
            'flower_type': 'Sativa'
        },
        {
            'name': 'Indica Cart - Granddaddy Purple',
            'description': '0.5g vape cartridge perfect for evening relaxation.',
            'price': Decimal('35.00'),
            'thc_content': Decimal('86.2'),
            'cbd_content': Decimal('0.8'),
            'flower_type': 'Indica'
        },
        {
            'name': 'Hybrid Cart - Wedding Cake',
            'description': '0.5g balanced hybrid cartridge with sweet vanilla notes.',
            'price': Decimal('35.00'),
            'thc_content': Decimal('87.8'),
            'cbd_content': Decimal('0.5'),
            'flower_type': 'Hybrid'
        },
        {
            'name': 'CBD Cart - Charlotte\'s Web',
            'description': '0.5g high-CBD cartridge with minimal psychoactive effects.',
            'price': Decimal('30.00'),
            'thc_content': Decimal('2.1'),
            'cbd_content': Decimal('85.4'),
            'flower_type': 'High CBD'
        },
        {
            'name': 'Disposable Vape - Blue Dream',
            'description': 'Convenient disposable vape pen with 0.3g of premium oil.',
            'price': Decimal('25.00'),
            'thc_content': Decimal('84.7'),
            'cbd_content': Decimal('0.9'),
            'flower_type': 'Hybrid'
        }
    ]
    
    created_products = []
    for product_data in vape_products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': vapes_category,
                'description': product_data['description'],
                'price': product_data['price'],
                'thc_content': product_data['thc_content'],
                'cbd_content': product_data['cbd_content'],
                'flower_type': product_data['flower_type'],
                'is_available': True
            }
        )
        created_products.append(product)
        print(f"{'✅ Created' if created else '📋 Found'} vape: {product.name} - ${product.price}")
    
    return created_products

def create_accessory_products(accessories_category):
    """Create accessory products"""
    accessory_products = [
        {
            'name': 'Glass Pipe - Ocean Blue',
            'description': 'Beautiful hand-blown glass pipe with ocean blue coloring.',
            'price': Decimal('25.00')
        },
        {
            'name': 'Rolling Papers - King Size',
            'description': 'Premium king size rolling papers. 32 papers per pack.',
            'price': Decimal('8.00')
        },
        {
            'name': 'Grinder - 4 Piece Aluminum',
            'description': 'High-quality aluminum grinder with pollen catcher.',
            'price': Decimal('35.00')
        },
        {
            'name': 'Storage Jar - Airtight Glass',
            'description': 'UV-resistant glass storage jar to keep your products fresh.',
            'price': Decimal('20.00')
        },
        {
            'name': 'Hemp Wick - Natural',
            'description': 'Natural hemp wick for clean, butane-free lighting.',
            'price': Decimal('12.00')
        },
        {
            'name': 'Lighter - Ocean City Hemp',
            'description': 'Custom Ocean City Hemp branded lighter.',
            'price': Decimal('5.00')
        },
        {
            'name': 'Rolling Tray - Bamboo',
            'description': 'Eco-friendly bamboo rolling tray with curved edges.',
            'price': Decimal('18.00')
        }
    ]
    
    created_products = []
    for product_data in accessory_products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': accessories_category,
                'description': product_data['description'],
                'price': product_data['price'],
                'is_available': True
            }
        )
        created_products.append(product)
        print(f"{'✅ Created' if created else '📋 Found'} accessory: {product.name} - ${product.price}")
    
    return created_products

def create_special_offers(products):
    """Create special offers and discounts"""
    offers_data = [
        {
            'title': 'Buy 2 Get 1 Half Off',
            'description': 'Buy any 2 flower products and get the 3rd at 50% off!',
            'discount_type': 'Percentage',
            'discount_value': Decimal('50.00'),
            'minimum_quantity': 3,
            'offer_display_text': 'Buy 2 Get 1 Half Off!',
            'category_name': 'Flower'
        },
        {
            'title': 'Edibles 3-Pack Special',
            'description': 'Buy 3 or more edible products and save 15%',
            'discount_type': 'Percentage',
            'discount_value': Decimal('15.00'),
            'minimum_quantity': 3,
            'offer_display_text': 'Buy 3+ Save 15%!',
            'category_name': 'Edibles'
        },
        {
            'title': 'New Customer Discount',
            'description': '$10 off your first order of $50 or more',
            'discount_type': 'Fixed Amount Off Total',
            'discount_value': Decimal('10.00'),
            'minimum_spend': Decimal('50.00'),
            'offer_display_text': '$10 off $50+ for new customers!'
        },
        {
            'title': 'Pre-roll Bundle Deal',
            'description': 'Mix and match any 5 pre-rolls for $50',
            'discount_type': 'Fixed Amount',
            'discount_value': Decimal('10.00'),
            'minimum_quantity': 5,
            'offer_display_text': 'Mix & Match 5 for $50!',
            'category_name': 'Pre-rolls'
        }
    ]
    
    created_offers = []
    for offer_data in offers_data:
        offer, created = SpecialOffer.objects.get_or_create(
            title=offer_data['title'],
            defaults={
                'description': offer_data['description'],
                'discount_type': offer_data['discount_type'],
                'discount_value': offer_data['discount_value'],
                'minimum_quantity': offer_data.get('minimum_quantity'),
                'minimum_spend': offer_data.get('minimum_spend'),
                'offer_display_text': offer_data['offer_display_text'],
                'is_active': True
            }
        )
        
        # Add applicable categories if specified
        if 'category_name' in offer_data:
            try:
                category = Category.objects.get(name=offer_data['category_name'])
                offer.applicable_categories.add(category)
            except Category.DoesNotExist:
                pass
        
        created_offers.append(offer)
        print(f"{'✅ Created' if created else '📋 Found'} offer: {offer.title}")
    
    return created_offers

def main():
    """Main function to create all test data"""
    print("🌿 Ocean City Hemp Kiosk - Creating Test Data")
    print("=" * 60)
    
    # Create categories
    print("\n📂 Creating Categories...")
    categories = create_categories()
    
    # Create products by category
    all_products = []
    
    print("\n🌸 Creating Flower Products...")
    flower_products = create_flower_products(categories['Flower'])
    all_products.extend(flower_products)
    
    print("\n🍯 Creating Edible Products...")
    edible_products = create_edible_products(categories['Edibles'])
    all_products.extend(edible_products)
    
    print("\n🚬 Creating Pre-roll Products...")
    preroll_products = create_preroll_products(categories['Pre-rolls'])
    all_products.extend(preroll_products)
    
    print("\n💎 Creating Concentrate Products...")
    concentrate_products = create_concentrate_products(categories['Concentrates'])
    all_products.extend(concentrate_products)
    
    print("\n💨 Creating Vape Products...")
    vape_products = create_vape_products(categories['Vapes'])
    all_products.extend(vape_products)
    
    print("\n🔥 Creating Accessory Products...")
    accessory_products = create_accessory_products(categories['Accessories'])
    all_products.extend(accessory_products)
    
    print("\n🎯 Creating Special Offers...")
    offers = create_special_offers(all_products)
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Test Data Creation Complete!")
    print(f"✅ Categories: {Category.objects.count()}")
    print(f"✅ Products: {Product.objects.count()}")
    print(f"✅ Special Offers: {SpecialOffer.objects.count()}")
    
    print("\n📊 Products by Category:")
    for category in Category.objects.all():
        count = category.products.count()
        print(f"  {category.emoji} {category.name}: {count} products")
    
    print(f"\n🌐 View your products at: http://127.0.0.1:8000/products/")
    print("🚀 Your kiosk is ready for testing!")

if __name__ == "__main__":
    main()
