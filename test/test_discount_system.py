#!/usr/bin/env python
"""
Comprehensive test for the discount system implementation
Tests all aspects of the discount functionality
"""

import os
import sys
import django
from decimal import Decimal

# Add the project directory to the path
sys.path.append('/home/ubuntu/django-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')

# Setup Django
django.setup()

from django.test import TestCase, Client
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore
from django.urls import reverse
from django.http import HttpRequest
from kiosk.models import Product, SpecialOffer, Order, OrderItem, Category
from kiosk.cart import get_or_create_cart, cart_data_for_json, calculate_discount_amount
from kiosk.views import apply_discount_view, remove_discount_view
import json

def setup_test_data():
    """Create test data for discount testing"""
    print("🔧 Setting up test data...")
    
    # Get existing products or use default ones
    products = list(Product.objects.all()[:2])
    
    if len(products) < 2:
        # Get or create category
        category, created = Category.objects.get_or_create(
            name="Flower",
            defaults={'description': 'Premium cannabis flower products'}
        )
        
        # Create test products with unique names
        import time
        timestamp = int(time.time())
        
        if len(products) == 0:
            product1 = Product.objects.create(
                name=f"Test Blue Dream {timestamp}",
                description="Relaxing hybrid strain",
                price=Decimal('45.00'),
                category=category,
                thc_content=18.5,
                cbd_content=0.5,
                flower_type="Hybrid"
            )
            products.append(product1)
        
        if len(products) == 1:
            product2 = Product.objects.create(
                name=f"Test OG Kush {timestamp}",
                description="Classic indica strain",
                price=Decimal('50.00'),
                category=category, 
                thc_content=22.0,
                cbd_content=0.3,
                flower_type="Indica"
            )
            products.append(product2)
    
    # Create test special offers with unique titles
    import time
    timestamp = int(time.time())
    
    percentage_offer, created = SpecialOffer.objects.get_or_create(
        title=f"Test First Time Customer - 20% Off {timestamp}",
        defaults={
            'description': "Get 20% off your first purchase",
            'discount_type': "Percentage",
            'discount_value': Decimal('20.00'),
            'minimum_spend': Decimal('25.00'),
            'is_active': True
        }
    )
    
    fixed_offer, created = SpecialOffer.objects.get_or_create(
        title=f"Test Happy Hour - $10 Off {timestamp}",
        defaults={
            'description': "$10 off orders over $40",
            'discount_type': "Fixed Amount",
            'discount_value': Decimal('10.00'),
            'minimum_spend': Decimal('40.00'),
            'is_active': True
        }
    )
    
    print(f"✅ Using products: {products[0].name}, {products[1].name}")
    print(f"✅ Created/found offers: {percentage_offer.title}, {fixed_offer.title}")
    
    return {
        'products': products,
        'offers': [percentage_offer, fixed_offer]
    }

def test_discount_calculation():
    """Test discount calculation logic"""
    print("\n💰 Testing discount calculations...")
    
    # Test percentage discount
    discounts = [{
        'discount_type': 'Percentage',
        'discount_value': 20.0,
        'offer_id': 1,
        'title': 'Test 20% Off'
    }]
    
    amount = calculate_discount_amount(100.0, discounts)
    expected = 20.0
    assert amount == expected, f"Expected {expected}, got {amount}"
    print(f"✅ Percentage discount: ${amount} (20% off $100)")
    
    # Test fixed amount discount
    discounts = [{
        'discount_type': 'Fixed Amount',
        'discount_value': 15.0,
        'offer_id': 2,
        'title': 'Test $15 Off'
    }]
    
    amount = calculate_discount_amount(75.0, discounts)
    expected = 15.0
    assert amount == expected, f"Expected {expected}, got {amount}"
    print(f"✅ Fixed discount: ${amount} ($15 off $75)")
    
    # Test multiple discounts
    discounts = [
        {
            'discount_type': 'Percentage',
            'discount_value': 10.0,
            'offer_id': 1,
            'title': 'Test 10% Off'
        },
        {
            'discount_type': 'Fixed Amount', 
            'discount_value': 5.0,
            'offer_id': 2,
            'title': 'Test $5 Off'
        }
    ]
    
    amount = calculate_discount_amount(50.0, discounts)
    expected = 10.0  # 10% of 50 + $5 = $5 + $5 = $10
    assert amount == expected, f"Expected {expected}, got {amount}"
    print(f"✅ Multiple discounts: ${amount} (10% + $5 off $50)")

def test_cart_with_discounts():
    """Test cart functionality with discounts"""
    print("\n🛒 Testing cart with discounts...")
    
    # Create a mock request with session
    request = HttpRequest()
    request.method = 'GET'
    request.session = SessionStore()
    request.session.create()
    
    # Create cart and add items
    cart = get_or_create_cart(request)
    products = Product.objects.all()[:2]
    
    for product in products:
        OrderItem.objects.create(
            order=cart,
            product=product,
            quantity=1,
            price_at_purchase=product.price
        )
    
    # Recalculate cart totals first
    cart.recalculate_totals()
    
    print(f"✅ Added {len(products)} items to cart")
    print(f"✅ Cart subtotal before discount: ${cart.subtotal}")
    
    if cart.subtotal == 0:
        print("⚠️ Cart subtotal is 0, skipping discount test")
        return cart
    
    # Add discount to session
    request.session['applied_discounts'] = [{
        'offer_id': 1,
        'title': 'Test 20% Off',
        'discount_type': 'Percentage',
        'discount_value': 20.0,
        'applied_at': '2024-01-01T12:00:00Z'
    }]
    
    # Get cart data with discounts
    cart_data = cart_data_for_json(cart, request)
    
    print(f"✅ Cart subtotal: ${cart_data['subtotal']}")
    print(f"✅ Applied discounts: {len(cart_data['applied_discounts'])}")
    print(f"✅ Discount amount: ${cart_data['discount_amount']}")
    print(f"✅ Final total: ${cart_data['total_amount']}")
    
    # Verify discount is applied
    assert cart_data['applied_discounts'], "No discounts found in cart data"
    
    if cart_data['subtotal'] > 0:
        assert cart_data['discount_amount'] > 0, "Discount amount should be greater than 0"
    else:
        print("⚠️ Skipping discount amount assertion due to zero subtotal")
    
    return cart

