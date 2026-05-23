#!/usr/bin/env python3
"""
Test receipt with proper age verification session handling
"""

import requests
import re
import time

def get_csrf_token(session, url):
    """Extract CSRF token from a page"""
    try:
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
            if csrf_match:
                return csrf_match.group(1)
    except Exception as e:
        print(f"Error getting CSRF token: {e}")
    return None

def test_receipt_with_session():
    """Test receipt with proper session handling"""
    print("🔍 Receipt Test with Session Management")
    print("="*45)
    
    session = requests.Session()
    
    try:
        # Step 1: Verify age
        print("1. Handling age verification...")
        csrf_token = get_csrf_token(session, "http://localhost:8000/verify-age/")
        
        if csrf_token:
            verify_response = session.post("http://localhost:8000/verify-age/", {
                'csrfmiddlewaretoken': csrf_token,
                'is_21_plus': 'on'  # Use correct field name
            }, timeout=10)
            
            print(f"   Age verification status: {verify_response.status_code}")
            if verify_response.status_code == 302:
                print("   ✔ Age verification successful")
            else:
                print("   ❌ Age verification failed")
                return False
        else:
            print("   ❌ Could not get CSRF token")
            return False
        
        # Step 2: Test receipt access
        print("\n2. Testing receipt access...")
        for order_id in [77, 76, 75]:
            try:
                print(f"   📄 Order {order_id}:")
                response = session.get(f"http://localhost:8000/print-receipt/{order_id}/", timeout=10)
                print(f"      Status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.text
                    print(f"      Content length: {len(content)} characters")
                    
                    # Check if it's still age verification
                    if "Age Verification" in content:
                        print(f"      ❌ Still getting age verification page")
                        continue
                    
                    # Check for receipt content
                    checks = [
                        ("OCEAN CITY KIOSK" in content, "Business name"),
                        ("Order:" in content, "Order label"), 
                        ("OCH-" in content, "Order number format"),
                        ("PAYMENT REQUIRED" in content, "Payment required"),
                        ("Total:" in content, "Total amount"),
                    ]
                    
                    print(f"      🔍 Content checks:")
                    all_passed = True
                    for check, description in checks:
                        status = "✔" if check else "❌"
                        print(f"         {status} {description}")
                        if not check:
                            all_passed = False
                    
                    if all_passed:
                        print(f"      🎉 Receipt working correctly!")
                        return True
                    else:
                        print(f"      📄 Content start: {content[:300]}...")
                        
                elif response.status_code == 302:
                    print(f"      🔄 Redirected")
                else:
                    print(f"      ❌ Error: {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ Error: {e}")
        
        print(f"\n❌ No working receipts found")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_receipt_with_session()
