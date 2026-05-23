#!/usr/bin/env python3
"""
Test Old Clear Session Button Removal
=====================================

Verify that all old clear session buttons have been completely removed.
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

def test_old_clear_session_removal():
    """Test that old clear session buttons are completely removed"""
    print("=== TESTING OLD CLEAR SESSION BUTTON REMOVAL ===")
    
    client = Client()
    
    print("\n1. Testing age verification and setup...")
    try:
        # Get age verification page
        response = client.get('/')
        print(f"   Age verification page: {response.status_code}")
        
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
                return
                
    except Exception as e:
        print(f"   ❌ Age verification error: {e}")
        return
    
    print("\n2. Testing product list page for old button removal...")
    try:
        response = client.get('/products/')
        print(f"   Product list status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for old clear session button indicators
            has_clear_session_float = 'clear-session-float' in content
            has_old_button_html = 'Clear Session (Admin/Debug only)' in content
            has_old_troubleshooting = 'production troubleshooting' in content
            has_floating_button = 'position: fixed' in content and 'clearSessionBtn' in content
            
            # Count clearSessionBtn elements (should only be 1 - the new one in action bar)
            clear_session_btn_count = content.count('id="clearSessionBtn"')
            
            print(f"   Old float button class: {'❌ FOUND' if has_clear_session_float else '✅ REMOVED'}")
            print(f"   Old button HTML: {'❌ FOUND' if has_old_button_html else '✅ REMOVED'}")
            print(f"   Old troubleshooting text: {'❌ FOUND' if has_old_troubleshooting else '✅ REMOVED'}")
            print(f"   Floating button CSS: {'❌ FOUND' if has_floating_button else '✅ REMOVED'}")
            print(f"   clearSessionBtn count: {clear_session_btn_count} (should be 1)")
            
            if clear_session_btn_count == 1 and not has_clear_session_float and not has_old_button_html:
                print("   ✅ Old clear session button completely removed!")
            else:
                print("   ❌ Some old clear session button remnants still found")
                
        else:
            print(f"   ❌ Product list failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Product list error: {e}")
    
    print("\n3. Testing age verification page for old button removal...")
    try:
        response = client.get('/')
        print(f"   Age verification status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for old clear session button indicators
            has_clear_session_float = 'clear-session-float' in content
            has_old_button_html = 'Clear Session (Admin/Debug only)' in content
            
            print(f"   Old float button class: {'❌ FOUND' if has_clear_session_float else '✅ REMOVED'}")
            print(f"   Old button HTML: {'❌ FOUND' if has_old_button_html else '✅ REMOVED'}")
            
            if not has_clear_session_float and not has_old_button_html:
                print("   ✅ Age verification page clean!")
            else:
                print("   ❌ Old clear session button found in age verification")
                
        else:
            print(f"   ❌ Age verification failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Age verification error: {e}")
    
    print("\n4. Expected state after cleanup:")
    print("   • Only ONE clearSessionBtn element (in action bar)")
    print("   • No 'clear-session-float' CSS class")
    print("   • No 'Clear Session (Admin/Debug only)' text")
    print("   • No floating circular button on left side")
    print("   • No 'production troubleshooting' references")
    print("   • Clean action bar with light-colored Clear button")
    
    print("\n=== OLD CLEAR SESSION BUTTON REMOVAL TEST COMPLETE ===")

if __name__ == '__main__':
    test_old_clear_session_removal()
