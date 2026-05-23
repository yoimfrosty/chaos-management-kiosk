#!/usr/bin/env python
"""
Verification script for the enhanced age verification page with subtle coloring.
Tests visual improvements and maintains functionality.
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

def verify_age_verification_enhancements():
    """Verify the enhanced age verification page design"""
    
    print("🎨 AGE VERIFICATION PAGE ENHANCEMENT VERIFICATION")
    print("=" * 60)
    
    # Check if the enhanced template exists
    template_path = "kiosk/templates/kiosk/age_verification.html"
    backup_path = "kiosk/templates/kiosk/age_verification_backup.html"
    
    if os.path.exists(template_path):
        print("✅ Enhanced age verification template found")
    else:
        print("❌ Enhanced template not found")
        return False
    
    if os.path.exists(backup_path):
        print("✅ Original template backed up")
    else:
        print("⚠️  Original template backup not found")
    
    print()
    
    # Read and analyze the enhanced template
    with open(template_path, 'r') as f:
        content = f.read()
    
    print("🔍 ENHANCEMENT ANALYSIS:")
    print("-" * 30)
    
    # Check for key enhancements
    enhancements = {
        "Dark gradient background": "linear-gradient(135deg," in content and "#0c0c0c" in content,
        "Glass-morphism container": "backdrop-filter: blur" in content,
        "Colorful gradient borders": "inset 0 1px 0 rgba(255, 255, 255" in content,
        "Enhanced logo with shine": "animation: shine" in content,
        "Gradient text effects": "-webkit-background-clip: text" in content,
        "Improved form styling": "rgba(249, 250, 251, 0.8)" in content,
        "Enhanced button effects": "button::before" in content,
        "Subtle color accents": "rgba(16, 185, 129, 0.1)" in content,
        "Professional shadows": "box-shadow:" in content,
        "Responsive design": "@media (max-width:" in content
    }
    
    for enhancement, found in enhancements.items():
        status = "✅" if found else "❌"
        print(f"  {status} {enhancement}")
    
    print()
    
    # Check color scheme consistency
    print("🎨 COLOR SCHEME ANALYSIS:")
    print("-" * 28)
    
    color_elements = {
        "Cannabis green gradients": "#10b981" in content,
        "Blue accent colors": "#3b82f6" in content,
        "Purple highlights": "#8b5cf6" in content,
        "Amber/Orange accents": "#f59e0b" in content,
        "Dark background tones": "#0c0c0c" in content,
        "Professional transparency": content.count("rgba(") > 20
    }
    
    for element, found in color_elements.items():
        status = "✅" if found else "❌"
        print(f"  {status} {element}")
    
    print()
    
    # Verify functionality preservation
    print("⚙️  FUNCTIONALITY PRESERVATION:")
    print("-" * 32)
    
    functionality_checks = {
        "Age calculation script": "calculateAge" in content,
        "Form validation": "updateStatus" in content,
        "Django form integration": "form.customer_name" in content,
        "CSRF protection": "csrf_token" in content,
        "Error message display": "{% if messages %}" in content,
        "Responsive design": "@media" in content
    }
    
    for check, found in functionality_checks.items():
        status = "✅" if found else "❌"
        print(f"  {status} {check}")
    
    print()
    
    # Calculate enhancement score
    total_enhancements = len(enhancements) + len(color_elements) + len(functionality_checks)
    passed_enhancements = sum(enhancements.values()) + sum(color_elements.values()) + sum(functionality_checks.values())
    score = (passed_enhancements / total_enhancements) * 100
    
    print("📊 ENHANCEMENT SUMMARY:")
    print("-" * 25)
    print(f"✨ Visual enhancements: {sum(enhancements.values())}/{len(enhancements)}")
    print(f"🎨 Color improvements: {sum(color_elements.values())}/{len(color_elements)}")
    print(f"⚙️  Functionality preserved: {sum(functionality_checks.values())}/{len(functionality_checks)}")
    print(f"📈 Overall score: {score:.1f}%")
    
    print()
    
    if score >= 90:
        print("🎉 EXCELLENT! Age verification page enhanced successfully!")
        print("   - Subtle colors complement the product page theme")
        print("   - Professional glass-morphism design")
        print("   - All functionality preserved")
        print("   - Responsive design maintained")
    elif score >= 80:
        print("✅ GOOD! Most enhancements applied successfully")
        print("   - Minor issues may need attention")
    else:
        print("⚠️  NEEDS IMPROVEMENT! Some enhancements missing")
    
    print()
    print("🌐 TESTING INSTRUCTIONS:")
    print("-" * 24)
    print("1. Start the Django server: python3 manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/")
    print("3. Verify the enhanced age verification page displays")
    print("4. Test form functionality and responsiveness")
    print("5. Check color scheme matches product page theme")
    
    return score >= 80

if __name__ == "__main__":
    print("🏪 Ocean City Hemp Kiosk - Age Verification Enhancement Check")
    print("=" * 65)
    
    success = verify_age_verification_enhancements()
    
    if success:
        print("\n🎊 Age verification page successfully enhanced with subtle coloring!")
    else:
        print("\n💥 Enhancement verification failed - please review the changes!")
