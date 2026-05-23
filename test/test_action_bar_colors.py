#!/usr/bin/env python3
"""
Test Action Bar Color Updates
============================

Test that the Clear button now has a light color and the Order# button has light blue.
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

def test_action_bar_colors():
    """Test the updated action bar colors"""
    print("=== TESTING ACTION BAR COLOR UPDATES ===")
    
    client = Client()
    
    print("\n1. Testing age verification and product page access...")
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
                
    except Exception as e:
        print(f"   ❌ Age verification error: {e}")
        return
    
    print("\n2. Testing product list page styling...")
    try:
        response = client.get('/products/')
        print(f"   Product list status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for new Clear button styling
            has_light_clear = '#e2e8f0' in content and '#cbd5e1' in content
            has_light_blue_order = '#bfdbfe' in content and '#93c5fd' in content
            
            # Check that old orange/red colors are gone from Clear button
            has_old_orange = '#f97316' in content or '#ea580c' in content
            has_old_yellow_order = '#f59e0b' in content and '#d97706' in content
            
            print(f"   Light clear button colors: {'✅' if has_light_clear else '❌'}")
            print(f"   Light blue order button: {'✅' if has_light_blue_order else '❌'}")
            print(f"   Old orange colors removed: {'✅' if not has_old_orange else '❌'}")
            print(f"   Old yellow order colors: {'✅' if not has_old_yellow_order else '❌'}")
            
            # Check for proper color scheme
            if has_light_clear and has_light_blue_order and not has_old_orange:
                print("   ✅ Color scheme updated successfully!")
            else:
                print("   ❌ Some color updates may be missing")
                
        else:
            print(f"   ❌ Product list failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Product list error: {e}")
    
    print("\n3. Expected visual changes:")
    print("   • Clear button: Light gray/blue-gray background")
    print("   • Order# button: Light blue background")
    print("   • Clear button text: Dark color for contrast")
    print("   • Order# button text: Dark blue color")
    print("   • No more orange/red Clear button")
    print("   • No more yellow/orange Order# button")
    
    print("\n=== COLOR UPDATE TEST COMPLETE ===")

if __name__ == '__main__':
    test_action_bar_colors()
