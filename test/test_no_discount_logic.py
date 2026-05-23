#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order, OrderItem, Product
from decimal import Decimal

def test_no_automatic_discounts():
    """Test that orders are created without automatic discounts"""
    print("=== TESTING NO AUTOMATIC DISCOUNTS ===\n")
    
    # Get a test product
    products = Product.objects.filter(is_available=True)[:2]
    if not products:
        print("No products available for testing")
        return
    
    # Create a test order
    order = Order.objects.create(
        status='Pending',
        session_key='test_session_no_discounts'
    )
    
    # Add items to the order
    item1 = OrderItem.objects.create(
        order=order,
        product=products[0],
        quantity=2,
        price_at_purchase=products[0].price
    )
    
    if len(products) > 1:
        item2 = OrderItem.objects.create(
            order=order,
            product=products[1],
            quantity=1,
            price_at_purchase=products[1].price
        )
    
    # Recalculate totals without any discounts
    order.recalculate_totals()
    
    print(f"Test Order {order.order_number}:")
    print(f"  Items added:")
    for item in order.items.all():
        print(f"    {item.quantity}x {item.product.name} @ ${item.price_at_purchase} = ${item.get_total_item_price()}")
    
    # Calculate expected totals
    expected_subtotal = sum(item.get_total_item_price() for item in order.items.all())
    expected_tax = expected_subtotal * Decimal(str(order.tax_rate))
    expected_total = expected_subtotal + expected_tax
    
    print(f"\n  Expected calculation:")
    print(f"    Subtotal: ${expected_subtotal}")
    print(f"    Tax (6%): ${expected_tax:.2f}")
    print(f"    Total: ${expected_total:.2f}")
    
    print(f"\n  Actual order values:")
    print(f"    Subtotal: ${order.subtotal}")
    print(f"    Discount: ${order.discount_amount}")
    print(f"    Tax: ${order.tax_amount}")
    print(f"    Total: ${order.total_amount}")
    
    # Verify no discounts were applied
    discounts_correct = order.discount_amount == Decimal('0.00')
    totals_correct = abs(order.total_amount - expected_total) < Decimal('0.01')
    
    print(f"\n  Results:")
    print(f"    ✅ No discounts applied: {discounts_correct}")
    print(f"    ✅ Totals correct: {totals_correct}")
    print(f"    ✅ Full price calculation: {order.subtotal == expected_subtotal}")
    
    # Clean up test order
    order.delete()
    
    if discounts_correct and totals_correct:
        print(f"\n🎉 SUCCESS: Order totals calculated correctly without automatic discounts!")
    else:
        print(f"\n❌ ISSUE: Something is not working as expected")

def test_existing_orders():
    """Test existing orders to see how they're calculated"""
    print("\n=== TESTING EXISTING ORDERS ===\n")
    
    orders = Order.objects.filter(items__isnull=False).distinct()[:3]
    
    for order in orders:
        # Recalculate without discounts
        old_total = order.total_amount
        old_discount = order.discount_amount
        
        order.recalculate_totals()  # This should now calculate without automatic discounts
        
        print(f"Order {order.order_number}:")
        print(f"  Old total: ${old_total}, Old discount: ${old_discount}")
        print(f"  New total: ${order.total_amount}, New discount: ${order.discount_amount}")
        print(f"  Status: {order.status}")
        
        if order.discount_amount == Decimal('0.00'):
            print(f"  ✅ Discount removed - now showing full price")
        else:
            print(f"  ⚠️  Discount still present (may be manually applied)")
        print()

if __name__ == "__main__":
    test_no_automatic_discounts()
    test_existing_orders()
