#!/usr/bin/env python3
"""
Test template rendering directly
"""

import requests
import re
import time

def test_template_rendering():
    """Test if the template renders properly when it does work"""
    print("🔍 Test Template Rendering")
    print("="*35)
    
    session = requests.Session()
    
    try:
        # Step 1: Age verification
        print("1. Setting up session...")
        response = session.get("http://localhost:8000/verify-age/", timeout=5)
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if not csrf_match:
            print("   ❌ No CSRF token found")
            return False
            
        csrf_token = csrf_match.group(1)
        
        verify_data = {
            'csrfmiddlewaretoken': csrf_token,
            'is_21_plus': 'on'
        }
        
        response = session.post("http://localhost:8000/verify-age/", data=verify_data)
        print(f"   ✔ Session setup complete")
        
        # Step 2: Try to access any page to see what we actually get
        print("2. Testing different URLs...")
        
        test_urls = [
            "/print-receipt/999999/",  # Non-existent order
            "/products/",              # Valid page
            "/",                       # Welcome page
        ]
        
        for url in test_urls:
            print(f"\n   📄 Testing {url}:")
            response = session.get(f"http://localhost:8000{url}", timeout=5)
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"      Content length: {len(content)} chars")
                
                # Check content type
                if "<!DOCTYPE html>" in content:
                    print(f"      ✔ HTML document")
                    
                    if "OCEAN CITY KIOSK" in content:
                        print(f"      ✔ Contains OCEAN CITY KIOSK")
                    
                    if "<style>" in content:
                        print(f"      ✔ Contains CSS")
                    
                    if "Welcome" in content:
                        print(f"      📋 Welcome page")
                    elif "Products" in content:
                        print(f"      📋 Products page")
                    elif "PAYMENT REQUIRED" in content:
                        print(f"      📋 Receipt page")
                    else:
                        print(f"      📋 Unknown page type")
                        
                else:
                    print(f"      ❌ Not HTML")
                    print(f"      📄 Content: {content[:100]}...")
                    
        # Step 3: Check what happens when we access a receipt URL that causes unstyled text
        print("\n3. Investigating the unstyled text issue...")
        print("   The issue might be:")
        print("   • Template not found")
        print("   • Context variables missing")  
        print("   • CSS not loading")
        print("   • Order object issues")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_template_rendering()
