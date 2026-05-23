#!/usr/bin/env python3

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order
from django.template.loader import render_to_string
from django.http import HttpRequest

def test_template_rendering():
    """Test if the template renders correctly"""
    
    print("🔍 Testing Template Rendering")
    print("=" * 50)
    
    # Get order 130
    try:
        order = Order.objects.get(id=130)
        print(f"✔ Found order: {order.order_number}")
        print(f"   Total: ${order.total}")
        print(f"   Status: {order.status}")
        print(f"   Items: {order.items.count()}")
    except Order.DoesNotExist:
        print("❌ Order 130 not found")
        return
    
    # Test template rendering
    context = {
        'order': order,
        'debug_info': {
            'order_id': order.id,
            'order_number': getattr(order, 'order_number', f'OCH-{order.id}'),
            'has_items': order.items.exists() if hasattr(order, 'items') else False,
            'items_count': order.items.count() if hasattr(order, 'items') else 0,
            'note': 'DEBUGGING BLANK RECEIPT'
        }
    }
    
    try:
        # Try to render the template
        rendered_html = render_to_string('kiosk/order_receipt.html', context)
        print(f"✔ Template rendered successfully")
        print(f"   Length: {len(rendered_html)} characters")
        print(f"   First 200 chars: {rendered_html[:200]}...")
        
        # Write to file for inspection
        with open('/home/ubuntu/django-app/debug_rendered_receipt.html', 'w') as f:
            f.write(rendered_html)
        print("✔ Written rendered HTML to debug_rendered_receipt.html")
        
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        import traceback
        traceback.print_exc()

def test_view_directly():
    """Test the view function directly"""
    
    print("\n🔍 Testing View Function Directly")
    print("=" * 50)
    
    from kiosk.views import print_receipt_no_age_check
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.get('/receipt-no-age/130/')
    
    try:
        response = print_receipt_no_age_check(request, 130)
        print(f"✔ View executed successfully")
        print(f"   Status code: {response.status_code}")
        print(f"   Content type: {response.get('Content-Type', 'Not set')}")
        
        if hasattr(response, 'content'):
            content_length = len(response.content)
            print(f"   Content length: {content_length}")
            if content_length > 0:
                print(f"   First 200 chars: {response.content[:200]}")
            else:
                print("   ❌ Content is empty!")
        
        # Check if it's a render response
        if hasattr(response, 'context_data'):
            print(f"   Context data: {response.context_data}")
            
    except Exception as e:
        print(f"❌ View execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_template_rendering()
    test_view_directly()
