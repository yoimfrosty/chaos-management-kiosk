#!/usr/bin/env python3
"""
Test Fixed Cart Panel Implementation
"""
import requests
import sys
from bs4 import BeautifulSoup

def test_fixed_cart_implementation():
    """Test that the fixed cart panel is properly implemented"""
    print("🧪 Testing Fixed Cart Panel Implementation")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    try:
        # Create session
        session = requests.Session()
        
        # Test 1: Access welcome page to get CSRF token
        print("\n1. Getting CSRF token from welcome page...")
        welcome_response = session.get(f"{base_url}/")
        if welcome_response.status_code != 200:
            print(f"❌ Failed to access welcome page: {welcome_response.status_code}")
            return False
            
        # Extract CSRF token
        soup = BeautifulSoup(welcome_response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        if not csrf_token:
            print("❌ CSRF token not found")
            return False
        csrf_value = csrf_token['value']
        print("✔ CSRF token obtained")
        
        # Test 2: Submit age verification
        print("\n2. Submitting age verification...")
        age_data = {
            'csrfmiddlewaretoken': csrf_value,
            'is_21_plus': 'on'  # Fixed field name
        }
        age_response = session.post(f"{base_url}/verify-age/", data=age_data, allow_redirects=False)
        if age_response.status_code == 302:  # Expect redirect after age verification
            print("✔ Age verification successful")
        else:
            print(f"❌ Age verification failed: {age_response.status_code}")
            print(f"Response content: {age_response.text[:200]}...")
            return False
        
        # Test 3: Access product list page
        print("\n3. Accessing product list page...")
        products_response = session.get(f"{base_url}/products/", allow_redirects=True)
        if products_response.status_code != 200:
            print(f"❌ Failed to access products page: {products_response.status_code}")
            print(f"Final URL: {products_response.url}")
            return False
        print("✔ Products page accessible")
        
        # Test 4: Check for fixed cart panel elements
        print("\n4. Checking fixed cart panel implementation...")
        soup = BeautifulSoup(products_response.text, 'html.parser')
        
        # Check cart panel exists with fixed positioning
        cart_panel = soup.find('div', {'id': 'cart-panel'})
        if not cart_panel:
            print("❌ Cart panel not found")
            return False
        print("✔ Cart panel found")
        
        # Check if cart panel has fixed positioning styles
        cart_style = cart_panel.get('style', '')
        if 'top: 80px' not in cart_style or 'height: calc(100vh - 80px)' not in cart_style:
            print("❌ Cart panel missing fixed positioning styles")
            return False
        print("✔ Cart panel has fixed positioning styles")
        
        # Check for fixed class
        cart_classes = cart_panel.get('class', [])
        if 'fixed' not in cart_classes:
            print("❌ Cart panel missing 'fixed' class")
            return False
        print("✔ Cart panel has 'fixed' class")
        
        # Test 5: Check for mobile cart toggle
        print("\n5. Checking mobile cart toggle...")
        mobile_toggle = soup.find('button', {'id': 'mobile-cart-toggle'})
        if not mobile_toggle:
            print("❌ Mobile cart toggle not found")
            return False
        print("✔ Mobile cart toggle found")
        
        # Check mobile toggle classes
        toggle_classes = mobile_toggle.get('class', [])
        if 'mobile-cart-toggle' not in toggle_classes:
            print("❌ Mobile cart toggle missing class")
            return False
        print("✔ Mobile cart toggle has correct class")
        
        # Test 6: Check for responsive CSS
        print("\n6. Checking responsive CSS...")
        style_tags = soup.find_all('style')
        has_responsive_css = False
        
        for style in style_tags:
            if style.string and '@media (max-width: 1024px)' in style.string:
                has_responsive_css = True
                break
        
        if not has_responsive_css:
            print("❌ Responsive CSS not found")
            return False
        print("✔ Responsive CSS found")
        
        # Test 7: Check main content margin adjustment
        print("\n7. Checking main content layout...")
        main_content = soup.find('div', {'class': lambda x: x and 'main-content' in x})
        if not main_content:
            print("❌ Main content with 'main-content' class not found")
            return False
        
        main_style = main_content.get('style', '')
        if 'margin-right: 320px' not in main_style:
            print("❌ Main content missing margin adjustment")
            return False
        print("✔ Main content has proper margin adjustment")
        
        # Test 8: Check cart backdrop for mobile
        print("\n8. Checking mobile cart backdrop...")
        cart_backdrop = soup.find('div', {'id': 'cart-backdrop'})
        if not cart_backdrop:
            print("❌ Cart backdrop not found")
            return False
        print("✔ Cart backdrop found")
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! Fixed cart panel implementation is complete.")
        print("\nFeatures verified:")
        print("✔ Cart panel has fixed positioning")
        print("✔ Cart panel positioned correctly (top: 80px)")
        print("✔ Cart panel has correct height calculation")
        print("✔ Main content has margin adjustment for cart width")
        print("✔ Mobile cart toggle button implemented")
        print("✔ Mobile cart backdrop implemented")
        print("✔ Responsive CSS media queries included")
        print("✔ All required CSS classes present")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the Django server is running:")
        print("   python manage.py runserver 0.0.0.0:8000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_fixed_cart_implementation()
    sys.exit(0 if success else 1)
