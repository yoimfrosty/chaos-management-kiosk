#!/usr/bin/env python3
"""
Comprehensive test for multiple discount scenarios to ensure the fix is robust
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

def test_multiple_scenarios():
    """Test multiple discount scenarios to ensure robustness"""
    print("🧪 COMPREHENSIVE DISCOUNT SYSTEM TEST")
    print("=" * 45)
    
    # Get products for testing
    products = list(Product.objects.all()[:4])
    if len(products) < 4:
        print("❌ Need at least 4 products for comprehensive testing")
        return False
    
    # Clean up any existing test offers
    SpecialOffer.objects.filter(title__contains="COMPREHENSIVE TEST").delete()
    
    print("📦 Test Products:")
    for i, product in enumerate(products):
        print(f"   {i+1}. {product.name} (${product.price})")
    
    # Create test scenarios
    scenarios = []
    
    # Scenario 1: Product-specific discount
    scenario1_offer = SpecialOffer.objects.create(
        title="COMPREHENSIVE TEST: Product A - 15% Off",
        description="15% off Product A only",
        discount_type="Percentage",
        discount_value=Decimal("15.00"),
        is_active=True
    )
    scenario1_offer.applicable_products.add(products[0])
    scenarios.append(("Product-Specific Discount", scenario1_offer, [products[0]], products[1:]))
    
    # Scenario 2: Multiple product discount
    scenario2_offer = SpecialOffer.objects.create(
        title="COMPREHENSIVE TEST: Products A&B - 20% Off",
        description="20% off Products A and B",
        discount_type="Percentage",
        discount_value=Decimal("20.00"),
        is_active=True
    )
    scenario2_offer.applicable_products.add(products[0], products[1])
    scenarios.append(("Multi-Product Discount", scenario2_offer, products[:2], products[2:]))
    
    # Test each scenario
    all_passed = True
    
    for scenario_name, offer, eligible_products, non_eligible_products in scenarios:
        print(f"\n🎯 TESTING: {scenario_name}")
        print("-" * (len(scenario_name) + 12))
        
        # Create fresh cart for each scenario
        cart = Order.objects.create(status='Pending')
        factory = RequestFactory()
        request = factory.get('/')
        request.session = {}
        
        print(f"🛒 Test cart: {cart.order_number}")
        print(f"📊 Offer: {offer.title} ({offer.discount_value}% off)")
        
        eligible_names = [p.name for p in eligible_products]
        non_eligible_names = [p.name for p in non_eligible_products[:2]]  # Test with 2 non-eligible
        print(f"✅ Eligible: {eligible_names}")
        print(f"🚫 Non-eligible: {non_eligible_names}")
        
        # Step 1: Add all eligible products
        print("\\n   Step 1: Adding eligible products...")
        total_eligible_value = Decimal('0.00')
        for product in eligible_products:
            OrderItem.objects.create(
                order=cart,
                product=product,
                quantity=1,
                price_at_purchase=product.price
            )
            total_eligible_value += product.price
            
            # Apply discounts
            applied = check_and_apply_automatic_discounts(request, cart, product)
            if applied:
                print(f"      {product.name}: Discount applied: {applied}")
            else:
                print(f"      {product.name}: No new discounts")
        
        # Calculate after eligible products
        session_discounts = request.session.get('applied_discounts', [])
        cart.recalculate_totals(session_discounts)
        
        expected_discount = total_eligible_value * (offer.discount_value / 100)
        print(f"   After eligible products:")
        print(f"      Subtotal: ${cart.subtotal}")
        print(f"      Discount: ${cart.discount_amount} (expected: ${expected_discount})")
        
        # Verify discount is correct for eligible products
        if abs(cart.discount_amount - expected_discount) < Decimal('0.01'):
            print("      ✅ Discount correctly applied to eligible products")
            step1_pass = True
        else:
            print("      ❌ Discount amount is incorrect")
            step1_pass = False
            all_passed = False
        
        discount_after_eligible = cart.discount_amount
        
        # Step 2: Add non-eligible products
        print("\\n   Step 2: Adding non-eligible products...")
        for product in non_eligible_products[:2]:  # Add 2 non-eligible
            OrderItem.objects.create(
                order=cart,
                product=product,
                quantity=1,
                price_at_purchase=product.price
            )
            
            # Check for new discounts (should be none)
            new_applied = check_and_apply_automatic_discounts(request, cart, product)
            if new_applied:
                print(f"      {product.name}: Unexpected discounts: {new_applied}")
            else:
                print(f"      {product.name}: No discounts (correct)")
        
        # Recalculate after non-eligible products
        session_discounts = request.session.get('applied_discounts', [])
        cart.recalculate_totals(session_discounts)
        
        print(f"   After non-eligible products:")
        print(f"      Subtotal: ${cart.subtotal}")
        print(f"      Discount: ${cart.discount_amount}")
        
        # Verify discount didn't change
        if abs(cart.discount_amount - discount_after_eligible) < Decimal('0.01'):
            print("      ✅ Discount unchanged after adding non-eligible products")
            step2_pass = True
        else:
            print("      ❌ Discount incorrectly changed")
            step2_pass = False
            all_passed = False
        
        # Verify final discount amount
        if abs(cart.discount_amount - expected_discount) < Decimal('0.01'):
            print("      ✅ Final discount amount is correct")
            step3_pass = True
        else:
            print("      ❌ Final discount amount is wrong")
            step3_pass = False
            all_passed = False
        
        scenario_pass = step1_pass and step2_pass and step3_pass
        print(f"\\n   Scenario Result: {'✅ PASS' if scenario_pass else '❌ FAIL'}")
        
        # Clean up
        offer.delete()
        cart.delete()
    
    print(f"\\n🎯 OVERALL RESULT:")
    if all_passed:
        print("🎉 ALL SCENARIOS PASSED!")
        print("✅ Product-specific discount system is working correctly")
        print("✅ Non-eligible products never receive discounts")
        print("✅ Multiple eligible products work correctly")
        print("✅ The discount system is robust and reliable")
    else:
        print("❌ SOME SCENARIOS FAILED!")
        print("🔧 Further fixes may be needed")
    
    return all_passed

def test_edge_cases():
    """Test edge cases for discount system"""
    print("\\n🔬 TESTING EDGE CASES")
    print("=" * 25)
    
    # Clean up
    SpecialOffer.objects.filter(title__contains="EDGE CASE TEST").delete()
    
    products = list(Product.objects.all()[:2])
    
    # Edge Case 1: Zero-value product
    print("\\n📍 Edge Case 1: Quantity changes")
    
    offer = SpecialOffer.objects.create(
        title="EDGE CASE TEST: 10% Off",
        description="10% off for testing",
        discount_type="Percentage",
        discount_value=Decimal("10.00"),
        is_active=True
    )
    offer.applicable_products.add(products[0])
    
    cart = Order.objects.create(status='Pending')
    factory = RequestFactory()
    request = factory.get('/')
    request.session = {}
    
    # Add eligible product with quantity 1
    item = OrderItem.objects.create(
        order=cart,
        product=products[0],
        quantity=1,
        price_at_purchase=products[0].price
    )
    
    # Apply discount
    check_and_apply_automatic_discounts(request, cart, products[0])
    session_discounts = request.session.get('applied_discounts', [])
    cart.recalculate_totals(session_discounts)
    
    discount_qty1 = cart.discount_amount
    print(f"   Quantity 1: Discount = ${discount_qty1}")
    
    # Increase quantity to 2
    item.quantity = 2
    item.save()
    cart.recalculate_totals(session_discounts)
    
    discount_qty2 = cart.discount_amount
    expected_qty2 = products[0].price * 2 * Decimal("0.10")
    
    print(f"   Quantity 2: Discount = ${discount_qty2} (expected: ${expected_qty2})")
    
    if abs(discount_qty2 - expected_qty2) < Decimal('0.01'):
        print("   ✅ Discount scales correctly with quantity")
        edge_case1_pass = True
    else:
        print("   ❌ Discount doesn't scale correctly")
        edge_case1_pass = False
    
    # Clean up
    offer.delete()
    cart.delete()
    
    return edge_case1_pass

if __name__ == "__main__":
    try:
        print("🚀 STARTING COMPREHENSIVE DISCOUNT SYSTEM VERIFICATION")
        print("=" * 60)
        
        # Run main tests
        main_tests_pass = test_multiple_scenarios()
        
        # Run edge case tests
        edge_tests_pass = test_edge_cases()
        
        print("\\n" + "=" * 60)
        print("🏁 FINAL VERIFICATION RESULTS")
        print("=" * 60)
        
        if main_tests_pass and edge_tests_pass:
            print("🎉 ALL TESTS PASSED!")
            print("✅ The discount system fix is COMPLETE and WORKING")
            print("✅ Discounts are now properly applied per-product")
            print("✅ Non-eligible products do not receive discounts")
            print("✅ The original issue has been RESOLVED")
        else:
            main_status = "✅ PASS" if main_tests_pass else "❌ FAIL"
            edge_status = "✅ PASS" if edge_tests_pass else "❌ FAIL"
            print(f"Main Tests: {main_status}")
            print(f"Edge Cases: {edge_status}")
            print("🔧 Some issues remain - further investigation needed")
        
    except Exception as e:
        print(f"\\n💥 ERROR: {e}")
        import traceback
        traceback.print_exc()
