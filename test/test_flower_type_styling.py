#!/usr/bin/env python3
"""
Test script to verify flower type button styling and emoji categories
"""
import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse

# Add the project root to the path
sys.path.insert(0, '/home/ubuntu/django-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Category, Product

def test_category_emojis():
    """Test that categories have emojis"""
    print("🧪 Testing Category Emojis...")
    
    categories = Category.objects.all()
    emoji_count = 0
    
    for category in categories:
        if category.emoji:
            emoji_count += 1
            print(f"  ✔ {category.emoji} {category.name}")
        else:
            print(f"  ❌ {category.name} (no emoji)")
    
    print(f"📊 Categories with emojis: {emoji_count}/{categories.count()}")
    print()

def test_flower_type_css_classes():
    """Test that the expected CSS classes are present in the template"""
    print("🎨 Testing Flower Type CSS Classes...")
    
    # Read the base template to check for CSS classes
    template_path = '/home/ubuntu/django-app/kiosk/templates/kiosk/base.html'
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    expected_classes = [
        'flower-type-indica',
        'flower-type-active-indica',
        'flower-type-sativa', 
        'flower-type-active-sativa',
        'flower-type-hybrid',
        'flower-type-active-hybrid',
        'flower-type-high-cbd',
        'flower-type-active-high-cbd'
    ]
    
    all_present = True
    for css_class in expected_classes:
        if css_class in template_content:
            print(f"  ✔ {css_class}")
        else:
            print(f"  ❌ {css_class} - NOT FOUND")
            all_present = False
    
    if all_present:
        print("🎉 All CSS classes are present!")
    else:
        print("⚠️  Some CSS classes are missing!")
    print()

def test_product_list_response():
    """Test that the product list page loads correctly"""
    print("🌐 Testing Product List Page...")
    
    client = Client()
    
    try:
        response = client.get(reverse('kiosk:product_list'))
        
        if response.status_code == 200:
            print(f"  ✔ Product list page loads successfully (status: {response.status_code})")
            
            # Check if flower type buttons are in the response
            content = response.content.decode('utf-8')
            
            flower_emojis = ['🟣', '🟢', '🟡', '🔵']  # Indica, Sativa, Hybrid, High CBD
            found_emojis = []
            
            for emoji in flower_emojis:
                if emoji in content:
                    found_emojis.append(emoji)
            
            if found_emojis:
                print(f"  ✔ Found flower type emojis: {' '.join(found_emojis)}")
            else:
                print("  ⚠️  No flower type emojis found in response")
                
        else:
            print(f"  ❌ Product list page failed (status: {response.status_code})")
            
    except Exception as e:
        print(f"  ❌ Error testing product list: {e}")
    
    print()

def main():
    print("🚀 Testing Flower Type Styling and Category Emojis Implementation")
    print("=" * 60)
    
    test_category_emojis()
    test_flower_type_css_classes()
    test_product_list_response()
    
    print("✨ Testing complete!")

if __name__ == '__main__':
    main()
