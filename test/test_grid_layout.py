#!/usr/bin/env python3
"""
Test script to verify the new 3-column grid layout is working correctly
"""
import requests
from bs4 import BeautifulSoup
import sys

def test_grid_layout():
    """Test the new grid layout implementation"""
    
    # Start a session to maintain cookies/session data
    session = requests.Session()
    
    print("🧪 Testing the new 3-column grid layout...")
    
    try:
        # Step 1: Access welcome page
        print("📋 Step 1: Accessing welcome page...")
        response = session.get('http://localhost:8000/')
        if response.status_code != 200:
            print(f"❌ Welcome page failed: {response.status_code}")
            return False
        print("✅ Welcome page accessible")
        
        # Step 2: Perform age verification
        print("📋 Step 2: Submitting age verification...")
        # Get CSRF token
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        if csrf_token:
            csrf_value = csrf_token.get('value')
        else:
            print("❌ Could not find CSRF token on welcome page")
            return False
            
        # Submit age verification
        age_data = {
            'csrfmiddlewaretoken': csrf_value,
            'is_21_plus': 'on'
        }
        response = session.post('http://localhost:8000/verify-age/', data=age_data)
        
        # Should redirect to products page
        if response.status_code not in [200, 302]:
            print(f"❌ Age verification failed: {response.status_code}")
            return False
        print("✅ Age verification successful")
        
        # Step 3: Access products page and check grid layout
        print("📋 Step 3: Checking products page grid layout...")
        response = session.get('http://localhost:8000/products/')
        if response.status_code != 200:
            print(f"❌ Products page failed: {response.status_code}")
            return False
        
        # Parse HTML and check for grid structure
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for 3-column grid container
        grid_container = soup.find('div', class_='grid grid-cols-3 gap-6')
        if not grid_container:
            print("❌ 3-column grid container not found")
            return False
        print("✅ Found 3-column grid container")
        
        # Check for products column (col-span-2)
        products_column = grid_container.find('div', class_='col-span-2 px-6')
        if not products_column:
            print("❌ Products column (col-span-2) not found")
            return False
        print("✅ Found products column spanning 2 columns")
        
        # Check for cart panel in third column
        cart_panel = grid_container.find('div', id='cart-panel')
        if not cart_panel:
            print("❌ Cart panel not found in grid")
            return False
        print("✅ Found cart panel in grid layout")
        
        # Verify cart panel is NOT using fixed positioning
        cart_style = cart_panel.get('style', '')
        if 'fixed' in cart_style or 'position: fixed' in cart_style:
            print("❌ Cart panel still using fixed positioning")
            return False
        print("✅ Cart panel is not using fixed positioning")
        
        # Check for mobile responsive CSS
        style_tags = soup.find_all('style')
        mobile_responsive = False
        for style in style_tags:
            if '@media (max-width: 1024px)' in style.text:
                mobile_responsive = True
                break
        
        if not mobile_responsive:
            print("❌ Mobile responsive CSS not found")
            return False
        print("✅ Found mobile responsive CSS")
        
        # Check that mobile cart toggle elements are NOT present
        mobile_toggle = soup.find('div', id='mobile-cart-toggle')
        cart_backdrop = soup.find('div', id='cart-backdrop')
        
        if mobile_toggle:
            print("❌ Mobile cart toggle still present (should be removed)")
            return False
        print("✅ Mobile cart toggle properly removed")
        
        if cart_backdrop:
            print("❌ Cart backdrop still present (should be removed)")
            return False
        print("✅ Cart backdrop properly removed")
        
        # Check for essential cart elements
        cart_items = soup.find('div', id='cart-items')
        cart_summary = soup.find('div', id='cart-summary')
        complete_order_btn = soup.find('button', id='complete-order-btn')
        clear_cart_btn = soup.find('button', id='clear-cart-btn')
        
        if not all([cart_items, cart_summary, complete_order_btn, clear_cart_btn]):
            print("❌ Missing essential cart elements")
            return False
        print("✅ All essential cart elements present")
        
        print("\n🎉 Grid layout test PASSED!")
        print("✅ Successfully converted from floating cart to 3-column grid layout")
        print("✅ Cart panel is now part of the regular page flow")
        print("✅ Mobile responsive design implemented")
        print("✅ All floating/fixed positioning removed")
        print("✅ Mobile cart toggle functionality properly cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_grid_layout()
    sys.exit(0 if success else 1)
