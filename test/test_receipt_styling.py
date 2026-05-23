#!/usr/bin/env python3
"""
Test receipt styling issue - check what's actually being returned
"""

import requests
import re
import json

def test_receipt_styling():
    """Test what the receipt page actually returns"""
    print("🔍 Testing Receipt Styling Issue")
    print("="*50)
    
    session = requests.Session()
    
    try:
        # Step 1: Get age verification page
        print("1. Getting age verification page...")
        response = session.get("http://localhost:8000/verify-age/", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Cannot access age verification page")
            return False
            
        # Extract CSRF token
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if not csrf_match:
            print(f"   ❌ Cannot find CSRF token")
            return False
            
        csrf_token = csrf_match.group(1)
        print(f"   ✔ CSRF token found")
        
        # Step 2: Submit age verification
        print("2. Submitting age verification...")
        verify_data = {
            'csrfmiddlewaretoken': csrf_token,
            'is_21_plus': 'on'
        }
        
        response = session.post("http://localhost:8000/verify-age/", 
                              data=verify_data, 
                              timeout=10,
                              allow_redirects=False)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 302:
            print(f"   ❌ Age verification failed")
            return False
            
        print(f"   ✔ Age verification successful")
        
        # Step 3: Test receipt pages
        print("3. Testing receipt pages...")
        
        for order_id in [1, 2, 3, 4, 5]:
            print(f"\n   📄 Testing order {order_id}:")
            response = session.get(f"http://localhost:8000/print-receipt/{order_id}/", timeout=10)
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"      Content length: {len(content)} characters")
                
                # Check if it's the styled template or plain text
                if "<!DOCTYPE html>" in content:
                    print(f"      ✔ HTML document returned")
                    
                    if "<style>" in content:
                        print(f"      ✔ Contains CSS styling")
                    else:
                        print(f"      ❌ No CSS styling found")
                        
                    if "OCEAN CITY KIOSK" in content:
                        print(f"      ✔ Business name found")
                    else:
                        print(f"      ❌ Business name not found")
                        
                    if "OCH-" in content:
                        print(f"      ✔ Order number format found")
                    else:
                        print(f"      ❌ Order number format not found")
                        
                    print(f"      📄 First 300 chars:")
                    print(f"         {content[:300]}...")
                    
                    return True  # Found a working receipt
                    
                else:
                    print(f"      ❌ Not an HTML document")
                    print(f"      📄 Content received:")
                    print(f"         {content[:200]}...")
                    
            elif response.status_code == 404:
                print(f"      ❌ Order not found")
            elif response.status_code == 302:
                print(f"      ❌ Still redirecting (age verification issue?)")
            else:
                print(f"      ❌ Error: {response.status_code}")
                
        print(f"\n❌ No working receipts found")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_receipt_styling()
    if success:
        print(f"\n🎉 Receipt styling working correctly!")
    else:
        print(f"\n❌ Receipt styling issue confirmed!")
