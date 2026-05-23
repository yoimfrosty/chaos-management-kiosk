#!/usr/bin/env python3
"""
Simple test to verify product-specific discount isolation
Tests the core issue: discounts should only apply to eligible products
"""

import subprocess
import sys

def run_django_command(command):
    """Run a Django management command and return the output"""
    try:
        result = subprocess.run(
            ["python3", "manage.py", "shell", "-c", command],
            capture_output=True,
            text=True,
            timeout=30,
            cwd="/Users/uba/Desktop/hemp-app/chaos-magement"
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", "Command timed out"
    except Exception as e:
        return "", str(e)

def main():
    print("🧪 TESTING PRODUCT-SPECIFIC DISCOUNT ISOLATION")
    print("=" * 55)
    print("Issue: When adding a discounted product, then a non-discounted product,")
    print("the non-discounted product should NOT receive the discount.")
    print()

    # Test command
    test_command = '''
from decimal import Decimal
from django.test import RequestFactory
from kiosk.models import Product, SpecialOffer, Order, OrderItem
from kiosk.views import check_and_apply_automatic_discounts

# Get two different products
products = list(Product.objects.all()[:2])
if len(products) < 2:
    print("ERROR: Need at least 2 products")
    exit()

product_eligible = products[0]
product_not_eligible = products[1]

print(f"Testing with:")
print(f"  Eligible: {product_eligible.name} (${product_eligible.price})")
print(f"  Not eligible: {product_not_eligible.name} (${product_not_eligible.price})")

# Create test discount that only applies to first product
test_offer = SpecialOffer.objects.create(
    title="TEST: 20% Off Single Product",
    description="Test discount for single product",
    discount_type="Percentage",
    discount_value=Decimal("20.00"),
    is_active=True
)
test_offer.applicable_products.add(product_eligible)

# Create test cart
cart = Order.objects.create(status="Pending")
factory = RequestFactory()
request = factory.get("/")
request.session = {}

print("\\nStep 1: Add eligible product")
# Add eligible product
OrderItem.objects.create(
    order=cart,
    product=product_eligible,
    quantity=1,
    price_at_purchase=product_eligible.price
)

# Apply automatic discounts
applied = check_and_apply_automatic_discounts(request, cart, product_eligible)
session_discounts = request.session.get("applied_discounts", [])
cart.recalculate_totals(session_discounts)

print(f"  Applied discounts: {applied}")
print(f"  Subtotal: ${cart.subtotal}")
print(f"  Discount: ${cart.discount_amount}")

# Store state after first product
discount_after_eligible = cart.discount_amount

print("\\nStep 2: Add non-eligible product")
# Add non-eligible product
OrderItem.objects.create(
    order=cart,
    product=product_not_eligible,
    quantity=1,
    price_at_purchase=product_not_eligible.price
)

# Check for new discounts (should be none)
new_applied = check_and_apply_automatic_discounts(request, cart, product_not_eligible)
session_discounts = request.session.get("applied_discounts", [])
cart.recalculate_totals(session_discounts)

print(f"  New discounts: {new_applied}")
print(f"  Subtotal: ${cart.subtotal}")
print(f"  Discount: ${cart.discount_amount}")

print("\\nVerification:")
expected_discount = product_eligible.price * Decimal("0.20")
print(f"  Expected discount (20% of ${product_eligible.price}): ${expected_discount}")
print(f"  Actual discount: ${cart.discount_amount}")

# Check if discount is correct
if abs(cart.discount_amount - expected_discount) < Decimal("0.01"):
    print("  ✅ PASS: Discount only applies to eligible product")
    success = True
else:
    print("  ❌ FAIL: Discount calculation is wrong")
    success = False

# Check if discount didn't change when adding non-eligible product
if abs(cart.discount_amount - discount_after_eligible) < Decimal("0.01"):
    print("  ✅ PASS: Discount unchanged when adding non-eligible product")
else:
    print("  ❌ FAIL: Discount changed when adding non-eligible product")
    success = False

# Cleanup
test_offer.delete()
cart.delete()

print(f"\\nResult: {'SUCCESS' if success else 'FAILURE'}")
'''

    print("Running test...")
    stdout, stderr = run_django_command(test_command)
    
    if stderr:
        print(f"❌ Error occurred: {stderr}")
        return False
    
    if stdout:
        print(stdout)
    else:
        print("⚠️ No output received from test")
        return False
    
    # Check if test passed
    if "SUCCESS" in stdout:
        print("\n🎉 OVERALL TEST RESULT: PASSED")
        print("✅ Product-specific discounts are working correctly")
        print("✅ Non-eligible products do not receive discounts")
        return True
    else:
        print("\n❌ OVERALL TEST RESULT: FAILED")
        print("🔧 Product-specific discount logic needs review")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
