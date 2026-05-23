#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
sys.path.append('/home/ubuntu/django-app')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')

# Setup Django
django.setup()

from django.template.loader import render_to_string, get_template
from django.template import Context, Template
from kiosk.models import Order
import traceback

def test_template_rendering():
    print("=== Testing Template Rendering ===")
    
    try:
        # First check if orders exist
        orders = Order.objects.all()
        print(f"Found {orders.count()} orders in database")
        
        if orders.exists():
            order = orders.first()
            print(f"Testing with order: {order.id} - {order.order_number}")
            
            # Test context
            context = {
                'order': order,
                'order_id': order.id,
                'debug_info': {'test': 'direct_rendering', 'order_exists': True}
            }
            
        else:
            print("No orders found, creating test context")
            context = {
                'order': None,
                'order_id': 999,
                'debug_info': {'test': 'no_order', 'order_exists': False}
            }
        
        # Test 1: Try rendering the simple test template
        print("\n--- Test 1: Simple Test Template ---")
        try:
            html = render_to_string('kiosk/simple_receipt_test.html', context)
            print(f"✓ Template rendered successfully")
            print(f"  HTML length: {len(html)} characters")
            print(f"  First 300 chars: {html[:300]}")
            if len(html) > 300:
                print(f"  ...truncated...")
        except Exception as e:
            print(f"✗ Error rendering simple test template: {e}")
            traceback.print_exc()
        
        # Test 2: Try rendering the original receipt template
        print("\n--- Test 2: Original Receipt Template ---")
        try:
            html = render_to_string('kiosk/order_receipt.html', context)
            print(f"✓ Original template rendered successfully")
            print(f"  HTML length: {len(html)} characters")
            print(f"  First 300 chars: {html[:300]}")
        except Exception as e:
            print(f"✗ Error rendering original template: {e}")
            traceback.print_exc()
        
        # Test 3: Check template loader directly
        print("\n--- Test 3: Template Loader Test ---")
        try:
            template = get_template('kiosk/simple_receipt_test.html')
            print(f"✓ Template loaded successfully: {template}")
            html = template.render(context)
            print(f"✓ Template rendered via get_template: {len(html)} characters")
        except Exception as e:
            print(f"✗ Error with get_template: {e}")
            traceback.print_exc()
        
        # Test 4: Check if template files exist
        print("\n--- Test 4: Template File Check ---")
        template_dir = Path('/home/ubuntu/django-app/kiosk/templates/kiosk')
        print(f"Template directory: {template_dir}")
        print(f"Directory exists: {template_dir.exists()}")
        
        if template_dir.exists():
            template_files = list(template_dir.glob('*.html'))
            print(f"Template files found: {[f.name for f in template_files]}")
            
            # Check file sizes
            for template_file in template_files:
                size = template_file.stat().st_size
                print(f"  {template_file.name}: {size} bytes")
        
    except Exception as e:
        print(f"✗ General error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_template_rendering()
