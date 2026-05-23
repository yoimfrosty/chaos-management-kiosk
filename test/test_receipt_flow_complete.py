#!/usr/bin/env python
import requests
import os
import sys
import django

# Setup Django
sys.path.append('/home/ubuntu/django-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order

def test_full_receipt_flow():
    print("=== Testing Full Receipt Flow with Age Verification ===")
    
    orders = Order.objects.all()
    if not orders.exists():
        print("No orders found")
        return
    
    order = orders.first()
    base_url = "http://localhost:8000"
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Step 1: Get age verification page
    print("--- Step 1: Get Age Verification Page ---")
    age_url = f"{base_url}/"  # This should redirect to age verification
    response = session.get(age_url)
    print(f"Status: {response.status_code}")
    print(f"URL after redirects: {response.url}")
    
    # Step 2: Submit age verification
    print("\n--- Step 2: Submit Age Verification ---")
    
    # Check if we need to get CSRF token
    if 'csrftoken' in session.cookies:
        csrf_token = session.cookies['csrftoken']
    else:
        # Try to get CSRF token from the page
        csrf_start = response.text.find('name="csrfmiddlewaretoken" value="')
        if csrf_start != -1:
            csrf_start += len('name="csrfmiddlewaretoken" value="')
            csrf_end = response.text.find('"', csrf_start)
            csrf_token = response.text[csrf_start:csrf_end]
        else:
            csrf_token = 'dummy'  # fallback
    
    print(f"CSRF Token: {csrf_token[:10]}...")
    
    # Submit age verification
    age_verify_data = {
        'csrfmiddlewaretoken': csrf_token,
        'age_verified': 'yes'
    }
    
    # Find the actual age verification submit URL
    age_verify_url = f"{base_url}/age-verification/"
    response = session.post(age_verify_url, data=age_verify_data)
    print(f"Age verification response: {response.status_code}")
    print(f"URL after age verification: {response.url}")
    
    # Step 3: Now try to access receipt
    print("\n--- Step 3: Access Receipt After Age Verification ---")
    receipt_url = f"{base_url}/print-receipt/{order.id}/"
    response = session.get(receipt_url)
    
    print(f"Receipt access status: {response.status_code}")
    print(f"Content length: {len(response.content)} bytes")
    print(f"Content type: {response.headers.get('content-type')}")
    
    # Check if we got the actual receipt
    content_text = response.content.decode('utf-8', errors='ignore')
    
    if 'Ocean City Kiosk' in content_text and 'Order #' in content_text:
        print("✓ SUCCESS: Got actual receipt content!")
        # Look for styling
        if '<style>' in content_text or 'css' in content_text.lower():
            print("✓ SUCCESS: Receipt includes CSS styling!")
        else:
            print("✗ WARNING: Receipt has no CSS styling")
            
        # Show a preview of the styled content
        if 'receipt-header' in content_text:
            print("✓ SUCCESS: Styled receipt classes found")
        
    elif 'Age Verification' in content_text:
        print("✗ ISSUE: Still getting age verification page")
        print("This means age verification is not working properly")
        
    else:
        print("✗ ISSUE: Got unexpected content")
        print(f"Content preview: {content_text[:300]}")

if __name__ == "__main__":
    test_full_receipt_flow()
