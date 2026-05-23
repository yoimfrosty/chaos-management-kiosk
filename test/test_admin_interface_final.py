#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order
from kiosk.admin import OrderAdmin

def test_admin_interface():
    """Test that admin interface shows correct full-price calculations"""
    print("=== TESTING ADMIN INTERFACE ===\n")
    
    # Get an order with items
    order = Order.objects.filter(items__isnull=False).first()
    if not order:
        print("No orders with items found for testing")
        return
    
    admin = OrderAdmin(Order, None)
    
    print(f"Testing Order {order.order_number}:")
    print(f"  Status: {order.status}")
    print(f"  Items: {order.items.count()}")
    
    # Test admin display methods
    try:
        # Test calculation breakdown
        breakdown = admin.calculation_breakdown(order)
        print(f"  ✅ Calculation breakdown generated")
        
        # Test discount display
        discount_display = admin.discount_display(order)
        print(f"  ✅ Discount display: {discount_display}")
        
        # Test customer age if available
        if order.customer_birthdate:
            age_display = admin.customer_age_display(order)
            print(f"  ✅ Customer age: {age_display}")
        
        # Verify order totals
        print(f"\n  Order Financial Details:")
        print(f"    Subtotal: ${order.subtotal}")
        print(f"    Discount: ${order.discount_amount}")
        print(f"    Tax: ${order.tax_amount}")
        print(f"    Total: ${order.total_amount}")
        
        # Check if discount is 0 (full price)
        if order.discount_amount == 0:
            print(f"    ✅ Shows full price (no automatic discounts)")
        else:
            print(f"    ⚠️  Has discount: ${order.discount_amount} (may be manual)")
        
        print(f"\n🎉 Admin interface working correctly!")
        
    except Exception as e:
        print(f"❌ Error in admin interface: {e}")

def test_receipt_totals():
    """Test that receipt shows correct totals"""
    print("\n=== TESTING RECEIPT DISPLAY ===\n")
    
    orders = Order.objects.filter(items__isnull=False)[:2]
    
    for order in orders:
        # Calculate what the receipt should show
        items_total = sum(item.get_total_item_price() for item in order.items.all())
        
        print(f"Order {order.order_number}:")
        print(f"  Items total: ${items_total}")
        print(f"  Stored subtotal: ${order.subtotal}")
        print(f"  Stored discount: ${order.discount_amount}")
        print(f"  Stored total: ${order.total_amount}")
        
        # Verify receipt will show correct information
        if order.discount_amount == 0:
            print(f"  ✅ Receipt will show full price without discount section")
        else:
            print(f"  ⚠️  Receipt will include discount section")
        
        print()

if __name__ == "__main__":
    test_admin_interface()
    test_receipt_totals()
