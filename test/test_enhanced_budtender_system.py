#!/usr/bin/env python3
"""
Enhanced Budtender Call System Test
Tests the complete flow from customer call to admin notifications
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
session = requests.Session()

def get_csrf_token():
    """Get CSRF token from the main page"""
    response = session.get(f"{BASE_URL}/")
    if 'csrftoken' in session.cookies:
        return session.cookies['csrftoken']
    return None

def test_age_verification():
    """Complete age verification to access call features"""
    print("🔍 Testing age verification...")
    
    # Get the age verification page
    response = session.get(f"{BASE_URL}/verify-age/")
    if response.status_code == 200:
        print("✔ Age verification page loaded")
        
        # Extract CSRF token from the age verification page
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            
            # Simulate age verification with correct field name
            verify_response = session.post(f"{BASE_URL}/verify-age/", {
                'csrfmiddlewaretoken': csrf_token,
                'is_21_plus': 'on'  # This is the correct field name from forms.py
            })
            
            if verify_response.status_code in [200, 302]:
                print("✔ Age verification completed")
                return True
            else:
                print(f"❌ Age verification failed: {verify_response.status_code}")
                return False
        else:
            print("❌ Could not find CSRF token in age verification page")
            return False
    else:
        print(f"❌ Failed to load age verification page: {response.status_code}")
        return False

def test_enhanced_budtender_call():
    """Test the enhanced budtender call with different reasons and priorities"""
    print("\n🌿 Testing Enhanced Budtender Call System...")
    
    test_cases = [
        {
            'reason': 'product_help',
            'priority': 'normal',
            'message': 'Customer needs product recommendations'
        },
        {
            'reason': 'dosage_help', 
            'priority': 'normal',
            'message': 'Customer needs dosage guidance'
        },
        {
            'reason': 'technical_issue',
            'priority': 'high',
            'message': 'Kiosk screen is not responding properly'
        },
        {
            'reason': 'payment_issue',
            'priority': 'high', 
            'message': 'Payment processing error'
        },
        {
            'reason': 'emergency',
            'priority': 'urgent',
            'message': 'Customer needs immediate assistance'
        }
    ]
    
    csrf_token = get_csrf_token()
    if not csrf_token:
        print("❌ Could not get CSRF token")
        return False
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📞 Test {i}: {test_case['reason']} ({test_case['priority']} priority)")
        
        try:
            response = session.post(f"{BASE_URL}/call-budtender/", 
                headers={
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token
                },
                data=json.dumps({
                    'reason': test_case['reason'],
                    'priority': test_case['priority'],
                    'kiosk_id': 'Test_Kiosk_Main',
                    'session_id': 'test_session_123',
                    'message': test_case['message']
                })
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"  ✔ Call successful: {data.get('message')}")
                    print(f"  📋 Call ID: {data.get('call_id', 'N/A')}")
                    success_count += 1
                else:
                    print(f"  ❌ Call failed: {data.get('message')}")
            else:
                print(f"  ❌ HTTP Error: {response.status_code}")
                print(f"  Response: {response.text[:200]}")
        
        except Exception as e:
            print(f"  ❌ Exception: {e}")
        
        # Small delay between calls
        time.sleep(1)
    
    print(f"\n📊 Summary: {success_count}/{len(test_cases)} calls successful")
    return success_count == len(test_cases)

def check_database_records():
    """Check if database records were created"""
    print("\n🗄️ Checking Database Records...")
    
    try:
        # Try to access admin to see if calls were recorded
        response = session.get(f"{BASE_URL}/admin/kiosk/budtendercall/")
        
        if response.status_code == 200:
            print("✔ Admin interface accessible")
            if "BudtenderCall" in response.text or "budtender" in response.text.lower():
                print("✔ Budtender call records appear to be in admin")
                return True
            else:
                print("⚠️ Admin accessible but budtender calls not visible (may need login)")
                return False
        else:
            print(f"⚠️ Admin not accessible: {response.status_code} (authentication required)")
            return False
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def test_websocket_endpoint():
    """Test if WebSocket endpoints are reachable"""
    print("\n🔌 Testing WebSocket Endpoints...")
    
    # Test basic HTTP upgrade for WebSocket endpoints
    websocket_paths = [
        '/ws/budtender/',
        '/ws/budtender-calls/', 
        '/ws/budtender-notifications/'
    ]
    
    for path in websocket_paths:
        try:
            # Try to make a request that would trigger WebSocket upgrade
            response = session.get(f"{BASE_URL}{path}")
            if response.status_code == 404:
                print(f"  ❌ {path} - Not Found (404)")
            elif response.status_code == 400:
                print(f"  ✔ {path} - WebSocket endpoint exists (400 expected for HTTP)")
            else:
                print(f"  ? {path} - Unexpected status: {response.status_code}")
        except Exception as e:
            print(f"  ❌ {path} - Error: {e}")

def main():
    """Main test function"""
    print("🧪 Enhanced Budtender Call System Test")
    print("=" * 50)
    
    # Test 1: Age verification
    if not test_age_verification():
        print("\n❌ Age verification failed - stopping tests")
        return
    
    # Test 2: Enhanced budtender calls
    call_success = test_enhanced_budtender_call()
    
    # Test 3: Database records
    db_success = check_database_records()
    
    # Test 4: WebSocket endpoints
    test_websocket_endpoint()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    if call_success:
        print("✔ Enhanced budtender calls: WORKING")
    else:
        print("❌ Enhanced budtender calls: ISSUES FOUND")
    
    if db_success:
        print("✔ Database integration: WORKING") 
    else:
        print("⚠️ Database integration: NEEDS VERIFICATION")
    
    print("\n🎯 Next Steps:")
    print("1. Login to admin at: http://127.0.0.1:8000/admin/")
    print("2. Navigate to: Kiosk > Budtender calls")
    print("3. Test real-time notifications in admin interface")
    print("4. Test quick action buttons (Acknowledge, Start Help, Resolve)")
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
