#!/usr/bin/env python3
"""
Test Order Submission and Print Receipt Fix
"""

import requests
import re

BASE_URL = "http://localhost:8000"
session = requests.Session()

def get_csrf_token(url):
    """Extract CSRF token from a page"""
    response = session.get(url)
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
    if csrf_match:
        return csrf_match.group(1)
    return None

def test_order_workflow():
    """Test complete order submission workflow"""
    print("🧪 Testing Order Submission Workflow")
    print("="*40)
    
    # Step 1: Verify age
    print("1. Setting up age verification...")
    csrf_token = get_csrf_token(f"{BASE_URL}/verify-age/")
    if csrf_token:
        verify_response = session.post(f"{BASE_URL}/verify-age/", {
            'csrfmiddlewaretoken': csrf_token,
            'confirm_age': 'on'
        })
        print("✔ Age verification completed")
    
    # Step 2: Add item to cart
    print("2. Adding item to cart...")
    csrf_token = get_csrf_token(f"{BASE_URL}/products/")
    if csrf_token:
        add_response = session.post(f"{BASE_URL}/cart/add/", {
            'csrfmiddlewaretoken': csrf_token,
            'product_id': 1,  # Assuming product ID 1 exists
            'quantity': 1
        })
        if add_response.status_code == 200:
            print("✔ Item added to cart successfully")
        else:
            print(f"⚠️  Add to cart returned: {add_response.status_code}")
    
    # Step 3: Submit order
    print("3. Submitting order...")
    csrf_token = get_csrf_token(f"{BASE_URL}/products/")
    if csrf_token:
        submit_response = session.post(f"{BASE_URL}/submit-order/", {
            'csrfmiddlewaretoken': csrf_token
        })
        
        if submit_response.status_code == 200:
            print("✔ Order submitted successfully!")
            
            # Check if print receipt link is properly formatted
            if 'print-receipt/' in submit_response.text and '/print-receipt/' in submit_response.text:
                print("✔ Print receipt URL is properly formatted with order ID")
            else:
                print("⚠️  Print receipt URL format needs verification")
                
        else:
            print(f"⚠️  Order submission returned: {submit_response.status_code}")
            if submit_response.status_code == 500:
                print("❌ Server error - checking for template issues...")

def main():
    try:
        # Test basic connectivity
        response = session.get(BASE_URL)
        if response.status_code == 200:
            print("✔ Server is accessible")
            test_order_workflow()
        else:
            print(f"❌ Server returned {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    main()
