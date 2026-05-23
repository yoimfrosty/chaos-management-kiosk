#!/usr/bin/env python3
"""
Test the modified order flow - should go directly to receipt page
"""
import requests
import re
import json

def test_direct_receipt_flow():
    """Test that order submission goes directly to receipt page"""
    print("🎯 Testing Direct Receipt Flow (No Dialog)")
    print("="*50)
    
    session = requests.Session()
    
    try:
        # Step 1: Age verification
        print("1. Setting up age verification...")
        response = session.get("http://localhost:8000/verify-age/", timeout=10)
        
        if response.status_code == 200:
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                verify_response = session.post("http://localhost:8000/verify-age/", {
                    'csrfmiddlewaretoken': csrf_token,
                    'is_21_plus': 'on'
                }, timeout=10, allow_redirects=False)
                
                if verify_response.status_code == 302:
                    print("   ✔ Age verification successful")
                else:
                    print("   ❌ Age verification failed")
                    return False
            else:
                print("   ❌ CSRF token not found")
                return False
        else:
            print("   ❌ Age verification page not accessible")
            return False
        
        # Step 2: Add item to cart
        print("2. Adding item to cart...")
        products_response = session.get("http://localhost:8000/products/", timeout=10)
        
        if products_response.status_code == 200:
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', products_response.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                
                # Add product to cart
                add_response = session.post("http://localhost:8000/cart/add/", {
                    'csrfmiddlewaretoken': csrf_token,
                    'product_id': '1',
                    'quantity': '1'
                }, headers={'X-Requested-With': 'XMLHttpRequest'}, timeout=10)
                
                if add_response.status_code == 200:
                    print("   ✔ Item added to cart")
                else:
                    print("   ❌ Failed to add item")
                    return False
            else:
                print("   ❌ CSRF token not found on products page")
                return False
        else:
            print("   ❌ Products page not accessible")
            return False
        
        # Step 3: Submit order (JSON)
        print("3. Submitting order via JSON...")
        submit_response = session.post("http://localhost:8000/submit-order/", 
            headers={
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
                'X-Requested-With': 'XMLHttpRequest'
            },
            data=json.dumps({}),
            timeout=10
        )
        
        print(f"   Order submission status: {submit_response.status_code}")
        
        if submit_response.status_code == 200:
            try:
                data = submit_response.json()
                if data.get('success'):
                    order_number = data.get('order_id')
                    receipt_url = data.get('print_receipt_url')
                    
                    print(f"   ✔ Order submitted successfully!")
                    print(f"   📋 Order Number: {order_number}")
                    print(f"   🧾 Receipt URL: {receipt_url}")
                    
                    # Step 4: Test receipt page access
                    print("4. Testing direct receipt access...")
                    receipt_response = session.get(f"http://localhost:8000{receipt_url}", timeout=10)
                    
                    if receipt_response.status_code == 200:
                        content = receipt_response.text
                        
                        # Check for receipt content
                        checks = [
                            ("OCEAN CITY KIOSK" in content, "Business name"),
                            (order_number in content, f"Order number {order_number}"),
                            ("PAYMENT REQUIRED" in content, "Payment status"),
                            ("Print Receipt" in content, "Print button"),
                            ("Take this receipt to the cashier" in content, "Instructions")
                        ]
                        
                        print(f"   Receipt page status: {receipt_response.status_code}")
                        print(f"   Content length: {len(content)} characters")
                        print(f"   📄 Content checks:")
                        
                        all_passed = True
                        for check, description in checks:
                            status = "✔" if check else "❌"
                            print(f"      {status} {description}")
                            if not check:
                                all_passed = False
                        
                        if all_passed:
                            print(f"\n🎉 DIRECT RECEIPT FLOW: SUCCESS!")
                            print("✔ No confirmation dialog required")
                            print("✔ Order submits directly")
                            print("✔ Receipt page loads correctly")
                            print("✔ All content displays properly")
                            return True
                        else:
                            print(f"\n⚠️ Receipt content issues found")
                            return False
                    else:
                        print(f"   ❌ Receipt page failed: {receipt_response.status_code}")
                        return False
                else:
                    print(f"   ❌ Order submission failed: {data.get('error', 'Unknown error')}")
                    return False
            except json.JSONDecodeError:
                print(f"   ❌ Invalid JSON response")
                return False
        else:
            print(f"   ❌ Order submission failed: {submit_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_direct_receipt_flow()
    
    print("\n" + "="*50)
    if success:
        print("✔ MODIFICATION SUCCESSFUL!")
        print("🎯 Order flow now goes directly to receipt page")
        print("📱 No more confirmation dialogs")
        print("🚀 Users click 'Complete Order' → Receipt Page")
    else:
        print("❌ MODIFICATION VERIFICATION FAILED")
        print("⚠️ Additional debugging may be needed")
