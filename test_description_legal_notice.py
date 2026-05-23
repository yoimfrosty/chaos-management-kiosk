#!/usr/bin/env python3
"""
Test script to verify the product description and legal notice functionality.
"""

import os
import sys
import django

# Add project root to Python path
sys.path.append('/Users/darshan/Desktop/chaos-magement')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Product, Category

def test_product_description_and_legal_notice():
    """Test the product description and legal notice functionality"""
    
    print("🧪 Testing Product Description and Legal Notice Functionality")
    print("=" * 60)
    
    # Test 1: Check database schema
    print("\n1. Checking Database Schema:")
    try:
        # Check if legal_notice field exists
        product = Product.objects.first()
        if product:
            print(f"   ✅ Product model has legal_notice field: {hasattr(product, 'legal_notice')}")
            print(f"   ✅ Sample product description: '{product.description[:50]}...'")
            print(f"   ✅ Sample legal notice: '{product.legal_notice[:50] if product.legal_notice else 'None'}...'")
        else:
            print("   ❌ No products found in database")
    except Exception as e:
        print(f"   ❌ Error checking schema: {e}")
    
    # Test 2: Check product distribution
    print("\n2. Product Distribution:")
    try:
        total_products = Product.objects.count()
        products_with_legal_notice = Product.objects.exclude(legal_notice__isnull=True).exclude(legal_notice='').count()
        
        print(f"   📊 Total products: {total_products}")
        print(f"   📊 Products with legal notice: {products_with_legal_notice}")
        print(f"   📊 Products without legal notice: {total_products - products_with_legal_notice}")
        
        if products_with_legal_notice > 0:
            print(f"   ✅ {(products_with_legal_notice/total_products*100):.1f}% of products have legal notices")
        else:
            print("   ⚠️  No products have legal notices yet")
            
    except Exception as e:
        print(f"   ❌ Error checking distribution: {e}")
    
    # Test 3: Show sample products
    print("\n3. Sample Products:")
    try:
        sample_products = Product.objects.all()[:5]
        for i, product in enumerate(sample_products, 1):
            print(f"   {i}. {product.name}")
            print(f"      Description: {product.description[:60]}...")
            if product.legal_notice:
                print(f"      Legal Notice: {product.legal_notice[:60]}...")
            else:
                print(f"      Legal Notice: None")
            print()
    except Exception as e:
        print(f"   ❌ Error showing samples: {e}")
    
    # Test 4: Check categories
    print("\n4. Categories with Products:")
    try:
        categories = Category.objects.all()
        for category in categories:
            product_count = category.products.count()
            products_with_notice = category.products.exclude(legal_notice__isnull=True).exclude(legal_notice='').count()
            icon = getattr(category, 'icon', '📦')  # Use default icon if not found
            print(f"   {icon} {category.name}: {product_count} products, {products_with_notice} with legal notices")
    except Exception as e:
        print(f"   ❌ Error checking categories: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Test completed! Check the web interface at http://127.0.0.1:8000/products/")
    print("💡 Click on the info (ℹ️) icon on any product to see the description and legal notice boxes")

if __name__ == "__main__":
    test_product_description_and_legal_notice()
