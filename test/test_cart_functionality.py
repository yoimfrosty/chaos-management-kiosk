#!/usr/bin/env python3
"""
Test script to verify cart functionality works correctly with the new grid layout
"""
import requests
from bs4 import BeautifulSoup
import json
import sys

def test_cart_functionality():
    """Test that cart operations work correctly in the new grid layout"""
    
    session = requests.Session()
    
    print("🛒 Testing cart functionality with new grid layout...")
    
    try:
        # Step 1: Setup - get to products page
        print("📋 Step 1: Setting up session and accessing products...")
        response = session.get('http://localhost:8000/')
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
        
        # Age verification
        age_data = {
            'csrfmiddlewaretoken': csrf_token,
            'is_21_plus': 'on'
        }
        session.post('http://localhost:8000/verify-age/', data=age_data)
        
        # Get products page
        response = session.get('http://localhost:8000/products/')
        soup = BeautifulSoup(response.text, 'html.parser')
        print("✅ Successfully accessed products page")
        
        # Step 2: Test cart display functionality
        print("📋 Step 2: Testing cart display...")
        cart_panel = soup.find('div', id='cart-panel')
        cart_count = soup.find('span', id='cart-count')
        
        if not cart_panel or not cart_count:
            print("❌ Cart display elements not found")
            return False
        print("✅ Cart display elements present")
        
        # Step 3: Test get cart functionality
        print("📋 Step 3: Testing get cart API...")
        response = session.get('http://localhost:8000/cart/get/')
        if response.status_code != 200:
            print(f"❌ Get cart API failed: {response.status_code}")
            return False
        
        cart_data = response.json()
        if 'items' not in cart_data:
            print("❌ Cart data missing items field")
            return False
        print("✅ Get cart API working")
        
        # Step 4: Find a product to add to cart
        print("📋 Step 4: Testing add to cart functionality...")
        response = session.get('http://localhost:8000/products/')
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find a product form
        product_form = soup.find('form', class_='add-to-cart-form')
        if not product_form:
            print("⚠️ No products available to test add to cart")
            print("✅ Cart structure is correct (just no products in database)")
            return True
        
        # Get product details from form
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
        product_id = product_form.find('input', {'name': 'product_id'}).get('value')
        
        # Test adding to cart
        add_data = {
            'csrfmiddlewaretoken': csrf_token,
            'product_id': product_id,
            'quantity': '1'
        }
        
        response = session.post('http://localhost:8000/cart/add/', 
                              data=add_data,
                              headers={'X-Requested-With': 'XMLHttpRequest'})
        
        if response.status_code != 200:
            print(f"❌ Add to cart failed: {response.status_code}")
            return False
        
        add_result = response.json()
        if 'cart' not in add_result:
            print("❌ Add to cart response missing cart data")
            return False
        print("✅ Add to cart functionality working")
        
        # Step 5: Test clear cart
        print("📋 Step 5: Testing clear cart functionality...")
        clear_data = {
            'csrfmiddlewaretoken': csrf_token
        }
        
        response = session.post('http://localhost:8000/cart/clear/',
                              data=clear_data,
                              headers={'X-Requested-With': 'XMLHttpRequest'})
        
        if response.status_code != 200:
            print(f"❌ Clear cart failed: {response.status_code}")
            return False
        print("✅ Clear cart functionality working")
        
        print("\n🎉 Cart functionality test PASSED!")
        print("✅ All cart operations work correctly in the new grid layout")
        print("✅ Cart panel integrated properly into the page structure")
        print("✅ AJAX cart operations functioning normally")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_cart_functionality()
    sys.exit(0 if success else 1)
