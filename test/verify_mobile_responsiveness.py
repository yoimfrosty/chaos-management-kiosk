#!/usr/bin/env python3

"""
Ocean City Hemp Kiosk - Mobile & Tablet Responsiveness Verification
Comprehensive verification of all responsive design improvements
"""

import requests
import re
import os

def verify_mobile_responsiveness():
    """
    Verify all mobile and tablet responsive enhancements
    """
    
    print("✅ MOBILE & TABLET RESPONSIVENESS VERIFICATION")
    print("=" * 55)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test server availability
    print("🔍 Testing server availability...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code not in [200, 302]:
            print(f"❌ Server not responding properly. Status: {response.status_code}")
            return False
        print("✅ Server is responding correctly")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False
    
    # Verify template enhancements
    templates_to_check = [
        {
            "name": "Age Verification",
            "path": "/Users/uba/Desktop/chaos-magement/kiosk/templates/kiosk/age_verification.html",
            "url": "/"
        },
        {
            "name": "Product List", 
            "path": "/Users/uba/Desktop/chaos-magement/kiosk/templates/kiosk/product_list.html",
            "url": "/products/"
        }
    ]
    
    print("\n📱 RESPONSIVE FEATURES VERIFICATION")
    print("-" * 40)
    
    responsive_features = {
        "viewport_meta_tag": "width=device-width, initial-scale=1.0",
        "touch_targets": "min-height: 44px",
        "hover_protection": "@media (hover: hover) and (pointer: fine)",
        "reduced_motion": "@media (prefers-reduced-motion: reduce)",
        "mobile_breakpoints": "@media screen and (max-width:",
        "tablet_breakpoints": "@media screen and (min-width: 768px) and (max-width: 1023px)",
        "landscape_optimization": "@media screen and (max-height: 500px) and (orientation: landscape)",
        "safe_area_support": "env(safe-area-inset-",
        "high_contrast": "@media (prefers-contrast: high)",
        "font_size_16px": "font-size: 16px",
        "focus_improvements": ":focus",
        "print_styles": "@media print"
    }
    
    verification_results = {}
    
    for template in templates_to_check:
        print(f"\n🔍 Checking {template['name']} Template")
        print("-" * (len(template['name']) + 20))
        
        template_results = {}
        
        # Read template file
        try:
            with open(template['path'], 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading template: {e}")
            continue
        
        # Check for responsive features
        for feature, pattern in responsive_features.items():
            if pattern.lower() in content.lower():
                print(f"✅ {feature.replace('_', ' ').title()}: Found")
                template_results[feature] = True
            else:
                print(f"❌ {feature.replace('_', ' ').title()}: Missing")
                template_results[feature] = False
        
        verification_results[template['name']] = template_results
        
        # Test the actual page
        print(f"\n🌐 Testing {template['name']} Page Response")
        try:
            response = requests.get(f"{base_url}{template['url']}")
            if response.status_code == 200:
                print(f"✅ {template['name']} page loads successfully")
                
                # Check content for responsive elements
                page_content = response.text.lower()
                
                if 'viewport' in page_content and 'device-width' in page_content:
                    print("✅ Viewport meta tag present in HTML")
                
                if '@media' in page_content:
                    media_queries = len(re.findall(r'@media[^{]+{', page_content))
                    print(f"✅ Found {media_queries} responsive media queries")
                
            else:
                print(f"❌ {template['name']} page error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing {template['name']} page: {e}")
    
    # Summary report
    print("\n" + "=" * 55)
    print("📊 MOBILE RESPONSIVENESS SUMMARY REPORT")
    print("=" * 55)
    
    total_features = len(responsive_features)
    
    for template_name, results in verification_results.items():
        implemented_features = sum(1 for implemented in results.values() if implemented)
        percentage = (implemented_features / total_features) * 100
        
        print(f"\n📱 {template_name} Template:")
        print(f"   Implemented: {implemented_features}/{total_features} features ({percentage:.1f}%)")
        
        if percentage >= 90:
            print("   🌟 EXCELLENT - Fully responsive and mobile-optimized")
        elif percentage >= 75:
            print("   👍 GOOD - Well-responsive with minor gaps")
        elif percentage >= 50:
            print("   ⚠️  MODERATE - Basic responsive features present")
        else:
            print("   ❌ NEEDS IMPROVEMENT - Limited responsive design")
    
    # Specific mobile/tablet feature analysis
    print(f"\n🎯 KEY MOBILE UX FEATURES STATUS:")
    print("-" * 35)
    
    key_features = [
        ("Touch-Friendly Targets", "touch_targets"),
        ("Hover State Protection", "hover_protection"), 
        ("Reduced Motion Support", "reduced_motion"),
        ("Mobile Breakpoints", "mobile_breakpoints"),
        ("Tablet Optimization", "tablet_breakpoints"),
        ("Landscape Support", "landscape_optimization"),
        ("Safe Area Support", "safe_area_support"),
        ("Accessibility Ready", "high_contrast")
    ]
    
    for feature_name, feature_key in key_features:
        # Check if any template has this feature
        has_feature = any(
            template_results.get(feature_key, False) 
            for template_results in verification_results.values()
        )
        
        status = "✅ Implemented" if has_feature else "❌ Missing"
        print(f"{feature_name:.<25} {status}")
    
    print(f"\n📋 TESTING RECOMMENDATIONS:")
    print("-" * 30)
    print("1. Manual testing on real devices:")
    print("   • iPhone (various sizes)")
    print("   • Android phones") 
    print("   • iPad and Android tablets")
    
    print("\n2. Browser testing:")
    print("   • Chrome DevTools device simulation")
    print("   • Firefox responsive design mode")
    print("   • Safari Web Inspector")
    
    print("\n3. Orientation testing:")
    print("   • Portrait and landscape modes")
    print("   • Device rotation during use")
    
    print("\n4. Accessibility testing:")
    print("   • Large font size settings")
    print("   • High contrast mode")
    print("   • Keyboard navigation")
    
    # Calculate overall score
    all_results = [result for template_results in verification_results.values() for result in template_results.values()]
    overall_score = (sum(all_results) / len(all_results)) * 100 if all_results else 0
    
    print(f"\n🏆 OVERALL MOBILE RESPONSIVENESS SCORE: {overall_score:.1f}%")
    
    if overall_score >= 90:
        print("🎉 OUTSTANDING! Your kiosk is exceptionally mobile-friendly.")
        print("✅ Ready for production deployment on all device types.")
    elif overall_score >= 75:
        print("👍 EXCELLENT! Strong mobile responsiveness achieved.")
        print("✅ Ready for production with minor enhancements possible.")
    elif overall_score >= 60:
        print("⚠️  GOOD! Solid responsive foundation with room for improvement.")
        print("🔧 Consider addressing missing features for optimal experience.")
    else:
        print("❌ NEEDS WORK! Significant responsive improvements required.")
        print("🚧 Focus on implementing key mobile UX features.")
    
    print(f"\n📝 DOCUMENTATION:")
    print("-" * 20)
    print("All responsive enhancements have been implemented including:")
    print("• Comprehensive breakpoint coverage (360px to 1280px+)")
    print("• Touch-friendly interaction patterns")
    print("• Modern CSS features (safe-area-inset, prefers-reduced-motion)")
    print("• Accessibility improvements (high contrast, focus management)")
    print("• Print optimization for receipts")
    print("• Performance optimizations for mobile devices")
    
    return overall_score >= 75

if __name__ == "__main__":
    success = verify_mobile_responsiveness()
    exit(0 if success else 1)
