#!/usr/bin/env python3
"""
Test product-specific discount functionality to ensure discounts only apply to eligible products
"""
import os
import django
import sys

# Setup Django
sys.path.append('/Users/uba/Desktop/hemp-app/chaos-magement')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaos_magement.settings')
django.setup()

from decimal import Decimal
from django.test import RequestFactory
from kiosk.models import Product, Category, SpecialOffer, Order, OrderItem
from kiosk.views import check_and_apply_automatic_discounts
from kiosk.cart import get_or_create_cart

def test_product_specific_discount_isolation():
    """Test that product-specific discounts only apply to eligible products"""
    print("🧪 TESTING PRODUCT-SPECIFIC DISCOUNT ISOLATION")
    print("=" * 60)
    
    # Get or create test products
    products = list(Product.objects.all()[:3])
    if len(products) < 3:
        print("❌ Need at least 3 products for testing")
        return False
    
    discounted_product = products[0]
    non_discounted_product1 = products[1] 
    non_discounted_product2 = products[2]
    
    print(f"🎯 Discounted product: {discounted_product.name} (${discounted_product.price})")
    print(f"🚫 Non-discounted product 1: {non_discounted_product1.name} (${non_discounted_product1.price})")
    print(f"🚫 Non-discounted product 2: {non_discounted_product2.name} (${non_discounted_product2.price})")
    
    # Create a product-specific discount offer
    offer, created = SpecialOffer.objects.get_or_create(
        title="Product-Specific Test Discount - 20% Off",
        defaults={
            'description': "20% off specific product only",
            'discount_type': "Percentage", 
            'discount_value': Decimal('20.00'),
            'is_active': True
        }
    )
    
    # Clear existing applicable products and add only the discounted product
    offer.applicable_products.clear()
    offer.applicable_products.add(discounted_product)
    offer.applicable_categories.clear()
    
    print(f"✅ Created product-specific discount: {offer.title}")
    print(f"   Applies to: {discounted_product.name} only")
    
    # Create test cart and request
    factory = RequestFactory()
    request = factory.get('/')
    request.session = {}
    
    cart = Order.objects.create(status='Pending')
    
    print("\n📦 TEST SCENARIO 1: Add discounted product first")
    print("-" * 50)
    
    # Add discounted product - should trigger discount
    OrderItem.objects.create(
        order=cart,
        product=discounted_product,
        quantity=1,
        price_at_purchase=discounted_product.price
    )
    
    # Check for automatic discounts
    applied_discounts = check_and_apply_automatic_discounts(request, cart, discounted_product)
    print(f"🎉 Discounts applied when adding {discounted_product.name}: {applied_discounts}")
    
    # Recalculate totals
    session_discounts = request.session.get('applied_discounts', [])
    cart.recalculate_totals(session_discounts)
    
    print(f"💰 Cart subtotal: ${cart.subtotal}")
    print(f"💸 Discount amount: ${cart.discount_amount}")
    print(f"💳 Total: ${cart.total_amount}")
    
    # Verify discount was applied
    if len(session_discounts) > 0:
        print("✅ Discount correctly applied to eligible product")
    else:
        print("❌ Discount was not applied to eligible product")
        return False
    
    # Store current state
    original_discount_amount = cart.discount_amount
    original_subtotal = cart.subtotal
    
    print("\n📦 TEST SCENARIO 2: Add non-discounted product")
    print("-" * 50)
    
    # Add non-discounted product - should NOT increase discount
    OrderItem.objects.create(
        order=cart,
        product=non_discounted_product1,
        quantity=1,
        price_at_purchase=non_discounted_product1.price
    )
    
    # Check for automatic discounts (should not find any new ones)
    new_discounts = check_and_apply_automatic_discounts(request, cart, non_discounted_product1)
    print(f"🚫 New discounts when adding {non_discounted_product1.name}: {new_discounts}")
    
    # Recalculate totals
    session_discounts = request.session.get('applied_discounts', [])
    cart.recalculate_totals(session_discounts)
    
    print(f"💰 Cart subtotal: ${cart.subtotal}")
    print(f"💸 Discount amount: ${cart.discount_amount}")
    print(f"💳 Total: ${cart.total_amount}")
    
    # Verify discount amount calculation
    expected_discount = discounted_product.price * Decimal('0.20')  # 20% of discounted product only
    
    print(f"\n🧮 DISCOUNT CALCULATION VERIFICATION")
    print(f"Expected discount (20% of ${discounted_product.price}): ${expected_discount}")
    print(f"Actual discount amount: ${cart.discount_amount}")
    
    if abs(cart.discount_amount - expected_discount) < Decimal('0.01'):
        print("✅ Discount correctly calculated for eligible product only")
    else:
        print("❌ Discount calculation is incorrect")
        return False
    
    # Verify total increased by exactly the non-discounted product price
    expected_new_subtotal = original_subtotal + non_discounted_product1.price
    if abs(cart.subtotal - expected_new_subtotal) < Decimal('0.01'):
        print("✅ Subtotal correctly increased by non-discounted product price")
    else:
        print("❌ Subtotal calculation is incorrect")
        return False
    
    print("\n📦 TEST SCENARIO 3: Add another non-discounted product")
    print("-" * 50)
    
    # Add another non-discounted product
    OrderItem.objects.create(
        order=cart,
        product=non_discounted_product2,
        quantity=2,  # Add 2 to test quantity
        price_at_purchase=non_discounted_product2.price
    )
    
    # Check for automatic discounts (should not find any new ones)
    new_discounts = check_and_apply_automatic_discounts(request, cart, non_discounted_product2)
    print(f"🚫 New discounts when adding {non_discounted_product2.name} x2: {new_discounts}")
    
    # Recalculate totals
    session_discounts = request.session.get('applied_discounts', [])
    cart.recalculate_totals(session_discounts)
    
    print(f"💰 Cart subtotal: ${cart.subtotal}")
    print(f"💸 Discount amount: ${cart.discount_amount}")
    print(f"💳 Total: ${cart.total_amount}")
    
    # Verify discount amount is still the same (only applies to original product)
    if abs(cart.discount_amount - expected_discount) < Decimal('0.01'):
        print("✅ Discount amount unchanged - correctly isolated to eligible product")
    else:
        print("❌ Discount incorrectly applied to non-eligible products")
        return False
    
    print("\n🎯 FINAL VERIFICATION")
    print("-" * 30)
    
    # Calculate expected totals
    total_cart_value = (discounted_product.price + 
                       non_discounted_product1.price + 
                       (non_discounted_product2.price * 2))
    
    expected_discount_only_on_eligible = discounted_product.price * Decimal('0.20')
    expected_subtotal_after_discount = total_cart_value - expected_discount_only_on_eligible
    
    print(f"Total cart value: ${total_cart_value}")
    print(f"Expected discount (only on {discounted_product.name}): ${expected_discount_only_on_eligible}")
    print(f"Expected subtotal after discount: ${expected_subtotal_after_discount}")
    print(f"Actual subtotal: ${cart.subtotal}")
    print(f"Actual discount: ${cart.discount_amount}")
    
    # Final verification
    success = True
    if abs(cart.subtotal - total_cart_value) > Decimal('0.01'):
        print("❌ Cart subtotal is incorrect")
        success = False
    
    if abs(cart.discount_amount - expected_discount_only_on_eligible) > Decimal('0.01'):
        print("❌ Discount amount is incorrect")
        success = False
    
    # Test universal discount for comparison
    print("\n📦 TEST SCENARIO 4: Universal discount comparison")
    print("-" * 50)
    
    # Create a universal discount
    universal_offer, created = SpecialOffer.objects.get_or_create(
        title="Universal Test Discount - 10% Off Everything",
        defaults={
            'description': "10% off all products",
            'discount_type': "Percentage",
            'discount_value': Decimal('10.00'),
            'is_active': True
        }
    )
    
    # Clear product/category restrictions to make it universal
    universal_offer.applicable_products.clear()
    universal_offer.applicable_categories.clear()
    
    # Create new cart for universal test
    universal_cart = Order.objects.create(status='Pending')
    universal_request = factory.get('/')
    universal_request.session = {}
    
    # Add same products
    OrderItem.objects.create(
        order=universal_cart,
        product=discounted_product,
        quantity=1,
        price_at_purchase=discounted_product.price
    )
    OrderItem.objects.create(
        order=universal_cart,
        product=non_discounted_product1,
        quantity=1,
        price_at_purchase=non_discounted_product1.price
    )
    
    # Apply universal discount
    applied_universal = check_and_apply_automatic_discounts(universal_request, universal_cart, discounted_product)
    print(f"🌟 Universal discounts applied: {applied_universal}")
    
    universal_discounts = universal_request.session.get('applied_discounts', [])
    universal_cart.recalculate_totals(universal_discounts)
    
    print(f"💰 Universal cart subtotal: ${universal_cart.subtotal}")
    print(f"💸 Universal discount amount: ${universal_cart.discount_amount}")
    
    # Universal discount should be 10% of both products
    expected_universal = (discounted_product.price + non_discounted_product1.price) * Decimal('0.10')
    print(f"Expected universal discount (10% of ${discounted_product.price + non_discounted_product1.price}): ${expected_universal}")
    
    if abs(universal_cart.discount_amount - expected_universal) < Decimal('0.01'):
        print("✅ Universal discount correctly applied to all products")
    else:
        print("❌ Universal discount calculation is incorrect")
        success = False
    
    # Cleanup
    offer.delete()
    universal_offer.delete()
    cart.delete()
    universal_cart.delete()
    
    return success

if __name__ == "__main__":
    print("🧪 PRODUCT-SPECIFIC DISCOUNT ISOLATION TEST")
    print("=" * 60)
    
    success = test_product_specific_discount_isolation()
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Product-specific discounts are working correctly")
        print("✅ Discounts only apply to eligible products")
        print("✅ Non-eligible products do not receive discounts") 
        print("✅ Discount calculations are accurate")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("🔧 Product-specific discount logic needs review")
