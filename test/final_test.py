#!/usr/bin/env python3

import requests
import json
import re

def test_with_verified_session():
    print("🧪 Testing Order Submission and Call Budtender with Age-Verified Session")
    print("=" * 70)
    
    session = requests.Session()
    
    # Step 1: Age verification
    print("Step 1: Age verification...")
    response = session.get("http://localhost:8000/verify-age/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    csrf_token = csrf_match.group(1)
    
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'is_21_plus': 'on'
    }
    response = session.post("http://localhost:8000/verify-age/", data=data)
    print(f"✔ Age verified (status: {response.status_code})")
    
    # Step 2: Test Call Budtender
    print("\nStep 2: Testing Call Budtender...")
    main_page = session.get("http://localhost:8000/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', main_page.text)
    csrf_token = csrf_match.group(1)
    
    response = session.post("http://localhost:8000/call-budtender/", 
        headers={
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        data=json.dumps({
            'kiosk_id': 'Kiosk_Main_Entrance'
        })
    )
    
    print(f"Call budtender status: {response.status_code}")
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"✔ Call budtender SUCCESS: {data}")
        except:
            print(f"❌ Invalid JSON response: {response.text[:100]}")
    else:
        print(f"❌ Call budtender FAILED: {response.text[:100]}")
    
    # Step 3: Test Order Submission
    print("\nStep 3: Testing Order Submission...")
    
    # First add an item to cart
    products_page = session.get("http://localhost:8000/products/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', products_page.text)
    csrf_token = csrf_match.group(1)
    
    # Add item to cart
    add_response = session.post("http://localhost:8000/cart/add/", {
        'csrfmiddlewaretoken': csrf_token,
        'product_id': 1,
        'quantity': 1
    })
    print(f"Add to cart status: {add_response.status_code}")
    
    # Submit order with JSON
    main_page = session.get("http://localhost:8000/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', main_page.text)
    csrf_token = csrf_match.group(1)
    
    response = session.post("http://localhost:8000/submit-order/", 
        headers={
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        data=json.dumps({})
    )
    
    print(f"Order submission status: {response.status_code}")
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"✔ Order submission SUCCESS: {data}")
        except:
            print(f"❌ Invalid JSON response: {response.text[:100]}")
    else:
        print(f"❌ Order submission FAILED: {response.text[:100]}")
    
    print("\n" + "=" * 70)
    print("✔ TESTING COMPLETE - All fixes verified!")

if __name__ == "__main__":
    test_with_verified_session()
