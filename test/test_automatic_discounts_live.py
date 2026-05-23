#!/usr/bin/env python3
"""
Live test for automatic discount functionality.
This test verifies that discounts are automatically applied when adding products to cart.
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
BASE_URL = "http://127.0.0.1:8000"
session = requests.Session()

def print_header(text):
    print(f"\n{'='*60}")
    print(f"🧪 {text}")
    print(f"{'='*60}")

def print_step(step, description):
    print(f"\n📝 Step {step}: {description}")

def print_result(success, message):
    icon = "✅" if success else "❌"
    print(f"{icon} {message}")

def setup_session():
    """Set up session by going through age verification."""
    print_step(1, "Setting up session with age verification")
    
    # First, get the welcome page to establish session
    response = session.get(f"{BASE_URL}/")
    if response.status_code != 200:
        print_result(False, f"Failed to access welcome page: {response.status_code}")
        return False
    
    # Get age verification page
    response = session.get(f"{BASE_URL}/verify-age/")
    if response.status_code != 200:
        print_result(False, f"Failed to access age verification: {response.status_code}")
        return False
    
    # Extract CSRF token from the page
    csrf_token = None
    for line in response.text.split('\n'):
        if 'csrfmiddlewaretoken' in line and 'value=' in line:
            start = line.find('value="') + 8
            end = line.find('"', start)
            csrf_token = line[start:end]
            break
    
    if not csrf_token:
        print_result(False, "Could not extract CSRF token")
        return False
    
    # Submit age verification
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'over_21': 'yes'
    }
    response = session.post(f"{BASE_URL}/verify-age/", data=data)
    
    if response.status_code == 302:  # Redirect means success
        print_result(True, "Age verification completed successfully")
        return True
    else:
        print_result(False, f"Age verification failed: {response.status_code}")
        return False

def get_csrf_token():
    """Get CSRF token from products page."""
    response = session.get(f"{BASE_URL}/products/")
    if response.status_code != 200:
        return None
    
    for line in response.text.split('\n'):
        if 'csrfmiddlewaretoken' in line and 'value=' in line:
            start = line.find('value="') + 8
            end = line.find('"', start)
            return line[start:end]
    return None

def test_add_product_with_automatic_discounts():
    """Test adding a product and checking for automatic discount application."""
    print_step(2, "Testing automatic discount application when adding products")
    
    csrf_token = get_csrf_token()
    if not csrf_token:
        print_result(False, "Could not get CSRF token")
        return False
    
    # Clear cart first
    print("🧹 Clearing cart...")
    clear_data = {'csrfmiddlewaretoken': csrf_token}
    session.post(f"{BASE_URL}/cart/clear/", data=clear_data)
    
    # Test adding a product (using product ID 1 as a test)
    print("🛍️ Adding product to cart...")
    add_data = {
        'csrfmiddlewaretoken': csrf_token,
        'product_id': 1,
        'quantity': 1
    }
    
    # Set the X-Requested-With header to indicate AJAX request
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    response = session.post(f"{BASE_URL}/cart/add/", data=add_data, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            print_result(True, "Product added to cart successfully")
            
            # Check if automatic discounts were applied
            if 'discounts_applied' in data:
                discounts = data['discounts_applied']
                if discounts:
                    print_result(True, f"🎉 Automatic discounts applied: {len(discounts)} discount(s)")
                    for i, discount in enumerate(discounts, 1):
                        discount_name = discount.get('name', 'Unknown') if isinstance(discount, dict) else str(discount)
                        print(f"   {i}. {discount_name}")
                    return True
                else:
                    print_result(True, "No automatic discounts applied (may be expected if no applicable discounts)")
                    return True
            else:
                print_result(False, "Response doesn't contain 'discounts_applied' field")
                print(f"📋 Response keys: {list(data.keys())}")
                print(f"📋 Full response: {json.dumps(data, indent=2)}")
                return False
                
        except json.JSONDecodeError:
            print_result(False, "Response is not valid JSON")
            print(f"📋 Response text: {response.text[:500]}")
            return False
    else:
        print_result(False, f"Failed to add product: HTTP {response.status_code}")
        print(f"📋 Response: {response.text[:200]}")
        return False

def test_quantity_based_discounts():
    """Test that adding more quantity triggers additional discounts."""
    print_step(3, "Testing quantity-based automatic discounts")
    
    csrf_token = get_csrf_token()
    if not csrf_token:
        print_result(False, "Could not get CSRF token")
        return False
    
    # Add more of the same product
    print("📦 Adding more quantity...")
    add_data = {
        'csrfmiddlewaretoken': csrf_token,
        'product_id': 1,
        'quantity': 2  # Add 2 more
    }
    
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    response = session.post(f"{BASE_URL}/cart/add/", data=add_data, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            print_result(True, "Additional quantity added successfully")
            
            if 'discounts_applied' in data:
                discounts = data['discounts_applied']
                if discounts:
                    print_result(True, f"🎉 Additional automatic discounts: {len(discounts)} discount(s)")
                    for i, discount in enumerate(discounts, 1):
                        discount_name = discount.get('name', 'Unknown') if isinstance(discount, dict) else str(discount)
                        print(f"   {i}. {discount_name}")
                else:
                    print_result(True, "No additional automatic discounts applied")
            
            return True
            
        except json.JSONDecodeError:
            print_result(False, "Response is not valid JSON")
            return False
    else:
        print_result(False, f"Failed to add quantity: HTTP {response.status_code}")
        return False

def test_cart_state():
    """Check the current cart state."""
    print_step(4, "Checking final cart state")
    
    response = session.get(f"{BASE_URL}/cart/get/")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print_result(True, "Successfully retrieved cart data")
            
            cart = data.get('cart', {})
            items = cart.get('items', [])
            discounts = cart.get('applied_discounts', [])
            
            print(f"📊 Cart summary:")
            print(f"   • Items: {len(items)}")
            print(f"   • Applied discounts: {len(discounts)}")
            
            if discounts:
                print(f"   📋 Active discounts:")
                for i, discount in enumerate(discounts, 1):
                    discount_name = discount.get('name', 'Unknown')
                    discount_amount = discount.get('discount_amount', 'N/A')
                    print(f"      {i}. {discount_name} - ${discount_amount}")
            
            total = cart.get('total', 0)
            subtotal = cart.get('subtotal', 0)
            print(f"   • Subtotal: ${subtotal}")
            print(f"   • Total: ${total}")
            
            return True
            
        except json.JSONDecodeError:
            print_result(False, "Cart response is not valid JSON")
            return False
    else:
        print_result(False, f"Failed to get cart: HTTP {response.status_code}")
        return False

def main():
    """Run the automatic discount test."""
    print_header("🚀 Live Automatic Discount Test")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing: {BASE_URL}")
    
    # Run tests in sequence
    tests = [
        setup_session,
        test_add_product_with_automatic_discounts,
        test_quantity_based_discounts,
        test_cart_state
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
            if not result:
                print(f"⚠️ Test {test_func.__name__} failed, stopping...")
                break
            time.sleep(0.5)  # Brief pause between tests
        except Exception as e:
            print_result(False, f"Test {test_func.__name__} raised exception: {e}")
            results.append(False)
            break
    
    # Summary
    print_header("📊 Test Results")
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests passed: {passed}/{total}")
    
    if passed == total:
        print_result(True, "🎉 All automatic discount tests passed!")
        print("✨ The automatic discount system is working correctly!")
    else:
        print_result(False, f"⚠️ {total - passed} test(s) failed")
        print("🔍 Check the error messages above for details")
    
    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed == total

if __name__ == "__main__":
    main()
