#!/usr/bin/env python3
"""
Test script to verify the complete order success flow including:
1. Adding items to cart
2. Placing order
3. Verifying order success response
4. Testing session clear endpoint
"""

import requests
import json
import time

BASE_URL = "http://0.0.0.0:8000"
session = requests.Session()

def get_csrf_token():
    """Get CSRF token from the page"""
    response = session.get(f"{BASE_URL}/products/")
    if response.status_code == 200:
        # Get CSRF token from cookies
        csrf_token = session.cookies.get('csrftoken')
        if csrf_token:
            return csrf_token
        
        # Fallback: Extract CSRF token from the page
        for line in response.text.split('\n'):
            if 'csrfmiddlewaretoken' in line and 'value=' in line:
                start = line.find('value="') + 7
                end = line.find('"', start)
                return line[start:end]
    return None

def test_order_success_flow():
    """Test the complete order success flow"""
    print("🧪 Testing Order Success Flow")
    print("=" * 50)
    
    # Step 1: Get CSRF token and verify age
    print("1. Getting CSRF token and verifying age...")
    csrf_token = get_csrf_token()
    if not csrf_token:
        print("❌ Failed to get CSRF token")
        return False
    
    # Verify age to access products
    age_data = {
        'csrfmiddlewaretoken': csrf_token,
        'is_21_plus': 'on'  # This is the correct field name
    }
    age_response = session.post(f"{BASE_URL}/verify-age/", data=age_data, 
                               allow_redirects=False)
    print(f"   Age verification: {age_response.status_code}")
    
    # Follow redirect if needed
    if age_response.status_code == 302:
        redirect_url = age_response.headers.get('Location', '')
        print(f"   Redirect to: {redirect_url}")
        if redirect_url:
            follow_response = session.get(f"{BASE_URL}{redirect_url}")
            print(f"   Follow redirect: {follow_response.status_code}")
    
    # Get a fresh CSRF token after age verification
    csrf_token = get_csrf_token()
    if not csrf_token:
        print("❌ Failed to get fresh CSRF token")
        return False
    
    # Step 2: Add items to cart
    print("2. Adding items to cart...")
    cart_data = {
        'product_id': 1,
        'quantity': 2
    }
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrf_token
    }
    
    add_response = session.post(f"{BASE_URL}/cart/add/", 
                               data=cart_data, headers=headers)
    if add_response.status_code == 200:
        result = add_response.json()
        print(f"   ✅ Added to cart: {result.get('message', 'Success')}")
        cart_info = result.get('cart', {})
        print(f"   Cart total: ${cart_info.get('total', 'N/A')}")
    else:
        print(f"   ❌ Failed to add to cart: {add_response.status_code}")
        try:
            error_info = add_response.json()
            print(f"   Error: {error_info.get('error', 'Unknown error')}")
        except:
            print(f"   Response: {add_response.text}")
        return False
    
    # Step 3: Verify cart contents
    print("3. Checking cart contents...")
    cart_response = session.get(f"{BASE_URL}/cart/get/")
    if cart_response.status_code == 200:
        cart_info = cart_response.json()
        print(f"   Cart items: {cart_info.get('item_count', 0)}")
        print(f"   Cart total: ${cart_info.get('total', 0)}")
    else:
        print(f"   ❌ Failed to get cart: {cart_response.status_code}")
        return False
    
    # Step 4: Place order (this endpoint is csrf_exempt)
    print("4. Placing order...")
    order_data = {'submit_order': True}
    order_headers = {
        'Content-Type': 'application/json'
    }
    order_response = session.post(f"{BASE_URL}/place-order/", 
                                 json=order_data, headers=order_headers)
    
    if order_response.status_code == 200:
        order_result = order_response.json()
        print(f"   ✅ Order placed successfully!")
        print(f"   Order ID: {order_result.get('order_id', 'N/A')}")
        print(f"   Database ID: {order_result.get('order_db_id', 'N/A')}")
        print(f"   View URL: {order_result.get('view_order_url', 'N/A')}")
        order_db_id = order_result.get('order_db_id')
    else:
        print(f"   ❌ Failed to place order: {order_response.status_code}")
        try:
            error_info = order_response.json()
            print(f"   Error: {error_info.get('error', 'Unknown error')}")
        except:
            print(f"   Response: {order_response.text}")
        return False
    
    # Step 5: Verify order exists
    if order_db_id:
        print("5. Verifying order exists...")
        order_view_response = session.get(f"{BASE_URL}/view-order/{order_db_id}/")
        print(f"   Order view page: {order_view_response.status_code}")
    
    # Step 6: Test session clear endpoint (this endpoint is csrf_exempt)
    print("6. Testing session clear endpoint...")
    clear_headers = {
        'Content-Type': 'application/json'
    }
    clear_response = session.post(f"{BASE_URL}/clear-session-after-order/", 
                                 json={}, headers=clear_headers)
    
    if clear_response.status_code == 200:
        clear_result = clear_response.json()
        print(f"   ✅ Session clear: {clear_result.get('message', 'Success')}")
    else:
        print(f"   ❌ Failed to clear session: {clear_response.status_code}")
        try:
            error_info = clear_response.json()
            print(f"   Error: {error_info.get('error', 'Unknown error')}")
        except:
            print(f"   Response: {clear_response.text}")
    
    # Step 7: Verify cart is empty after session clear
    print("7. Verifying cart is empty after session clear...")
    final_cart_response = session.get(f"{BASE_URL}/cart/get/")
    if final_cart_response.status_code == 200:
        final_cart_info = final_cart_response.json()
        item_count = final_cart_info.get('item_count', 0)
        if item_count == 0:
            print(f"   ✅ Cart is empty: {item_count} items")
        else:
            print(f"   ⚠️ Cart still has items: {item_count}")
    else:
        print(f"   ❌ Failed to check final cart: {final_cart_response.status_code}")
    
    print("\n🎉 Order Success Flow Test Complete!")
    return True

if __name__ == "__main__":
    test_order_success_flow()
