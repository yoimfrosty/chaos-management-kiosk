#!/usr/bin/env python3
"""
Test receipt with real order creation
"""

import requests
import re
import json
import time

def test_receipt_with_real_order():
    """Test receipt page with a real order"""
    print("🔍 Testing Receipt with Real Order Creation")
    print("="*50)
    
    session = requests.Session()
    
    try:
        # Step 1: Age verification
        print("1. Getting age verification...")
        response = session.get("http://localhost:8000/verify-age/", timeout=5)
        print(f"   Age verification page: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Cannot access age verification page")
            return False
            
        # Extract CSRF token
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if not csrf_match:
            print(f"   ❌ Cannot find CSRF token")
            return False
            
        csrf_token = csrf_match.group(1)
        print(f"   ✔ CSRF token found: {csrf_token[:10]}...")
        
        # Submit age verification
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
        
        if response.status_code != 302:
            print(f"   ❌ Age verification failed")
            return False
            
        print(f"   ✔ Age verification successful")
        
        # Step 3: Add item to cart
        print("3. Adding item to cart...")
        products_response = session.get("http://localhost:8000/products/", timeout=5)
        if products_response.status_code != 200:
            print(f"   ❌ Cannot access products page: {products_response.status_code}")
            return False
            
        # Extract CSRF token from products page
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', products_response.text)
        if not csrf_match:
            print(f"   ❌ Cannot find CSRF token on products page")
            return False
            
        csrf_token = csrf_match.group(1)
        
        # Add first product to cart
        cart_data = {
            'csrfmiddlewaretoken': csrf_token,
            'product_id': '1',
            'quantity': '1'
        }
        
        add_response = session.post("http://localhost:8000/cart/add/",
                                  data=cart_data,
                                  headers={'X-Requested-With': 'XMLHttpRequest'},
                                  timeout=5)
        
        print(f"   Add to cart response: {add_response.status_code}")
        
        if add_response.status_code == 200:
            print(f"   ✔ Item added to cart successfully")
        else:
            print(f"   ❌ Failed to add item to cart")
            print(f"   Response: {add_response.text[:200]}...")
            return False
        
        # Step 4: Submit order
        print("4. Submitting order...")
        
        submit_response = session.post("http://localhost:8000/submit-order/",
                                     headers={
                                         'Content-Type': 'application/json',
                                         'X-CSRFToken': csrf_token,
                                         'X-Requested-With': 'XMLHttpRequest'
                                     },
                                     data=json.dumps({}),
                                     timeout=5)
        
        print(f"   Submit order response: {submit_response.status_code}")
        
        if submit_response.status_code == 200:
            try:
                data = submit_response.json()
                if data.get('success'):
                    order_number = data.get('order_id')
                    order_db_id = data.get('order_db_id')
                    print_url = data.get('print_receipt_url')
                    
                    print(f"   ✔ Order submitted successfully!")
                    print(f"   📋 Order Number: {order_number}")
                    print(f"   🆔 Database ID: {order_db_id}")
                    print(f"   🖨️  Print URL: {print_url}")
                    
                    # Step 5: Test receipt access
                    print("5. Testing receipt access...")
                    receipt_response = session.get(f"http://localhost:8000{print_url}", timeout=5)
                    print(f"   📄 Receipt response: {receipt_response.status_code}")
                    
                    if receipt_response.status_code == 200:
                        content = receipt_response.text
                        print(f"   Content length: {len(content)} characters")
                        
                        # Check for receipt content
                        checks = [
                            ("OCEAN CITY KIOSK" in content, "Business name"),
                            ("Order Number:" in content, "Order number label"),
                            (order_number in content, f"Order number {order_number}"),
                            ("PAYMENT REQUIRED" in content, "Payment required"),
                            ("Print Receipt" in content, "Print button"),
                            ("printReceipt()" in content, "Print function"),
                            ("Thank you for choosing" in content, "Thank you message")
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
                            print(f"      📄 Receipt snippet (first 300 chars):")
                            print(f"         {content[:300]}...")
                            return True
                        else:
                            print(f"      ⚠️  Receipt page loaded but content issues found")
                            # Show what we got instead
                            print(f"      📄 Received content start:")
                            print(f"         {content[:400]}...")
                            
                    else:
                        print(f"   ❌ Receipt page failed: {receipt_response.status_code}")
                        
                else:
                    print(f"   ❌ Order submission failed: {data.get('error', 'Unknown error')}")
                    
            except json.JSONDecodeError:
                print(f"   ❌ Invalid JSON response from order submission")
                print(f"   Response: {submit_response.text[:200]}...")
                
        else:
            print(f"   ❌ Order submission failed: {submit_response.status_code}")
            print(f"   Response: {submit_response.text[:200]}...")
                
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_receipt_with_real_order()
    if success:
        print(f"\n🎉 RECEIPT TEST PASSED!")
    else:
        print(f"\n❌ RECEIPT TEST FAILED!")
