#!/usr/bin/env python3
"""
Test receipt with proper session handling
"""

import requests
import re

def test_with_session():
    """Test receipt with proper session management"""
    print("🔍 Testing Receipt with Session")
    print("="*35)
    
    # Use session to maintain cookies
    session = requests.Session()
    
    try:
        # Step 1: Get age verification page
        print("1. Getting age verification page...")
        response = session.get("http://localhost:8000/verify-age/")
        print(f"   Status: {response.status_code}")
        
        # Extract CSRF token
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if not csrf_match:
            print("   ❌ No CSRF token found")
            return False
            
        csrf_token = csrf_match.group(1)
        print(f"   ✔ CSRF token: {csrf_token[:10]}...")
        
        # Step 2: Submit age verification
        print("2. Submitting age verification...")
        verify_data = {
            'csrfmiddlewaretoken': csrf_token,
            'is_21_plus': 'on'
        }
        
        response = session.post("http://localhost:8000/verify-age/", data=verify_data, allow_redirects=False)
        print(f"   Status: {response.status_code}")
        print(f"   Redirect: {response.headers.get('Location', 'None')}")
        
        if response.status_code != 302:
            print("   ❌ Age verification failed")
            return False
            
        print("   ✔ Age verification successful")
        
        # Step 3: Check session cookies
        print("3. Checking session...")
        for cookie in session.cookies:
            if 'session' in cookie.name.lower():
                print(f"   🍪 Session cookie: {cookie.name}")
        
        # Step 4: Test receipt URL
        print("4. Testing receipt URL...")
        response = session.get("http://localhost:8000/test-receipt/1/", allow_redirects=False)
        print(f"   Status: {response.status_code}")
        print(f"   Content length: {len(response.content)} bytes")
        
        if response.status_code == 302:
            print(f"   Redirect to: {response.headers.get('Location', 'Unknown')}")
            print("   ❌ Still being redirected - age verification not working")
            return False
        elif response.status_code == 200:
            content = response.text
            if len(content) > 0:
                print("   ✔ Got content!")
                print(f"   📄 First 300 chars: {content[:300]}...")
                
                if "OCEAN CITY KIOSK" in content:
                    print("   ✔ Business name found")
                if "<style>" in content:
                    print("   ✔ CSS found")
                if "PAYMENT REQUIRED" in content:
                    print("   ✔ Payment status found")
                    
                return True
            else:
                print("   ❌ Empty response")
                return False
        else:
            print(f"   ❌ Error status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_with_session()
    if success:
        print(f"\n🎉 Receipt working with proper session!")
    else:
        print(f"\n❌ Session or template issue confirmed")
