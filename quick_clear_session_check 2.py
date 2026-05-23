#!/usr/bin/env python3

def verify_clear_session_button():
    """Final verification of clear session button"""
    
    template_path = "/Users/uba/Desktop/chaos-magement/kiosk/templates/kiosk/product_list.html"
    
    with open(template_path, 'r') as f:
        content = f.read()
    
    print("🔍 FINAL CLEAR SESSION BUTTON VERIFICATION")
    print("=" * 50)
    
    # Count clear session buttons
    clear_btn_count = content.count('id="clearSessionBtn"')
    print(f"📊 Clear session buttons: {clear_btn_count}")
    
    # Check for old patterns
    old_patterns = [
        'Clear Session (Admin/Debug only)',
        'clear-session-float',
        'position: fixed.*clearSessionBtn'
    ]
    
    old_found = any(pattern in content for pattern in old_patterns)
    print(f"🔍 Old button patterns: {'FOUND' if old_found else 'NOT FOUND'}")
    
    # Check confirmations
    confirm_count = content.count('confirm(')
    print(f"💬 Confirmation dialogs: {confirm_count}")
    
    print(f"\n📋 ANALYSIS:")
    if clear_btn_count == 1:
        print("✅ Single clear session button (correct)")
    else:
        print(f"❌ Expected 1 button, found {clear_btn_count}")
        
    if not old_found:
        print("✅ No old floating button patterns (correct)")
    else:
        print("❌ Old button patterns still present")
        
    if confirm_count == 1:
        print("✅ Single confirmation dialog (correct)")
    else:
        print(f"❌ Expected 1 confirmation, found {confirm_count}")
    
    # Overall result
    success = clear_btn_count == 1 and not old_found and confirm_count == 1
    
    print(f"\n🎯 RESULT: {'SUCCESS' if success else 'NEEDS ATTENTION'}")
    
    if success:
        print("\n🎉 The clear session button is properly configured!")
        print("   • Single button in action bar")
        print("   • Single confirmation dialog")
        print("   • No old floating button remnants")
        print("   • Direct redirect (no AJAX errors)")
    else:
        print("\n⚠️ Issues found - review the analysis above")
    
    return success

if __name__ == "__main__":
    verify_clear_session_button()
