#!/usr/bin/env python3
"""
Test script for Phase 2 cart functionality
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/home/ubuntu/django-app')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from kiosk.models import Product, Order, OrderItem
from kiosk.cart import get_or_create_cart, cart_data_for_json

def test_cart_functionality():
    """Test the cart functionality programmatically"""
    print("🧪 Testing Phase 2 Cart Functionality")
    print("=" * 50)
    
    # Create a test client
    client = Client()
    
    # 1. Test age verification requirement
    print("1. Testing age verification requirement...")
    response = client.get(reverse('kiosk:product_list'))
    print(f"   Product list without age verification: {response.status_code} (should be 302 redirect)")
    
    # 2. Set age verification in session
    print("2. Setting age verification in session...")
    session = client.session
    session['is_21_plus'] = True
    session.save()
    
    # 3. Test product list access
    print("3. Testing product list access after age verification...")
    response = client.get(reverse('kiosk:product_list'))
    print(f"   Product list with age verification: {response.status_code} (should be 200)")
    
    # 4. Test cart creation
    print("4. Testing cart creation...")
    response = client.get(reverse('kiosk:get_cart'))
    cart_data = response.json()
    print(f"   Cart data: {cart_data}")
    print(f"   Order number: {cart_data.get('order_number')}")
    print(f"   Items count: {len(cart_data.get('items', []))}")
    
    # 5. Test adding product to cart
    print("5. Testing add to cart...")
    # Get a product to add
    product = Product.objects.filter(is_available=True).first()
    if product:
        print(f"   Adding product: {product.name} (${product.price})")
        response = client.post(reverse('kiosk:add_to_cart'), {
            'product_id': product.id,
            'quantity': 2
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        if response.status_code == 200:
            cart_data = response.json()
            print(f"   ✔ Product added successfully!")
            print(f"   Items in cart: {len(cart_data['cart']['items'])}")
            print(f"   Subtotal: ${cart_data['cart']['subtotal']}")
            print(f"   Total: ${cart_data['cart']['total_amount']}")
        else:
            print(f"   ❌ Failed to add product: {response.status_code}")
    else:
        print("   ❌ No products available for testing")
    
    # 6. Test cart totals calculation
    print("6. Testing cart totals...")
    orders = Order.objects.filter(status='Pending')
    if orders.exists():
        order = orders.first()
        print(f"   Order: {order.order_number}")
        print(f"   Items: {order.items.count()}")
        print(f"   Subtotal: ${order.subtotal}")
        print(f"   Tax ({order.tax_rate * 100}%): ${order.tax_amount}")
        print(f"   Total: ${order.total_amount}")
    
    print("\n✔ Phase 2 testing completed!")

if __name__ == "__main__":
    test_cart_functionality()
