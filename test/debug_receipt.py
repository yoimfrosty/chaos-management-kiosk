#!/usr/bin/env python3
"""
Debug the receipt template rendering issue
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse

# Add the project to Python path
sys.path.append('/home/ubuntu/django-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')

# Setup Django
django.setup()

from kiosk.models import Order, Product, Category, OrderItem

def debug_receipt():
    """Debug receipt rendering"""
    print("🔍 Debug Receipt Template Rendering")
    print("="*50)
    
    try:
        # Create test data
        category = Category.objects.get_or_create(
            name="Test Category",
            defaults={"description": "Test category"}
        )[0]
        
        product = Product.objects.get_or_create(
            name="Debug Product",
            defaults={
                "category": category,
                "price": 25.00,
                "description": "Debug product",
                "thc_content": 15.0,
                "flower_type": "Hybrid"
            }
        )[0]
        
        # Create test order
        order = Order.objects.create(
            session_key="debug_receipt_test",
            status="Submitted",
            subtotal=25.00,
            tax_amount=1.50,
            tax_rate=0.06,
            total_amount=26.50
        )
        
        # Add order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price_at_purchase=product.price
        )
        
        print(f"✔ Created test order: {order.order_number}")
        print(f"📦 Product: {product.name} - ${product.price}")
        print(f"💰 Total: ${order.total_amount}")
        
        # Test receipt page
        client = Client()
        
        # Set age verification session
        session = client.session
        session['is_21_plus'] = True
        session.save()
        
        url = reverse('kiosk:print_receipt', args=[order.id])
        print(f"🔗 Testing URL: {url}")
        
        response = client.get(url, follow=True)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📄 Content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Debug content
            print(f"\n🔍 First 500 characters:")
            print(f"'{content[:500]}...'")
            
            print(f"\n🔍 Looking for specific content:")
            checks = [
                ("order_number" in content.lower(), "Variable 'order_number' in content"),
                ("order.order_number" in content, "Template variable 'order.order_number' in content"),
                (order.order_number in content, f"Actual order number '{order.order_number}' in content"),
                ("OCEAN CITY KIOSK" in content, "Business name in content"),
                ("PAYMENT REQUIRED" in content, "Payment required text in content"),
                ("Print Receipt" in content, "Print button text in content"),
            ]
            
            for check, description in checks:
                status = "✔" if check else "❌"
                print(f"   {status} {description}")
            
            # Check if template variables are being rendered
            if "{{" in content and "}}" in content:
                print(f"\n⚠️  Unrendered template variables found!")
                import re
                variables = re.findall(r'\{\{[^}]+\}\}', content)
                for var in variables[:5]:  # Show first 5
                    print(f"   - {var}")
            
            # Check context
            if hasattr(response, 'context') and response.context:
                print(f"\n📊 Template context:")
                context = response.context
                if 'order' in context:
                    order_obj = context['order']
                    print(f"   Order ID: {order_obj.id}")
                    print(f"   Order Number: {order_obj.order_number}")
                    print(f"   Items count: {order_obj.items.count()}")
                else:
                    print(f"   ❌ No 'order' in context")
                    print(f"   Available keys: {list(context.keys()) if context else 'None'}")
            else:
                print(f"\n❌ No context available")
                
        else:
            print(f"❌ Receipt page failed: {response.status_code}")
            if response.content:
                print(f"Error content: {response.content.decode('utf-8')[:200]}")
        
        # Cleanup
        order.delete()
        print(f"\n🧹 Cleaned up test order")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_receipt()
