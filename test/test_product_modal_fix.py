#!/usr/bin/env python3
"""
Test script to verify the product modal functionality is working correctly
"""

import os
import sys
import time
import django
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup Django environment
sys.path.append('/Users/uba/Desktop/chaos-magement')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OceanCityKiosk.settings')
django.setup()

def test_product_modal_functionality():
    """Test the product modal functionality"""
    print("🧪 TESTING PRODUCT MODAL FUNCTIONALITY")
    print("=" * 50)
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1280,720')
    
    driver = None
    
    try:
        # Initialize Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome driver initialized")
        
        # Navigate to age verification (root)
        driver.get('http://127.0.0.1:8000/')
        print("📱 Navigated to age verification page")
        
        # Click "Yes, I am 21+" button
        try:
            yes_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "age-verify-yes"))
            )
            yes_button.click()
            print("✅ Clicked age verification button")
            
            # Wait for redirect to product page
            WebDriverWait(driver, 10).until(
                EC.url_contains('/products/')
            )
            print("✅ Redirected to product page")
            
        except TimeoutException:
            print("❌ Age verification elements not found or not clickable")
            return False
        
        # Wait for products to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-card"))
            )
            print("✅ Product cards loaded")
            
        except TimeoutException:
            print("❌ Product cards not found")
            return False
        
        # Find all product info icons
        info_icons = driver.find_elements(By.CLASS_NAME, "product-info-icon")
        print(f"📦 Found {len(info_icons)} product info icons")
        
        if not info_icons:
            print("❌ No product info icons found")
            return False
        
        # Test clicking on the first product info icon
        first_icon = info_icons[0]
        product_id = first_icon.get_attribute('data-product-id')
        print(f"🔍 Testing modal for product ID: {product_id}")
        
        # Scroll to the element to make sure it's visible
        driver.execute_script("arguments[0].scrollIntoView(true);", first_icon)
        time.sleep(1)
        
        # Click the info icon
        try:
            first_icon.click()
            print("✅ Clicked product info icon")
            
            # Wait for modal to appear
            modal = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "productInfoModal"))
            )
            
            # Check if modal has 'show' class
            modal_classes = modal.get_attribute('class')
            if 'show' in modal_classes:
                print("✅ Modal is visible (has 'show' class)")
            else:
                print("❌ Modal is not visible (missing 'show' class)")
                return False
            
            # Check modal content
            modal_content_checks = [
                ('productInfoName', 'Product name'),
                ('productInfoPrice', 'Product price'),
                ('productInfoDescription', 'Product description'),
                ('productInfoCategory', 'Product category'),
            ]
            
            all_content_present = True
            for element_id, description in modal_content_checks:
                try:
                    element = driver.find_element(By.ID, element_id)
                    content = element.text.strip()
                    if content and content != description and content != 'Product Name' and content != '$0.00':
                        print(f"✅ {description}: '{content}'")
                    else:
                        print(f"❌ {description}: Missing or default value")
                        all_content_present = False
                except NoSuchElementException:
                    print(f"❌ {description}: Element not found")
                    all_content_present = False
            
            if all_content_present:
                print("✅ All modal content is present and populated")
            else:
                print("❌ Some modal content is missing or not populated")
                return False
            
            # Test the "Add to Order" button
            try:
                add_to_cart_btn = driver.find_element(By.ID, "addToCartFromModal")
                if add_to_cart_btn.is_enabled():
                    print("✅ 'Add to Order' button is enabled")
                else:
                    print("❌ 'Add to Order' button is disabled")
                    return False
            except NoSuchElementException:
                print("❌ 'Add to Order' button not found")
                return False
            
            # Test closing the modal
            try:
                close_btn = driver.find_element(By.CLASS_NAME, "close-modal")
                close_btn.click()
                print("✅ Clicked close button")
                
                # Wait for modal to disappear
                WebDriverWait(driver, 5).until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#productInfoModal.show"))
                )
                print("✅ Modal closed successfully")
                
            except TimeoutException:
                print("❌ Modal did not close")
                return False
            except NoSuchElementException:
                print("❌ Close button not found")
                return False
            
            print("\n🎉 ALL MODAL TESTS PASSED!")
            return True
            
        except TimeoutException:
            print("❌ Modal did not appear after clicking info icon")
            return False
        except Exception as e:
            print(f"❌ Error clicking info icon: {str(e)}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False
        
    finally:
        if driver:
            driver.quit()
            print("🧹 Browser closed")

if __name__ == "__main__":
    success = test_product_modal_functionality()
    if success:
        print("\n✅ PRODUCT MODAL FUNCTIONALITY TEST COMPLETED SUCCESSFULLY")
    else:
        print("\n❌ PRODUCT MODAL FUNCTIONALITY TEST FAILED")
    
    exit(0 if success else 1)
