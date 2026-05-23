#!/usr/bin/env python
import requests
import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append('/home/ubuntu/django-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from kiosk.models import Order

def test_receipt_access():
    print("=== Testing Receipt Access ===")
    
    # Check if we have orders
    orders = Order.objects.all()
    print(f"Found {orders.count()} orders in database")
    
    if not orders.exists():
        print("No orders found - cannot test receipt")
        return
    
    order = orders.first()
    print(f"Testing with order ID: {order.id} ({order.order_number})")
    
    # Test local server access
    base_url = "http://localhost:8000"
    
    # Test 1: Direct receipt access (should fail without age verification)
    print(f"\n--- Test 1: Direct Receipt Access ---")
    receipt_url = f"{base_url}/print-receipt/{order.id}/"
    print(f"Testing URL: {receipt_url}")
    
    try:
        response = requests.get(receipt_url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)} bytes")
        print(f"Content Type: {response.headers.get('content-type', 'Not specified')}")
        
        if response.content:
            content_preview = response.content[:200].decode('utf-8', errors='ignore')
            print(f"Content Preview: {content_preview}")
        else:
            print("No content returned")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    # Test 2: Test simple receipt template
    print(f"\n--- Test 2: Simple Receipt Template ---")
    simple_url = f"{base_url}/test-receipt/{order.id}/"
    print(f"Testing URL: {simple_url}")
    
    try:
        response = requests.get(simple_url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)} bytes")
        
        if response.content:
            content_preview = response.content[:200].decode('utf-8', errors='ignore')
            print(f"Content Preview: {content_preview}")
        else:
            print("No content returned")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    # Test 3: Age verification page
    print(f"\n--- Test 3: Age Verification Page ---")
    age_url = f"{base_url}/age-verification/"
    print(f"Testing URL: {age_url}")
    
    try:
        response = requests.get(age_url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)} bytes")
        
        if response.content and len(response.content) > 0:
            print("✓ Age verification page loads")
        else:
            print("✗ Age verification page returns no content")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_receipt_access()
