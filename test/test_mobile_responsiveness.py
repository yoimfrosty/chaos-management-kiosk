#!/usr/bin/env python3

import time
import requests
import sys

def test_mobile_responsiveness():
    """
    Test mobile and tablet responsiveness of the Ocean City Hemp Kiosk app
    """
    
    print("🔍 MOBILE & TABLET RESPONSIVENESS TEST")
    print("=" * 50)
    
    # Test URLs
    base_url = "http://127.0.0.1:8000"
    test_urls = [
        "/",  # Age verification page
        "/products/",  # Product list page
    ]
    
    # Test different viewport sizes
    viewport_tests = [
        {"name": "iPhone SE", "width": "375", "height": "667"},
        {"name": "iPhone 12/13/14", "width": "390", "height": "844"}, 
        {"name": "iPhone 12/13/14 Pro Max", "width": "428", "height": "926"},
        {"name": "iPad Mini", "width": "768", "height": "1024"},
        {"name": "iPad Air/Pro", "width": "820", "height": "1180"},
        {"name": "Samsung Galaxy S21", "width": "360", "height": "800"},
        {"name": "Samsung Galaxy Tab", "width": "800", "height": "1280"},
    ]
    
    print("Testing server availability...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code not in [200, 302]:
            print(f"❌ Server not responding properly. Status: {response.status_code}")
            return False
        print("✅ Server is responding")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure to run: python manage.py runserver")
        return False
    
    print("\n📱 RESPONSIVE DESIGN ANALYSIS")
    print("-" * 30)
    
    # Age Verification Page Analysis
    print("\n1️⃣ AGE VERIFICATION PAGE RESPONSIVENESS:")
    age_verification_issues = []
    
    # Check for proper viewport meta tag
    try:
        response = requests.get(f"{base_url}/")
        if 'viewport' not in response.text:
            age_verification_issues.append("Missing viewport meta tag")
        elif 'width=device-width' not in response.text:
            age_verification_issues.append("Viewport not set to device-width")
        else:
            print("✅ Proper viewport meta tag found")
    except:
        age_verification_issues.append("Unable to check viewport meta tag")
    
    # Check for responsive breakpoints in CSS
    try:
        response = requests.get(f"{base_url}/")
        content = response.text.lower()
        
        if '@media (max-width: 640px)' in content:
            print("✅ Mobile breakpoint (640px) implemented")
        else:
            age_verification_issues.append("Missing mobile breakpoint (640px)")
            
        if '@media (max-width: 480px)' in content:
            print("✅ Small mobile breakpoint (480px) implemented")
        else:
            age_verification_issues.append("Missing small mobile breakpoint (480px)")
            
        if '@media (min-width: 768px) and (max-width: 1024px)' in content:
            print("✅ Tablet breakpoint (768px-1024px) implemented")
        else:
            age_verification_issues.append("Missing tablet-specific breakpoint")
            
    except:
        age_verification_issues.append("Unable to analyze CSS breakpoints")
    
    # Product List Page Analysis  
    print("\n2️⃣ PRODUCT LIST PAGE RESPONSIVENESS:")
    product_list_issues = []
    
    try:
        response = requests.get(f"{base_url}/products/")
        content = response.text.lower()
        
        # Check grid responsiveness
        if 'grid-template-columns: 1fr 1fr 1fr' in content:
            print("✅ Desktop grid (3 columns) found")
            
        if 'grid-template-columns: 1fr 1fr' in content and '@media (max-width: 768px)' in content:
            print("✅ Tablet/mobile grid (2 columns) found")
        else:
            product_list_issues.append("Missing responsive grid for mobile/tablet")
            
        # Check action bar responsiveness
        if 'fixed-action-bar' in content and '@media (max-width:' in content:
            print("✅ Action bar has responsive styles")
        else:
            product_list_issues.append("Action bar may not be fully responsive")
            
        # Check category navigation responsiveness
        if 'category-nav' in content and 'flex-wrap: wrap' in content:
            print("✅ Category navigation can wrap on smaller screens")
        else:
            product_list_issues.append("Category navigation may not wrap properly")
            
    except:
        product_list_issues.append("Unable to analyze product list responsiveness")
    
    print("\n3️⃣ COMMON MOBILE UX PATTERNS:")
    mobile_ux_analysis = []
    
    # Check for touch-friendly sizes
    print("🤏 Touch Target Analysis:")
    try:
        response = requests.get(f"{base_url}/products/")
        content = response.text
        
        # Look for minimum touch target sizes (44px recommended)
        if 'min-height: 44px' in content or 'min-height: 40px' in content:
            print("✅ Touch targets have minimum height")
        else:
            mobile_ux_analysis.append("Touch targets may be too small (recommend min 44px)")
            
        # Check for hover states that might interfere on mobile
        if ':hover' in content and '@media (hover: hover)' not in content:
            mobile_ux_analysis.append("Hover states present without hover media query protection")
        else:
            print("✅ Hover states properly handled")
    
    except:
        mobile_ux_analysis.append("Unable to analyze touch targets")
    
    print("\n4️⃣ PERFORMANCE FOR MOBILE:")
    performance_issues = []
    
    # Check for heavy animations that might impact mobile performance
    try:
        response = requests.get(f"{base_url}/products/")
        content = response.text.lower()
        
        # Count animations
        animation_count = content.count('@keyframes') + content.count('animation:')
        if animation_count > 10:
            performance_issues.append(f"High number of animations ({animation_count}) may impact mobile performance")
        else:
            print(f"✅ Reasonable animation count: {animation_count}")
            
        # Check for reduced motion preferences
        if 'prefers-reduced-motion' in content:
            print("✅ Respects user's reduced motion preference")
        else:
            performance_issues.append("Missing @media (prefers-reduced-motion: reduce) support")
            
    except:
        performance_issues.append("Unable to analyze performance factors")
    
    # Summary Report
    print("\n" + "=" * 50)
    print("📊 RESPONSIVENESS REPORT SUMMARY")
    print("=" * 50)
    
    total_issues = len(age_verification_issues) + len(product_list_issues) + len(mobile_ux_analysis) + len(performance_issues)
    
    if total_issues == 0:
        print("🎉 EXCELLENT! No major responsiveness issues found.")
        print("✅ Your app appears to be well-optimized for mobile and tablet devices.")
    else:
        print(f"⚠️  Found {total_issues} potential issues that could improve mobile experience:")
        
        if age_verification_issues:
            print("\n🔴 Age Verification Page Issues:")
            for issue in age_verification_issues:
                print(f"   • {issue}")
                
        if product_list_issues:
            print("\n🔴 Product List Page Issues:")
            for issue in product_list_issues:
                print(f"   • {issue}")
                
        if mobile_ux_analysis:
            print("\n🔴 Mobile UX Issues:")
            for issue in mobile_ux_analysis:
                print(f"   • {issue}")
                
        if performance_issues:
            print("\n🔴 Mobile Performance Issues:")
            for issue in performance_issues:
                print(f"   • {issue}")
    
    print("\n📋 RECOMMENDED MANUAL TESTS:")
    print("-" * 30)
    print("1. Open browser developer tools (F12)")
    print("2. Toggle device simulation")
    print("3. Test these viewport sizes:")
    
    for viewport in viewport_tests:
        print(f"   • {viewport['name']}: {viewport['width']}x{viewport['height']}px")
    
    print("\n4. Verify:")
    print("   ✓ Text remains readable at all sizes")
    print("   ✓ Buttons are easy to tap (44px+ touch targets)")
    print("   ✓ Navigation remains accessible")
    print("   ✓ Images scale properly")
    print("   ✓ Horizontal scrolling is avoided")
    print("   ✓ Forms are easy to fill on mobile")
    
    print("\n🌟 ADVANCED MOBILE TESTING:")
    print("• Test on actual devices when possible")
    print("• Check landscape orientation")
    print("• Test with different font sizes (accessibility)")
    print("• Verify performance on slower devices")
    
    return total_issues == 0

if __name__ == "__main__":
    success = test_mobile_responsiveness()
    sys.exit(0 if success else 1)
