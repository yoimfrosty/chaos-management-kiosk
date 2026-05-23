#!/usr/bin/env python3
"""
Test Order Submission and Call Budtender Fixes
"""

import requests
import json
import re

BASE_URL = "http://localhost:8000"
session = requests.Session()

def get_csrf_token():
    """Get CSRF token from server"""
    response = session.get(f"{BASE_URL}/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    if csrf_match:
        return csrf_match.group(1)
    return None

def setup_session():
    """Set up session with age verification"""
    print("🔧 Setting up session...")
    # First get the age verification page
    response = session.get(f"{BASE_URL}/verify-age/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    
    if csrf_match:
        csrf_token = csrf_match.group(1)
        response = session.post(f"{BASE_URL}/verify-age/", {
            'csrfmiddlewaretoken': csrf_token,
            'confirm_age': 'on'
        })
        if response.status_code in [200, 302]:
            print("✔ Age verification completed")
            return True
    print("❌ Failed to setup session")
    return False

def test_call_budtender():
    """Test call budtender functionality"""
    print("\n🔍 Testing Call Budtender...")
    
    # Get CSRF token from main page to maintain session
    response = session.get(f"{BASE_URL}/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    csrf_token = csrf_match.group(1) if csrf_match else None
    
    if not csrf_token:
        print("❌ Could not get CSRF token")
        return False
        print("❌ Could not get CSRF token")
        return False
    
    # Test the call budtender endpoint
    response = session.post(f"{BASE_URL}/call-budtender/", 
        headers={
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        data=json.dumps({
            'kiosk_id': 'Kiosk_Main_Entrance'
        })
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Response data: {data}")
            if data.get('success') or data.get('status') == 'success':
                print("✔ Call budtender working correctly")
                return True
            else:
                print(f"❌ Call budtender failed: {data.get('message', 'Unknown error')}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text[:200]}")
    else:
        print(f"❌ Call budtender failed with status {response.status_code}")
        print(f"Response: {response.text[:200]}")
    
    return False

def test_order_submission():
    """Test order submission functionality"""
    print("\n🔍 Testing Order Submission...")
    
    # Get CSRF token from main page to maintain session
    response = session.get(f"{BASE_URL}/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    csrf_token = csrf_match.group(1) if csrf_match else None
    
    if not csrf_token:
        print("❌ Could not get CSRF token")
        return False
    
    # Add item to cart
    add_response = session.post(f"{BASE_URL}/cart/add/", {
        'csrfmiddlewaretoken': csrf_token,
        'product_id': 1,
        'quantity': 1
    })
    
    if add_response.status_code == 200:
        print("✔ Item added to cart")
    else:
        print(f"⚠️  Add to cart returned {add_response.status_code}")
    
    # Get fresh CSRF token for JSON request
    response = session.get(f"{BASE_URL}/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    csrf_token = csrf_match.group(1) if csrf_match else None
    
    # Test order submission with JSON request
    response = session.post(f"{BASE_URL}/submit-order/", 
        headers={
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        data=json.dumps({})
    )
    
    print(f"Order submission status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Response data: {data}")
            if data.get('success'):
                print("✔ Order submission working correctly")
                return True
            else:
                print(f"❌ Order submission failed: {data.get('error', 'Unknown error')}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text[:200]}")
    else:
        print(f"❌ Order submission failed with status {response.status_code}")
        print(f"Response: {response.text[:200]}")
    
    return False

def main():
    """Run all tests"""
    print("🧪 Testing Order Submission and Call Budtender Fixes")
    print("="*60)
    
    # Test server connectivity
    try:
        response = session.get(BASE_URL, timeout=5)
        print("✔ Server is running and accessible")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    # Setup session
    if not setup_session():
        print("❌ Could not setup session, tests may fail")
    
    # Run tests
    call_budtender_result = test_call_budtender()
    order_submission_result = test_order_submission()
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS:")
    print(f"Call Budtender: {'✔ PASSED' if call_budtender_result else '❌ FAILED'}")
    print(f"Order Submission: {'✔ PASSED' if order_submission_result else '❌ FAILED'}")
    
    if call_budtender_result and order_submission_result:
        print("\n🎉 ALL TESTS PASSED! Both issues have been fixed.")
    else:
        print("\n⚠️  Some tests failed. Please check the server logs for more details.")

if __name__ == "__main__":
    main()
