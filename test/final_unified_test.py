#!/usr/bin/env python3
"""
Final comprehensive test of the unified receipt functionality
"""

import requests
import re
import os
import sys
import django

def test_with_requests():
    """Test receipt functionality using requests library"""
    print("🧾 Testing Receipt Functionality with Requests")
    print("="*60)
    
    session = requests.Session()
    
    try:
        # Step 1: Age verification
        print("1. Age verification...")
        response = session.get("http://localhost:8000/verify-age/", timeout=10)
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        
        if csrf_match:
            csrf_token = csrf_match.group(1)
            verify_response = session.post("http://localhost:8000/verify-age/", {
                'csrfmiddlewaretoken': csrf_token,
                'is_21_plus': 'on'
            }, timeout=10, allow_redirects=False)
            
            if verify_response.status_code == 302:
                print("   ✔ Age verification successful")
            else:
                print("   ❌ Age verification failed")
                return False
        else:
            print("   ❌ Could not get CSRF token")
            return False
        
        # Step 2: Test receipt content
        print("\n2. Testing receipt content...")
        for order_id in [77, 76, 75, 74, 73]:
            response = session.get(f"http://localhost:8000/print-receipt/{order_id}/", timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # Skip if still getting age verification
                if "Age Verification" in content:
                    continue
                
                print(f"   📄 Order {order_id}:")
                print(f"      Content length: {len(content)} characters")
                
                # Check for unified receipt elements
                checks = [
                    ("OCEAN CITY KIOSK" in content, "Business name"),
                    ("Order:" in content, "Order label"),
                    ("OCH-" in content, "Order number format"),
                    ("Total:" in content, "Total amount"),
                    ("PAYMENT REQUIRED" in content or "Status:" in content, "Payment status"),
                ]
                
                all_passed = True
                for check, description in checks:
                    status = "✔" if check else "❌"
                    print(f"         {status} {description}")
                    if not check:
                        all_passed = False
                
                if all_passed:
                    print(f"      🎉 Receipt content verified!")
                    print(f"      📄 Sample content:")
                    print(f"         {content[:200]}...")
                    return True
                else:
                    print(f"      ⚠️ Some content missing")
        
        print("   ❌ No working receipts found")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_django_client():
    """Test receipt functionality using Django test client"""
    print("\n🧾 Testing Receipt Functionality with Django Client")
    print("="*60)
    
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
        django.setup()
        
        from django.test import Client
        from django.urls import reverse
        from kiosk.models import Order
        
        # Get existing orders
        orders = Order.objects.filter(status='Submitted')[:5]
        if not orders:
            print("   ❌ No submitted orders found")
            return False
        
        print(f"   Found {orders.count()} orders to test")
        
        client = Client()
        session = client.session
        session['is_21_plus'] = True
        session.save()
        
        for order in orders:
            print(f"   📄 Testing order {order.order_number} (ID: {order.id}):")
            
            url = reverse('kiosk:print_receipt', args=[order.id])
            response = client.get(url, follow=True)
            
            print(f"      Status: {response.status_code}")
            print(f"      Content length: {len(response.content)} bytes")
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # Check content
                checks = [
                    ("OCEAN CITY KIOSK" in content, "Business name"),
                    (order.order_number in content, f"Order number {order.order_number}"),
                    (f"${order.total_amount}" in content, f"Total amount ${order.total_amount}"),
                    ("Order:" in content, "Order label"),
                ]
                
                all_passed = True
                for check, description in checks:
                    status = "✔" if check else "❌"
                    print(f"         {status} {description}")
                    if not check:
                        all_passed = False
                
                if all_passed:
                    print(f"      🎉 Django client test passed!")
                    return True
                else:
                    print(f"      ⚠️ Some content checks failed")
                    print(f"      📄 Content start: {content[:200]}...")
            else:
                print(f"      ❌ Failed to load receipt")
        
        print("   ❌ No working receipts found with Django client")
        return False
        
    except Exception as e:
        print(f"❌ Django client error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive tests"""
    print("🎯 FINAL COMPREHENSIVE RECEIPT TEST")
    print("="*70)
    
    requests_success = test_with_requests()
    django_success = test_with_django_client()
    
    print("\n" + "="*70)
    print("📊 FINAL RESULTS:")
    print("="*70)
    
    if requests_success:
        print("✔ REQUESTS TEST: Receipt functionality working!")
        print("   - Age verification successful")
        print("   - Receipt pages accessible")
        print("   - Content rendering correctly")
    else:
        print("❌ REQUESTS TEST: Issues found")
    
    if django_success:
        print("✔ DJANGO CLIENT TEST: Receipt functionality working!")
        print("   - Template rendering successful")
        print("   - Order data displaying correctly")
        print("   - All content checks passed")
    else:
        print("❌ DJANGO CLIENT TEST: Issues found")
    
    if requests_success and django_success:
        print("\n🎉 UNIFIED RECEIPT SYSTEM: FULLY OPERATIONAL!")
        print("   The receipt template issue has been resolved.")
        print("   All tests are now passing.")
    else:
        print("\n⚠️ PARTIAL SUCCESS: Some issues remain")
    
    return requests_success and django_success

if __name__ == "__main__":
    sys.path.append('/home/ubuntu/django-app')
    success = main()
    sys.exit(0 if success else 1)
