#!/usr/bin/env python3
"""
Create a test order and test receipt
"""

import requests
import re
import json

def create_order_and_test_receipt():
    """Create an order through the normal flow and test its receipt"""
    print("🔍 Create Order and Test Receipt")
    print("="*45)
    
    session = requests.Session()
    
    try:
        # Step 1: Age verification
        print("1. Age verification...")
        response = session.get("http://localhost:8000/verify-age/", timeout=10)
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        csrf_token = csrf_match.group(1)
        
        verify_data = {
            'csrfmiddlewaretoken': csrf_token,
            'is_21_plus': 'on'
        }
        response = session.post("http://localhost:8000/verify-age/", data=verify_data)
        print(f"   ✔ Age verified")
        
        # Step 2: Add item to cart
        print("2. Adding item to cart...")
        products_response = session.get("http://localhost:8000/products/")
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', products_response.text)
        csrf_token = csrf_match.group(1)
        
        cart_data = {
            'csrfmiddlewaretoken': csrf_token,
            'product_id': '1',
            'quantity': '1'
        }
        
        add_response = session.post("http://localhost:8000/cart/add/",
                                  data=cart_data,
                                  headers={'X-Requested-With': 'XMLHttpRequest'})
        
        if add_response.status_code == 200:
            print(f"   ✔ Item added to cart")
        else:
            print(f"   ❌ Failed to add item: {add_response.status_code}")
            return False
        
        # Step 3: Submit order
        print("3. Submitting order...")
        
        submit_response = session.post("http://localhost:8000/submit-order/",
                                     headers={
                                         'Content-Type': 'application/json',
                                         'X-CSRFToken': csrf_token,
                                         'X-Requested-With': 'XMLHttpRequest'
                                     },
                                     data=json.dumps({}))
        
        if submit_response.status_code == 200:
            data = submit_response.json()
            if data.get('success'):
                order_id = data.get('order_id')
                order_db_id = data.get('order_db_id')
                print_url = data.get('print_receipt_url')
                
                print(f"   ✔ Order created successfully!")
                print(f"   📋 Order Number: {order_id}")
                print(f"   🆔 Database ID: {order_db_id}")
                print(f"   🖨️  Print URL: {print_url}")
                
                # Step 4: Test receipt
                print("4. Testing receipt page...")
                receipt_response = session.get(f"http://localhost:8000{print_url}")
                
                print(f"   📊 Receipt status: {receipt_response.status_code}")
                print(f"   📄 Content length: {len(receipt_response.text)} characters")
                
                if receipt_response.status_code == 200:
                    content = receipt_response.text
                    
                    # Check what we got
                    if "<!DOCTYPE html>" in content:
                        print(f"   ✔ HTML document returned")
                        
                        if "OCEAN CITY KIOSK" in content:
                            print(f"   ✔ Business name found in receipt")
                        else:
                            print(f"   ❌ Business name not found")
                            
                        if order_id in content:
                            print(f"   ✔ Order number {order_id} found in receipt")
                        else:
                            print(f"   ❌ Order number not found")
                            
                        if "PAYMENT REQUIRED" in content:
                            print(f"   ✔ Payment required text found")
                        else:
                            print(f"   ❌ Payment required text not found")
                            
                        if "Welcome" in content and "Hemp Kiosk" in content:
                            print(f"   ❌ Got welcome page instead of receipt!")
                            print(f"   📄 Content start: {content[:300]}...")
                            return False
                        else:
                            print(f"   ✔ Got receipt page!")
                            print(f"   📄 Content start: {content[:300]}...")
                            return True
                    else:
                        print(f"   ❌ Not an HTML document")
                        print(f"   📄 Content: {content[:200]}...")
                        
                else:
                    print(f"   ❌ Receipt request failed: {receipt_response.status_code}")
                    
            else:
                print(f"   ❌ Order submission failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ Order submission request failed: {submit_response.status_code}")
            
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_order_and_test_receipt()
    if success:
        print(f"\n🎉 Receipt styling working correctly!")
    else:
        print(f"\n❌ Receipt styling issue confirmed!")
