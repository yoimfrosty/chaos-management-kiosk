#!/usr/bin/env python3
"""
Test to verify the exact redirect behavior after order completion
"""

import requests
import time

BASE_URL = "http://0.0.0.0:8000"
session = requests.Session()

def test_redirect_flow():
    """Test the exact redirect flow after order completion"""
    print("🧪 Testing Order Completion Redirect Flow")
    print("=" * 50)
    
    # Step 1: Get CSRF token and verify age
    response = session.get(f"{BASE_URL}/products/")
    csrf_token = session.cookies.get('csrftoken')
    
    age_data = {'csrfmiddlewaretoken': csrf_token, 'is_21_plus': 'on'}
    session.post(f"{BASE_URL}/verify-age/", data=age_data)
    
    # Step 2: Add item to cart
    headers = {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrf_token}
    cart_data = {'product_id': 1, 'quantity': 1}
    session.post(f"{BASE_URL}/cart/add/", data=cart_data, headers=headers)
    
    # Step 3: Place order
    order_headers = {'Content-Type': 'application/json'}
    order_data = {'submit_order': True}
    order_response = session.post(f"{BASE_URL}/place-order/", 
                                 json=order_data, headers=order_headers)
    
    if order_response.status_code == 200:
        order_result = order_response.json()
        print(f"✅ Order placed: {order_result.get('order_id')}")
        
        # Step 4: Test what happens when we call the clear session endpoint
        clear_response = session.post(f"{BASE_URL}/clear-session-after-order/", 
                                     json={}, headers=order_headers)
        
        if clear_response.status_code == 200:
            print("✅ Session cleared successfully")
            
            # Step 5: Test what URL we would be redirected to
            print("\n🔍 Testing redirect destinations:")
            
            # Test root URL
            root_response = session.get(f"{BASE_URL}/")
            print(f"   Root URL (/): {root_response.status_code}")
            print(f"   Contains 'Welcome to Ocean City Hemp': {'Welcome to Ocean City Hemp' in root_response.text}")
            print(f"   Contains 'Start Your Order': {'Start Your Order' in root_response.text}")
            
            # Test products URL
            products_response = session.get(f"{BASE_URL}/products/")
            print(f"   Products URL (/products/): {products_response.status_code}")
            if products_response.status_code == 302:
                print(f"   Redirects to: {products_response.headers.get('Location', 'Unknown')}")
            
            print(f"\n📍 Current JavaScript redirect URL should be: /")
            print(f"📍 This should show the welcome page with 'Start Your Order' button")
            
        else:
            print(f"❌ Session clear failed: {clear_response.status_code}")
    else:
        print(f"❌ Order placement failed: {order_response.status_code}")

if __name__ == "__main__":
    test_redirect_flow()
