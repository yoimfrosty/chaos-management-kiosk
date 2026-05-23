#!/usr/bin/env python3
"""
Test script to verify the cart panel positioning after adjustments
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.sessions.models import Session

# Add the project directory to Python path
sys.path.append('/home/ubuntu/django-app')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_kiosk.settings')
django.setup()

def test_cart_positioning():
    """Test that the cart panel positioning has been correctly adjusted"""
    
    print("🧪 Testing Cart Positioning Adjustments...")
    
    client = Client()
    
    # Set up age verification
    session = client.session
    session['is_21_plus'] = True
    session.save()
    
    # Test product list page loads
    response = client.get('/products/')
    
    print(f"✅ Page Status: {response.status_code}")
    
    # Check if the cart panel has updated positioning
    content = response.content.decode('utf-8')
    
    # Test 1: Cart panel positioning
    if 'top: 120px' in content and 'height: calc(100vh - 120px)' in content:
        print("✅ Cart panel positioned correctly (top: 120px)")
    else:
        print("❌ Cart panel positioning not found or incorrect")
        if 'top: 80px' in content:
            print("⚠️  Found old positioning (top: 80px) - needs update")
    
    # Test 2: Mobile cart toggle positioning  
    if 'top: 140px' in content:
        print("✅ Mobile cart toggle positioned correctly (top: 140px)")
    else:
        print("❌ Mobile cart toggle positioning not found")
        if 'top: 50%' in content:
            print("⚠️  Found old mobile toggle positioning - needs update")
    
    # Test 3: Check for navigation elements
    nav_elements = [
        'Browse', 'Specials', 'About', 'Help', 
        'Order #:', 'Age Verified'
    ]
    
    nav_found = 0
    for element in nav_elements:
        if element in content:
            nav_found += 1
    
    print(f"✅ Navigation elements found: {nav_found}/{len(nav_elements)}")
    
    # Test 4: Check cart functionality CSS
    css_checks = [
        'position: fixed',
        'z-index: 60',
        'mobile-cart-toggle',
        'cart-backdrop'
    ]
    
    css_found = 0
    for css_rule in css_checks:
        if css_rule in content:
            css_found += 1
    
    print(f"✅ CSS rules found: {css_found}/{len(css_checks)}")
    
    # Test 5: Check for proper spacing
    if 'margin-right: 320px' in content:
        print("✅ Main content margin preserved for desktop")
    else:
        print("⚠️  Main content margin not found")
    
    print("\n📊 Cart Positioning Test Summary:")
    print("=" * 50)
    
    if ('top: 120px' in content and 
        'top: 140px' in content and 
        nav_found >= 4 and 
        css_found >= 3):
        print("🎉 SUCCESS: Cart positioning properly adjusted!")
        print("✅ Cart panel now floats below navigation bar")
        print("✅ Mobile cart toggle positioned correctly") 
        print("✅ Navigation elements remain accessible")
        return True
    else:
        print("❌ ISSUES FOUND: Cart positioning needs review")
        return False

if __name__ == '__main__':
    success = test_cart_positioning()
    sys.exit(0 if success else 1)
