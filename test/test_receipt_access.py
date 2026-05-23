#!/usr/bin/env python3
"""
Test receipt with proper age verification session
"""

import requests
import time

def test_receipt_with_age_verification():
    """Test receipt page with age verification session"""
    print("🔍 Testing Receipt with Age Verification")
    print("="*50)
    
    session = requests.Session()
    
    try:
        # Step 1: Get the age verification page to get CSRF token
        print("1. Getting age verification page...")
        response = session.get("http://localhost:8000/verify-age/", timeout=5)
        print(f"   Age verification page: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Cannot access age verification page")
            return False
            
        # Extract CSRF token
        content = response.text
        csrf_start = content.find('name="csrfmiddlewaretoken" value="') + len('name="csrfmiddlewaretoken" value="')
        csrf_end = content.find('"', csrf_start)
        csrf_token = content[csrf_start:csrf_end] if csrf_start > 33 else None
        
        if not csrf_token:
            print(f"   ❌ Cannot find CSRF token")
            return False
            
        print(f"   ✔ CSRF token found: {csrf_token[:10]}...")
        
        # Step 2: Submit age verification
        print("2. Submitting age verification...")
        verify_data = {
            'csrfmiddlewaretoken': csrf_token,
            'is_21_plus': 'on'
        }
        
        response = session.post("http://localhost:8000/verify-age/", 
                              data=verify_data, 
                              timeout=5,
                              allow_redirects=False)
        
        print(f"   Age verification response: {response.status_code}")
        
        if response.status_code == 302:
            print(f"   ✔ Age verification successful (redirected)")
        else:
            print(f"   ❌ Age verification failed")
            return False
        
        # Step 3: Now try to access receipt pages
        print("3. Testing receipt access...")
        
        for order_id in [1, 2, 3, 4, 5]:
            response = session.get(f"http://localhost:8000/print-receipt/{order_id}/", timeout=5)
            print(f"   📄 Order {order_id}: Status {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"      Content length: {len(content)} characters")
                
                # Check if it's still the age verification page
                if "Age Verification" in content:
                    print(f"      ❌ Still getting age verification page")
                    continue
                
                # Check for receipt content
                checks = [
                    ("OCEAN CITY KIOSK" in content, "Business name"),
                    ("Order Number:" in content, "Order number label"),
                    ("OCH-" in content, "Order number format"),
                    ("PAYMENT REQUIRED" in content, "Payment required"),
                    ("Print Receipt" in content, "Print button"),
                    ("printReceipt()" in content, "Print function")
                ]
                
                print(f"      🔍 Content checks:")
                all_passed = True
                for check, description in checks:
                    status = "✔" if check else "❌"
                    print(f"         {status} {description}")
                    if not check:
                        all_passed = False
                
                if all_passed:
                    print(f"      🎉 Receipt page working correctly!")
                    
                    # Show a snippet of the receipt
                    print(f"      📄 Receipt snippet (first 300 chars):")
                    print(f"         {content[:300]}...")
                    
                    return True
                else:
                    print(f"      ⚠️  Receipt page loaded but content issues found")
                    # Show what we got instead
                    print(f"      📄 Received content start:")
                    print(f"         {content[:200]}...")
                    
            elif response.status_code == 404:
                print(f"      ❌ Order not found")
            elif response.status_code == 302:
                print(f"      🔄 Redirected")
            else:
                print(f"      ❌ Error: {response.status_code}")
                
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_receipt_with_age_verification()
