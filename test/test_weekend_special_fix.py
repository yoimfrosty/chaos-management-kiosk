#!/usr/bin/env python3
"""
Test the specific scenario described in the conversation summary:
1. User adds a discounted product → discount should apply
2. User adds a non-discounted product → that product should NOT get the discount
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/Users/uba/Desktop/hemp-app/chaos-magement')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from decimal import Decimal
from django.test import RequestFactory
from kiosk.models import Product, SpecialOffer, Order, OrderItem
from kiosk.views import check_and_apply_automatic_discounts

def test_weekend_special_scenario():
    """Test the Weekend Special scenario from the conversation summary"""
    print("🧪 TESTING WEEKEND SPECIAL DISCOUNT SCENARIO")
    print("=" * 50)
    print("Reproducing the issue from conversation summary:")
    print("- Add discounted product (should get 10% off)")
    print("- Add non-discounted product (should NOT get discount)")
    print()
    
    # Find the Weekend Special offer
    weekend_special = SpecialOffer.objects.filter(
        title__contains="Weekend Special"
    ).first()
    
    if not weekend_special:
        print("❌ Weekend Special offer not found")
        return False
    
    print(f"📊 Found offer: {weekend_special.title}")
    print(f"   Discount: {weekend_special.discount_value}% off")
    
    # Get eligible and non-eligible products
    eligible_products = list(weekend_special.applicable_products.all())
    all_products = list(Product.objects.all())
    non_eligible_products = [p for p in all_products if p not in eligible_products]
    
    if not eligible_products or not non_eligible_products:
        print("❌ Need both eligible and non-eligible products for test")
        return False
    
    eligible_product = eligible_products[0]
    non_eligible_product = non_eligible_products[0]
    
    print(f"✅ Eligible product: {eligible_product.name} (${eligible_product.price})")
    print(f"🚫 Non-eligible product: {non_eligible_product.name} (${non_eligible_product.price})")
    
    # Create fresh cart
    cart = Order.objects.create(status='Pending')
    factory = RequestFactory()
    request = factory.get('/')
    request.session = {}
    
    print(f"\n🛒 Created test cart: {cart.order_number}")
    
    # STEP 1: Add eligible product (should trigger discount)
    print("\n1️⃣ Adding eligible product to cart...")
    OrderItem.objects.create(
        order=cart,
        product=eligible_product,
        quantity=1,
        price_at_purchase=eligible_product.price
    )
    
    # Apply automatic discounts
    applied_discounts = check_and_apply_automatic_discounts(request, cart, eligible_product)
    print(f"   Automatic discounts applied: {applied_discounts}")
    
    # Calculate totals
    session_discounts = request.session.get('applied_discounts', [])
    cart.recalculate_totals(session_discounts)
    
    print(f"   Subtotal: ${cart.subtotal}")
    print(f"   Discount: ${cart.discount_amount}")
    print(f"   Total: ${cart.total_amount}")
    
    # Verify discount was applied
    expected_discount = eligible_product.price * (weekend_special.discount_value / 100)
    if abs(cart.discount_amount - expected_discount) < Decimal('0.01'):
        print("   ✅ Correct discount applied to eligible product")
        step1_success = True
    else:
        print(f"   ❌ Wrong discount amount. Expected: ${expected_discount}, Got: ${cart.discount_amount}")
        step1_success = False
    
    # Store state after first product
    discount_after_first = cart.discount_amount
    
    # STEP 2: Add non-eligible product (should NOT increase discount)
    print("\n2️⃣ Adding non-eligible product to cart...")
    OrderItem.objects.create(
        order=cart,
        product=non_eligible_product,
        quantity=1,
        price_at_purchase=non_eligible_product.price
    )
    
    # Check for new discounts (should be none for this product)
    new_discounts = check_and_apply_automatic_discounts(request, cart, non_eligible_product)
    print(f"   New discounts for non-eligible product: {new_discounts}")
    
    # Recalculate totals
    session_discounts = request.session.get('applied_discounts', [])
    cart.recalculate_totals(session_discounts)
    
    print(f"   Subtotal: ${cart.subtotal}")
    print(f"   Discount: ${cart.discount_amount}")
    print(f"   Total: ${cart.total_amount}")
    
    # VERIFICATION
    print("\n🔍 VERIFICATION:")
    
    # Check that discount amount didn't change
    if abs(cart.discount_amount - discount_after_first) < Decimal('0.01'):
        print("   ✅ Discount amount unchanged when adding non-eligible product")
        step2_success = True
    else:
        print(f"   ❌ Discount changed! Was: ${discount_after_first}, Now: ${cart.discount_amount}")
        step2_success = False
    
    # Check that discount only applies to eligible product
    if abs(cart.discount_amount - expected_discount) < Decimal('0.01'):
        print("   ✅ Discount still only applies to eligible product")
        step3_success = True
    else:
        print(f"   ❌ Total discount is wrong. Expected: ${expected_discount}, Got: ${cart.discount_amount}")
        step3_success = False
    
    # Check total cart value
    expected_subtotal = eligible_product.price + non_eligible_product.price
    if abs(cart.subtotal - expected_subtotal) < Decimal('0.01'):
        print("   ✅ Cart subtotal includes both products correctly")
        step4_success = True
    else:
        print(f"   ❌ Cart subtotal wrong. Expected: ${expected_subtotal}, Got: ${cart.subtotal}")
        step4_success = False
    
    # Print detailed breakdown
    print("\n📋 CART BREAKDOWN:")
    for item in cart.items.all():
        is_eligible = weekend_special.applicable_products.filter(id=item.product.id).exists()
        status = "✅ ELIGIBLE" if is_eligible else "🚫 NOT ELIGIBLE"
        item_total = item.get_total_item_price()
        print(f"   {item.product.name}: ${item.price_at_purchase} x {item.quantity} = ${item_total} {status}")
    
    print(f"   Subtotal: ${cart.subtotal}")
    print(f"   Discount: ${cart.discount_amount} (should only apply to eligible items)")
    print(f"   After discount: ${cart.subtotal - cart.discount_amount}")
    print(f"   Tax: ${cart.tax_amount}")
    print(f"   Total: ${cart.total_amount}")
    
    # Overall result
    all_success = step1_success and step2_success and step3_success and step4_success
    
    print("\n🎯 FINAL RESULT:")
    if all_success:
        print("   🎉 ALL TESTS PASSED!")
        print("   ✅ Product-specific discounts work correctly")
        print("   ✅ Non-eligible products do not receive discounts")
        print("   ✅ The original issue has been FIXED")
    else:
        print("   ❌ SOME TESTS FAILED!")
        print("   🔧 Product-specific discount logic needs further review")
    
    # Cleanup
    cart.delete()
    
    return all_success

if __name__ == "__main__":
    try:
        success = test_weekend_special_scenario()
        if success:
            print("\n✅ CONCLUSION: The discount system is working correctly!")
            print("Discounts are now applied per-product, not globally.")
        else:
            print("\n❌ CONCLUSION: Issues remain with the discount system.")
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        import traceback
        traceback.print_exc()
