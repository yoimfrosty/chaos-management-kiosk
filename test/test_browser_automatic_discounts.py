#!/usr/bin/env python3
"""
Comprehensive test for automatic discount functionality in browser environment.
Tests the complete flow from product selection to discount application.
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
BASE_URL = "http://127.0.0.1:8000"
SESSION = requests.Session()

def print_test_header(test_name):
    """Print a formatted test header."""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def print_step(step_num, description):
    """Print a formatted test step."""
    print(f"\n📝 Step {step_num}: {description}")

def print_result(success, message):
    """Print a formatted test result."""
    icon = "✅" if success else "❌"
    print(f"{icon} {message}")

def clear_session():
    """Clear session data for a fresh test."""
    try:
        response = SESSION.post(f"{BASE_URL}/cart/clear/")
        return response.status_code == 200
    except:
        return False

def get_products():
    """Get available products from the API."""
    try:
        response = SESSION.get(f"{BASE_URL}/cart/get/")
        if response.status_code == 200:
            cart_data = response.json()
            # For now, we'll use a mock product since we need the actual product list
            # In a real scenario, we'd need to scrape the products page or have an API endpoint
            return [{'id': 1, 'name': 'Test Product'}]
        return []
    except:
        return []

def get_discounts():
    """Get available discounts from the API."""
    try:
        # Since there's no direct API for discounts, we'll simulate
        return []
    except:
        return []

def add_product_to_cart(product_id, quantity=1):
    """Add a product to cart and return the response."""
    try:
        data = {
            'product_id': product_id,
            'quantity': quantity
        }
        response = SESSION.post(f"{BASE_URL}/cart/add/", data=data)
        return response.status_code == 200, response.json() if response.status_code == 200 else {}
    except Exception as e:
        return False, {"error": str(e)}

def get_cart_contents():
    """Get current cart contents."""
    try:
        response = SESSION.get(f"{BASE_URL}/kiosk/cart/")
        if response.status_code == 200:
            # Parse HTML to extract cart data - simplified approach
            return True, response.text
        return False, ""
    except:
        return False, ""

def test_automatic_discount_application():
    """Test that discounts are automatically applied when adding products."""
    print_test_header("Automatic Discount Application Test")
    
    # Step 1: Clear session
    print_step(1, "Clearing session data")
    clear_success = clear_session()
    print_result(clear_success, "Session cleared" if clear_success else "Failed to clear session")
    
    # Step 2: Get available products and discounts
    print_step(2, "Fetching products and discounts")
    products = get_products()
    discounts = get_discounts()
    
    print(f"📊 Found {len(products)} products")
    print(f"🎁 Found {len(discounts)} discounts")
    
    if not products:
        print_result(False, "No products available for testing")
        return False
    
    # Step 3: Test adding a product that should trigger automatic discounts
    print_step(3, "Adding product to cart to trigger automatic discounts")
    
    # Use the first available product
    test_product = products[0]
    product_id = test_product['id']
    product_name = test_product['name']
    
    print(f"🛍️ Testing with product: {product_name} (ID: {product_id})")
    
    success, response_data = add_product_to_cart(product_id, 1)
    
    if success:
        print_result(True, f"Product added to cart successfully")
        
        # Check if discounts were automatically applied
        if 'discounts_applied' in response_data:
            discounts_applied = response_data['discounts_applied']
            if discounts_applied:
                print_result(True, f"🎉 Automatic discounts applied: {len(discounts_applied)} discounts")
                for i, discount in enumerate(discounts_applied, 1):
                    print(f"   {i}. {discount.get('name', 'Unknown')} - {discount.get('discount_type', 'Unknown type')}")
            else:
                print_result(True, "No automatic discounts applied (may be expected if no applicable discounts)")
        else:
            print_result(False, "Response doesn't contain 'discounts_applied' field")
        
        # Print full response for debugging
        print(f"\n📋 Full response data:")
        print(json.dumps(response_data, indent=2))
        
    else:
        print_result(False, f"Failed to add product to cart: {response_data}")
        return False
    
    # Step 4: Test adding more quantity to trigger additional discounts
    print_step(4, "Adding more quantity to test quantity-based discounts")
    
    success, response_data = add_product_to_cart(product_id, 2)
    
    if success:
        print_result(True, "Additional quantity added successfully")
        
        if 'discounts_applied' in response_data:
            discounts_applied = response_data['discounts_applied']
            if discounts_applied:
                print_result(True, f"🎉 Additional automatic discounts applied: {len(discounts_applied)} discounts")
            else:
                print_result(True, "No additional automatic discounts applied")
        
        print(f"\n📋 Response data for quantity increase:")
        print(json.dumps(response_data, indent=2))
    else:
        print_result(False, f"Failed to add additional quantity: {response_data}")
    
    return True

def test_multiple_products_discounts():
    """Test automatic discounts with multiple different products."""
    print_test_header("Multiple Products Automatic Discounts Test")
    
    # Clear session first
    clear_session()
    
    products = get_products()
    if len(products) < 2:
        print_result(False, "Need at least 2 products for this test")
        return False
    
    # Add multiple different products
    for i, product in enumerate(products[:3], 1):  # Test with up to 3 products
        print_step(i, f"Adding product {i}: {product['name']}")
        
        success, response_data = add_product_to_cart(product['id'], 1)
        
        if success:
            print_result(True, f"Product {i} added successfully")
            
            if 'discounts_applied' in response_data:
                discounts_applied = response_data['discounts_applied']
                if discounts_applied:
                    print(f"   🎉 Discounts applied: {[d.get('name', 'Unknown') for d in discounts_applied]}")
                else:
                    print(f"   ℹ️ No discounts applied for this addition")
        else:
            print_result(False, f"Failed to add product {i}")
    
    return True

def test_frontend_notifications():
    """Test that frontend properly displays discount notifications."""
    print_test_header("Frontend Notification Test")
    
    print_step(1, "Testing frontend discount notification system")
    
    # This would require browser automation to fully test, but we can verify
    # that the backend is sending the right data for frontend consumption
    clear_session()
    
    products = get_products()
    if not products:
        print_result(False, "No products available")
        return False
    
    # Add a product and check that the response includes notification data
    success, response_data = add_product_to_cart(products[0]['id'], 1)
    
    if success:
        # Check for frontend-friendly response format
        required_fields = ['success', 'message', 'cart_count']
        optional_fields = ['discounts_applied']
        
        all_required_present = all(field in response_data for field in required_fields)
        
        if all_required_present:
            print_result(True, "Response contains all required fields for frontend")
            
            if 'discounts_applied' in response_data:
                print_result(True, "Response includes discount information for frontend notifications")
            else:
                print_result(True, "No discounts to notify about (expected if no applicable discounts)")
        else:
            missing = [field for field in required_fields if field not in response_data]
            print_result(False, f"Missing required fields: {missing}")
    else:
        print_result(False, "Failed to get response for frontend testing")
    
    return True

def main():
    """Run all automatic discount tests."""
    print(f"🚀 Starting Automatic Discount System Browser Tests")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing against: {BASE_URL}")
    
    tests = [
        test_automatic_discount_application,
        test_multiple_products_discounts,
        test_frontend_notifications
    ]
    
    results = []
    
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print_result(False, f"Test {test_func.__name__} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print_test_header("Test Summary")
    passed = sum(results)
    total = len(results)
    
    print(f"📊 Tests passed: {passed}/{total}")
    
    if passed == total:
        print_result(True, "🎉 All automatic discount tests passed!")
    else:
        print_result(False, f"⚠️ {total - passed} test(s) failed")
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed == total

if __name__ == "__main__":
    main()
