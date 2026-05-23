#!/usr/bin/env python3
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, '/Users/uba/Desktop/hemp-app/chaos-magement')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaos_magement.settings')
django.setup()

from decimal import Decimal
from django.test import RequestFactory
from kiosk.models import Product, SpecialOffer, Order, OrderItem
from kiosk.views import check_and_apply_automatic_discounts

def main():
    print("🧪 TESTING PRODUCT-SPECIFIC DISCOUNT LOGIC")
    print("=" * 50)
    
    # Get test products
    products = list(Product.objects.all()[:2])
    if len(products) < 2:
        print("❌ Need at least 2 products for testing")
        return
    
    product_a = products[0]
    product_b = products[1] 
    
    print(f"📦 Product A (eligible): {product_a.name} (${product_a.price})")
    print(f"📦 Product B (not eligible): {product_b.name} (${product_b.price})")
    
    # Delete any existing test offers to avoid conflicts
    SpecialOffer.objects.filter(title__contains="Test Product-Specific").delete()
    
    # Create product-specific discount offer (only applies to product A)
    offer = SpecialOffer.objects.create(
        title="Test Product-Specific 20% Off",
        description="20% off specific product only",
        discount_type="Percentage",
        discount_value=Decimal('20.00'),
        is_active=True
    )
    offer.applicable_products.add(product_a)  # Only applies to product A
    offer.save()
    
    print(f"✅ Created offer: {offer.title}")
    print(f"   Applies to: {list(offer.applicable_products.values_list('name', flat=True))}")
    
    # Create test cart and mock request
    cart = Order.objects.create(status='Pending')
    factory = RequestFactory()
    request = factory.get('/')
    request.session = {}
    
    print(f"\n🛒 Created test cart: {cart.order_number}")
    
    print("\n1️⃣ STEP 1: Add eligible product (should trigger discount)")
    print("-" * 40)
    
    # Add product A (eligible for discount)
    item_a = OrderItem.objects.create(
        order=cart,
        product=product_a,
        quantity=1,
        price_at_purchase=product_a.price
    )
    print(f"➕ Added {product_a.name} to cart")
    
    # Check for automatic discounts
    applied_discounts = check_and_apply_automatic_discounts(request, cart, product_a)
    print(f"🎉 Automatic discounts applied: {applied_discounts}")
    
    # Calculate cart totals with discount
    session_discounts = request.session.get('applied_discounts', [])
    cart.recalculate_totals(session_discounts)
    
    print(f"💰 Cart subtotal: ${cart.subtotal}")
    print(f"💸 Discount amount: ${cart.discount_amount}")
    print(f"💳 Total: ${cart.total_amount}")
    
    # Store state after first product
    discount_after_first = cart.discount_amount
    subtotal_after_first = cart.subtotal
    
    print(f"\n2️⃣ STEP 2: Add non-eligible product (should NOT increase discount)")
    print("-" * 40)
    
    # Add product B (NOT eligible for discount)
    item_b = OrderItem.objects.create(
        order=cart,
        product=product_b,
        quantity=1,
        price_at_purchase=product_b.price
    )
    print(f"➕ Added {product_b.name} to cart")
    
    # Check for new automatic discounts (should be none)
    new_discounts = check_and_apply_automatic_discounts(request, cart, product_b)
    print(f"🚫 New discounts for non-eligible product: {new_discounts}")
    
    # Recalculate cart totals
    session_discounts = request.session.get('applied_discounts', [])
    cart.recalculate_totals(session_discounts)
    
    print(f"💰 Cart subtotal: ${cart.subtotal}")
    print(f"💸 Discount amount: ${cart.discount_amount}")
    print(f"💳 Total: ${cart.total_amount}")
    
    print(f"\n🧮 VERIFICATION")
    print("-" * 20)
    
    # Calculate expected values
    expected_total_subtotal = product_a.price + product_b.price
    expected_discount = product_a.price * Decimal('0.20')  # 20% only on product A
    
    print(f"Expected total subtotal: ${expected_total_subtotal}")
    print(f"Expected discount (20% of ${product_a.price} only): ${expected_discount}")
    print(f"Actual total subtotal: ${cart.subtotal}")
    print(f"Actual discount: ${cart.discount_amount}")
    
    # Verify results
    success = True
    
    # Check if discount amount is correct (only applies to product A)
    if abs(cart.discount_amount - expected_discount) < Decimal('0.01'):
        print("✅ Discount correctly calculated for eligible product only")
    else:
        print("❌ Discount calculation is incorrect")
        success = False
    
    # Check if subtotal is correct
    if abs(cart.subtotal - expected_total_subtotal) < Decimal('0.01'):
        print("✅ Subtotal correctly includes both products")
    else:
        print("❌ Subtotal calculation is incorrect")
        success = False
    
    # Check that discount didn't change when adding non-eligible product
    if abs(cart.discount_amount - discount_after_first) < Decimal('0.01'):
        print("✅ Discount amount unchanged when adding non-eligible product")
    else:
        print("❌ Discount incorrectly increased when adding non-eligible product")
        success = False
    
    print(f"\n3️⃣ STEP 3: Verify cart items and individual pricing")
    print("-" * 40)
    
    for item in cart.items.all():
        item_total = item.get_total_item_price()
        print(f"📋 {item.product.name}: {item.quantity} x ${item.price_at_purchase} = ${item_total}")
    
    print(f"\n🎯 FINAL RESULT")
    print("-" * 15)
    
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Product-specific discounts work correctly")
        print("✅ Discounts only apply to eligible products")
        print("✅ Non-eligible products don't affect discount calculations")
    else:
        print("❌ TESTS FAILED!")
        print("🔧 Product-specific discount logic needs review")
    
    # Cleanup
    print(f"\n🧹 Cleaning up test data...")
    offer.delete()
    cart.delete()
    print("✅ Cleanup complete")
    
    return success

if __name__ == "__main__":
    main()
