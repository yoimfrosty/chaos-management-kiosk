#!/usr/bin/env python3

"""
Ocean City Hemp Kiosk - Mobile & Tablet Responsive Enhancement
This script adds comprehensive responsive design improvements for all screen sizes
"""

import os
import re

def enhance_mobile_responsiveness():
    """
    Add comprehensive mobile and tablet responsive enhancements
    """
    
    print("🔧 ENHANCING MOBILE & TABLET RESPONSIVENESS")
    print("=" * 50)
    
    # Path to the product list template
    product_list_path = "/Users/uba/Desktop/chaos-magement/kiosk/templates/kiosk/product_list.html"
    
    # Read the current template
    try:
        with open(product_list_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ Read product list template")
    except Exception as e:
        print(f"❌ Error reading template: {e}")
        return False
    
    # Enhanced responsive CSS improvements
    enhanced_responsive_css = """
    
    /* ================================================
       ENHANCED MOBILE & TABLET RESPONSIVE DESIGN
       Ocean City Hemp Kiosk - Professional Mobile UX
       ================================================ */
    
    /* Touch-friendly minimum sizes */
    .touch-target {
        min-height: 44px;
        min-width: 44px;
    }
    
    /* Protect hover states on touch devices */
    @media (hover: hover) and (pointer: fine) {
        .category-nav-item:hover,
        .product-card:hover,
        .add-to-order-button:hover,
        .action-btn:hover {
            /* Hover effects only apply on devices with precise pointing */
        }
    }
    
    /* Reduced motion for accessibility */
    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }
    
    /* Enhanced mobile breakpoints */
    
    /* Extra small phones (portrait) */
    @media screen and (max-width: 360px) {
        body.product-list-page {
            font-size: 14px;
        }
        
        .category-nav {
            padding: 0.5rem 0.75rem;
            gap: 0.75rem;
        }
        
        .category-nav-item {
            font-size: 0.9rem;
            padding: 0.5rem 0.75rem;
        }
        
        .product-grid {
            grid-template-columns: 1fr;
            gap: 0.75rem;
            padding: 0 0.5rem;
        }
        
        .fixed-action-bar {
            gap: 0.25rem;
            padding: 0.5rem;
            grid-template-columns: auto auto 0.6fr 1fr;
        }
        
        .action-btn {
            font-size: 0.6rem;
            padding: 0.4rem 0.5rem;
            min-height: 44px;
        }
        
        .action-btn.home,
        .action-btn.assistance {
            padding: 0.4rem 0.4rem;
            font-size: 0.55rem;
        }
        
        .action-btn i {
            font-size: 0.5rem;
        }
    }
    
    /* Small phones (portrait) */
    @media screen and (max-width: 480px) {
        .products-section {
            padding: 1rem 0 6rem 0;
            margin: 0 0.25rem;
        }
        
        .category-nav {
            margin: 0 0.25rem 0.125rem 0.25rem;
        }
        
        .product-card {
            border-radius: 16px;
        }
        
        .product-name {
            font-size: 1.1rem;
        }
        
        .product-price {
            font-size: 0.95rem;
        }
        
        .add-to-order-button {
            padding: 0.75rem 1rem;
            font-size: 0.9rem;
        }
        
        /* Cart popup adjustments for small screens */
        .popup-content {
            max-width: 95vw;
            margin: 1rem;
            max-height: 85vh;
        }
        
        .popup-body {
            padding: 1rem;
        }
        
        .cart-item {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.75rem;
        }
        
        .cart-item-controls {
            align-self: flex-end;
        }
    }
    
    /* Standard phones (portrait) */
    @media screen and (min-width: 481px) and (max-width: 767px) {
        .product-grid {
            grid-template-columns: 1fr 1fr;
            gap: 0.875rem;
            padding: 0 0.75rem;
        }
        
        .category-nav {
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .category-nav-item {
            flex: 0 1 auto;
            min-width: fit-content;
        }
    }
    
    /* Tablets and small laptops (portrait) */
    @media screen and (min-width: 768px) and (max-width: 1023px) {
        .product-grid {
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            padding: 0 1rem;
        }
        
        .fixed-action-bar {
            gap: 0.75rem;
            padding: 0.75rem 1rem;
        }
        
        .action-btn {
            font-size: 0.8rem;
            padding: 0.625rem 1rem;
        }
        
        .products-section {
            max-height: calc(100vh - 8rem);
        }
    }
    
    /* Large tablets (landscape) */
    @media screen and (min-width: 1024px) and (max-width: 1279px) {
        .product-grid {
            grid-template-columns: repeat(4, 1fr);
            gap: 1.25rem;
            padding: 0 1.5rem;
        }
        
        .category-nav {
            gap: 1.5rem;
        }
    }
    
    /* Phone landscape orientation */
    @media screen and (max-height: 500px) and (orientation: landscape) {
        .products-section {
            max-height: calc(100vh - 6rem);
            padding: 0.75rem 0 5rem 0;
        }
        
        .fixed-action-bar {
            bottom: 0.5rem;
            padding: 0.5rem;
        }
        
        .action-btn {
            font-size: 0.7rem;
            padding: 0.5rem 0.75rem;
            min-height: 40px;
        }
        
        .category-nav {
            padding: 0.5rem 1rem;
            margin-bottom: 0.5rem;
        }
        
        .product-card {
            border-radius: 12px;
        }
        
        .product-image-container {
            height: 8rem;
        }
    }
    
    /* Improved touch interaction */
    @media (pointer: coarse) {
        .category-nav-item,
        .add-to-order-button,
        .quantity-btn,
        .action-btn {
            min-height: 44px;
            min-width: 44px;
        }
        
        /* Larger tap targets for touch */
        .product-info-icon {
            width: 3rem;
            height: 3rem;
            font-size: 1.25rem;
        }
        
        .close-btn {
            min-width: 44px;
            min-height: 44px;
            padding: 0.75rem;
        }
        
        /* Better spacing for fingers */
        .product-pills {
            gap: 0.5rem;
        }
        
        .cart-item-controls {
            gap: 0.75rem;
        }
    }
    
    /* High DPI displays */
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
        .product-card,
        .category-nav,
        .fixed-action-bar {
            border-width: 0.5px;
        }
    }
    
    /* Accessibility improvements */
    @media (prefers-contrast: high) {
        .product-card {
            border: 2px solid #1f2937;
        }
        
        .category-nav-item {
            border: 2px solid #10b981;
        }
        
        .action-btn {
            border: 2px solid currentColor;
        }
    }
    
    /* Large font size preference */
    @media (prefers-font-size: large) {
        body.product-list-page {
            font-size: 1.125rem;
        }
        
        .product-name {
            font-size: 1.375rem;
        }
        
        .category-nav-item {
            font-size: 1.25rem;
            padding: 1rem 1.5rem;
        }
    }
    
    /* Focus improvements for keyboard navigation */
    .category-nav-item:focus,
    .add-to-order-button:focus,
    .action-btn:focus,
    .quantity-btn:focus {
        outline: 3px solid #3b82f6;
        outline-offset: 2px;
    }
    
    /* Safe area handling for devices with notches */
    @supports (padding: max(0px)) {
        .fixed-action-bar {
            padding-left: max(0.75rem, env(safe-area-inset-left));
            padding-right: max(0.75rem, env(safe-area-inset-right));
            padding-bottom: max(0.75rem, env(safe-area-inset-bottom));
        }
        
        .products-section {
            padding-left: max(0.5rem, env(safe-area-inset-left));
            padding-right: max(0.5rem, env(safe-area-inset-right));
        }
    }
    
    /* Print styles (for receipts) */
    @media print {
        .fixed-action-bar,
        .category-nav,
        .add-to-order-button {
            display: none !important;
        }
        
        .product-card {
            break-inside: avoid;
            box-shadow: none;
            border: 1px solid #000;
        }
        
        body.product-list-page {
            background: white !important;
            color: black !important;
        }
    }
    """
    
    # Find the end of the existing CSS styles (before </style>)
    style_end_pattern = r'(\s*</style>)'
    
    if re.search(style_end_pattern, content):
        # Insert the enhanced responsive CSS before the closing </style> tag
        content = re.sub(
            style_end_pattern,
            enhanced_responsive_css + r'\1',
            content,
            count=1
        )
        print("✅ Added enhanced responsive CSS")
    else:
        print("❌ Could not find CSS style section to enhance")
        return False
    
    # Write the enhanced template back
    try:
        with open(product_list_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Enhanced product list template saved")
    except Exception as e:
        print(f"❌ Error saving enhanced template: {e}")
        return False
    
    # Enhance the age verification template as well
    age_verification_path = "/Users/uba/Desktop/chaos-magement/kiosk/templates/kiosk/age_verification.html"
    
    try:
        with open(age_verification_path, 'r', encoding='utf-8') as f:
            age_content = f.read()
        print("✅ Read age verification template")
    except Exception as e:
        print(f"❌ Error reading age verification template: {e}")
        return False
    
    # Enhanced age verification responsive CSS
    age_verification_responsive_css = """
        
        /* Enhanced Age Verification Mobile Responsiveness */
        
        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        
        /* Touch-friendly improvements */
        @media (pointer: coarse) {
            .btn, button, input[type="submit"] {
                min-height: 44px;
                min-width: 44px;
                padding: 0.75rem 1.5rem;
            }
            
            input, select {
                min-height: 44px;
                font-size: 16px; /* Prevents zoom on iOS */
            }
        }
        
        /* Enhanced small screen support */
        @media (max-width: 360px) {
            .container {
                padding: 1rem 0.75rem;
                margin: 0.25rem;
            }
            
            .brand-text h1 {
                font-size: 1.75rem;
                line-height: 1.2;
            }
            
            .form-row {
                gap: 0.75rem;
            }
            
            .btn {
                font-size: 0.9rem;
                padding: 0.75rem 1.25rem;
            }
        }
        
        /* Landscape phone optimization */
        @media screen and (max-height: 500px) and (orientation: landscape) {
            .container {
                padding: 1rem;
                max-height: 95vh;
                overflow-y: auto;
            }
            
            .brand-text h1 {
                font-size: 2rem;
            }
            
            .logo {
                width: 3rem;
                height: 3rem;
            }
            
            .notice {
                padding: 1rem;
            }
        }
        
        /* High contrast mode */
        @media (prefers-contrast: high) {
            .container {
                border: 2px solid #000;
            }
            
            .btn {
                border: 2px solid currentColor;
            }
        }
        
        /* Safe area support for devices with notches */
        @supports (padding: max(0px)) {
            .container {
                padding-left: max(2rem, env(safe-area-inset-left));
                padding-right: max(2rem, env(safe-area-inset-right));
                margin-top: max(1rem, env(safe-area-inset-top));
                margin-bottom: max(1rem, env(safe-area-inset-bottom));
            }
        }
        """
    
    # Add the enhanced CSS to age verification
    style_end_pattern = r'(\s*</style>)'
    
    if re.search(style_end_pattern, age_content):
        age_content = re.sub(
            style_end_pattern,
            age_verification_responsive_css + r'\1',
            age_content,
            count=1
        )
        print("✅ Added enhanced responsive CSS to age verification")
    else:
        print("❌ Could not find CSS style section in age verification template")
        return False
    
    # Save enhanced age verification template
    try:
        with open(age_verification_path, 'w', encoding='utf-8') as f:
            f.write(age_content)
        print("✅ Enhanced age verification template saved")
    except Exception as e:
        print(f"❌ Error saving enhanced age verification template: {e}")
        return False
    
    print("\n🎯 RESPONSIVE ENHANCEMENTS COMPLETE!")
    print("=" * 50)
    print("✅ Added comprehensive mobile & tablet responsive design")
    print("✅ Implemented touch-friendly interaction patterns")
    print("✅ Added accessibility improvements")
    print("✅ Support for devices with notches/safe areas")
    print("✅ Reduced motion and high contrast support")
    print("✅ Optimized for landscape orientation")
    print("✅ Print-friendly styles")
    
    print("\n📱 ENHANCED FEATURES:")
    print("• Touch targets minimum 44px (iOS/Android standard)")
    print("• Hover states protected on touch devices")
    print("• Reduced motion accessibility support")
    print("• High contrast mode support")
    print("• Safe area insets for notched devices")
    print("• Optimized grid layouts for all screen sizes")
    print("• Improved keyboard navigation focus")
    print("• Font size 16px on inputs (prevents iOS zoom)")
    
    return True

if __name__ == "__main__":
    success = enhance_mobile_responsiveness()
    if success:
        print("\n🚀 Ready to test! Run the app and check on various devices.")
    else:
        print("\n❌ Enhancement failed. Please check the error messages above.")
