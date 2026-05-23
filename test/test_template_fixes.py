#!/usr/bin/env python3
"""
Test template rendering fixes
"""
import requests
import re
from bs4 import BeautifulSoup

def test_template_rendering():
    """Test that template variables are rendering properly"""
    print("🧪 Testing Template Rendering Fixes")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    session = requests.Session()
    
    try:
        # Get CSRF token from welcome page
        print("\n1. Getting CSRF token...")
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
        
        # Submit age verification
        print("\n2. Submitting age verification...")
        age_data = {
            'csrfmiddlewaretoken': csrf_value,
            'is_21_plus': 'on'
        }
        age_response = session.post(f"{base_url}/verify-age/", data=age_data, allow_redirects=False)
        if age_response.status_code != 302:
            print(f"❌ Age verification failed: {age_response.status_code}")
            return False
        print("✔ Age verification successful")
        
        # Access products page
        print("\n3. Testing products page rendering...")
        products_response = session.get(f"{base_url}/products/", allow_redirects=True)
        if products_response.status_code != 200:
            print(f"❌ Failed to access products page: {products_response.status_code}")
            return False
        
        content = products_response.text
        print("✔ Products page loaded")
        
        # Test specific template rendering issues
        print("\n4. Checking template rendering...")
        
        # Check Order number rendering
        if "Order #:" in content and not "{{ cart.order_number }}" in content:
            print("✔ Order number template rendering fixed")
        else:
            print("❌ Order number still has template issues")
            
        # Check flower type rendering
        if "🌿 All Types" in content:
            print("✔ 'All Types' button rendering correctly")
        else:
            print("❌ 'All Types' button not found")
            
        # Check for unrendered template variables
        unrendered_patterns = [
            "{{ type_display }}",
            "{{ product.description|truncatewords:20 }}",
            "{{\\s*cart.order_number\\s*}}"
        ]
        
        issues_found = []
        for pattern in unrendered_patterns:
            if re.search(pattern, content):
                issues_found.append(pattern)
        
        if not issues_found:
            print("✔ No unrendered template variables found")
        else:
            print(f"❌ Found unrendered template variables: {issues_found}")
            
        # Check for proper flower type icons
        flower_icons = ["🟣", "🟢", "🟡", "🔵"]
        icons_found = sum(1 for icon in flower_icons if icon in content)
        
        if icons_found >= 3:  # Should have at least 3 different flower type icons
            print(f"✔ Flower type icons rendering properly ({icons_found} found)")
        else:
            print(f"❌ Flower type icons not rendering properly ({icons_found} found)")
            
        # Check for product information
        if "THC:" in content and "CBD:" in content:
            print("✔ Product information (THC/CBD) rendering correctly")
        else:
            print("❌ Product information not rendering properly")
            
        print("\n" + "=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_template_rendering()
    if success:
        print("🎉 Template rendering test completed!")
    else:
        print("❌ Template rendering test failed!")
