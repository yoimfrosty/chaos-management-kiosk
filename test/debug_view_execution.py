#!/usr/bin/env python3
"""
Debug the print_receipt_view execution to find why it returns empty responses
"""

import os
import sys
import django
from django.test import Client, RequestFactory
from django.urls import reverse
from django.http import HttpRequest

# Add the project to Python path
sys.path.append('/home/ubuntu/django-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')

# Setup Django
django.setup()

from kiosk.models import Order, Product, Category, OrderItem
from kiosk.views import print_receipt_view
from kiosk.decorators import age_verified_required

def debug_view_execution():
    """Debug the print_receipt_view execution step by step"""
    print("🔍 Debug View Execution")
    print("="*50)
    
    try:
        # 1. Get or create a test order
        print("1. Setting up test order...")
        
        # Get existing order or create one
        order = Order.objects.filter(status='Submitted').first()
        
        if not order:
            # Create test data
            category = Category.objects.get_or_create(
                name="Debug Category",
                defaults={"description": "Debug category"}
            )[0]
            
            product = Product.objects.get_or_create(
                name="Debug Product",
                defaults={
                    "category": category,
                    "price": 25.00,
                    "description": "Debug product",
                    "thc_content": 15.0,
                    "strain_type": "Hybrid"
                }
            )[0]
            
            # Create test order
            order = Order.objects.create(
                session_key="debug_view_test",
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
            
            print(f"   ✔ Created test order: {order.order_number} (ID: {order.id})")
        else:
            print(f"   ✔ Using existing order: {order.order_number} (ID: {order.id})")
        
        # 2. Test direct view function call
        print(f"\n2. Testing direct view function call...")
        
        factory = RequestFactory()
        request = factory.get(f'/print-receipt/{order.id}/')
        
        # Set age verification in session
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware(lambda x: x)
        middleware.process_request(request)
        request.session.save()
        request.session['is_21_plus'] = True
        request.session.save()
        
        print(f"   🔗 Request path: {request.path}")
        print(f"   🎟️  Session age verified: {request.session.get('is_21_plus')}")
        
        # Call the view function directly (without decorator)
        print(f"\n3. Testing view function without decorator...")
        try:
            # Import the actual view function
            from kiosk.views import print_receipt_view as raw_view
            
            # Call it directly, bypassing decorator
            response = raw_view(request, order.id)
            
            print(f"   📊 Direct call status: {response.status_code}")
            print(f"   📄 Direct call content length: {len(response.content)} bytes")
            
            if hasattr(response, 'context_data'):
                print(f"   📊 Context data: {response.context_data}")
            
            content = response.content.decode('utf-8')
            if len(content) > 0:
                print(f"   ✔ Direct call returned content!")
                print(f"   📄 First 200 chars: {content[:200]}...")
            else:
                print(f"   ❌ Direct call returned empty content")
                
        except Exception as e:
            print(f"   ❌ Direct call failed: {e}")
            import traceback
            traceback.print_exc()
        
        # 4. Test with Django test client (full pipeline)
        print(f"\n4. Testing with Django test client...")
        
        client = Client()
        session = client.session
        session['is_21_plus'] = True
        session.save()
        
        url = reverse('kiosk:print_receipt', args=[order.id])
        print(f"   🔗 URL: {url}")
        
        response = client.get(url, follow=True)
        
        print(f"   📊 Client response status: {response.status_code}")
        print(f"   📄 Client content length: {len(response.content)} bytes")
        
        if response.redirect_chain:
            print(f"   🔄 Redirects: {response.redirect_chain}")
        
        content = response.content.decode('utf-8')
        if len(content) > 0:
            print(f"   ✔ Client returned content!")
            print(f"   📄 First 200 chars: {content[:200]}...")
            
            # Check template rendering
            if response.templates:
                print(f"   📋 Templates used: {[t.name for t in response.templates]}")
            else:
                print(f"   ❌ No templates used")
                
            if hasattr(response, 'context') and response.context:
                print(f"   📊 Context keys: {list(response.context.keys())}")
                if 'order' in response.context:
                    ctx_order = response.context['order']
                    print(f"   📋 Context order: {ctx_order.order_number} (ID: {ctx_order.id})")
                else:
                    print(f"   ❌ No 'order' in context")
            else:
                print(f"   ❌ No context available")
                
        else:
            print(f"   ❌ Client returned empty content")
        
        # 5. Test template rendering separately
        print(f"\n5. Testing template rendering separately...")
        
        from django.template.loader import render_to_string
        try:
            template_content = render_to_string('kiosk/order_receipt.html', {'order': order})
            print(f"   📄 Template render length: {len(template_content)} chars")
            
            if len(template_content) > 0:
                print(f"   ✔ Template renders correctly!")
                print(f"   📄 First 200 chars: {template_content[:200]}...")
            else:
                print(f"   ❌ Template renders empty")
                
        except Exception as e:
            print(f"   ❌ Template render failed: {e}")
            import traceback
            traceback.print_exc()
        
        # 6. Check if order has required relationships
        print(f"\n6. Checking order relationships...")
        print(f"   📋 Order items count: {order.items.count()}")
        print(f"   📊 Order status: {order.status}")
        print(f"   💰 Order total: ${order.total_amount}")
        
        if order.items.count() > 0:
            item = order.items.first()
            print(f"   📦 First item: {item.product.name} x {item.quantity}")
        else:
            print(f"   ❌ No order items found")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_view_execution()
