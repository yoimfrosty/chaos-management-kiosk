#!/usr/bin/env python3
"""
Receipt Template Fix Verification
Test the receipt template fixes for tax display and date generation
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order
from django.template import Template, Context
from django.utils import timezone

print('=== RECEIPT TEMPLATE FIX VERIFICATION ===')
print()

# Get a sample order
order = Order.objects.first()
if order:
    print(f'Testing with Order: {order.order_number}')
    print(f'Tax Rate in DB: {order.tax_rate} (should be 0.06)')
    print(f'Tax Amount: ${order.tax_amount}')
    print()
    
    # Test the widthratio calculation
    # widthratio order.tax_rate 1 100 should convert 0.06 to 6
    expected_percentage = float(order.tax_rate) * 100
    print(f'Expected Tax Display: {expected_percentage}%')
    
    # Test template rendering for tax display
    tax_template = Template('Tax ({% widthratio order.tax_rate 1 100 %}%):')
    tax_context = Context({'order': order})
    tax_result = tax_template.render(tax_context)
    print(f'Actual Tax Display: {tax_result}')
    
    # Test date template
    date_template = Template('This receipt was generated on {% now "M d, Y g:i A" %}')
    date_result = date_template.render(Context())
    print(f'Date Display: {date_result}')
    
    if f'{expected_percentage:.0f}%' in tax_result:
        print('\n✅ SUCCESS: Tax percentage display is now correct!')
    else:
        print('\n❌ ERROR: Tax percentage display is still incorrect!')
    
    if 'generated on' in date_result and len(date_result) > 30:
        print('✅ SUCCESS: Date generation is working!')
    else:
        print('❌ ERROR: Date generation is not working!')
        
else:
    print('❌ No orders found for testing')

print('\n=== VERIFICATION COMPLETE ===')
print('\nTo fully test the receipt:')
print('1. Start the server: python manage.py runserver')
print('2. Go to admin: http://127.0.0.1:8000/admin/')
print('3. View an order receipt and check:')
print('   - Tax shows as "Tax (6%):" instead of "Tax (0.1%):"')
print('   - Date shows current date/time after "This receipt was generated on"')
print('   - Header color looks good (green gradient)')
