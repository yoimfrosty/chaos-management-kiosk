#!/usr/bin/env python3
"""
Test the simple receipt template to isolate the styling issue
"""

import requests
import re

def test_simple_receipt():
    """Test the simple receipt template"""
    print("🔍 Testing Simple Receipt Template")
    print("="*40)
    
    session = requests.Session()
    
    try:
        # Step 1: Age verification
        print("1. Setting up age verification...")
        response = session.get("http://localhost:8000/verify-age/", timeout=10)
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if not csrf_match:
            print("   ❌ No CSRF token found")
            return False
            
        csrf_token = csrf_match.group(1)
        
        verify_data = {
            'csrfmiddlewaretoken': csrf_token,
            'is_21_plus': 'on'
        }
        
        response = session.post("http://localhost:8000/verify-age/", data=verify_data)
        print(f"   ✔ Age verification complete")
        
        # Step 2: Test simple receipt URLs
        print("2. Testing simple receipt template...")
        
        for order_id in [1, 999]:  # Test both existing and non-existing
            print(f"\n   📄 Testing order {order_id}:")
            response = session.get(f"http://localhost:8000/test-receipt/{order_id}/", timeout=10)
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"      Content length: {len(content)} characters")
                
                # Check for key elements
                checks = [
                    ("<!DOCTYPE html>" in content, "HTML document"),
                    ("<style>" in content, "CSS styling"),
                    ("OCEAN CITY KIOSK" in content, "Business name"),
                    ("PAYMENT REQUIRED" in content, "Payment status"),
                    ("OCH-" in content, "Order number format"),
                    ("Total:" in content, "Total amount"),
                    ("Debug Info:" in content, "Debug information")
                ]
                
                print(f"      🔍 Content checks:")
                all_passed = True
                for check, description in checks:
                    status = "✔" if check else "❌"
                    print(f"         {status} {description}")
                    if not check:
                        all_passed = False
                
                if all_passed:
                    print(f"      🎉 Simple receipt working correctly!")
                    print(f"      📄 Preview: {content[content.find('<body>'):content.find('<body>')+200]}...")
                    return True
                else:
                    print(f"      ⚠️  Some checks failed")
                    print(f"      📄 Content start: {content[:400]}...")
                    
            else:
                print(f"      ❌ Failed with status {response.status_code}")
                
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_receipt()
    if success:
        print(f"\n🎉 Simple receipt template works - issue is with main template!")
    else:
        print(f"\n❌ Issue persists even with simple template")
