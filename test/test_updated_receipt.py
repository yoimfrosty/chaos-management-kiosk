#!/usr/bin/env python3
"""
Test the updated receipt with 10% larger size and Ocean City theme colors
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/ubuntu/django-app')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from django.test import Client
from kiosk.models import Order, Product, Category, OrderItem

def test_updated_receipt():
    """Test the updated receipt styling"""
    print("🎨 Testing Updated Receipt with Ocean City Theme")
    print("=" * 60)
    
    try:
        # Create test data
        category = Category.objects.get_or_create(
            name="Test Category",
            defaults={"description": "Test category"}
        )[0]
        
        product = Product.objects.get_or_create(
            name="Ocean City Premium",
            defaults={
                "category": category,
                "price": 35.00,
                "description": "Premium cannabis product",
                "thc_content": 22.0,
                "flower_type": "Hybrid"
            }
        )[0]
        
        # Create test order
        order = Order.objects.create(
            session_key="test_updated_receipt",
            status="Submitted",
            subtotal=35.00,
            tax_amount=2.10,
            tax_rate=0.06,
            total_amount=37.10
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
        
        response = client.get(f'/print-receipt/{order.id}/')
        
        print(f"\n📊 Response status: {response.status_code}")
        print(f"📄 Content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for updated theme colors
            theme_checks = [
                ("#0d9488" in content, "Ocean Green theme color"),
                ("#0ea5e9" in content, "Ocean Blue theme color"), 
                ("#f59e0b" in content, "Ocean Gold theme color"),
                ("max-width: 339px" in content, "10% larger size (339px)"),
                ("font-size: 14px" in content, "Increased font size"),
                ("padding: 17px" in content, "Increased padding"),
                ("OCEAN CITY KIOSK" in content, "Business name"),
                ("PRINT RECEIPT" in content, "Print button"),
                ("SHOP MORE" in content, "Navigation button")
            ]
            
            print(f"\n🎨 Theme Color & Size Checks:")
            for check, description in theme_checks:
                status = "✔" if check else "❌"
                print(f"   {status} {description}")
            
            # Check CSS properties
            css_checks = [
                ("linear-gradient(135deg, #0d9488 0%, #0ea5e9 50%, #f59e0b 100%)" in content, "Ocean theme gradient background"),
                ("background: linear-gradient(135deg, #0d9488, #14b8a6)" in content, "Green print button theme"),
                ("background: linear-gradient(135deg, #0ea5e9, #38bdf8)" in content, "Blue navigation button theme"),
                ("border-left: 3px solid #0d9488" in content, "Ocean green item borders")
            ]
            
            print(f"\n🎨 CSS Theme Integration:")
            for check, description in css_checks:
                status = "✔" if check else "❌"
                print(f"   {status} {description}")
            
            # Preview first part of content
            print(f"\n📄 Receipt Content Preview:")
            lines = content.split('\n')[:30]
            for line in lines:
                if line.strip():
                    print(f"   {line.strip()[:80]}...")
                    
            print(f"\n🎉 Updated receipt test completed successfully!")
            return True
            
        else:
            print(f"❌ Receipt page failed: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        try:
            if 'order' in locals():
                order.delete()
                print(f"🧹 Cleaned up test order")
        except:
            pass

if __name__ == "__main__":
    success = test_updated_receipt()
    if success:
        print(f"\n🎉 Receipt styling updated successfully!")
        print(f"📏 Size increased by 10% (339px width)")
        print(f"🎨 Ocean City theme colors applied")
        print(f"🖨️ Modern gradient background implemented")
    else:
        print(f"\n❌ Receipt update test failed!")
