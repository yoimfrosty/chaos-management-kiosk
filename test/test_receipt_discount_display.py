#!/usr/bin/env python3
"""
Test receipt discount display functionality
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from kiosk.models import Product, Category, Order, OrderItem, SpecialOffer
from decimal import Decimal

def test_receipt_with_discounts():
    """Test that receipt displays discount information correctly"""
    print("🧪 Testing receipt discount display...")
    
    client = Client()
    
    # Set age verification session
    session = client.session
    session['is_21_plus'] = True
    session.save()
    
    # Create test data with unique names
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    
    category = Category.objects.create(
        name=f"Test Category {unique_id}",
        emoji="🌿"
    )
    
    product = Product.objects.create(
        name=f"Test Product {unique_id}",
        price=Decimal('50.00'),
        category=category,
        description="Test product for receipt testing"
    )
    
    # Create a discount offer
    discount_offer = SpecialOffer.objects.create(
        title=f"Test Discount {unique_id}",
        description="Test discount for receipt",
        discount_type="Percentage",
        discount_value=Decimal('15.00'),
        is_active=True
    )
    
    try:
        # Add product to cart
        response = client.post(reverse('kiosk:add_to_cart'), {
            'product_id': product.id,
            'quantity': 1
        })
        
        # Apply discount
        response = client.post(reverse('kiosk:apply_discount'), {
            'offer_id': discount_offer.id
        })
        
        if response.status_code == 200:
            print("✅ Product added and discount applied successfully")
        else:
            print(f"❌ Failed to apply discount: {response.status_code}")
            return False
        
        # Submit order
        response = client.post(reverse('kiosk:submit_order'), 
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Order submitted successfully")
                
                # Test the receipt display
                print_receipt_url = data.get('print_receipt_url')
                if print_receipt_url:
                    print(f"✅ Receipt URL generated: {print_receipt_url}")
                    
                    # Get the order ID from the URL
                    order_id = print_receipt_url.split('/')[-2]
                    
                    # Test receipt page
                    response = client.get(reverse('kiosk:print_receipt', args=[order_id]))
                    
                    if response.status_code == 200:
                        content = response.content.decode('utf-8')
                        
                        # Check if discount information is in the receipt
                        if 'Applied Discounts' in content:
                            print("✅ Discount section found in receipt")
                        else:
                            print("❌ Discount section not found in receipt")
                            
                        if f'Test Discount {unique_id}' in content:
                            print("✅ Discount title found in receipt")
                        else:
                            print("❌ Discount title not found in receipt")
                            
                        if '15% off' in content:
                            print("✅ Discount value found in receipt")
                        else:
                            print("❌ Discount value not found in receipt")
                            
                        print("✅ Receipt generated successfully with discount information")
                        return True
                    else:
                        print(f"❌ Failed to load receipt: {response.status_code}")
                        return False
                else:
                    print("❌ No receipt URL in response")
                    return False
            else:
                print(f"❌ Order submission failed: {data}")
                return False
        else:
            print(f"❌ Failed to submit order: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False
    
    finally:
        # Cleanup
        try:
            Product.objects.filter(name__startswith="Test Product").delete()
            Category.objects.filter(name__startswith="Test Category").delete()
            SpecialOffer.objects.filter(title__startswith="Test Discount").delete()
        except:
            pass

if __name__ == "__main__":
    success = test_receipt_with_discounts()
    if success:
        print("\n🎉 Receipt discount display test completed successfully!")
    else:
        print("\n❌ Receipt discount display test failed!")
    
    sys.exit(0 if success else 1)