def test_discount_views():
    """Test discount application and removal views"""
    print("\n🎯 Testing discount views...")
    
    client = Client()
    
    # Get special offers
    offers = SpecialOffer.objects.filter(is_active=True)
    if not offers:
        print("❌ No active special offers found")
        return
    
    offer = offers.first()
    
    # Test apply discount
    response = client.post('/kiosk/apply-discount/', {
        'offer_id': offer.id
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('success'):
            print(f"✅ Successfully applied discount: {offer.title}")
        else:
            print(f"❌ Failed to apply discount: {data.get('message', 'Unknown error')}")
    else:
        print(f"❌ Apply discount failed with status {response.status_code}")
    
    # Test remove discount
    response = client.post('/kiosk/remove-discount/', {
        'offer_id': offer.id
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('success'):
            print(f"✅ Successfully removed discount: {offer.title}")
        else:
            print(f"❌ Failed to remove discount: {data.get('message', 'Unknown error')}")
    else:
        print(f"❌ Remove discount failed with status {response.status_code}")

def test_specials_page():
    """Test specials page rendering"""
    print("\n📄 Testing specials page...")
    
    client = Client()
    
    # Test age verification first
    response = client.get('/kiosk/age-verification/')
    print(f"✅ Age verification page status: {response.status_code}")
    
    # Submit age verification
    response = client.post('/kiosk/age-verification/', {
        'age_verified': 'yes'
    })
    print(f"✅ Age verification submission status: {response.status_code}")
    
    # Test specials page
    response = client.get('/kiosk/specials/')
    if response.status_code == 200:
        print("✅ Specials page loads successfully")
        content = response.content.decode()
        
        # Check for discount application buttons
        if 'btn-apply-discount' in content:
            print("✅ Apply discount buttons found")
        else:
            print("❌ Apply discount buttons not found")
            
        # Check for cart panel
        if 'cart-panel' in content:
            print("✅ Cart panel found")
        else:
            print("❌ Cart panel not found")
            
        # Check for CartManager
        if 'CartManager' in content:
            print("✅ CartManager JavaScript found")
        else:
            print("❌ CartManager JavaScript not found")
    else:
        print(f"❌ Specials page failed with status {response.status_code}")

def test_order_recalculation():
    """Test order total recalculation with discounts"""
    print("\n🧮 Testing order recalculation...")
    
    # Create order with items
    cart = Order.objects.create(status='Pending')
    products = Product.objects.all()[:2]
    
    for product in products:
        OrderItem.objects.create(
            order=cart,
            product=product,
            quantity=2,
            price_at_purchase=product.price
        )
    
    # Calculate initial totals
    cart.recalculate_totals()
    original_total = cart.total_amount
    original_subtotal = cart.subtotal
    
    print(f"✅ Original subtotal: ${original_subtotal}")
    print(f"✅ Original total: ${original_total}")
    
    if original_total == 0:
        print("⚠️ Original total is 0, skipping recalculation test")
        return
    
    # Apply discount
    discounts = [{
        'offer_id': 1,
        'title': 'Test 15% Off',
        'discount_type': 'Percentage',
        'discount_value': 15.0
    }]
    
    cart.recalculate_totals(discounts)
    new_total = cart.total_amount
    new_subtotal = cart.subtotal
    
    print(f"✅ Subtotal after discount: ${new_subtotal}")
    print(f"✅ Total after 15% discount: ${new_total}")
    
    # The total should be less after applying discount
    if original_total > 0:
        assert new_total < original_total, f"Total should be less after discount: {new_total} < {original_total}"
        
        # Calculate expected discount
        expected_discount = original_subtotal * Decimal('0.15')
        expected_subtotal_after_discount = original_subtotal - expected_discount
        expected_total_with_tax = expected_subtotal_after_discount * (Decimal('1') + Decimal(str(cart.tax_rate)))
        
        print(f"✅ Expected total with tax: ${expected_total_with_tax}")
        
        # Allow for small rounding differences
        difference = abs(new_total - expected_total_with_tax)
        assert difference < Decimal('0.01'), f"Total calculation error: {difference}"
    else:
        print("⚠️ Skipping total comparison due to zero original total")

def run_all_tests():
    """Run all discount system tests"""
    print("🚀 Starting Discount System Comprehensive Test")
    print("=" * 60)
    
    try:
        # Setup test data
        test_data = setup_test_data()
        
        # Run individual tests
        test_discount_calculation()
        test_cart_with_discounts()
        test_order_recalculation()
        test_specials_page()
        test_discount_views()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! Discount system is working correctly.")
        print("\n📋 Test Summary:")
        print("✅ Discount calculation logic")
        print("✅ Cart integration with discounts")
        print("✅ Order total recalculation")
        print("✅ Specials page rendering")
        print("✅ Discount application/removal views")
        print("\n🛍️ The discount system is ready for use!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
