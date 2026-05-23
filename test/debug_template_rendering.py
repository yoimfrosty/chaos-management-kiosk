#!/usr/bin/env python3
"""
Debug template rendering directly
"""

import os
import sys
import django

# Setup Django
sys.path.append('/home/ubuntu/django-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order
from django.template.loader import render_to_string
from django.test import Client
from django.urls import reverse

def test_template_rendering():
    """Test template rendering directly"""
    print("🔍 Debug Template Rendering")
    print("="*50)
    
    try:
        # Get order 130
        order = Order.objects.get(id=130)
        print(f"✔ Found order: {order.order_number}")
        print(f"   Total: ${order.total_amount}")
        print(f"   Status: {order.status}")
        print(f"   Items: {order.items.count()}")
        
        # Test template rendering directly
        print(f"\n📄 Testing template rendering...")
        context = {'order': order}
        
        try:
            rendered_html = render_to_string('kiosk/order_receipt.html', context)
            print(f"✔ Template rendered successfully!")
            print(f"   Length: {len(rendered_html)} characters")
            
            if len(rendered_html) > 0:
                print(f"   📄 First 200 chars: {rendered_html[:200]}...")
                
                # Save to file for inspection
                with open('/home/ubuntu/django-app/debug_rendered.html', 'w') as f:
                    f.write(rendered_html)
                print(f"✔ Saved rendered content to debug_rendered.html")
                
                # Check for key content
                checks = [
                    ("OCEAN CITY KIOSK" in rendered_html, "Business name"),
                    ("Order" in rendered_html, "Order text"),
                    (order.order_number in rendered_html, f"Order number {order.order_number}"),
                    ("PAYMENT REQUIRED" in rendered_html, "Payment required"),
                    ("$" in rendered_html, "Currency symbol"),
                ]
                
                print(f"\n🔍 Content checks:")
                for check, description in checks:
                    status = "✔" if check else "❌"
                    print(f"   {status} {description}")
                    
            else:
                print(f"❌ Template rendered but produced empty content!")
                
        except Exception as e:
            print(f"❌ Template rendering failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Test Django client
        print(f"\n🌐 Testing Django client...")
        client = Client()
        
        # Set age verification
        session = client.session
        session['is_21_plus'] = True
        session.save()
        
        url = reverse('kiosk:print_receipt', args=[order.id])
        print(f"   URL: {url}")
        
        response = client.get(url)
        print(f"   Status: {response.status_code}")
        print(f"   Content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if len(content) > 0:
                print(f"   ✔ Client returned content!")
                print(f"   📄 First 200 chars: {content[:200]}...")
            else:
                print(f"   ❌ Client returned empty content!")
                
                # Check context
                if hasattr(response, 'context') and response.context:
                    print(f"   📊 Context keys: {list(response.context.keys())}")
                    if 'order' in response.context:
                        ctx_order = response.context['order']
                        print(f"   📋 Context order: {ctx_order.order_number}")
                    else:
                        print(f"   ❌ No 'order' in context")
                else:
                    print(f"   ❌ No context available")
        else:
            print(f"   ❌ Client request failed: {response.status_code}")
            
    except Order.DoesNotExist:
        print(f"❌ Order 130 not found")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_template_rendering()
