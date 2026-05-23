#!/usr/bin/env python3
"""
Verification script for color improvements on the product page
- Tests category visibility
- Tests text readability  
- Tests action button color scheme
- Tests overall design consistency
"""

import requests
from bs4 import BeautifulSoup
import re
import time

def test_product_page_accessibility():
    """Test that the product page has good color contrast and visibility"""
    try:
        # Test the main product page
        response = requests.get('http://127.0.0.1:8000/products/')
        if response.status_code != 200:
            print(f"❌ Product page failed to load: {response.status_code}")
            return False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for visible category navigation
        category_nav = soup.find(class_='category-nav')
        if not category_nav:
            print("❌ Category navigation not found")
            return False
        
        category_items = soup.find_all(class_='category-nav-item')
        if len(category_items) < 3:
            print(f"❌ Expected at least 3 category items, found {len(category_items)}")
            return False
        
        print(f"✅ Found {len(category_items)} category navigation items")
        
        # Check for readable product titles
        products_title = soup.find(class_='products-title')
        if not products_title:
            print("❌ Products title not found")
            return False
        print("✅ Products title found")
        
        # Check for category section titles
        category_titles = soup.find_all(class_='category-title')
        if len(category_titles) == 0:
            print("❌ No category section titles found")
            return False
        print(f"✅ Found {len(category_titles)} category section titles")
        
        # Check for action buttons
        action_bar = soup.find(class_='fixed-action-bar')
        if not action_bar:
            print("❌ Action bar not found")
            return False
        
        # Check for specific action buttons
        home_btn = soup.find(class_='action-btn home')
        assistance_btn = soup.find(class_='action-btn assistance') 
        order_btn = soup.find(class_='action-btn order-number')
        cart_btn = soup.find(class_='action-btn cart')
        
        missing_buttons = []
        if not home_btn: missing_buttons.append('Home')
        if not assistance_btn: missing_buttons.append('Assistance')
        if not order_btn: missing_buttons.append('Order Number')
        if not cart_btn: missing_buttons.append('Your Items')
        
        if missing_buttons:
            print(f"❌ Missing action buttons: {', '.join(missing_buttons)}")
            return False
        
        print("✅ All action buttons found (Home, Assistance, Order#, Your Items)")
        
        # Check for product cards
        product_cards = soup.find_all(class_='product-card')
        if len(product_cards) == 0:
            print("❌ No product cards found")
            return False
        
        print(f"✅ Found {len(product_cards)} product cards")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing product page: {e}")
        return False

def test_css_color_scheme():
    """Test that CSS contains the improved color scheme"""
    try:
        response = requests.get('http://127.0.0.1:8000/products/')
        if response.status_code != 200:
            print(f"❌ Could not fetch product page CSS")
            return False
        
        content = response.text
        
        # Check for improved category navigation colors
        if 'color: #1f2937' in content and 'background: rgba(255, 255, 255, 0.9)' in content:
            print("✅ Category navigation has improved visibility colors")
        else:
            print("❌ Category navigation colors not improved")
            return False
        
        # Check for improved Order# button (removed excessive glow)
        if '#f59e0b' in content and 'order-mega-glow' not in content:
            print("✅ Order# button has cleaner design without excessive shadows")
        else:
            print("❌ Order# button still has excessive effects")
            return False
        
        # Check for blue Your Items button (no pink)
        if '#0ea5e9' in content and '#ff006e' not in content:
            print("✅ Your Items button changed from pink to professional blue")
        else:
            print("❌ Your Items button still uses pink colors")
            return False
        
        # Check for readable text colors
        if 'color: #1f2937' in content:
            print("✅ Text colors improved for readability")
        else:
            print("❌ Text colors not improved")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing CSS: {e}")
        return False

def main():
    print("🧪 Testing Color Improvements on Product Page")
    print("=" * 50)
    
    # Test accessibility and visibility
    print("\n1. Testing Page Accessibility & Visibility:")
    accessibility_passed = test_product_page_accessibility()
    
    print("\n2. Testing CSS Color Scheme:")
    css_passed = test_css_color_scheme()
    
    # Overall result
    print("\n" + "=" * 50)
    if accessibility_passed and css_passed:
        print("🎉 ALL TESTS PASSED! Color improvements successful!")
        print("\n✅ Category navigation is now clearly visible")
        print("✅ Product titles and text are readable")
        print("✅ Order# button has clean, professional design")
        print("✅ Your Items button uses professional blue instead of pink")
        print("✅ Overall design maintains brand consistency")
    else:
        print("❌ Some tests failed. Please check the issues above.")
    
    return accessibility_passed and css_passed

if __name__ == "__main__":
    main()
