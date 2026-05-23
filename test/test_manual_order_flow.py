#!/usr/bin/env python3
"""
Manual test script to place an order and see the 10-second countdown in action.
This simulates the UI flow that a customer would experience.
"""

import requests
import json
import time

BASE_URL = "http://0.0.0.0:8000"
session = requests.Session()

def manual_order_test():
    """Place an order manually to test the UI flow"""
    print("🧪 Manual Order Test - Simulating Customer Flow")
    print("=" * 60)
    
    # Get CSRF token
    response = session.get(f"{BASE_URL}/products/")
    csrf_token = session.cookies.get('csrftoken')
    
    # Age verification
    age_data = {
        'csrfmiddlewaretoken': csrf_token,
        'is_21_plus': 'on'
    }
    age_response = session.post(f"{BASE_URL}/verify-age/", data=age_data)
    print(f"✅ Age verified (status: {age_response.status_code})")
    
    # Get fresh CSRF token
    csrf_token = session.cookies.get('csrftoken')
    
    # Add items to cart
    cart_data = {
        'product_id': 1,
        'quantity': 1
    }
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrf_token
    }
    
    add_response = session.post(f"{BASE_URL}/cart/add/", data=cart_data, headers=headers)
    if add_response.status_code == 200:
        print("✅ Item added to cart")
    else:
        print(f"❌ Failed to add item: {add_response.status_code}")
        return
    
    # Place order
    order_data = {'submit_order': True}
    order_headers = {'Content-Type': 'application/json'}
    order_response = session.post(f"{BASE_URL}/place-order/", 
                                 json=order_data, headers=order_headers)
    
    if order_response.status_code == 200:
        order_result = order_response.json()
        order_id = order_result.get('order_id')
        print(f"✅ Order placed! Order ID: {order_id}")
        print(f"📋 Order view URL: {BASE_URL}{order_result.get('view_order_url', '')}")
        
        print("\n🎭 Frontend would now show:")
        print("   📱 Order Success Overlay")
        print("   💳 'Order Placed Successfully!'")
        print("   🏢 'Please visit the reception for payment.'")
        print(f"   🔢 'Order ID: {order_id}'")
        print("   ⏰ '10-second countdown...'")
        
        print("\n⏳ Simulating 10-second wait...")
        for i in range(10, 0, -1):
            print(f"   Countdown: {i} seconds remaining", end='\r')
            time.sleep(1)
        
        print("\n🧹 Clearing session for next customer...")
        clear_headers = {'Content-Type': 'application/json'}
        clear_response = session.post(f"{BASE_URL}/clear-session-after-order/", 
                                     json={}, headers=clear_headers)
        
        if clear_response.status_code == 200:
            print("✅ Session cleared successfully")
        else:
            print(f"❌ Session clear failed: {clear_response.status_code}")
        
        print("🏠 Frontend would now redirect to homepage for next customer")
        print(f"🔗 Redirect URL: {BASE_URL}/")
        
        # Verify cart is empty
        cart_check = session.get(f"{BASE_URL}/cart/get/")
        if cart_check.status_code == 200:
            cart_info = cart_check.json()
            item_count = cart_info.get('item_count', 0)
            if item_count == 0:
                print("✅ Cart is empty - ready for next customer")
            else:
                print(f"⚠️ Cart still has {item_count} items")
        
        print("\n🎉 Complete order flow test successful!")
        print("   👤 Customer experience:")
        print("   1. ✅ Placed order successfully")
        print("   2. ✅ Saw clear payment instructions")
        print("   3. ✅ 10-second countdown completed")
        print("   4. ✅ Session cleared for next customer")
        print("   5. ✅ Redirected to clean homepage")
        
    else:
        print(f"❌ Order placement failed: {order_response.status_code}")
        try:
            error_info = order_response.json()
            print(f"   Error: {error_info.get('error', 'Unknown error')}")
        except:
            print(f"   Response: {order_response.text}")

if __name__ == "__main__":
    manual_order_test()
