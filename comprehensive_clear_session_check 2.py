#!/usr/bin/env python3
"""
Comprehensive check for old clear session button removal
"""

import requests
import time
import os

def test_clear_session_buttons():
    """Test the clear session buttons on all pages"""
    print("🧪 TESTING CLEAR SESSION BUTTONS")
    print("=" * 50)
    
    # Check if server is running
    base_url = "http://127.0.0.1:8000"
    
    pages_to_test = [
        ("Age Verification", "/"),
        ("Product List", "/products/"),
        ("Test Page", "/test-clear-session/")
    ]
    
    for page_name, url in pages_to_test:
        print(f"\n📄 Testing {page_name}: {base_url}{url}")
        try:
            response = requests.get(f"{base_url}{url}", timeout=5)
            if response.status_code == 200:
                content = response.text
                
                # Count clear session buttons
                clear_session_count = content.count('id="clearSessionBtn"')
                floating_button_indicators = content.count('position: fixed') if 'clearSessionBtn' in content else 0
                
                # Check for the specific old button pattern
                old_button_pattern = 'Clear Session (Admin/Debug only)'
                has_old_button = old_button_pattern in content
                
                # Check for double confirmation dialogs
                confirm_count = content.count('confirm(')
                
                print(f"   ✅ Status: {response.status_code}")
                print(f"   🔲 Clear session buttons: {clear_session_count}")
                print(f"   🔄 Fixed position elements: {floating_button_indicators}")
                print(f"   ⚠️  Old button pattern: {'YES' if has_old_button else 'NO'}")
                print(f"   💬 Confirm dialogs: {confirm_count}")
                
                if clear_session_count > 1:
                    print(f"   ❌ PROBLEM: Multiple clear session buttons found!")
                elif clear_session_count == 1:
                    print(f"   ✅ OK: Single clear session button found")
                else:
                    print(f"   ⚪ INFO: No clear session buttons (expected for age verification)")
                    
                if has_old_button:
                    print(f"   ❌ PROBLEM: Old floating button still present!")
                    
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️  Server not running - start with: python manage.py runserver")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def check_template_files():
    """Check template files for old button remnants"""
    print(f"\n📁 CHECKING TEMPLATE FILES")
    print("=" * 50)
    
    template_dir = "/Users/uba/Desktop/chaos-magement/kiosk/templates/kiosk/"
    
    old_patterns = [
        ('Old Button ID', 'id="clearSessionBtn"'),
        ('Floating Class', 'class="clear-session-float"'), 
        ('Fixed Position', 'position: fixed'),
        ('Admin Debug Text', 'Clear Session (Admin/Debug only)'),
        ('Right Position', 'right: 20px'),
        ('Bottom Position', 'bottom: 20px')
    ]
    
    files_to_check = ['product_list.html', 'base.html', 'base_clean.html', 'age_verification.html']
    
    for filename in files_to_check:
        filepath = os.path.join(template_dir, filename)
        if os.path.exists(filepath):
            print(f"\n📄 {filename}:")
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    found_issues = []
                    for pattern_name, pattern in old_patterns:
                        count = content.count(pattern)
                        if count > 0:
                            if pattern == 'id="clearSessionBtn"' and filename == 'product_list.html' and count == 1:
                                # This is expected - the new action bar button
                                found_issues.append(f"   ✅ {pattern_name}: {count} (expected new button)")
                            elif pattern == 'position: fixed' and count <= 4:  
                                # Some fixed positioning is normal (modals, notifications)
                                found_issues.append(f"   ⚪ {pattern_name}: {count} (likely normal modals)")
                            else:
                                found_issues.append(f"   ❌ {pattern_name}: {count} (investigate)")
                    
                    if found_issues:
                        for issue in found_issues:
                            print(issue)
                    else:
                        print("   ✅ Clean - no old button patterns found")
                        
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
        else:
            print(f"   ⚠️  File not found: {filename}")

def main():
    print("🔍 COMPREHENSIVE CLEAR SESSION BUTTON CHECK")
    print("=" * 60)
    
    # Check template files first
    check_template_files()
    
    # Test actual rendered pages
    test_clear_session_buttons()
    
    print(f"\n" + "=" * 60)
    print("📋 SUMMARY:")
    print("1. If multiple clearSessionBtn found = Remove duplicates")
    print("2. If old floating button found = Remove old HTML/CSS")
    print("3. If double confirmations = Check for multiple event listeners")
    print("4. Expected: 1 clear button in product_list.html action bar only")
    
    print(f"\n🚀 TO FIX ISSUES:")
    print("1. Remove test files: rm test_clear_session.html")
    print("2. Remove old floating CSS: search for 'clear-session-float'")
    print("3. Check for duplicate JavaScript event listeners")

if __name__ == "__main__":
    main()
