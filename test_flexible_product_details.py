#!/usr/bin/env python3
"""
Test script to demonstrate the flexible Product Details system.
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

def test_flexible_product_details():
    """Test the flexible Product Details system"""
    
    print("🧪 Testing Flexible Product Details System")
    print("=" * 60)
    
    # Test 1: Current Product Details
    print("\n1. Current Product Details:")
    try:
        products_with_details = Product.objects.filter(custom_fields__isnull=False).distinct()
        
        for product in products_with_details:
            custom_fields = product.custom_fields.all().order_by('display_order')
            print(f"   📦 {product.name} (${product.price}):")
            
            for field in custom_fields:
                print(f"      • {field.field_name}: {field.field_value}")
            print()
            
    except Exception as e:
        print(f"   ❌ Error checking product details: {e}")
    
    # Test 2: Demonstrate flexibility - Add new field types
    print("\n2. Demonstrating Flexibility - Adding New Field Types:")
    try:
        # Get a sample product
        sample_product = Product.objects.filter(name__icontains='Purple').first()
        
        if sample_product:
            # Add some unique fields
            new_fields = [
                ('Lab Tested', 'Yes - COA Available'),
                ('Harvest Date', 'December 2024'),
                ('Terpene Profile', 'Myrcene, Limonene, Pinene'),
                ('Growing Method', 'Indoor Hydroponic'),
                ('Curing Time', '30 days'),
            ]
            
            for order, (field_name, field_value) in enumerate(new_fields, start=10):
                field, created = ProductCustomField.objects.get_or_create(
                    product=sample_product,
                    field_name=field_name,
                    defaults={'field_value': field_value, 'display_order': order}
                )
                if created:
                    print(f"   ✅ Added: {field_name} = {field_value}")
                else:
                    print(f"   ℹ️  Exists: {field_name} = {field.field_value}")
            
            print(f"\n   📊 {sample_product.name} now has {sample_product.custom_fields.count()} custom fields")
            
    except Exception as e:
        print(f"   ❌ Error adding new field types: {e}")
    
    # Test 3: Show how easy it is to modify/delete fields
    print("\n3. Field Management Operations:")
    try:
        # Find a field to modify
        field_to_modify = ProductCustomField.objects.filter(field_name='THC').first()
        
        if field_to_modify:
            old_value = field_to_modify.field_value
            field_to_modify.field_value = '25.3%'
            field_to_modify.save()
            print(f"   ✏️  Modified {field_to_modify.product.name} THC: {old_value} → {field_to_modify.field_value}")
        
        # Show deletion example (without actually deleting)
        deletable_fields = ProductCustomField.objects.filter(field_name='Curing Time')
        print(f"   🗑️  Found {deletable_fields.count()} 'Curing Time' fields that could be deleted")
        
    except Exception as e:
        print(f"   ❌ Error with field management: {e}")
    
    # Test 4: Statistics
    print("\n4. System Statistics:")
    try:
        total_products = Product.objects.count()
        products_with_custom_fields = Product.objects.filter(custom_fields__isnull=False).distinct().count()
        total_custom_fields = ProductCustomField.objects.count()
        unique_field_names = ProductCustomField.objects.values_list('field_name', flat=True).distinct()
        
        print(f"   📊 Total Products: {total_products}")
        print(f"   📊 Products with Custom Fields: {products_with_custom_fields}")
        print(f"   📊 Total Custom Fields: {total_custom_fields}")
        print(f"   📊 Unique Field Types: {len(unique_field_names)}")
        print(f"   📊 Field Types: {', '.join(sorted(unique_field_names))}")
        
    except Exception as e:
        print(f"   ❌ Error getting statistics: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Flexible Product Details Test completed!")
    print("\n🎯 Key Features:")
    print("   • No hardcoded fields - completely flexible")
    print("   • Easy to add, edit, delete any field type")
    print("   • Admin interface for management")
    print("   • Display order control")
    print("   • No percentage/gram limitations")
    print("\n💡 Usage:")
    print("   • Frontend: http://127.0.0.1:8000/products/ (click info icon)")
    print("   • Admin: http://127.0.0.1:8000/admin/kiosk/product/ (edit any product)")
    print("   • Custom Fields: http://127.0.0.1:8000/admin/kiosk/productcustomfield/")

if __name__ == "__main__":
    test_flexible_product_details()
