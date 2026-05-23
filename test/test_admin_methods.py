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

def test_admin_methods():
    """Test all the admin methods that might cause format errors"""
    print("=== TESTING ADMIN METHODS ===\n")
    
    admin = OrderAdmin(Order, None)
    
    # Get an order with items and customer info
    order = Order.objects.filter(items__isnull=False, customer_name__isnull=False).first()
    
    if not order:
        print("No suitable test order found")
        return
    
    print(f"Testing with Order {order.order_number}")
    
    try:
        # Test customer_age_display
        age_display = admin.customer_age_display(order)
        print(f"✅ customer_age_display: {age_display}")
    except Exception as e:
        print(f"❌ customer_age_display error: {e}")
    
    try:
        # Test calculation_breakdown
        calc_breakdown = admin.calculation_breakdown(order)
        print(f"✅ calculation_breakdown: Generated {len(calc_breakdown)} chars of HTML")
    except Exception as e:
        print(f"❌ calculation_breakdown error: {e}")
    
    try:
        # Test discount_display
        discount_display = admin.discount_display(order)
        print(f"✅ discount_display: {discount_display}")
    except Exception as e:
        print(f"❌ discount_display error: {e}")
    
    try:
        # Test item_count
        item_count = admin.item_count(order)
        print(f"✅ item_count: {item_count}")
    except Exception as e:
        print(f"❌ item_count error: {e}")
    
    try:
        # Test receipt_link
        receipt_link = admin.receipt_link(order)
        print(f"✅ receipt_link: Generated receipt link")
    except Exception as e:
        print(f"❌ receipt_link error: {e}")

if __name__ == "__main__":
    test_admin_methods()
