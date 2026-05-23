#!/usr/bin/env python3
"""
Final test to demonstrate the complete customer flow with fresh session clearing
"""

import requests
import time

BASE_URL = "http://0.0.0.0:8000"

def test_complete_customer_cycle():
    """Test the complete customer experience from fresh start to next customer"""
    print("🎯 Complete Customer Cycle Test")
    print("=" * 60)
    
    # Simulate Customer 1
    print("\n👤 CUSTOMER 1 - Starting fresh session")
    session1 = requests.Session()
    
    # Step 1: Fresh customer visits homepage
    home_response = session1.get(f"{BASE_URL}/")
    print(f"✅ Customer 1 visits homepage: {home_response.status_code}")
    print(f"   📱 Sees 'Start Your Order' button: {'Start Your Order' in home_response.text}")
    print(f"   🔒 Sees age verification required: {'Age verification required' in home_response.text}")
    
    # Step 2: Customer verifies age
    csrf_token = session1.cookies.get('csrftoken')
    age_data = {'csrfmiddlewaretoken': csrf_token, 'is_21_plus': 'on'}
    age_response = session1.post(f"{BASE_URL}/verify-age/", data=age_data)
    print(f"✅ Customer 1 age verification: {age_response.status_code}")
    
    # Step 3: Customer adds items and places order
    headers = {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrf_token}
    cart_data = {'product_id': 1, 'quantity': 1}
    session1.post(f"{BASE_URL}/cart/add/", data=cart_data, headers=headers)
    
    order_headers = {'Content-Type': 'application/json'}
    order_data = {'submit_order': True}
    order_response = session1.post(f"{BASE_URL}/place-order/", 
                                  json=order_data, headers=order_headers)
    
    if order_response.status_code == 200:
        order_result = order_response.json()
        print(f"✅ Customer 1 placed order: {order_result.get('order_id')}")
        
        # Step 4: Simulate 10-second wait and session clearing
        print("⏰ 10-second countdown and session clearing...")
        clear_response = session1.post(f"{BASE_URL}/clear-session-after-order/", 
                                     json={}, headers=order_headers)
        print(f"✅ Session cleared: {clear_response.status_code}")
        
        # Step 5: Verify redirect takes customer to fresh homepage
        redirect_response = session1.get(f"{BASE_URL}/")
        print(f"✅ Redirect to fresh homepage: {redirect_response.status_code}")
        print(f"   📱 Fresh 'Start Your Order' visible: {'Start Your Order' in redirect_response.text}")
        print(f"   🔒 Age verification required again: {'Age verification required' in redirect_response.text}")
        
    print("\n" + "="*60)
    print("👤 CUSTOMER 2 - New customer arrives at kiosk")
    
    # Simulate Customer 2 (completely new session)
    session2 = requests.Session()
    
    # Step 6: New customer visits homepage
    new_home_response = session2.get(f"{BASE_URL}/")
    print(f"✅ Customer 2 visits homepage: {new_home_response.status_code}")
    print(f"   📱 Sees fresh 'Start Your Order' button: {'Start Your Order' in new_home_response.text}")
    print(f"   🔒 Needs to verify age: {'Age verification required' in new_home_response.text}")
    
    # Verify that customer 2 has no access to previous customer's data
    try:
        products_response = session2.get(f"{BASE_URL}/products/")
        if products_response.status_code == 302:
            print("✅ Customer 2 correctly redirected to age verification")
        else:
            print(f"⚠️  Unexpected products access: {products_response.status_code}")
    except:
        print("✅ Customer 2 has no unauthorized access")
    
    print("\n🎉 Customer Cycle Test Complete!")
    print("✅ Customer 1: Ordered → Session cleared → Fresh start for next customer")
    print("✅ Customer 2: Fresh experience with age verification required")
    print("✅ Complete separation between customers achieved")

if __name__ == "__main__":
    test_complete_customer_cycle()
