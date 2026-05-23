#!/usr/bin/env python3
"""
Update Existing Orders Tax Calculation
Recalculate tax for existing orders to ensure 6% rate is applied
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order
from decimal import Decimal

print('=== UPDATING EXISTING ORDERS TAX CALCULATION ===')
print()

# Get all orders
orders = Order.objects.all()
print(f'Found {orders.count()} orders in the system')

if orders.count() > 0:
    updated_count = 0
    
    for order in orders:
        # Store original values
        original_tax = order.tax_amount
        original_total = order.total_amount
        
        # Recalculate with current 6% tax rate
        order.recalculate_totals()
        
        # Check if anything changed
        if original_tax != order.tax_amount or original_total != order.total_amount:
            print(f'Order {order.order_number}:')
            print(f'  Tax: ${original_tax} → ${order.tax_amount}')
            print(f'  Total: ${original_total} → ${order.total_amount}')
            updated_count += 1
        else:
            print(f'Order {order.order_number}: Already correct')
    
    print(f'\n✅ Updated {updated_count} orders with correct 6% tax calculation')
    print(f'✅ {orders.count() - updated_count} orders were already correct')
else:
    print('No orders found in the system')

print('\n=== UPDATE COMPLETE ===')
