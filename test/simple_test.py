#!/usr/bin/env python3
"""
Simple test to verify age verification works and test endpoints
"""

import requests
import json
import re

BASE_URL = "http://localhost:8000"
session = requests.Session()

def test_complete_flow():
    """Test the complete flow: age verification -> test endpoints"""
    print("🧪 Testing Complete Flow")
    print("=" * 50)
    
    print("Step 1: Getting age verification page...")
    response = session.get(f"{BASE_URL}/verify-age/")
    print(f"✔ Age verification page loaded (status: {response.status_code})")
    
    # Extract CSRF token from the form
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    if not csrf_match:
        print("❌ Could not find CSRF token")
        return False
    
    csrf_token = csrf_match.group(1)
    print(f"✔ CSRF token obtained: {csrf_token[:10]}...")
    
    print("\nStep 2: Submitting age verification...")
    verify_response = session.post(f"{BASE_URL}/verify-age/", {
        'csrfmiddlewaretoken': csrf_token,
        'is_21_plus': 'on'  # Fixed: use correct field name
    })
    print(f"✔ Age verification submitted (status: {verify_response.status_code})")
    
    # Check if we were redirected to products page
    if verify_response.status_code == 302 or 'product' in verify_response.url:
        print("✔ Successfully redirected after age verification")
    
    print("\nStep 3: Testing Call Budtender...")
    # Get a fresh CSRF token for JSON request
    main_page = session.get(f"{BASE_URL}/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', main_page.text)
    if csrf_match:
        csrf_token = csrf_match.group(1)
        print(f"✔ Fresh CSRF token for JSON: {csrf_token[:10]}...")
        
        response = session.post(f"{BASE_URL}/call-budtender/", 
            headers={
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            data=json.dumps({
                'kiosk_id': 'Kiosk_Main_Entrance'
            })
        )
        
        print(f"Call budtender response: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✔ Call budtender success: {data}")
            except:
                print(f"❌ Invalid JSON: {response.text[:100]}")
        else:
            print(f"❌ Call budtender failed: {response.text[:100]}")
    
    print("\nStep 4: Testing Order Submission...")
    # First add something to cart
    main_page = session.get(f"{BASE_URL}/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', main_page.text)
    if csrf_match:
        csrf_token = csrf_match.group(1)
        
        # Try to add item to cart
        add_response = session.post(f"{BASE_URL}/cart/add/", {
            'csrfmiddlewaretoken': csrf_token,
            'product_id': 1,
            'quantity': 1
        })
        print(f"Add to cart response: {add_response.status_code}")
        
        # Test order submission
        order_response = session.post(f"{BASE_URL}/submit-order/", 
            headers={
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            data=json.dumps({})
        )
        
        print(f"Order submission response: {order_response.status_code}")
        if order_response.status_code == 200:
            try:
                data = order_response.json()
                print(f"✔ Order submission success: {data}")
            except:
                print(f"❌ Invalid JSON: {order_response.text[:100]}")
        else:
            print(f"❌ Order submission failed: {order_response.text[:100]}")

if __name__ == "__main__":
    test_complete_flow()
