#!/usr/bin/env python3
"""
Check what orders exist in the database
"""

import os
import sys
import django

# Add the project to Python path
sys.path.append('/home/ubuntu/django-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')

# Setup Django
django.setup()

from kiosk.models import Order, OrderItem

def check_orders():
    """Check what orders exist in the database"""
    print("🔍 Checking Orders in Database")
    print("="*40)
    
    orders = Order.objects.all().order_by('-created_at')
    
    print(f"Total orders found: {orders.count()}")
    
    if orders.count() == 0:
        print("❌ No orders in database")
        return False
    
    print("\n📋 Recent orders:")
    for order in orders[:10]:  # Show first 10
        items_count = order.items.count()
        print(f"   Order {order.id}: {order.order_number} - {order.status} - {items_count} items - ${order.total_amount}")
        
        # Show items for first few orders
        if order.id <= 5:
            for item in order.items.all()[:3]:  # Show first 3 items
                print(f"      - {item.product.name} x{item.quantity} @ ${item.price_at_purchase}")
    
    # Test a specific order
    test_order = orders.first()
    print(f"\n🧪 Testing order {test_order.id} ({test_order.order_number}):")
    print(f"   Status: {test_order.status}")
    print(f"   Items: {test_order.items.count()}")
    print(f"   Total: ${test_order.total_amount}")
    print(f"   Created: {test_order.created_at}")
    
    return True

if __name__ == "__main__":
    check_orders()
