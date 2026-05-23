#!/usr/bin/env python
"""
Script to add dummy products and categories to the Ocean City Hemp Kiosk
"""

import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Category, Product

def create_dummy_categories():
    """Create 5 specific categories with emojis"""
    categories_data = [
        {"name": "Flowers", "emoji": "�", "description": "Premium cannabis flower strains"},
        {"name": "Pre-rolls", "emoji": "🚬", "description": "Convenient pre-rolled joints ready to enjoy"},
        {"name": "Vaporizers", "emoji": "💨", "description": "High-quality vape cartridges and pods"},
        {"name": "Concentrates", "emoji": "�", "description": "Premium cannabis concentrates and extracts"},
        {"name": "Edibles", "emoji": "🍭", "description": "Delicious cannabis-infused edibles and treats"}
    ]
    
    created_categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={
                "emoji": cat_data["emoji"],
                "description": cat_data["description"]
            }
        )
        created_categories.append(category)
        print(f"{'Created' if created else 'Found'} category: {category.name} {category.emoji}")
    
    return created_categories

def create_dummy_products(categories):
    """Create 5 products in each of the 5 categories (25 total)"""
    products_data = [
        # Flowers (5 products)
        {
            "name": "Purple Haze",
            "category": "Flowers",
            "description": "A classic indica strain with deep relaxing effects and a sweet berry aroma",
            "price": Decimal("45.00"),
            "thc_content": Decimal("22.5"),
            "cbd_content": Decimal("0.8"),
            "flower_type": "Indica",
            "weight": Decimal("3.5"),
            "is_available": True
        },
        {
            "name": "Green Crack",
            "category": "Flowers",
            "description": "An energizing sativa perfect for daytime use with citrusy flavors",
            "price": Decimal("42.00"),
            "thc_content": Decimal("18.2"),
            "cbd_content": Decimal("0.3"),
            "flower_type": "Sativa",
            "weight": Decimal("3.5"),
            "is_available": True
        },
        {
            "name": "Blue Dream",
            "category": "Flowers",
            "description": "A balanced hybrid offering both relaxation and euphoria",
            "price": Decimal("40.00"),
            "thc_content": Decimal("19.8"),
            "cbd_content": Decimal("1.2"),
            "flower_type": "Hybrid",
            "weight": Decimal("3.5"),
            "is_available": True
        },
        {
            "name": "OG Kush",
            "category": "Flowers",
            "description": "Classic strain with earthy pine flavors and strong relaxing effects",
            "price": Decimal("48.00"),
            "thc_content": Decimal("24.1"),
            "cbd_content": Decimal("0.5"),
            "flower_type": "Hybrid",
            "weight": Decimal("3.5"),
            "is_available": True
        },
        {
            "name": "Sour Diesel",
            "category": "Flowers",
            "description": "Energizing sativa with diesel aroma and uplifting effects",
            "price": Decimal("44.00"),
            "thc_content": Decimal("20.3"),
            "cbd_content": Decimal("0.7"),
            "flower_type": "Sativa",
            "weight": Decimal("3.5"),
            "is_available": True
        },
        
        # Pre-rolls (5 products)
        {
            "name": "Wedding Cake Pre-Roll",
            "category": "Pre-rolls",
            "description": "Single premium pre-roll featuring Wedding Cake strain",
            "price": Decimal("12.00"),
            "thc_content": Decimal("24.1"),
            "cbd_content": Decimal("0.6"),
            "flower_type": "Hybrid",
            "weight": Decimal("0.5"),
            "is_available": True
        },
        {
            "name": "Gelato Pre-Roll Pack",
            "category": "Pre-rolls",
            "description": "Pack of 3 premium pre-rolls featuring Gelato strain",
            "price": Decimal("35.00"),
            "thc_content": Decimal("21.5"),
            "cbd_content": Decimal("0.4"),
            "flower_type": "Hybrid",
            "weight": Decimal("1.5"),
            "is_available": True
        },
        {
            "name": "Jack Herer Pre-Roll",
            "category": "Pre-rolls",
            "description": "Energizing sativa pre-roll perfect for daytime use",
            "price": Decimal("10.00"),
            "thc_content": Decimal("18.7"),
            "cbd_content": Decimal("0.3"),
            "flower_type": "Sativa",
            "weight": Decimal("0.5"),
            "is_available": True
        },
        {
            "name": "Granddaddy Purple Pre-Roll",
            "category": "Pre-rolls",
            "description": "Relaxing indica pre-roll with grape flavors",
            "price": Decimal("11.00"),
            "thc_content": Decimal("23.2"),
            "cbd_content": Decimal("0.8"),
            "flower_type": "Indica",
            "weight": Decimal("0.5"),
            "is_available": True
        },
        {
            "name": "Mixed Strain 5-Pack",
            "category": "Pre-rolls",
            "description": "Variety pack of 5 different strain pre-rolls",
            "price": Decimal("50.00"),
            "thc_content": Decimal("20.0"),
            "cbd_content": Decimal("0.5"),
            "flower_type": "Hybrid",
            "weight": Decimal("2.5"),
            "is_available": True
        },
        
        # Vaporizers (5 products)
        {
            "name": "Live Resin Cart - OG Kush",
            "category": "Vaporizers",
            "description": "Premium live resin cartridge with authentic OG Kush flavor",
            "price": Decimal("65.00"),
            "thc_content": Decimal("85.0"),
            "cbd_content": Decimal("0.5"),
            "flower_type": "Hybrid",
            "weight": Decimal("1.0"),
            "is_available": True
        },
        {
            "name": "Distillate Cart - Blue Dream",
            "category": "Vaporizers",
            "description": "High-quality distillate cartridge with Blue Dream terpenes",
            "price": Decimal("45.00"),
            "thc_content": Decimal("88.5"),
            "cbd_content": Decimal("0.2"),
            "flower_type": "Hybrid",
            "weight": Decimal("1.0"),
            "is_available": True
        },
        {
            "name": "Full Spectrum Cart - Sour Diesel",
            "category": "Vaporizers",
            "description": "Full spectrum oil cartridge with natural Sour Diesel profile",
            "price": Decimal("55.00"),
            "thc_content": Decimal("78.3"),
            "cbd_content": Decimal("2.1"),
            "flower_type": "Sativa",
            "weight": Decimal("1.0"),
            "is_available": True
        },
        {
            "name": "Disposable Vape - Gelato",
            "category": "Vaporizers",
            "description": "Convenient disposable vape pen with Gelato strain",
            "price": Decimal("35.00"),
            "thc_content": Decimal("82.0"),
            "cbd_content": Decimal("0.3"),
            "flower_type": "Hybrid",
            "weight": Decimal("0.5"),
            "is_available": True
        },
        {
            "name": "CBD Cart - Charlotte's Web",
            "category": "Vaporizers",
            "description": "High-CBD cartridge with minimal THC for wellness",
            "price": Decimal("40.00"),
            "thc_content": Decimal("2.5"),
            "cbd_content": Decimal("75.0"),
            "flower_type": "High CBD",
            "weight": Decimal("1.0"),
            "is_available": True
        },
        
        # Concentrates (5 products)
        {
            "name": "Shatter - Gelato",
            "category": "Concentrates",
            "description": "Premium shatter with sweet gelato flavor profile",
            "price": Decimal("50.00"),
            "thc_content": Decimal("78.5"),
            "cbd_content": Decimal("0.2"),
            "flower_type": "Hybrid",
            "weight": Decimal("1.0"),
            "is_available": True
        },
        {
            "name": "Live Rosin - Wedding Cake",
            "category": "Concentrates",
            "description": "Solventless live rosin with rich terpene profile",
            "price": Decimal("80.00"),
            "thc_content": Decimal("72.8"),
            "cbd_content": Decimal("0.9"),
            "flower_type": "Hybrid",
            "weight": Decimal("1.0"),
            "is_available": True
        },
        {
            "name": "Wax - Purple Punch",
            "category": "Concentrates",
            "description": "Soft wax concentrate with grape and berry flavors",
            "price": Decimal("45.00"),
            "thc_content": Decimal("68.3"),
            "cbd_content": Decimal("0.6"),
            "flower_type": "Indica",
            "weight": Decimal("1.0"),
            "is_available": True
        },
        {
            "name": "Diamonds - MAC",
            "category": "Concentrates",
            "description": "THCA diamonds with intense potency and flavor",
            "price": Decimal("90.00"),
            "thc_content": Decimal("92.1"),
            "cbd_content": Decimal("0.1"),
            "flower_type": "Hybrid",
            "weight": Decimal("1.0"),
            "is_available": True
        },
        {
            "name": "Hash - Moroccan Style",
            "category": "Concentrates",
            "description": "Traditional hash with authentic flavors and effects",
            "price": Decimal("35.00"),
            "thc_content": Decimal("45.2"),
            "cbd_content": Decimal("1.8"),
            "flower_type": "Hybrid",
            "weight": Decimal("1.0"),
            "is_available": True
        },
        
        # Edibles (5 products)
        {
            "name": "Gummy Bears - Mixed Berry",
            "category": "Edibles",
            "description": "Delicious mixed berry gummies, 10mg THC each, 10 count",
            "price": Decimal("25.00"),
            "thc_content": Decimal("100.0"),
            "cbd_content": Decimal("0.0"),
            "flower_type": "Hybrid",
            "weight": Decimal("0.0"),
            "is_available": True
        },
        {
            "name": "Chocolate Bar - Dark Chocolate",
            "category": "Edibles",
            "description": "Premium dark chocolate bar with 100mg THC total",
            "price": Decimal("30.00"),
            "thc_content": Decimal("100.0"),
            "cbd_content": Decimal("0.0"),
            "flower_type": "Hybrid",
            "weight": Decimal("0.0"),
            "is_available": True
        },
        {
            "name": "Cookies - Snickerdoodle",
            "category": "Edibles",
            "description": "Homemade-style snickerdoodle cookies, 25mg THC each",
            "price": Decimal("15.00"),
            "thc_content": Decimal("25.0"),
            "cbd_content": Decimal("0.0"),
            "flower_type": "Hybrid",
            "weight": Decimal("0.0"),
            "is_available": True
        },
        {
            "name": "Mints - Peppermint",
            "category": "Edibles",
            "description": "Refreshing peppermint mints, 5mg THC each, 20 count",
            "price": Decimal("20.00"),
            "thc_content": Decimal("100.0"),
            "cbd_content": Decimal("0.0"),
            "flower_type": "Hybrid",
            "weight": Decimal("0.0"),
            "is_available": True
        },
        {
            "name": "Drink Mix - Lemonade",
            "category": "Edibles",
            "description": "Cannabis-infused lemonade drink mix, 50mg THC per packet",
            "price": Decimal("18.00"),
            "thc_content": Decimal("50.0"),
            "cbd_content": Decimal("0.0"),
            "flower_type": "Hybrid",
            "weight": Decimal("0.0"),
            "is_available": True
        }
    ]
    
    # Create a lookup dictionary for categories
    category_lookup = {cat.name: cat for cat in categories}
    
    created_products = []
    for prod_data in products_data:
        category = category_lookup.get(prod_data["category"])
        if not category:
            print(f"Warning: Category '{prod_data['category']}' not found for product '{prod_data['name']}'")
            continue
        
        product, created = Product.objects.get_or_create(
            name=prod_data["name"],
            defaults={
                "category": category,
                "description": prod_data["description"],
                "price": prod_data["price"],
                "thc_content": prod_data["thc_content"],
                "cbd_content": prod_data["cbd_content"],
                "flower_type": prod_data["flower_type"],
                "weight": prod_data["weight"],
                "is_available": prod_data["is_available"]
            }
        )
        created_products.append(product)
        print(f"{'Created' if created else 'Found'} product: {product.name} - ${product.price}")
    
    return created_products

def main():
    print("🌿 Adding dummy data to Ocean City Hemp Kiosk")
    print("=" * 50)
    
    # Create categories
    print("\n📁 Creating categories...")
    categories = create_dummy_categories()
    
    # Create products
    print("\n🛍️ Creating products...")
    products = create_dummy_products(categories)
    
    print("\n✅ Dummy data creation complete!")
    print(f"   Categories created: {len(categories)}")
    print(f"   Products created: {len(products)}")
    print("\n📊 Product breakdown:")
    print("   • Flowers: 5 products")
    print("   • Pre-rolls: 5 products") 
    print("   • Vaporizers: 5 products")
    print("   • Concentrates: 5 products")
    print("   • Edibles: 5 products")
    print("\nYou can now view the products in:")
    print("   • Kiosk interface: http://localhost:8000/")
    print("   • Admin panel: http://localhost:8000/admin/")

if __name__ == "__main__":
    main()
