#!/usr/bin/env python3
"""
Simple test to check template rendering
"""

import os
import sys

# Set Django settings before importing anything
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')

import django
django.setup()

from django.template.loader import render_to_string
from kiosk.models import Order

def test_template_rendering():
    """Test template rendering directly"""
    print("🔍 Testing Template Rendering")
    print("="*40)
    
    try:
        # Get an existing order
        order = Order.objects.first()
        if not order:
            print("❌ No orders found")
            return
            
        print(f"✔ Using order: {order.order_number} (ID: {order.id})")
        print(f"   Items: {order.items.count()}")
        print(f"   Total: ${order.total_amount}")
        
        # Test template rendering
        print(f"\n🎨 Testing template rendering...")
        content = render_to_string('kiosk/order_receipt.html', {'order': order})
        
        print(f"   Content length: {len(content)} characters")
        
        if len(content) > 0:
            print(f"   ✔ Template renders successfully!")
            print(f"   📄 First 300 chars:")
            print(f"   {content[:300]}...")
        else:
            print(f"   ❌ Template renders empty")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_template_rendering()
