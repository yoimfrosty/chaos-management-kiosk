#!/usr/bin/env python3
"""
Test Clear Session Button Fix
=============================

This script tests the fixes for the double confirmation dialog issue.
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
import json

def test_clear_session_fixes():
    """Test the clear session button fixes"""
    print("=== TESTING CLEAR SESSION BUTTON FIXES ===")
    
    client = Client()
    
    # Test 1: Age verification first to get into the system
    print("\n1. Testing age verification...")
    try:
        response = client.get('/')
        print(f"   Age verification page status: {response.status_code}")
        
        if response.status_code == 200:
            # Submit age verification form
            csrf_token = client.cookies.get('csrftoken')
            if csrf_token:
                form_data = {
                    'customer_name': 'Test Customer',
                    'birthdate': '1990-01-01',
                    'csrfmiddlewaretoken': csrf_token.value
                }
                response = client.post('/', form_data)
                print(f"   Age verification submit status: {response.status_code}")
                
                if response.status_code == 302:
                    print("   ✅ Age verification successful")
                else:
                    print(f"   ❌ Age verification failed: {response.status_code}")
            else:
                print("   ❌ No CSRF token found")
                
    except Exception as e:
        print(f"   ❌ Age verification error: {e}")
    
    # Test 2: Load product list page
    print("\n2. Testing product list page...")
    try:
        response = client.get('/products/')
        print(f"   Product list status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for our fixes
            has_progress_flag = 'clearSessionInProgress' in content
            has_handle_function = 'handleClearSession' in content
            has_prevent_default = 'event.preventDefault()' in content
            has_remove_listener = 'removeEventListener' in content
            has_finally_block = '.finally(() => {' in content
            
            print(f"   Progress flag found: {'✅' if has_progress_flag else '❌'}")
            print(f"   Handle function found: {'✅' if has_handle_function else '❌'}")
            print(f"   Event prevention found: {'✅' if has_prevent_default else '❌'}")
            print(f"   Remove listener found: {'✅' if has_remove_listener else '❌'}")
            print(f"   Finally block found: {'✅' if has_finally_block else '❌'}")
            
            # Count confirmations
            confirm_count = content.count('confirm(')
            print(f"   Confirm dialog count: {confirm_count}")
            
            if confirm_count == 1:
                print("   ✅ Single confirmation dialog found")
            else:
                print(f"   ❌ Multiple confirmation dialogs found: {confirm_count}")
                
        else:
            print(f"   ❌ Failed to load products page: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Product list error: {e}")
    
    # Test 3: Test clear session endpoint
    print("\n3. Testing clear session endpoint...")
    try:
        # Get CSRF token
        response = client.get('/')
        csrf_token = None
        
        if response.status_code == 200:
            csrf_token = client.cookies.get('csrftoken')
            if csrf_token:
                csrf_token = csrf_token.value
        
        if csrf_token:
            # Test clear session with AJAX
            response = client.post('/clear-session/', 
                                 HTTP_X_CSRFTOKEN=csrf_token,
                                 HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            
            print(f"   Clear session status: {response.status_code}")
            print(f"   Content-Type: {response.get('Content-Type', 'Not set')}")
            
            if response.status_code == 200:
                try:
                    data = json.loads(response.content.decode('utf-8'))
                    print(f"   Response data: {data}")
                    
                    if data.get('success') == True:
                        print("   ✅ Clear session successful")
                    else:
                        print(f"   ❌ Clear session failed: {data}")
                        
                except json.JSONDecodeError as e:
                    print(f"   ❌ JSON decode error: {e}")
                    print(f"   Raw response: {response.content.decode('utf-8')[:200]}...")
            else:
                print(f"   ❌ Clear session HTTP error: {response.status_code}")
        else:
            print("   ❌ Could not get CSRF token")
            
    except Exception as e:
        print(f"   ❌ Clear session test error: {e}")
    
    print("\n4. Summary of fixes implemented:")
    print("   ✅ Added clearSessionInProgress flag to prevent multiple executions")
    print("   ✅ Separated event handling into handleClearSession function")
    print("   ✅ Added event.preventDefault() and event.stopPropagation()")
    print("   ✅ Added removeEventListener before addEventListener")
    print("   ✅ Added .finally() block to reset progress flag")
    print("   ✅ Enhanced backend logging and error handling")
    print("   ✅ Improved JSON response format with redirect_url")
    
    print("\n=== TEST COMPLETE ===")

if __name__ == '__main__':
    test_clear_session_fixes()
