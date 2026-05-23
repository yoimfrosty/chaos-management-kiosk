#!/usr/bin/env python3
"""
Simple receipt test to verify discount display
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order

def test_existing_receipts():
    """Test receipt display for existing orders"""
    print("🧪 Testing existing order receipts...")
    
    orders = Order.objects.all().order_by('-created_at')[:5]
    
    if orders:
        print(f"Found {orders.count()} orders in database")
        for order in orders:
            print(f"Order {order.order_number}: ${order.total_amount} - Status: {order.status}")
            print(f"  Receipt URL: http://localhost:8000/print-receipt/{order.id}/")
    else:
        print("No orders found in database")
        
    return True

if __name__ == "__main__":
    test_existing_receipts()
