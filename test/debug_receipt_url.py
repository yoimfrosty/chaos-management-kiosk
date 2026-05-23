#!/usr/bin/env python3
"""
Debug receipt URL issue - check redirects and responses
"""

import requests
import re

def debug_receipt_url():
    """Debug what happens when we access receipt URLs"""
    print("🔍 Debug Receipt URL Issue")
    print("="*40)
    
    session = requests.Session()
    
    try:
        # Step 1: Age verification
        print("1. Setting up age verification...")
        response = session.get("http://localhost:8000/verify-age/")
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        csrf_token = csrf_match.group(1)
        
        verify_data = {
            'csrfmiddlewaretoken': csrf_token,
            'is_21_plus': 'on'
        }
        response = session.post("http://localhost:8000/verify-age/", data=verify_data, allow_redirects=False)
        print(f"   ✔ Age verification: {response.status_code}")
        
        # Step 2: Test receipt URLs with full redirect tracking
        print("\n2. Testing receipt URLs with redirect tracking...")
        
        for order_id in [1, 2, 3, 4, 5]:
            print(f"\n   📄 Testing order {order_id}:")
            
            # Don't follow redirects initially
            response = session.get(f"http://localhost:8000/print-receipt/{order_id}/", allow_redirects=False)
            print(f"      Initial response: {response.status_code}")
            
            if response.status_code == 302:
                redirect_url = response.headers.get('Location', 'Unknown')
                print(f"      Redirected to: {redirect_url}")
                
                # Follow the redirect
                response = session.get(f"http://localhost:8000/print-receipt/{order_id}/", allow_redirects=True)
                print(f"      Final response: {response.status_code}")
                print(f"      Final URL: {response.url}")
                
            if response.status_code == 200:
                content = response.text
                
                # Check what we actually got
                if "Welcome" in content and "Ocean City Hemp Kiosk" in content:
                    print(f"      ❌ Got welcome page instead of receipt")
                elif "OCEAN CITY KIOSK" in content and "PAYMENT REQUIRED" in content:
                    print(f"      ✔ Got receipt page!")
                    return order_id  # Found working receipt
                elif "Order not found" in content:
                    print(f"      ❌ Order not found error")
                else:
                    print(f"      ❓ Unknown content type")
                    print(f"         First 200 chars: {content[:200]}...")
            
        print(f"\n❌ No working receipt URLs found")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    working_order = debug_receipt_url()
    if working_order:
        print(f"\n🎉 Found working receipt for order {working_order}")
    else:
        print(f"\n❌ No working receipts found - orders may not exist")
