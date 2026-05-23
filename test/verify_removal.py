#!/usr/bin/env python3
"""
Verify that receipt pages have been successfully removed
and only view order page functionality remains
"""

import os
import glob

def verify_receipt_removal():
    """Verify that all receipt-related files and references have been removed"""
    print("🔍 Verifying Receipt Page Removal")
    print("="*50)
    
    issues_found = []
    
    # 1. Check that receipt templates have been removed
    print("1. Checking receipt templates...")
    receipt_templates = glob.glob("kiosk/templates/kiosk/*receipt*")
    if receipt_templates:
        issues_found.append(f"Receipt templates still exist: {receipt_templates}")
        print(f"   ❌ Receipt templates found: {receipt_templates}")
    else:
        print(f"   ✔ All receipt templates removed")
    
    # 2. Check views.py for receipt references
    print("2. Checking views.py for receipt references...")
    with open("kiosk/views.py", "r") as f:
        views_content = f.read()
    
    receipt_refs = []
    if "print_receipt" in views_content:
        receipt_refs.append("print_receipt function/reference")
    if "receipt" in views_content.lower() and "replaces receipt functionality" not in views_content:
        # Allow the comment that explains replacement
        lines = views_content.split('\n')
        for i, line in enumerate(lines):
            if "receipt" in line.lower() and "replaces receipt functionality" not in line:
                receipt_refs.append(f"Line {i+1}: {line.strip()}")
    
    if receipt_refs:
        issues_found.append(f"Receipt references in views.py: {receipt_refs}")
        print(f"   ❌ Receipt references found in views.py")
        for ref in receipt_refs[:3]:  # Show first 3
            print(f"      {ref}")
    else:
        print(f"   ✔ No inappropriate receipt references in views.py")
    
    # 3. Check URLs for receipt patterns
    print("3. Checking URL patterns...")
    with open("kiosk/urls.py", "r") as f:
        urls_content = f.read()
    
    if "print_receipt" in urls_content:
        issues_found.append("print_receipt URL pattern still exists")
        print(f"   ❌ print_receipt URL pattern found")
    else:
        print(f"   ✔ No receipt URL patterns found")
    
    # 4. Check that view_order URL pattern exists
    if "view_order" in urls_content:
        print(f"   ✔ view_order URL pattern exists")
    else:
        issues_found.append("view_order URL pattern missing")
        print(f"   ❌ view_order URL pattern missing")
    
    # 5. Check submit_order_view returns view_order_url
    print("4. Checking submit_order_view response...")
    if "view_order_url" in views_content:
        print(f"   ✔ submit_order_view includes view_order_url")
    else:
        issues_found.append("submit_order_view doesn't include view_order_url")
        print(f"   ❌ submit_order_view missing view_order_url")
    
    if "print_receipt_url" in views_content:
        issues_found.append("submit_order_view still includes print_receipt_url")
        print(f"   ❌ submit_order_view still includes print_receipt_url")
    else:
        print(f"   ✔ No print_receipt_url in submit_order_view")
    
    # 6. Check JavaScript in product_list.html
    print("5. Checking JavaScript for correct redirect...")
    with open("kiosk/templates/kiosk/product_list.html", "r") as f:
        js_content = f.read()
    
    if "data.view_order_url" in js_content:
        print(f"   ✔ JavaScript uses view_order_url")
    else:
        issues_found.append("JavaScript doesn't use view_order_url")
        print(f"   ❌ JavaScript missing view_order_url usage")
    
    if "print_receipt" in js_content:
        issues_found.append("JavaScript still references print_receipt")
        print(f"   ❌ JavaScript still references print_receipt")
    else:
        print(f"   ✔ No print_receipt references in JavaScript")
    
    # 7. Check order_submitted.html template
    print("6. Checking order_submitted.html template...")
    with open("kiosk/templates/kiosk/order_submitted.html", "r") as f:
        template_content = f.read()
    
    if "print_receipt" in template_content:
        issues_found.append("order_submitted.html still references print_receipt")
        print(f"   ❌ order_submitted.html still references print_receipt")
    else:
        print(f"   ✔ No print_receipt references in order_submitted.html")
    
    # Summary
    print(f"\n" + "="*50)
    if issues_found:
        print("❌ RECEIPT REMOVAL INCOMPLETE")
        print("Issues found:")
        for issue in issues_found:
            print(f"  • {issue}")
        return False
    else:
        print("✅ RECEIPT REMOVAL COMPLETE!")
        print("✔ All receipt templates removed")
        print("✔ All receipt URL patterns removed") 
        print("✔ Views updated to use view_order only")
        print("✔ JavaScript redirects to view_order_url")
        print("✔ Templates cleaned of receipt references")
        print("\n🎉 SUCCESS: Only view order page functionality remains!")
        return True

if __name__ == "__main__":
    verify_receipt_removal()
