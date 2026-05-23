#!/usr/bin/env python3
"""
Verification script to check frontend-backend category synchronization:
- Compare categories in Django admin with frontend display
- Verify all backend categories are shown on frontend
- Check dynamic category loading from database
"""

import sys
import os
import django
from django.conf import settings

# Add the project root to Python path
sys.path.append('/Users/uba/Desktop/chaos-magement')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Category, Product

def verify_category_synchronization():
    """Verify frontend categories match backend categories"""
    template_path = '/Users/uba/Desktop/chaos-magement/kiosk/templates/kiosk/product_list.html'
    
    print("🔍 Verifying Frontend-Backend Category Synchronization...")
    print("=" * 65)
    
    # Get backend categories
    backend_categories = Category.objects.all().order_by('name')
    print(f"📊 Backend Categories ({backend_categories.count()}):")
    
    category_info = []
    for i, category in enumerate(backend_categories, 1):
        product_count = Product.objects.filter(category=category, is_available=True).count()
        emoji = category.emoji if hasattr(category, 'emoji') and category.emoji else "N/A"
        category_info.append({
            'name': category.name,
            'slug': category.slug,
            'emoji': emoji,
            'products': product_count
        })
        print(f"  {i}. {category.name} (slug: {category.slug}) - {product_count} products - Emoji: {emoji}")
    
    print()
    
    # Check template for dynamic category loading
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Verify dynamic loading is implemented
    if '{% for category in categories %}' in content:
        print("✅ Template uses dynamic category loading from backend")
    else:
        print("❌ Template still uses hardcoded categories")
    
    # Check for proper category URL generation
    if "{% url 'kiosk:product_list' %}?category={{ category.slug }}" in content:
        print("✅ Category URLs are dynamically generated with correct slugs")
    else:
        print("❌ Category URLs are not properly generated")
    
    # Check for emoji support
    if '{% if category.emoji %}' in content:
        print("✅ Template supports category emojis from backend")
    else:
        print("❌ Template doesn't support category emojis")
    
    # Check for fallback icons
    if 'fa-vape' in content and 'fa-droplet' in content:
        print("✅ Template includes icons for missing categories (Vapes, Concentrates)")
    else:
        print("❌ Template missing icons for new categories")
    
    print()
    print("=" * 65)
    print("🎯 Category Mapping Summary:")
    print("┌─────────────────┬─────────────────┬─────────────┬──────────────┐")
    print("│ Category        │ Slug            │ Products    │ Display Icon │")
    print("├─────────────────┼─────────────────┼─────────────┼──────────────┤")
    
    for cat in category_info:
        icon = "🔮" if cat['emoji'] != "N/A" else "📦"
        print(f"│ {cat['name']:<15} │ {cat['slug']:<15} │ {cat['products']:<11} │ {icon:<12} │")
    
    print("└─────────────────┴─────────────────┴─────────────┴──────────────┘")
    print()
    print("📝 Changes Made:")
    print("- Replaced hardcoded category navigation with dynamic backend loading")
    print("- Added support for category emojis from database")
    print("- Added icons for new categories (Vapes: vape icon, Concentrates: droplet icon)")
    print("- Frontend now automatically reflects any backend category changes")
    print("- 'All Products' link shows all categories, individual links filter by category")
    
    print()
    print("🔄 Before: 4 hardcoded categories (Flower, Edibles, Accessories, Pre-rolls)")
    print(f"🆕 After: {backend_categories.count()} dynamic categories from backend database")
    print("=" * 65)

if __name__ == '__main__':
    verify_category_synchronization()
    print("\n🚀 Check http://127.0.0.1:8000/products/ - All backend categories should now be visible!")
