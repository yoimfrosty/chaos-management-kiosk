#!/usr/bin/env python3
"""
Debug age verification process
"""

import requests
import re

def debug_age_verification():
    """Debug the age verification process"""
    print("🔍 Debug Age Verification")
    print("="*30)
    
    session = requests.Session()
    
    try:
        # Get age verification page
        print("1. Getting age verification page...")
        response = session.get("http://localhost:8000/verify-age/", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Content length: {len(response.text)} chars")
        
        # Extract CSRF token
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"   ✔ CSRF token found: {csrf_token[:20]}...")
        else:
            print("   ❌ CSRF token not found")
            return False
        
        # Submit age verification
        print("\n2. Submitting age verification...")
        post_data = {
            'csrfmiddlewaretoken': csrf_token,
            'is_21_plus': 'on'
        }
        
        verify_response = session.post("http://localhost:8000/verify-age/", 
                                     data=post_data, 
                                     timeout=10,
                                     allow_redirects=False)  # Don't follow redirects
        
        print(f"   Status: {verify_response.status_code}")
        print(f"   Content length: {len(verify_response.text)} chars")
        
        if verify_response.status_code == 302:
            print(f"   ✔ Redirected to: {verify_response.headers.get('Location', 'Unknown')}")
        else:
            print(f"   ❌ Not redirected")
            # Check for error messages
            if "must confirm" in verify_response.text.lower():
                print("   ❌ Checkbox validation error")
            print(f"   📄 Response start: {verify_response.text[:500]}...")
        
        # Test a receipt page
        print("\n3. Testing receipt access...")
        receipt_response = session.get("http://localhost:8000/print-receipt/77/", timeout=10)
        print(f"   Status: {receipt_response.status_code}")
        print(f"   Content length: {len(receipt_response.text)} chars")
        
        content = receipt_response.text
        if "Age Verification" in content:
            print("   ❌ Still getting age verification page")
        elif "OCEAN CITY KIOSK" in content:
            print("   ✔ Getting receipt page!")
        else:
            print("   📄 Content start: {content[:200]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_age_verification()
