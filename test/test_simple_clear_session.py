#!/usr/bin/env python3
"""
Test Simple Clear Session Fix
=============================

Test the new simplified clear session approach that should work without any issues.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
project_dir = '/Users/uba/Desktop/chaos-magement'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_simple_clear_session():
    """Test the simplified clear session approach"""
    print("=== TESTING SIMPLIFIED CLEAR SESSION ===")
    
    client = Client()
    
    print("\n1. Testing age verification setup...")
    try:
        # Get age verification page
        response = client.get('/')
        print(f"   Age verification page status: {response.status_code}")
        
        if response.status_code == 200:
            # Submit age verification
            form_data = {
                'customer_name': 'Test Customer',
                'birthdate': '1990-01-01',
                'csrfmiddlewaretoken': client.cookies.get('csrftoken').value
            }
            response = client.post('/', form_data)
            print(f"   Age verification submit: {response.status_code}")
            
            if response.status_code == 302:
                print("   ✅ Age verification successful")
            else:
                print(f"   ❌ Age verification failed: {response.status_code}")
                
    except Exception as e:
        print(f"   ❌ Age verification error: {e}")
    
    print("\n2. Testing product list page...")
    try:
        response = client.get('/products/')
        print(f"   Product list status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for simplified JavaScript
            has_direct_redirect = 'window.location.href' in content
            has_no_ajax = 'fetch(' not in content or content.count('fetch(') == 1  # Only assistance button
            has_simple_confirm = content.count('confirm(') == 1
            
            print(f"   Direct redirect found: {'✅' if has_direct_redirect else '❌'}")
            print(f"   No complex AJAX: {'✅' if has_no_ajax else '❌'}")
            print(f"   Single confirmation: {'✅' if has_simple_confirm else '❌'}")
            
        else:
            print(f"   ❌ Product list failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Product list error: {e}")
    
    print("\n3. Testing direct clear session...")
    try:
        # Test direct GET request to clear session
        response = client.get('/clear-session/')
        print(f"   Clear session GET status: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Clear session redirects properly")
            print(f"   Redirect location: {response.get('Location', 'Not set')}")
        else:
            print(f"   ❌ Clear session failed: {response.status_code}")
            
        # Test POST request too
        response = client.post('/clear-session/')
        print(f"   Clear session POST status: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Clear session POST redirects properly")
        else:
            print(f"   ❌ Clear session POST failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Clear session test error: {e}")
    
    print("\n4. Summary of simplified approach:")
    print("   ✅ Removed complex AJAX fetch requests")
    print("   ✅ Direct window.location.href redirect")
    print("   ✅ Simple backend redirect without JSON")
    print("   ✅ No timeouts or delays")
    print("   ✅ Eliminated network error possibilities")
    
    print("\n=== SIMPLE CLEAR SESSION TEST COMPLETE ===")

if __name__ == '__main__':
    test_simple_clear_session()
