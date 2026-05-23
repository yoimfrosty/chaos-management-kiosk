#!/usr/bin/env python3
"""
Django-based test to debug receipt rendering
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

def debug_receipt_rendering():
    """Debug receipt rendering with Django test client"""
    print("🔍 Debug Receipt Rendering with Django Client")
    print("="*50)
    
    try:
        # Check if we have the order from the previous test
        print("1. Looking for recent orders...")
        recent_orders = Order.objects.order_by('-created_at')[:5]
        
        for order in recent_orders:
            print(f"   Order {order.id}: {order.order_number} - Status: {order.status}")
        
        if not recent_orders:
            print("   No orders found. Creating test order...")
            
            # Create test data
            category = Category.objects.get_or_create(
                name="Test Category",
                defaults={"description": "Test category"}
            )[0]
            
            product = Product.objects.get_or_create(
                name="Test Product",
                defaults={
                    "category": category,
                    "price": 25.00,
                    "description": "Test product",
                    "thc_content": 15.0,
                    "strain_type": "Hybrid"
                }
            )[0]
            
            # Create test order
            order = Order.objects.create(
                session_key="debug_test",
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
            
            print(f"   ✔ Created test order: {order.order_number}")
        else:
            order = recent_orders[0]
            print(f"   ✔ Using most recent order: {order.order_number}")
        
        # Test receipt with Django client
        print(f"\n2. Testing receipt with Django client...")
        client = Client()
        
        # Set age verification session
        session = client.session
        session['is_21_plus'] = True
        session.save()
        
        # Test the receipt URL
        url = reverse('kiosk:print_receipt', args=[order.id])
        print(f"   🔗 Testing URL: {url}")
        
        response = client.get(url, follow=True)
        
        print(f"   📊 Response status: {response.status_code}")
        print(f"   📄 Content length: {len(response.content)} bytes")
        
        if response.redirect_chain:
            print(f"   🔄 Redirects: {response.redirect_chain}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            if len(content) == 0:
                print(f"   ❌ EMPTY RESPONSE!")
                print(f"   Template used: {response.templates}")
                
                # Check template context
                if hasattr(response, 'context') and response.context:
                    print(f"   📊 Template context:")
                    context = response.context
                    for key, value in context.items():
                        print(f"      {key}: {type(value)} = {value}")
                else:
                    print(f"   ❌ No context available")
            else:
                print(f"   ✔ Response has content")
                print(f"   📄 First 300 characters:")
                print(f"      {content[:300]}...")
                
                # Check for key elements
                checks = [
                    ("OCEAN CITY KIOSK" in content, "Business name"),
                    ("Order Number:" in content, "Order number label"),
                    (order.order_number in content, f"Order number {order.order_number}"),
                    ("PAYMENT REQUIRED" in content, "Payment required"),
                    ("Print Receipt" in content, "Print button"),
                ]
                
                print(f"\n   🔍 Content checks:")
                for check, description in checks:
                    status = "✔" if check else "❌"
                    print(f"      {status} {description}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
            if response.content:
                print(f"   Error content: {response.content.decode('utf-8')[:200]}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_receipt_rendering()
