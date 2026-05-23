#!/usr/bin/env python3
"""
Test Products Verification Script
Verifies that the test products and categories were created successfully
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Category, Product, SpecialOffer

def verify_test_data():
    """Verify that test data was created successfully"""
    print("🧪 Verifying Test Products and Categories")
    print("=" * 60)
    
    # Check categories
    categories = Category.objects.all()
    print(f"\n📂 Categories ({categories.count()}):")
    for category in categories:
        product_count = category.products.count()
        print(f"  {category.emoji} {category.name}: {product_count} products")
        
        # Show some sample products from each category
        sample_products = category.products.all()[:3]
        for product in sample_products:
            thc_cbd = ""
            if product.thc_content:
                thc_cbd += f"THC: {product.thc_content}%"
            if product.cbd_content:
                if thc_cbd:
                    thc_cbd += f", CBD: {product.cbd_content}%"
                else:
                    thc_cbd += f"CBD: {product.cbd_content}%"
            
            flower_type = f" ({product.flower_type})" if product.flower_type else ""
            thc_cbd_display = f" [{thc_cbd}]" if thc_cbd else ""
            
            print(f"    • {product.name}{flower_type} - ${product.price}{thc_cbd_display}")
        
        if category.products.count() > 3:
            print(f"    ... and {category.products.count() - 3} more")
        print()
    
    # Check special offers
    offers = SpecialOffer.objects.all()
    print(f"🎯 Special Offers ({offers.count()}):")
    for offer in offers:
        applicable_to = []
        if offer.applicable_categories.exists():
            cat_names = [cat.name for cat in offer.applicable_categories.all()]
            applicable_to.append(f"Categories: {', '.join(cat_names)}")
        if offer.applicable_products.exists():
            applicable_to.append(f"Products: {offer.applicable_products.count()}")
        if not applicable_to:
            applicable_to.append("All products")
        
        conditions = []
        if offer.minimum_quantity:
            conditions.append(f"Min qty: {offer.minimum_quantity}")
        if offer.minimum_spend:
            conditions.append(f"Min spend: ${offer.minimum_spend}")
        
        condition_text = f" ({', '.join(conditions)})" if conditions else ""
        applicable_text = f" - {', '.join(applicable_to)}"
        
        print(f"  • {offer.title}: {offer.discount_value}% off{condition_text}{applicable_text}")
        if offer.offer_display_text:
            print(f"    Display: \"{offer.offer_display_text}\"")
    
    # Price range analysis
    print(f"\n💰 Price Analysis:")
    all_products = Product.objects.all()
    if all_products:
        prices = [float(p.price) for p in all_products]
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
        
        print(f"  Price range: ${min_price:.2f} - ${max_price:.2f}")
        print(f"  Average price: ${avg_price:.2f}")
        
        # Price breakdown by category
        print(f"\n  Price ranges by category:")
        for category in categories:
            cat_products = category.products.all()
            if cat_products:
                cat_prices = [float(p.price) for p in cat_products]
                cat_min = min(cat_prices)
                cat_max = max(cat_prices)
                cat_avg = sum(cat_prices) / len(cat_prices)
                print(f"    {category.emoji} {category.name}: ${cat_min:.2f} - ${cat_max:.2f} (avg: ${cat_avg:.2f})")
    
    # THC/CBD analysis for cannabis products
    print(f"\n🧪 Cannabinoid Analysis:")
    cannabis_products = Product.objects.filter(thc_content__isnull=False)
    if cannabis_products:
        thc_values = [float(p.thc_content) for p in cannabis_products if p.thc_content]
        cbd_values = [float(p.cbd_content) for p in cannabis_products if p.cbd_content and p.cbd_content > 0]
        
        if thc_values:
            print(f"  THC range: {min(thc_values):.1f}% - {max(thc_values):.1f}%")
            print(f"  Average THC: {sum(thc_values)/len(thc_values):.1f}%")
        
        if cbd_values:
            print(f"  CBD range: {min(cbd_values):.1f}% - {max(cbd_values):.1f}%")
            print(f"  Average CBD: {sum(cbd_values)/len(cbd_values):.1f}%")
        
        # High CBD products
        high_cbd = Product.objects.filter(cbd_content__gte=10)
        if high_cbd:
            print(f"  High-CBD products ({high_cbd.count()}):")
            for product in high_cbd:
                print(f"    • {product.name}: THC {product.thc_content}%, CBD {product.cbd_content}%")
    
    print(f"\n" + "=" * 60)
    print("✅ Test data verification complete!")
    print(f"📊 Total: {Category.objects.count()} categories, {Product.objects.count()} products, {SpecialOffer.objects.count()} offers")
    print("🌐 Ready to test at: http://127.0.0.1:8000/products/")

if __name__ == "__main__":
    verify_test_data()
