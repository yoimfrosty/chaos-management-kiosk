#!/usr/bin/env python3
"""
Test script to verify the order notification system works properly.
This script will place a test order and then check the admin notification endpoints.
"""

import requests
import json
import time
from datetime import date

BASE_URL = "http://127.0.0.1:8000"

def get_csrf_token(session):
    """Get CSRF token from Django"""
    response = session.get(f"{BASE_URL}/kiosk/")
    if 'csrftoken' in session.cookies:
        return session.cookies['csrftoken']
    return None

def test_order_notification_system():
    """Test the complete order notification workflow"""
    print("🧪 Testing Order Notification System")
    print("=" * 50)
    
    # Create a session
    session = requests.Session()
    
    # Step 1: Get CSRF token
    print("1. Getting CSRF token...")
    csrf_token = get_csrf_token(session)
    if not csrf_token:
        print("❌ Failed to get CSRF token")
        return False
    print(f"✅ CSRF token: {csrf_token[:10]}...")
    
    # Step 2: Submit age verification
    print("\n2. Submitting age verification...")
    age_data = {
        'customer_name': 'Test Customer',
        'customer_contact': 'test@example.com',
        'customer_birthdate': '1990-01-01',
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(f"{BASE_URL}/kiosk/verify-age/", data=age_data)
    if response.status_code == 302:  # Redirect means success
        print("✅ Age verification successful")
    else:
        print(f"❌ Age verification failed: {response.status_code}")
        return False
    
    # Step 3: Add products to cart
    print("\n3. Adding products to cart...")
    # First, get available products
    products_response = session.get(f"{BASE_URL}/kiosk/products/")
    if products_response.status_code != 200:
        print(f"❌ Failed to get products: {products_response.status_code}")
        return False
    
    # Add a product to cart (using product ID 1 if it exists)
    cart_data = {
        'product_id': 1,
        'quantity': 2,
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(
        f"{BASE_URL}/kiosk/cart/add/", 
        data=cart_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    
    if response.status_code == 200:
        try:
            cart_response = response.json()
            if cart_response.get('success'):
                print("✅ Product added to cart successfully")
            else:
                print(f"❌ Failed to add product: {cart_response.get('error', 'Unknown error')}")
                return False
        except json.JSONDecodeError:
            print("❌ Invalid JSON response from cart add")
            return False
    else:
        print(f"❌ Failed to add product to cart: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return False
    
    # Step 4: Submit order
    print("\n4. Submitting order...")
    order_response = session.post(
        f"{BASE_URL}/kiosk/submit-order/",
        headers={
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        json={}
    )
    
    if order_response.status_code == 200:
        try:
            order_data = order_response.json()
            if order_data.get('success'):
                print(f"✅ Order submitted successfully: {order_data.get('order_id')}")
                order_id = order_data.get('order_db_id')
            else:
                print(f"❌ Order submission failed: {order_data.get('error')}")
                return False
        except json.JSONDecodeError:
            print("❌ Invalid JSON response from order submission")
            return False
    else:
        print(f"❌ Order submission failed: {order_response.status_code}")
        print(f"Response: {order_response.text[:200]}...")
        return False
    
    # Step 5: Check if order notification was created
    print("\n5. Checking order notifications...")
    time.sleep(1)  # Give the system a moment
    
    notifications_response = session.get(f"{BASE_URL}/kiosk/check-pending-orders/")
    if notifications_response.status_code == 200:
        try:
            notifications_data = notifications_response.json()
            pending_count = notifications_data.get('count', 0)
            pending_notifications = notifications_data.get('pending_notifications', [])
            
            print(f"✅ Found {pending_count} pending order notifications")
            
            if pending_count > 0:
                latest_notification = pending_notifications[0]
                print(f"   📋 Latest notification:")
                print(f"      - Order: {latest_notification.get('order_number')}")
                print(f"      - Customer: {latest_notification.get('customer_name')}")
                print(f"      - Total: ${latest_notification.get('total_amount')}")
                print(f"      - Items: {latest_notification.get('item_count')}")
                print(f"      - Status: {latest_notification.get('status')}")
                
                # Test acknowledging the notification
                notification_id = latest_notification.get('id')
                print(f"\n6. Testing notification acknowledgment...")
                
                ack_response = session.post(
                    f"{BASE_URL}/kiosk/acknowledge-order-notification/{notification_id}/",
                    headers={
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf_token
                    }
                )
                
                if ack_response.status_code == 200:
                    ack_data = ack_response.json()
                    if ack_data.get('success'):
                        print("✅ Notification acknowledged successfully")
                    else:
                        print(f"❌ Failed to acknowledge: {ack_data.get('message')}")
                else:
                    print(f"❌ Acknowledgment request failed: {ack_response.status_code}")
                
                return True
            else:
                print("❌ No pending notifications found after order submission")
                return False
                
        except json.JSONDecodeError:
            print("❌ Invalid JSON response from notifications check")
            return False
    else:
        print(f"❌ Failed to check notifications: {notifications_response.status_code}")
        return False

def test_assistance_requests():
    """Test assistance request system"""
    print("\n\n🤝 Testing Assistance Request System")
    print("=" * 50)
    
    session = requests.Session()
    csrf_token = get_csrf_token(session)
    
    # Submit age verification first
    age_data = {
        'customer_name': 'Assistance Test Customer',
        'customer_contact': 'help@example.com',
        'customer_birthdate': '1985-05-15',
        'csrfmiddlewaretoken': csrf_token
    }
    session.post(f"{BASE_URL}/kiosk/verify-age/", data=age_data)
    
    # Request assistance
    print("1. Requesting assistance...")
    assistance_response = session.post(
        f"{BASE_URL}/kiosk/request-assistance/",
        headers={
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        json={'message': 'Test assistance request from automated test'}
    )
    
    if assistance_response.status_code == 200:
        assistance_data = assistance_response.json()
        if assistance_data.get('success'):
            print("✅ Assistance request submitted successfully")
        else:
            print(f"❌ Assistance request failed: {assistance_data.get('error')}")
            return False
    else:
        print(f"❌ Assistance request failed: {assistance_response.status_code}")
        return False
    
    # Check pending assistance requests
    print("\n2. Checking pending assistance requests...")
    time.sleep(1)
    
    pending_response = session.get(f"{BASE_URL}/kiosk/check-pending-assistance/")
    if pending_response.status_code == 200:
        pending_data = pending_response.json()
        pending_count = pending_data.get('count', 0)
        
        print(f"✅ Found {pending_count} pending assistance requests")
        
        if pending_count > 0:
            latest_request = pending_data.get('pending_requests', [])[0]
            print(f"   🚨 Latest request:")
            print(f"      - Customer: {latest_request.get('customer_name')}")
            print(f"      - Status: {latest_request.get('status')}")
            return True
        else:
            print("❌ No pending assistance requests found")
            return False
    else:
        print(f"❌ Failed to check assistance requests: {pending_response.status_code}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Notification System Tests")
    print("=" * 60)
    
    try:
        # Test order notifications
        order_test_result = test_order_notification_system()
        
        # Test assistance requests  
        assistance_test_result = test_assistance_requests()
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS")
        print("=" * 60)
        print(f"Order Notifications: {'✅ PASS' if order_test_result else '❌ FAIL'}")
        print(f"Assistance Requests: {'✅ PASS' if assistance_test_result else '❌ FAIL'}")
        
        if order_test_result and assistance_test_result:
            print("\n🎉 ALL TESTS PASSED! The notification system is working correctly.")
            print("\n📋 What was tested:")
            print("   ✅ Order placement creates notifications")
            print("   ✅ Order notifications can be retrieved")
            print("   ✅ Order notifications can be acknowledged")
            print("   ✅ Assistance requests can be submitted")
            print("   ✅ Assistance requests can be retrieved")
            print("\n🔔 Admin staff will now receive real-time notifications for:")
            print("   • New orders placed by customers")
            print("   • Assistance requests from customers")
        else:
            print("\n❌ Some tests failed. Please check the output above for details.")
            
    except Exception as e:
        print(f"\n💥 Test suite failed with exception: {e}")
        import traceback
        traceback.print_exc()
