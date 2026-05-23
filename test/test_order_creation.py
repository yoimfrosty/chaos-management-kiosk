#!/usr/bin/env python3
"""
Test order placement to create notifications.
"""

import requests
import json
from datetime import date

BASE_URL = "http://127.0.0.1:8000"

def create_test_order():
    """Create a test order to generate notifications"""
    print("🛒 Creating Test Order")
    print("=" * 30)
    
    session = requests.Session()
    
    # Step 1: Get the welcome page to establish session
    print("1. Establishing session...")
    response = session.get(f"{BASE_URL}/")
    csrf_token = None
    if 'csrftoken' in session.cookies:
        csrf_token = session.cookies['csrftoken']
        print(f"   ✅ CSRF token: {csrf_token[:10]}...")
    else:
        print("   ❌ No CSRF token found")
        return False
    
    # Step 2: Submit age verification
    print("2. Age verification...")
    age_data = {
        'customer_name': 'Test Customer',
        'customer_contact': 'test@example.com',
        'customer_birthdate': '1990-01-01',
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(f"{BASE_URL}/verify-age/", data=age_data, allow_redirects=False)
    if response.status_code in [200, 302]:
        print("   ✅ Age verified")
    else:
        print(f"   ❌ Age verification failed: {response.status_code}")
        return False
    
    # Step 3: Go to products page and add items
    print("3. Adding product to cart...")
    
    # First let's check what products are available
    products_response = session.get(f"{BASE_URL}/products/")
    if products_response.status_code == 200:
        print("   ✅ Products page accessible")
        
        # Try to add a product (assuming product ID 1 exists)
        cart_data = {
            'product_id': 1,
            'quantity': 1,
            'csrfmiddlewaretoken': csrf_token
        }
        
        add_response = session.post(
            f"{BASE_URL}/cart/add/",
            data=cart_data,
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        
        if add_response.status_code == 200:
            try:
                cart_result = add_response.json()
                if cart_result.get('success'):
                    print("   ✅ Product added to cart")
                else:
                    print(f"   ❌ Failed to add product: {cart_result.get('error')}")
                    return False
            except json.JSONDecodeError:
                print("   ❌ Invalid response from cart/add")
                return False
        else:
            print(f"   ❌ Cart add failed: {add_response.status_code}")
            return False
    else:
        print(f"   ❌ Products page failed: {products_response.status_code}")
        return False
    
    # Step 4: Submit the order
    print("4. Submitting order...")
    
    order_response = session.post(
        f"{BASE_URL}/submit-order/",
        headers={
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        json={}
    )
    
    if order_response.status_code == 200:
        try:
            order_result = order_response.json()
            if order_result.get('success'):
                print(f"   ✅ Order placed: {order_result.get('order_id')}")
                return True
            else:
                print(f"   ❌ Order failed: {order_result.get('error')}")
                return False
        except json.JSONDecodeError:
            print(f"   ❌ Invalid JSON from order submission")
            return False
    else:
        print(f"   ❌ Order submission failed: {order_response.status_code}")
        print(f"   Response: {order_response.text[:200]}...")
        return False

def check_notifications():
    """Check if notifications were created"""
    print("\n🔔 Checking Notifications")
    print("=" * 30)
    
    session = requests.Session()
    
    # Check order notifications
    print("1. Order notifications...")
    response = session.get(f"{BASE_URL}/check-pending-orders/")
    if response.status_code == 200:
        data = response.json()
        count = data.get('count', 0)
        print(f"   📋 Found {count} pending order notifications")
        if count > 0:
            for notification in data.get('pending_notifications', []):
                print(f"      - Order: {notification.get('order_number')}")
                print(f"        Customer: {notification.get('customer_name')}")
                print(f"        Total: ${notification.get('total_amount')}")
        return count > 0
    else:
        print(f"   ❌ Failed to check: {response.status_code}")
        return False

if __name__ == "__main__":
    print("🧪 Order Notification Test")
    print("=" * 40)
    
    # Create test order
    order_created = create_test_order()
    
    if order_created:
        # Check for notifications
        import time
        time.sleep(1)  # Give the system a moment
        notifications_found = check_notifications()
        
        if notifications_found:
            print("\n🎉 SUCCESS! Order notification system is working!")
            print("\n📝 Next steps:")
            print("   1. Go to: http://127.0.0.1:8000/admin/")
            print("   2. Log in with admin credentials")  
            print("   3. You should see notification indicators and pop-ups")
            print("   4. Check the Orders and Order Notifications admin pages")
        else:
            print("\n❌ Order was created but no notifications found")
    else:
        print("\n❌ Failed to create test order")
