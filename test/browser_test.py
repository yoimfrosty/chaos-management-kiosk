#!/usr/bin/env python3

import requests
import json
import re

def test_browser_simulation():
    print("🧪 Browser Simulation Test - Order Submission & Call Budtender")
    print("=" * 65)
    
    session = requests.Session()
    
    # Simulate browser flow
    print("1. Loading welcome page...")
    response = session.get("http://localhost:8000/")
    print(f"   Status: {response.status_code}")
    
    print("2. Going to age verification...")
    response = session.get("http://localhost:8000/verify-age/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    csrf_token = csrf_match.group(1)
    print(f"   Status: {response.status_code}, CSRF: {csrf_token[:10]}...")
    
    print("3. Submitting age verification...")
    response = session.post("http://localhost:8000/verify-age/", {
        'csrfmiddlewaretoken': csrf_token,
        'is_21_plus': 'on'
    })
    print(f"   Status: {response.status_code}, URL: {response.url}")
    
    print("4. Testing Call Budtender (simulating JavaScript)...")
    # Get fresh CSRF token from product page
    response = session.get("http://localhost:8000/products/")
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    csrf_token = csrf_match.group(1) if csrf_match else None
    
    if csrf_token:
        response = session.post("http://localhost:8000/call-budtender/", 
            headers={
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
                'X-Requested-With': 'XMLHttpRequest'
            },
            data=json.dumps({
                'kiosk_id': 'Kiosk_Main_Entrance'
            })
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✔ SUCCESS: {data}")
            except:
                print(f"   ❌ Invalid JSON: {response.text[:100]}")
        else:
            print(f"   ❌ FAILED: {response.text[:200]}")
    
    print("\n5. Testing Order Submission...")
    # Add an item to cart first
    response = session.post("http://localhost:8000/cart/add/", {
        'csrfmiddlewaretoken': csrf_token,
        'product_id': 1,
        'quantity': 1
    })
    print(f"   Add to cart: {response.status_code}")
    
    # Submit order
    response = session.post("http://localhost:8000/submit-order/", 
        headers={
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
            'X-Requested-With': 'XMLHttpRequest'
        },
        data=json.dumps({})
    )
    
    print(f"   Submit order status: {response.status_code}")
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"   ✔ SUCCESS: {data}")
        except:
            print(f"   ❌ Invalid JSON: {response.text[:100]}")
    else:
        print(f"   ❌ FAILED: {response.text[:200]}")
    
    print("\n" + "=" * 65)
    print("🎉 Test Complete!")

if __name__ == "__main__":
    test_browser_simulation()
