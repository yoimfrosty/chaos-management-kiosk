#!/usr/bin/env python3
"""
Test script to verify the complete flow including age verification
"""
import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse

# Add the project root to the path
sys.path.insert(0, '/home/ubuntu/django-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

def test_age_verification_and_flower_types():
    """Test the complete flow including age verification and flower type buttons"""
    print("🔒 Testing Age Verification Flow...")
    
    client = Client()
    
    # Test age verification page
    age_response = client.get('/verify-age/')
    if age_response.status_code == 200:
        print("  ✔ Age verification page loads successfully")
        
        # Submit age verification with correct form field
        verify_response = client.post('/verify-age/', {'is_21_plus': 'on'})
        if verify_response.status_code == 302:
            print("  ✔ Age verification submission redirects properly")
            
            # Follow the redirect and test product list
            product_response = client.get('/products/', follow=True)
            if product_response.status_code == 200:
                print("  ✔ Product list accessible after age verification")
                
                content = product_response.content.decode('utf-8')
                
                # Check for flower type elements
                flower_checks = [
                    ('🟣', 'Indica emoji'),
                    ('🟢', 'Sativa emoji'), 
                    ('🟡', 'Hybrid emoji'),
                    ('🔵', 'High CBD emoji'),
                    ('flower-type-button', 'Flower type button class'),
                    ('flower-type-indica', 'Indica CSS class'),
                    ('flower-type-sativa', 'Sativa CSS class'),
                    ('flower-type-hybrid', 'Hybrid CSS class'),
                ]
                
                print("\n🌸 Checking flower type elements:")
                for check_item, description in flower_checks:
                    if check_item in content:
                        print(f"  ✔ {description}")
                    else:
                        print(f"  ❌ {description} - NOT FOUND")
                
                # Check for category emojis
                category_emojis = ['🌿', '🌸', '🍫', '💎', '💨', '🧴', '🚬']
                found_category_emojis = []
                
                for emoji in category_emojis:
                    if emoji in content:
                        found_category_emojis.append(emoji)
                
                if found_category_emojis:
                    print(f"\n📂 Found category emojis: {' '.join(found_category_emojis)}")
                else:
                    print("\n⚠️  No category emojis found")
                    
            else:
                print(f"  ❌ Product list failed after age verification (status: {product_response.status_code})")
        else:
            print(f"  ❌ Age verification submission failed (status: {verify_response.status_code})")
            print(f"  📄 Response content: {verify_response.content.decode('utf-8')[:200]}...")
    else:
        print(f"  ❌ Age verification page failed (status: {age_response.status_code})")

def main():
    print("🧪 Testing Complete Cannabis Kiosk Flow with Flower Type Styling")
    print("=" * 70)
    
    test_age_verification_and_flower_types()
    
    print("\n✨ Flow testing complete!")

if __name__ == '__main__':
    main()
