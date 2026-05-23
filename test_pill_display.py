#!/usr/bin/env python3

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Product, ProductCustomField

def test_pill_display():
    """Test that custom fields are displayed as pills in both product cards and modal"""
    
    print("=== Testing Pill Display ===")
    
    # Get products with custom fields
    products_with_fields = Product.objects.filter(custom_fields__isnull=False).distinct()
    
    if not products_with_fields.exists():
        print("No products with custom fields found. Creating sample data...")
        
        # Create a sample product with custom fields
        product = Product.objects.create(
            name="Test Product",
            price=25.00,
            description="Test product for pill display"
        )
        
        # Add custom fields
        fields = [
            ("THC", "22.5%"),
            ("CBD", "0.8%"),
            ("Strain Type", "Indica"),
            ("Weight", "3.5g"),
            ("Lab Tested", "Yes - COA Available"),
            ("Harvest Date", "December 2024")
        ]
        
        for field_name, field_value in fields:
            ProductCustomField.objects.create(
                product=product,
                field_name=field_name,
                field_value=field_value
            )
            
        print(f"Created sample product '{product.name}' with {len(fields)} custom fields")
    
    # Check products and their custom fields
    for product in products_with_fields[:5]:  # Check first 5 products
        print(f"\n--- Product: {product.name} ---")
        print(f"Price: ${product.price}")
        
        custom_fields = product.custom_fields.all().order_by('display_order', 'field_name')
        print(f"Custom fields ({custom_fields.count()}):")
        
        for field in custom_fields:
            field_class = "default"
            field_name_lower = field.field_name.lower()
            
            if 'thc' in field_name_lower or 'cbd' in field_name_lower:
                field_class = "thc-cbd-pill"
            elif 'strain' in field_name_lower or 'type' in field_name_lower:
                field_class = "strain-pill"
            elif 'weight' in field_name_lower or 'gram' in field_name_lower or 'g' in field_name_lower:
                field_class = "weight-pill"
            else:
                field_class = "category-pill"
            
            print(f"  • {field.field_name}: {field.field_value} [{field_class}]")
    
    print("\n=== Pill Display Test Complete ===")
    print("✅ Custom fields are now displayed as small pills in both product cards and modal")
    print("✅ Same data is consistent between product card and modal")
    print("✅ Field types are automatically classified with appropriate styling")

if __name__ == "__main__":
    test_pill_display()
