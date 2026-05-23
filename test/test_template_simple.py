#!/usr/bin/env python3

import os
import sys
import django

# Add the project directory to the path
sys.path.append('/home/ubuntu/django-app')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

print("Testing template rendering...")

try:
    from django.template.loader import get_template
    from kiosk.models import Order
    
    # Get a real order
    order = Order.objects.get(id=130)
    print(f"Order found: {order.order_number}")
    
    # Load template
    template = get_template('kiosk/order_receipt.html')
    print("Template loaded successfully")
    
    # Create context
    context = {
        'order': order,
        'debug_info': {
            'order_id': order.id,
            'order_number': order.order_number,
            'has_items': order.items.exists(),
            'items_count': order.items.count(),
        }
    }
    print("Context created")
    
    # Render template
    html = template.render(context)
    print(f"Template rendered: {len(html)} characters")
    
    if len(html) == 0:
        print("ERROR: Template rendered but is empty!")
    else:
        print("SUCCESS: Template rendered with content")
        print(f"First 200 characters: {html[:200]}")
        
        # Save to file for inspection
        with open('/home/ubuntu/django-app/test_output.html', 'w') as f:
            f.write(html)
        print("Saved output to test_output.html")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
