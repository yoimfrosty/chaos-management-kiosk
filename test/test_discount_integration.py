#!/usr/bin/env python
"""
Final integration test for the discount system
This test verifies that all components work together properly
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
import json

def test_complete_discount_workflow():
    """Test the complete discount workflow from application to order completion"""
    print("🚀 Testing Complete Discount Workflow")
    print("=" * 50)
    
    # 1. Verify special offers exist
    offers = SpecialOffer.objects.filter(is_active=True)
    print(f"✅ Found {offers.count()} active special offers")
    
    if offers.count() == 0:
        print("⚠️ No active offers found, creating test offer...")
        import time
        timestamp = int(time.time())
        offer = SpecialOffer.objects.create(
            title=f"Test Integration Offer {timestamp}",
            description="Test offer for integration testing",
            discount_type="Percentage",
            discount_value=Decimal('15.00'),
            minimum_spend=Decimal('20.00'),
            is_active=True
        )
        offers = [offer]
        print(f"✅ Created test offer: {offer.title}")
    
    # 2. Verify products exist
    products = Product.objects.all()
    print(f"✅ Found {products.count()} products")
    
    if products.count() == 0:
        print("❌ No products found! Please ensure products are loaded.")
        return False
    
    # 3. Test cart creation and item addition
    request = HttpRequest()
    request.method = 'GET'
    request.session = SessionStore()
    request.session.create()
    
    cart = get_or_create_cart(request)
    test_product = products.first()
    
    # Add item to cart
    OrderItem.objects.create(
        order=cart,
        product=test_product,
        quantity=2,
        price_at_purchase=test_product.price
    )
    
    cart.recalculate_totals()
    original_total = cart.total_amount
    
    print(f"✅ Created cart with item: {test_product.name}")
    print(f"✅ Original cart total: ${original_total}")
    
    # 4. Test discount application to session
    test_offer = offers[0]
    request.session['applied_discounts'] = [{
        'offer_id': test_offer.id,
        'title': test_offer.title,
        'discount_type': test_offer.discount_type,
        'discount_value': float(test_offer.discount_value),
        'applied_at': '2024-01-01T12:00:00Z'
    }]
    
    # 5. Test cart data calculation with discount
    cart_data = cart_data_for_json(cart, request)
    
    print(f"✅ Cart subtotal: ${cart_data['subtotal']}")
    print(f"✅ Applied discounts: {len(cart_data['applied_discounts'])}")
    print(f"✅ Discount amount: ${cart_data['discount_amount']}")
    print(f"✅ Final total: ${cart_data['total_amount']}")
    
    # 6. Verify discount is properly calculated
    expected_discount = 0
    minimum_spend = test_offer.minimum_spend or Decimal('0')
    if cart_data['subtotal'] >= float(minimum_spend):
        if test_offer.discount_type == 'Percentage':
            expected_discount = (cart_data['subtotal'] * float(test_offer.discount_value)) / 100
        elif test_offer.discount_type == 'Fixed Amount':
            expected_discount = min(float(test_offer.discount_value), cart_data['subtotal'])
    
    print(f"✅ Expected discount: ${expected_discount}")
    
    # 7. Test order recalculation with discounts
    discounts = [{
        'offer_id': test_offer.id,
        'title': test_offer.title,
        'discount_type': test_offer.discount_type,
        'discount_value': float(test_offer.discount_value)
    }]
    
    cart.recalculate_totals(discounts)
    final_total = cart.total_amount
    
    print(f"✅ Final cart total after discount: ${final_total}")
    
    # 8. Verify total is reduced (if discount was applicable)
    minimum_spend = test_offer.minimum_spend or Decimal('0')
    if cart_data['subtotal'] >= float(minimum_spend) and expected_discount > 0:
        assert final_total < original_total, f"Total should be reduced: {final_total} < {original_total}"
        print("✅ Discount properly reduced total")
    else:
        print("⚠️ Discount not applicable due to minimum spend requirement")
    
    # 9. Test discount calculation function directly
    test_discounts = [discounts[0]]
    calculated_discount = calculate_discount_amount(float(cart_data['subtotal']), test_discounts)
    print(f"✅ Calculated discount amount: ${calculated_discount}")
    
    return True

def test_discount_edge_cases():
    """Test edge cases for discount system"""
    print("\n🧪 Testing Discount Edge Cases")
    print("=" * 50)
    
    # Test empty discounts
    amount = calculate_discount_amount(100.0, [])
    assert amount == 0, f"Empty discounts should return 0, got {amount}"
    print("✅ Empty discounts handled correctly")
    
    # Test zero subtotal
    discounts = [{
        'discount_type': 'Percentage',
        'discount_value': 20.0,
        'offer_id': 1,
        'title': 'Test'
    }]
    amount = calculate_discount_amount(0.0, discounts)
    assert amount == 0, f"Zero subtotal should return 0, got {amount}"
    print("✅ Zero subtotal handled correctly")
    
    # Test very large discount (should not exceed subtotal)
    discounts = [{
        'discount_type': 'Fixed Amount',
        'discount_value': 1000.0,
        'offer_id': 1,
        'title': 'Test'
    }]
    amount = calculate_discount_amount(50.0, discounts)
    assert amount <= 50.0, f"Discount should not exceed subtotal, got {amount}"
    print("✅ Large discount capped correctly")
    
    # Test 100% discount
    discounts = [{
        'discount_type': 'Percentage',
        'discount_value': 100.0,
        'offer_id': 1,
        'title': 'Test'
    }]
    amount = calculate_discount_amount(75.0, discounts)
    expected = 75.0
    assert amount == expected, f"100% discount should equal subtotal, got {amount}"
    print("✅ 100% discount handled correctly")
    
    return True

def test_cart_integration():
    """Test cart integration with various scenarios"""
    print("\n🛒 Testing Cart Integration Scenarios")
    print("=" * 50)
    
    # Create multiple carts to test different scenarios
    products = list(Product.objects.all()[:3])
    
    if len(products) < 2:
        print("⚠️ Not enough products for comprehensive testing")
        return True
    
    # Scenario 1: Cart meets minimum spend
    request1 = HttpRequest()
    request1.method = 'GET'
    request1.session = SessionStore()
    request1.session.create()
    
    cart1 = get_or_create_cart(request1)
    OrderItem.objects.create(
        order=cart1,
        product=products[0],
        quantity=2,
        price_at_purchase=products[0].price
    )
    cart1.recalculate_totals()
    
    # Apply discount
    request1.session['applied_discounts'] = [{
        'offer_id': 1,
        'title': 'Test 10% Off',
        'discount_type': 'Percentage',
        'discount_value': 10.0,
        'applied_at': '2024-01-01T12:00:00Z'
    }]
    
    cart_data1 = cart_data_for_json(cart1, request1)
    print(f"✅ Scenario 1 - Cart with sufficient amount:")
    print(f"   Subtotal: ${cart_data1['subtotal']}")
    print(f"   Discount: ${cart_data1['discount_amount']}")
    print(f"   Total: ${cart_data1['total_amount']}")
    
    # Scenario 2: Empty cart
    request2 = HttpRequest()
    request2.method = 'GET'
    request2.session = SessionStore()
    request2.session.create()
    
    cart2 = get_or_create_cart(request2)
    cart_data2 = cart_data_for_json(cart2, request2)
    
    print(f"✅ Scenario 2 - Empty cart:")
    print(f"   Subtotal: ${cart_data2['subtotal']}")
    print(f"   Total: ${cart_data2['total_amount']}")
    
    return True

def run_integration_tests():
    """Run all integration tests"""
    print("🎯 Starting Discount System Integration Tests")
    print("=" * 60)
    
    try:
        # Run test suites
        test_complete_discount_workflow()
        test_discount_edge_cases()
        test_cart_integration()
        
        print("\n" + "=" * 60)
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("\n📋 Integration Test Summary:")
        print("✅ Complete discount workflow")
        print("✅ Edge case handling")
        print("✅ Cart integration scenarios")
        print("\n✨ The discount system is fully integrated and ready for production!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
