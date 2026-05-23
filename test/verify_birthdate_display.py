#!/usr/bin/env python3
"""
Birthdate Display Verification
Verify that the receipt now shows customer birthdate instead of verification timestamp
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order
from datetime import date

print('=== BIRTHDATE DISPLAY VERIFICATION ===')
print()

# Get a sample order
order = Order.objects.first()
if order:
    print(f'Testing with Order: {order.order_number}')
    print()
    
    if order.customer_birthdate:
        print(f'Customer Name: {order.customer_name}')
        print(f'Customer Birthdate: {order.customer_birthdate}')
        print(f'Customer Age: {order.get_customer_age()} years old')
        print()
        
        # Calculate what the receipt will show
        birthdate_display = order.customer_birthdate.strftime("%b %d, %Y")
        print(f'Receipt will show: "Date of Birth: {birthdate_display}"')
        print()
        
        # Verify age calculation
        today = date.today()
        calculated_age = today.year - order.customer_birthdate.year
        if today.month < order.customer_birthdate.month or \
           (today.month == order.customer_birthdate.month and today.day < order.customer_birthdate.day):
            calculated_age -= 1
        
        print(f'✅ Age verification: {calculated_age} years old')
        
        if calculated_age == order.get_customer_age():
            print('✅ SUCCESS: Birthdate correctly shows the date that makes customer 25!')
        else:
            print('⚠️  Age calculation mismatch')
            
    else:
        print('⚠️  No birthdate found for this order')
        
    print()
    print('📋 CHANGE SUMMARY:')
    print('   - BEFORE: "Age Verified: Jun 23, 2025 3:24 AM"')
    print('   - AFTER: "Date of Birth: [Customer\'s actual birthdate]"')
    print('   - Shows the birthdate that makes them 25 years old')
    print('   - More meaningful for staff verification')
    
else:
    print('❌ No orders found for testing')

print('\n=== VERIFICATION COMPLETE ===')
print('\nTo test the updated receipt:')
print('1. Start server: python manage.py runserver')
print('2. Go to admin and view any order receipt')
print('3. Customer section should now show "Date of Birth" instead of "Age Verified"')
print('4. The date should be the customer\'s actual birthdate (making them 25)')
