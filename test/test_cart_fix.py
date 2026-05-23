#!/usr/bin/env python3

import requests
import re
import json

def test_cart_functionality():
    """Test the cart functionality with proper session handling"""
    print("🧪 Testing cart functionality...")
    
    # Django test setup
    BASE_URL = "http://127.0.0.1:8000"
    session = requests.Session()
    
    def get_csrf_token(response_text):
        """Extract CSRF token from HTML response"""
        match = re.search(r'<input[^>]*name=[\'"]csrfmiddlewaretoken[\'"][^>]*value=[\'"]([^\'\"]*)[\'"]', response_text)
        return match.group(1) if match else None
    
    try:
        # Step 1: Get age verification page
        print("1. Getting age verification page...")
        response = session.get(f"{BASE_URL}/verify-age/")
        csrf_token = get_csrf_token(response.text)
        print(f"   CSRF token: {csrf_token[:20] if csrf_token else 'None'}...")
        
        # Step 2: Submit age verification
        print("2. Submitting age verification...")
        response = session.post(f"{BASE_URL}/verify-age/", data={
            'is_21_plus': 'on',
            'csrfmiddlewaretoken': csrf_token
        }, allow_redirects=False)
        print(f"   Response status: {response.status_code}")
        
        # Step 3: Check if cart is accessible
        print("3. Checking cart accessibility...")
        response = session.get(f"{BASE_URL}/cart/get/", headers={'X-Requested-With': 'XMLHttpRequest'})
        print(f"   Cart response status: {response.status_code}")
        if response.status_code == 200:
            cart_data = response.json()
            print(f"   Initial cart: {cart_data.get('item_count', 0)} items")
        
        # Step 4: Get products page for CSRF token
        print("4. Getting products page...")
        response = session.get(f"{BASE_URL}/products/")
        csrf_token = get_csrf_token(response.text)
        print(f"   New CSRF token: {csrf_token[:20] if csrf_token else 'None'}...")
        
        # Step 5: Add item to cart
        print("5. Adding item to cart...")
        response = session.post(f"{BASE_URL}/cart/add/", data={
            'product_id': 1,
            'quantity': 1,
            'csrfmiddlewaretoken': csrf_token
        }, headers={'X-Requested-With': 'XMLHttpRequest'})
        
        print(f"   Add to cart response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                add_response = response.json()
                print(f"   ✅ Success! Response keys: {list(add_response.keys())}")
                
                # Check if cart structure is as expected
                if 'cart' in add_response and 'items' in add_response['cart']:
                    print(f"   Cart now has {len(add_response['cart']['items'])} items")
                    for item in add_response['cart']['items']:
                        print(f"     - {item['name']} (Order Item ID: {item['id']}, Product ID: {item['product_id']})")
                else:
                    print("   ⚠️ Cart structure unexpected!")
                    print(f"   Response: {json.dumps(add_response, indent=2)}")
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ Failed to parse JSON: {e}")
                print(f"   Raw response: {response.text[:200]}...")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            print(f"   Response: {response.text[:500]}...")
        
        # Step 6: Test order placement
        print("6. Testing order placement...")
        response = session.post(f"{BASE_URL}/place-order/", 
                               json={'submit_order': True},
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-CSRFToken': csrf_token,
                                   'X-Requested-With': 'XMLHttpRequest'
                               })
        
        print(f"   Order placement response status: {response.status_code}")
        if response.status_code == 200:
            try:
                order_response = response.json()
                print(f"   ✅ Order placed! Response: {json.dumps(order_response, indent=2)}")
            except json.JSONDecodeError as e:
                print(f"   ❌ Failed to parse JSON: {e}")
                print(f"   Response text: {response.text}")
        else:
            print(f"   ❌ Order placement failed: {response.text[:500]}...")
        
        print("✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cart_functionality()
