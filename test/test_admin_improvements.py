#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order, OrderItem
from django.test import Client
from django.contrib.auth.models import User
from decimal import Decimal

def test_admin_improvements():
    """Test all admin improvements for order totals and receipts"""
    print("=== ADMIN IMPROVEMENTS TEST ===\n")
    
    # Test order with discount (the problematic one from screenshot)
    try:
        order = Order.objects.get(order_number='OCH-B1A62C')
        print(f"Testing Order {order.order_number}:")
        print(f"  Status: {order.status}")
        print(f"  Subtotal: ${order.subtotal}")
        print(f"  Discount: ${order.discount_amount}")
        print(f"  Tax Rate: {order.tax_rate}")
        print(f"  Tax Amount: ${order.tax_amount}")
        print(f"  Total: ${order.total_amount}")
        
        # Verify calculation
        after_discount = order.subtotal - order.discount_amount
        expected_tax = after_discount * order.tax_rate
        expected_total = after_discount + expected_tax
        
        print(f"\n  Manual Calculation:")
        print(f"    Subtotal: ${order.subtotal}")
        print(f"    Less discount: -${order.discount_amount}")
        print(f"    After discount: ${after_discount}")
        print(f"    Tax ({order.tax_rate*100}%): ${expected_tax:.2f}")
        print(f"    Expected total: ${expected_total:.2f}")
        print(f"    Stored total: ${order.total_amount}")
        print(f"    ✅ Correct: {abs(order.total_amount - expected_total) < 0.01}")
        
        # Test items calculation
        items_total = sum(item.get_total_item_price() for item in order.items.all())
        print(f"\n  Items verification:")
        for item in order.items.all():
            print(f"    {item.quantity}x {item.product.name} @ ${item.price_at_purchase} = ${item.get_total_item_price()}")
        print(f"    Total from items: ${items_total}")
        print(f"    Matches subtotal: {items_total == order.subtotal}")
        
        # Test get_customer_age method
        if order.customer_birthdate:
            age = order.get_customer_age()
            print(f"\n  Customer info:")
            print(f"    Name: {order.customer_name}")
            print(f"    Birthdate: {order.customer_birthdate}")
            print(f"    Calculated age: {age} years")
        
    except Order.DoesNotExist:
        print("Test order OCH-B1A62C not found")
    
    print(f"\n=== TESTING RECEIPT FUNCTIONALITY ===")
    
    # Test receipt for orders with items
    orders_with_items = Order.objects.filter(items__isnull=False).distinct()[:3]
    
    for order in orders_with_items:
        print(f"\nOrder {order.order_number}:")
        print(f"  Has {order.items.count()} items")
        print(f"  Customer: {order.customer_name or 'Not provided'}")
        print(f"  Receipt URL: /admin/kiosk/order/{order.id}/receipt/")
        print(f"  Total calculation correct: {test_order_calculation(order)}")

def test_order_calculation(order):
    """Test if an order's calculation is correct"""
    try:
        items_total = sum(item.get_total_item_price() for item in order.items.all())
        after_discount = items_total - order.discount_amount
        expected_tax = after_discount * Decimal(str(order.tax_rate))
        expected_total = after_discount + expected_tax
        
        return abs(order.total_amount - expected_total) < Decimal('0.01')
    except Exception as e:
        print(f"    Error calculating: {e}")
        return False

if __name__ == "__main__":
    test_admin_improvements()
