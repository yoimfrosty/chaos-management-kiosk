#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order

def test_receipt_functionality():
    """Test receipt URLs and functionality"""
    print("=== RECEIPT FUNCTIONALITY TEST ===\n")
    
    # Get orders with items
    orders_with_items = Order.objects.filter(items__isnull=False).distinct()
    
    print(f"Found {orders_with_items.count()} orders with items")
    
    for order in orders_with_items[:3]:  # Test first 3 orders
        print(f"\nOrder {order.order_number}:")
        print(f"  Status: {order.status}")
        print(f"  Items: {order.items.count()}")
        print(f"  Customer: {order.customer_name or 'Not provided'}")
        print(f"  Total: ${order.total_amount}")
        print(f"  Receipt URL: /admin/kiosk/order/{order.id}/receipt/")
        
        # Test calculation breakdown
        actual_subtotal = sum(item.get_total_item_price() for item in order.items.all())
        after_discount = actual_subtotal - order.discount_amount
        expected_tax = after_discount * order.tax_rate
        expected_total = after_discount + expected_tax
        
        print(f"  Calculation Check:")
        print(f"    Subtotal: ${actual_subtotal}")
        if order.discount_amount > 0:
            print(f"    Discount: -${order.discount_amount}")
            print(f"    After discount: ${after_discount}")
        print(f"    Tax: ${expected_tax:.2f}")
        print(f"    Total: ${expected_total:.2f}")
        print(f"    ✅ Match: {abs(order.total_amount - expected_total) < 0.01}")

if __name__ == "__main__":
    test_receipt_functionality()
