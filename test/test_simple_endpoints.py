#!/usr/bin/env python3
"""
Simple test script to verify notification endpoints work.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    """Test the notification endpoints directly"""
    print("🧪 Testing Notification Endpoints")
    print("=" * 40)
    
    session = requests.Session()
    
    # Test 1: Check pending assistance requests
    print("1. Testing assistance requests endpoint...")
    try:
        response = session.get(f"{BASE_URL}/kiosk/check-pending-assistance/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
            print("   ✅ Assistance endpoint working")
        else:
            print(f"   ❌ Failed: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Check pending order notifications  
    print("\n2. Testing order notifications endpoint...")
    try:
        response = session.get(f"{BASE_URL}/kiosk/check-pending-orders/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
            print("   ✅ Order notifications endpoint working")
        else:
            print(f"   ❌ Failed: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Check admin panel access
    print("\n3. Testing admin panel...")
    try:
        response = session.get(f"{BASE_URL}/admin/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Admin panel accessible")
        else:
            print(f"   ❌ Admin panel status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_endpoints()
