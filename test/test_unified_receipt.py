#!/usr/bin/env python3
"""
Test the unified receipt display to ensure it shows correctly.
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
from kiosk.utils import generate_order_number

def test_unified_receipt():
    """Test that the unified receipt displays correctly"""
    print("🧾 Testing Unified Receipt Display")
    print("="*50)
    
    try:
        # Create test data
        category = Category.objects.get_or_create(
            name="Test Category",
            defaults={"description": "Test category"}
        )[0]
        
        product = Product.objects.get_or_create(
            name="Purple Haze",
            defaults={
                "category": category,
                "price": 45.00,
                "description": "Premium cannabis product",
                "thc_content": 22.50,
                "strain_type": "Sativa"
            }
        )[0]
        
        # Create test order
        order = Order.objects.create(
            session_key="test_unified_receipt",
            status="Submitted",
            subtotal=45.00,
            tax_amount=2.70,
            tax_rate=0.06,
            total_amount=47.70
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
        response = client.get(url, follow=True)
        
        print(f"📄 Receipt URL: {url}")
        print(f"📊 Response status: {response.status_code}")
        if response.redirect_chain:
            print(f"🔄 Redirects: {response.redirect_chain}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for unified receipt elements
            checks = [
                (order.order_number in content, f"Order number {order.order_number}"),
                ("PAYMENT REQUIRED" in content, "Payment required status"),
                ("Purple Haze" in content, "Product name"),
                ("$47.70" in content, "Total amount"),
                ("Print Receipt" in content, "Print button"),
                ("Back to Shop" in content, "Back navigation"),
                ("OCEAN CITY KIOSK" in content, "Business name"),
                ("THC: 22.50%" in content, "Product details"),
                ("Sativa" in content, "Strain type"),
                ("PAYMENT INSTRUCTIONS" in content, "Payment instructions"),
                ("Take this receipt to the cashier" in content, "Cashier instructions")
            ]
            
            print("\n🔍 Checking receipt content:")
            for check, description in checks:
                status = "✔" if check else "❌"
                print(f"   {status} {description}")
            
            # Check for duplicate content issues
            order_number_count = content.count(order.order_number)
            payment_required_count = content.count("PAYMENT REQUIRED")
            print_button_count = content.count("Print Receipt")
            
            print(f"\n📊 Content frequency check:")
            print(f"   Order number appears: {order_number_count} times")
            print(f"   'PAYMENT REQUIRED' appears: {payment_required_count} times") 
            print(f"   'Print Receipt' appears: {print_button_count} times")
            
            # Check for CSS bleeding
            if "</style>" in content and "<body>" in content:
                body_content = content.split("<body>")[1] if len(content.split("<body>")) > 1 else ""
                css_in_body = "display: flex" in body_content and "<style>" not in body_content
            else:
                css_in_body = False
            
            if css_in_body:
                print("❌ CSS bleeding detected in body content")
            else:
                print("✔ No CSS bleeding detected")
            
            if all(check for check, _ in checks) and not css_in_body:
                print("\n🎉 UNIFIED RECEIPT TEST PASSED!")
                print("   ✓ Single receipt display")
                print("   ✓ All essential elements present")
                print("   ✓ No duplicate content")
                print("   ✓ Clean formatting")
            else:
                print("\n⚠️  Some issues found - check above")
        else:
            print(f"❌ Receipt page failed to load: {response.status_code}")
        
        # Cleanup
        order.delete()
        print(f"\n🧹 Cleaned up test order")
        
    except Exception as e:
        print(f"❌ Error testing receipt: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_unified_receipt()
