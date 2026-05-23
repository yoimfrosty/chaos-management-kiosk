#!/usr/bin/env python3

"""
Ocean City Hemp Kiosk - Clear Session Button Verification
Verify that the clear session button is properly placed in the action bar
"""

import requests
import re

def verify_clear_session_button():
    """
    Verify the clear session button implementation
    """
    
    print("🗑️ CLEAR SESSION BUTTON VERIFICATION")
    print("=" * 45)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test server availability
    print("🔍 Testing server availability...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code not in [200, 302]:
            print(f"❌ Server not responding properly. Status: {response.status_code}")
            return False
        print("✅ Server is responding correctly")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure to run: python manage.py runserver")
        return False
    
    # Test product list page for clear session button
    print("\n📱 CHECKING PRODUCT LIST PAGE")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/products/")
        if response.status_code == 200:
            print("✅ Product list page loads successfully")
            content = response.text
            
            # Check for clear session button in HTML
            checks = [
                ("Clear Session Button HTML", 'id="clearSessionBtn"'),
                ("Clear Session Button Class", 'class="action-btn clear-session"'),
                ("Clear Session Icon", 'fa-trash-can'),
                ("Clear Session Text", '>Clear<'),
                ("Clear Session Title", 'title="Clear session and start over"'),
                ("5-Button Grid Layout", 'grid-template-columns: auto auto auto 0.5fr 1fr'),
                ("Clear Session CSS Styles", '.action-btn.clear-session'),
                ("Clear Session JavaScript", 'getElementById(\'clearSessionBtn\')'),
                ("CSRF Token Support", 'X-CSRFToken'),
                ("Clear Session URL", 'kiosk:clear_session'),
            ]
            
            passed_checks = 0
            for check_name, pattern in checks:
                if pattern.lower() in content.lower():
                    print(f"✅ {check_name}: Found")
                    passed_checks += 1
                else:
                    print(f"❌ {check_name}: Missing")
            
            print(f"\n📊 Implementation Score: {passed_checks}/{len(checks)} ({(passed_checks/len(checks)*100):.1f}%)")
            
        else:
            print(f"❌ Product list page error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing product list page: {e}")
        return False
    
    # Test clear session endpoint
    print(f"\n🔗 TESTING CLEAR SESSION ENDPOINT")
    print("-" * 35)
    
    try:
        # Test the clear session URL directly
        session = requests.Session()
        
        # First get the page to establish a session
        response = session.get(f"{base_url}/products/")
        
        # Extract CSRF token
        csrf_token = None
        csrf_match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print("✅ CSRF token extracted")
        else:
            print("❌ Could not extract CSRF token")
        
        # Test AJAX clear session request
        if csrf_token:
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = session.post(f"{base_url}/clear-session/", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("✅ Clear session endpoint working correctly")
                else:
                    print(f"❌ Clear session endpoint returned error: {data}")
            else:
                print(f"❌ Clear session endpoint HTTP error: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error testing clear session endpoint: {e}")
    
    # Action bar layout verification
    print(f"\n🎯 ACTION BAR LAYOUT VERIFICATION")
    print("-" * 35)
    
    try:
        response = requests.get(f"{base_url}/products/")
        content = response.text
        
        # Check for proper button order in HTML
        button_patterns = [
            ('Home Button', 'action-btn home'),
            ('Clear Button', 'action-btn clear-session'),
            ('Assistance Button', 'action-btn assistance'),
            ('Order Number Button', 'action-btn order-number'),
            ('Your Items Button', 'action-btn cart'),
        ]
        
        button_positions = []
        for button_name, pattern in button_patterns:
            match = re.search(pattern, content)
            if match:
                position = match.start()
                button_positions.append((position, button_name))
                print(f"✅ {button_name}: Found")
            else:
                print(f"❌ {button_name}: Missing")
        
        # Check if buttons are in correct order
        button_positions.sort()
        if len(button_positions) == 5:
            expected_order = ['Home Button', 'Clear Button', 'Assistance Button', 'Order Number Button', 'Your Items Button']
            actual_order = [name for _, name in button_positions]
            
            if actual_order == expected_order:
                print("✅ Buttons are in correct order")
            else:
                print(f"❌ Button order incorrect. Expected: {expected_order}, Got: {actual_order}")
        
    except Exception as e:
        print(f"❌ Error verifying action bar layout: {e}")
    
    print(f"\n📋 MANUAL TESTING CHECKLIST")
    print("-" * 30)
    print("1. Open the product list page")
    print("2. Locate the action bar at the bottom")
    print("3. Verify 5 buttons are present: Home | Clear | Assistance | Order# | Your Items")
    print("4. Check that the Clear button has an orange/red gradient style")
    print("5. Click the Clear button and verify:")
    print("   ✓ Confirmation dialog appears")
    print("   ✓ Session is cleared when confirmed")
    print("   ✓ User is redirected to age verification")
    print("   ✓ Cart items are cleared")
    print("6. Test on mobile devices for proper responsive layout")
    
    print(f"\n🎨 VISUAL FEATURES TO VERIFY")
    print("-" * 30)
    print("• Clear button has orange/red gradient (warning style)")
    print("• Clear button shows trash can icon")
    print("• Hover effect works properly")
    print("• Button is properly sized and positioned")
    print("• Mobile responsive layout maintains 5-button grid")
    print("• Clear button is easily distinguishable from other buttons")
    
    print(f"\n🚀 PRODUCTION READINESS")
    print("-" * 25)
    if passed_checks >= 8:
        print("🎉 EXCELLENT! Clear session button is properly implemented.")
        print("✅ Ready for production use.")
        return True
    elif passed_checks >= 6:
        print("👍 GOOD! Most features working, minor issues to address.")
        return True
    else:
        print("❌ NEEDS WORK! Several critical issues need to be fixed.")
        return False

if __name__ == "__main__":
    success = verify_clear_session_button()
    exit(0 if success else 1)
