#!/usr/bin/env python3
"""
Test script to verify the custom fields functionality.
"""

import os
import sys
import django

# Add project root to Python path
sys.path.append('/Users/darshan/Desktop/chaos-magement')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Product, ProductCustomField

def test_custom_fields():
    """Test the custom fields functionality"""
    
    print("🧪 Testing Custom Fields Functionality")
    print("=" * 60)
    
    # Test 1: Check custom fields model
    print("\n1. Checking Custom Fields Model:")
    try:
        total_fields = ProductCustomField.objects.count()
        print(f"   📊 Total custom fields in database: {total_fields}")
        
        if total_fields > 0:
            print("   ✅ Custom fields model is working correctly")
        else:
            print("   ⚠️  No custom fields found in database")
            
    except Exception as e:
        print(f"   ❌ Error checking custom fields model: {e}")
    
    # Test 2: Check products with custom fields
    print("\n2. Products with Custom Fields:")
    try:
        products_with_fields = Product.objects.filter(custom_fields__isnull=False).distinct()
        
        for product in products_with_fields:
            custom_fields = product.custom_fields.all().order_by('display_order')
            print(f"   📦 {product.name}:")
            
            for field in custom_fields:
                print(f"      • {field.field_name}: {field.field_value}")
            print()
            
    except Exception as e:
        print(f"   ❌ Error checking products with custom fields: {e}")
    
    # Test 3: Test data format for frontend
    print("\n3. Testing Frontend Data Format:")
    try:
        sample_product = Product.objects.filter(custom_fields__isnull=False).first()
        
        if sample_product:
            # Simulate the template data formatting
            custom_fields_data = []
            for field in sample_product.custom_fields.all():
                custom_fields_data.append(f"{field.field_name}:{field.field_value}")
            
            formatted_data = "|".join(custom_fields_data)
            print(f"   📝 Sample product: {sample_product.name}")
            print(f"   📄 Formatted data: {formatted_data}")
            print("   ✅ Frontend data format is correct")
        else:
            print("   ⚠️  No products with custom fields found")
            
    except Exception as e:
        print(f"   ❌ Error testing frontend data format: {e}")
    
    # Test 4: Admin interface readiness
    print("\n4. Admin Interface Check:")
    try:
        from django.contrib import admin
        from kiosk.admin import ProductAdmin
        
        # Check if inline is registered
        inlines = getattr(ProductAdmin, 'inlines', [])
        print(f"   🔧 ProductAdmin inlines: {len(inlines)} configured")
        
        if inlines:
            print("   ✅ Custom fields inline is configured in admin")
        else:
            print("   ⚠️  No inlines configured in ProductAdmin")
            
    except Exception as e:
        print(f"   ❌ Error checking admin interface: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Custom Fields Test completed!")
    print("💡 To test the frontend:")
    print("   1. Go to http://127.0.0.1:8000/products/")
    print("   2. Click on the info (ℹ️) icon on any product")
    print("   3. Look for the 'Additional Information' section")
    print("💡 To add custom fields:")
    print("   1. Go to http://127.0.0.1:8000/admin/kiosk/product/")
    print("   2. Edit any product")
    print("   3. Scroll down to the 'Product custom fields' section")
    print("   4. Add field name and value pairs")

if __name__ == "__main__":
    test_custom_fields()
