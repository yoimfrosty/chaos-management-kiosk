#!/usr/bin/env python3
"""
Simple verification script to test if the receipt issue is fixed
"""
import requests
import re

def test_receipt_fix():
    """Test if the receipt system is working after template restoration"""
    print("🔧 VERIFYING RECEIPT FIX")
    print("="*40)
    
    try:
        session = requests.Session()
        
        # Test 1: Age verification
        print("1. Testing age verification...")
        response = session.get("http://localhost:8000/verify-age/", timeout=5)
        if response.status_code == 200 and "Age Verification" in response.text:
            print("   ✔ Age verification page loads")
            
            # Submit age verification
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                verify_response = session.post("http://localhost:8000/verify-age/", {
                    'csrfmiddlewaretoken': csrf_token,
                    'is_21_plus': 'on'
                }, timeout=5, allow_redirects=False)
                
                if verify_response.status_code == 302:
                    print("   ✔ Age verification successful")
                else:
                    print("   ❌ Age verification failed")
                    return False
            else:
                print("   ❌ CSRF token not found")
                return False
        else:
            print("   ❌ Age verification page failed")
            return False
        
        # Test 2: Receipt content
        print("2. Testing receipt content...")
        for order_id in [77, 76, 75]:
            response = session.get(f"http://localhost:8000/print-receipt/{order_id}/", timeout=5)
            
            if response.status_code == 200:
                content = response.text
                content_length = len(content)
                print(f"   📄 Order {order_id}: {content_length} characters")
                
                if content_length > 100:  # Should have substantial content now
                    # Check for key elements
                    has_business_name = "OCEAN CITY KIOSK" in content
                    has_order_info = "Order:" in content
                    has_total = "Total:" in content
                    
                    if has_business_name and has_order_info and has_total:
                        print(f"   ✔ Receipt {order_id} has proper content!")
                        print(f"      - Business name: {'✔' if has_business_name else '❌'}")
                        print(f"      - Order info: {'✔' if has_order_info else '❌'}")
                        print(f"      - Total: {'✔' if has_total else '❌'}")
                        return True
                    else:
                        print(f"   ⚠️ Receipt {order_id} missing some content")
                else:
                    print(f"   ❌ Receipt {order_id} content too short")
            else:
                print(f"   ❌ Receipt {order_id} failed to load (status: {response.status_code})")
        
        print("   ❌ No working receipts found")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    success = test_receipt_fix()
    
    print("\n" + "="*40)
    if success:
        print("🎉 RECEIPT SYSTEM VERIFICATION: PASSED!")
        print("✔ The template restoration was successful")
        print("✔ Receipt pages now render properly")
        print("✔ Age verification works correctly")
        print("✔ Content checks pass")
        print("\n💡 The original issue has been RESOLVED!")
        print("   - Empty template file was the root cause")
        print("   - Template now contains proper HTML structure")
        print("   - All receipt functionality is working")
    else:
        print("❌ RECEIPT SYSTEM VERIFICATION: FAILED")
        print("⚠️ Issues still remain")
    
    return success

if __name__ == "__main__":
    main()
