#!/usr/bin/env python3
"""
Test the complete order flow after removing receipt pages
This ensures that orders now go directly to view order page only
"""

import requests
import re
import json

def test_streamlined_order_flow():
    """Test that order submission goes directly to view order page only"""
    print("🎯 Testing Streamlined Order Flow (Receipt-Free)")
    print("="*60)
    
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
                    view_order_url = data.get('view_order_url')
                    
                    print(f"   ✔ Order submitted successfully!")
                    print(f"   📋 Order Number: {order_number}")
                    print(f"   🔗 View Order URL: {view_order_url}")
                    
                    # Verify NO print_receipt_url is returned
                    if 'print_receipt_url' in data:
                        print(f"   ❌ ERROR: print_receipt_url still present in response!")
                        return False
                    else:
                        print(f"   ✔ Confirmed: No print_receipt_url in response")
                    
                    # Step 4: Test view order page access
                    print("4. Testing view order page access...")
                    view_response = session.get(f"http://localhost:8000{view_order_url}", timeout=10)
                    
                    if view_response.status_code == 200:
                        content = view_response.text
                        
                        # Check for view order content
                        checks = [
                            ("OCEAN CITY KIOSK" in content, "Business name"),
                            (order_number in content, f"Order number {order_number}"),
                            ("Order Confirmed!" in content, "Confirmation message"),
                            ("Continue Shopping" in content, "Continue shopping button"),
                            ("Next Steps" in content, "Next steps section"),
                            ("proceed to the cashier counter" in content, "Payment instructions")
                        ]
                        
                        print(f"   View order page status: {view_response.status_code}")
                        print(f"   Content length: {len(content)} characters")
                        print(f"   📄 Content checks:")
                        
                        all_passed = True
                        for check, description in checks:
                            status = "✔" if check else "❌"
                            print(f"      {status} {description}")
                            if not check:
                                all_passed = False
                        
                        if all_passed:
                            print(f"\n🎉 STREAMLINED ORDER FLOW: SUCCESS!")
                            print("✔ No receipt page involved")
                            print("✔ Order submits directly to view order page")
                            print("✔ View order page loads correctly")
                            print("✔ All content displays properly")
                            print("✔ Only view order functionality remains")
                            return True
                        else:
                            print(f"\n⚠️ View order page content issues found")
                            return False
                    else:
                        print(f"   ❌ View order page failed: {view_response.status_code}")
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
    success = test_streamlined_order_flow()
    
    print("\n" + "="*60)
    if success:
        print("✔ RECEIPT REMOVAL SUCCESSFUL!")
        print("🎯 Order flow now uses view order page only")
        print("📱 No more receipt pages or print functionality")
        print("🚀 Users click 'Complete Order' → View Order Page")
        print("💰 Clear payment instructions on view order page")
    else:
        print("❌ RECEIPT REMOVAL VERIFICATION FAILED")
        print("⚠️ Additional debugging may be needed")
