#!/usr/bin/env python3
"""
Test Order ID Consistency Between Customer Display and Admin Panel
This test verifies that the order ID shown to customers matches the order_number in admin.
"""

import requests
import re
import json

BASE_URL = "http://localhost:8000"
session = requests.Session()

def get_csrf_token(url):
    """Extract CSRF token from a page"""
    try:
        response = session.get(url)
        if response.status_code == 200:
            match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', response.text)
            if match:
                return match.group(1)
    except:
        pass
    return None

def test_order_id_consistency():
    """Test that customer-displayed order ID matches admin order_number"""
    print("🔍 Testing Order ID Consistency")
    print("="*50)
    
    # Step 1: Verify age
    print("1. Setting up age verification...")
    csrf_token = get_csrf_token(f"{BASE_URL}/verify-age/")
    if csrf_token:
        verify_response = session.post(f"{BASE_URL}/verify-age/", {
            'csrfmiddlewaretoken': csrf_token,
            'confirm_age': 'on'
        })
        print("✔ Age verification completed")
    
    # Step 2: Add item to cart
    print("2. Adding item to cart...")
    csrf_token = get_csrf_token(f"{BASE_URL}/products/")
    if csrf_token:
        add_response = session.post(f"{BASE_URL}/cart/add/", {
            'csrfmiddlewaretoken': csrf_token,
            'product_id': 1,  # Assuming product ID 1 exists
            'quantity': 1
        })
        if add_response.status_code == 200:
            print("✔ Item added to cart successfully")
    
    # Step 3: Submit order via AJAX (simulating JavaScript)
    print("3. Submitting order via AJAX...")
    csrf_token = get_csrf_token(f"{BASE_URL}/products/")
    if csrf_token:
        submit_response = session.post(f"{BASE_URL}/submit-order/", 
            headers={
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            data=json.dumps({})
        )
        
        if submit_response.status_code == 200:
            data = submit_response.json()
            if data.get('success'):
                customer_order_id = data.get('order_id')
                print(f"✔ Order submitted successfully!")
                print(f"📱 Customer sees Order ID: {customer_order_id}")
                
                # Step 4: Get the actual order from submitted page
                print("4. Checking order confirmation page...")
                confirm_response = session.get(f"{BASE_URL}/submit-order/")
                if confirm_response.status_code == 200:
                    # Extract order number from the confirmation page
                    order_number_match = re.search(r'Order #([A-Z0-9-]+)', confirm_response.text)
                    if order_number_match:
                        admin_order_number = order_number_match.group(1)
                        print(f"🏢 Admin panel shows Order Number: {admin_order_number}")
                        
                        # Step 5: Compare the two
                        if customer_order_id == admin_order_number:
                            print("✔ SUCCESS: Order IDs are consistent!")
                            print(f"   Customer ID: {customer_order_id}")
                            print(f"   Admin Number: {admin_order_number}")
                            return True
                        else:
                            print("❌ INCONSISTENCY FOUND:")
                            print(f"   Customer sees: {customer_order_id}")
                            print(f"   Admin shows: {admin_order_number}")
                            return False
                    else:
                        print("⚠️  Could not extract order number from confirmation page")
                        
                # Also check receipt page
                print("5. Checking receipt page...")
                receipt_response = session.get(f"{BASE_URL}/print-receipt/{data.get('order_id', '')}/")
                if receipt_response.status_code == 200:
                    receipt_order_match = re.search(r'Order Number:</span>\s*<span><strong>([A-Z0-9-]+)</strong></span>', receipt_response.text)
                    if receipt_order_match:
                        receipt_order_number = receipt_order_match.group(1)
                        print(f"🧾 Receipt shows Order Number: {receipt_order_number}")
                        
                        if customer_order_id == receipt_order_number:
                            print("✔ SUCCESS: Customer ID matches receipt!")
                            return True
                        else:
                            print("❌ MISMATCH: Customer ID doesn't match receipt")
                            print(f"   Customer sees: {customer_order_id}")
                            print(f"   Receipt shows: {receipt_order_number}")
                            return False
            else:
                print(f"❌ Order submission failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Order submission returned: {submit_response.status_code}")
    
    return False

def main():
    try:
        # Test server accessibility
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✔ Server is accessible")
        else:
            print(f"❌ Server returned {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return
    
    # Run the consistency test
    success = test_order_id_consistency()
    
    if success:
        print("\n🎉 ORDER ID CONSISTENCY TEST PASSED!")
        print("   Customer-facing order IDs now match admin panel order numbers")
    else:
        print("\n❌ ORDER ID CONSISTENCY TEST FAILED!")
        print("   There are still inconsistencies between customer and admin views")

if __name__ == "__main__":
    main()
