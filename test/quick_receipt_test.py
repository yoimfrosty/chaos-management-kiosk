#!/usr/bin/env python3
"""
Quick test of receipt accessibility now that template is fixed
"""

import requests
import time

def test_receipt_quick():
    """Quick test of receipt page"""
    print("🔍 Quick Receipt Test")
    print("="*30)
    
    try:
        # Test server accessibility
        response = requests.get("http://localhost:8000", timeout=5)
        print(f"✔ Server accessible: {response.status_code}")
        
        # Test some order IDs
        for order_id in [77, 76, 75]:  # IDs we know exist
            try:
                print(f"\n📄 Testing order {order_id}:")
                response = requests.get(f"http://localhost:8000/print-receipt/{order_id}/", timeout=10)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.text
                    print(f"   Content length: {len(content)} characters")
                    
                    # Check for key elements
                    checks = [
                        ("OCEAN CITY KIOSK" in content, "Business name"),
                        ("Order:" in content, "Order label"),
                        ("OCH-" in content, "Order number format"),
                        ("PAYMENT REQUIRED" in content, "Payment required"),
                        ("Total:" in content, "Total amount"),
                    ]
                    
                    all_good = True
                    for check, description in checks:
                        status = "✔" if check else "❌"
                        print(f"   {status} {description}")
                        if not check:
                            all_good = False
                    
                    if all_good:
                        print(f"   🎉 Receipt working correctly!")
                        return True
                    else:
                        print(f"   📄 Content preview: {content[:200]}...")
                        
                elif response.status_code == 302:
                    print(f"   🔄 Redirected (likely age verification)")
                elif response.status_code == 404:
                    print(f"   ❌ Order not found")
                else:
                    print(f"   ❌ Error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"   ⏰ Timeout for order {order_id}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
        print(f"\n❌ No working receipts found yet")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_receipt_quick()
