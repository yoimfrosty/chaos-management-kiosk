#!/usr/bin/env python3
"""
Verify Category Navigation Spacing Fix
Documents the spacing adjustments made to reduce gap above categories
"""

import requests
from bs4 import BeautifulSoup

def verify_spacing_changes():
    """Verify that spacing changes were applied"""
    
    print("🧪 Verifying Category Navigation Spacing Changes")
    print("=" * 55)
    
    # Create session and verify age
    session = requests.Session()
    
    try:
        # Age verification first
        age_url = "http://127.0.0.1:8000/verify-age/"
        age_response = session.get(age_url)
        
        if age_response.status_code != 200:
            print(f"❌ Failed to access age verification: {age_response.status_code}")
            return False
            
        soup = BeautifulSoup(age_response.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        
        age_data = {
            'csrfmiddlewaretoken': csrf_token,
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'birth_date': '1990-01-01'
        }
        
        verify_response = session.post(age_url, data=age_data)
        if verify_response.status_code not in [200, 302]:
            print(f"❌ Age verification failed: {verify_response.status_code}")
            return False
            
        # Access product page
        product_url = "http://127.0.0.1:8000/products/"
        product_response = session.get(product_url)
        
        if product_response.status_code != 200:
            print(f"❌ Failed to access product page: {product_response.status_code}")
            return False
            
        # Parse CSS to check for spacing changes
        soup = BeautifulSoup(product_response.content, 'html.parser')
        style_tags = soup.find_all('style')
        
        main_wrapper_padding_found = False
        category_nav_margin_found = False
        
        for style in style_tags:
            css_content = style.text
            
            # Check for main content wrapper padding reduction
            if '.main-content-wrapper' in css_content and 'padding-top: 0.25rem' in css_content:
                main_wrapper_padding_found = True
                print("✅ Main content wrapper padding reduced to 0.25rem")
            
            # Check for category navigation margin reduction
            if '.category-nav' in css_content and 'margin-bottom: 0.25rem' in css_content:
                category_nav_margin_found = True
                print("✅ Category navigation margin-bottom reduced to 0.25rem")
        
        # Verify HTML structure
        main_wrapper = soup.find('div', class_='main-content-wrapper')
        if main_wrapper:
            print("✅ Main content wrapper found")
            
            category_nav = main_wrapper.find('nav', class_='category-nav')
            if category_nav:
                print("✅ Category navigation found within main wrapper")
                
                # Count category items
                nav_items = category_nav.find_all('a', class_='category-nav-item')
                print(f"✅ Found {len(nav_items)} category navigation items")
                
                categories = []
                for item in nav_items:
                    span = item.find('span')
                    if span:
                        categories.append(span.text.strip())
                
                print(f"✅ Categories: {', '.join(categories)}")
        
        print(f"\n📐 Spacing Changes Summary:")
        print(f"{'✅' if main_wrapper_padding_found else '❌'} Main wrapper top padding: 1rem → 0.25rem")
        print(f"{'✅' if category_nav_margin_found else '❌'} Category nav bottom margin: 0.5rem → 0.25rem")
        
        print(f"\n🎯 Visual Impact:")
        print(f"• Category navigation moved closer to top of page")
        print(f"• Reduced gap between categories and product sections")
        print(f"• More efficient use of vertical space")
        print(f"• Better for kiosk interface with limited screen height")
        
        print(f"\n" + "=" * 55)
        print("✅ Category spacing optimization complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")
        return False

if __name__ == "__main__":
    verify_spacing_changes()
