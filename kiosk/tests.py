from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
import json
from unittest.mock import patch

from .models import Product, Category, Order, OrderItem, SpecialOffer
from .forms import AgeVerificationForm
from .cart import get_or_create_cart, clear_cart, cart_data_for_json


class ModelTests(TestCase):
    """Test cases for Kiosk models"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name="Test Flower",
            description="Premium cannabis flowers"
        )
        
        self.product = Product.objects.create(
            name="OG Kush",
            description="Classic indica-dominant strain",
            category=self.category,
            price=Decimal('25.99'),
            thc_content=Decimal('22.5'),
            cbd_content=Decimal('1.2'),
            is_available=True
        )
        
    def test_category_str_representation(self):
        """Test Category string representation"""
        self.assertEqual(str(self.category), "Test Flower")
        
    def test_product_str_representation(self):
        """Test Product string representation"""
        self.assertEqual(str(self.product), "OG Kush")
        
    def test_product_price_formatting(self):
        """Test product price is correctly formatted"""
        self.assertEqual(self.product.price, Decimal('25.99'))
        
    def test_product_availability_default(self):
        """Test product is available by default"""
        self.assertTrue(self.product.is_available)
        
    def test_order_total_calculation(self):
        """Test order total calculation with tax"""
        order = Order.objects.create()
        
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price_at_purchase=self.product.price
        )
        
        order.recalculate_totals()
        
        # Calculate expected total (subtotal + 6% tax)
        subtotal = self.product.price * 2  # $51.98
        tax = subtotal * Decimal('0.06')  # Tax rate from model
        expected_total = subtotal + tax
        
        self.assertEqual(order.subtotal, subtotal)
        self.assertAlmostEqual(order.tax_amount, tax, places=2)
        self.assertAlmostEqual(order.total_amount, expected_total, places=2)
        
    def test_special_offer_str_representation(self):
        """Test SpecialOffer string representation"""
        offer = SpecialOffer.objects.create(
            title="20% Off All Flowers",
            description="Limited time offer",
            discount_type="Percentage",
            discount_value=Decimal('20.00'),
            is_active=True
        )
        self.assertEqual(str(offer), "20% Off All Flowers")


class ViewTests(TestCase):
    """Test cases for Kiosk views"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Edibles",
            description="Cannabis-infused edibles"
        )
        
        self.product = Product.objects.create(
            name="Gummy Bears",
            description="10mg THC per piece",
            category=self.category,
            price=Decimal('15.99'),
            thc_content=Decimal('10.0'),
            is_available=True
        )
        
    def test_welcome_view(self):
        """Test welcome page loads correctly"""
        response = self.client.get(reverse('kiosk:welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ocean City Hemp")
        
    def test_age_verification_view_get(self):
        """Test age verification page loads"""
        response = self.client.get(reverse('kiosk:verify_age'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Age Verification Required")
        
    def test_age_verification_view_post_valid(self):
        """Test age verification with valid data"""
        response = self.client.post(reverse('kiosk:verify_age'), {
            'is_21_plus': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get('is_21_plus'))
        
    def test_age_verification_view_post_invalid(self):
        """Test age verification with invalid data"""
        response = self.client.post(reverse('kiosk:verify_age'), {
            'is_21_plus': False
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You must confirm that you are 21 years of age or older to proceed.")
        
    def test_product_list_requires_age_verification(self):
        """Test product list redirects if not age verified"""
        response = self.client.get(reverse('kiosk:product_list'))
        self.assertEqual(response.status_code, 302)
        
    def test_product_list_with_age_verification(self):
        """Test product list loads when age verified"""
        # Set age verification in session
        session = self.client.session
        session['is_21_plus'] = True
        session.save()
        
        response = self.client.get(reverse('kiosk:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Browse Products")
        self.assertContains(response, self.product.name)
        
    def test_product_list_category_filter(self):
        """Test product list category filtering"""
        session = self.client.session
        session['is_21_plus'] = True
        session.save()
        
        response = self.client.get(reverse('kiosk:product_list'), {'category': self.category.slug})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        
    def test_about_us_view(self):
        """Test about us page loads"""
        # Set age verification in session
        session = self.client.session
        session['is_21_plus'] = True
        session.save()
        
        response = self.client.get(reverse('kiosk:about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About Ocean City Hemp")
        
    def test_help_view(self):
        """Test help page loads"""
        # Set age verification in session
        session = self.client.session
        session['is_21_plus'] = True
        session.save()
        
        response = self.client.get(reverse('kiosk:help'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Help & FAQ")
        
    def test_specials_view(self):
        """Test specials page loads"""
        # Set age verification in session
        session = self.client.session
        session['is_21_plus'] = True
        session.save()
        
        # Create a special offer
        SpecialOffer.objects.create(
            title="Test Special",
            description="Test description",
            discount_type="Percentage", 
            discount_value=Decimal('15.00'),
            is_active=True
        )
        
        response = self.client.get(reverse('kiosk:specials'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Special Offers & Deals")
        self.assertContains(response, "Test Special")


class CartTests(TestCase):
    """Test cases for shopping cart functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=Decimal('19.99'),
            is_available=True
        )
        
        # Set up session with age verification
        session = self.client.session
        session['is_21_plus'] = True
        session.save()
        
    def test_add_to_cart(self):
        """Test adding item to cart"""
        response = self.client.post(reverse('kiosk:add_to_cart'), {
            'product_id': self.product.id,
            'quantity': 2
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Item added to cart')
        
    def test_update_cart_item(self):
        """Test updating cart item quantity"""
        # First add item to cart
        response = self.client.post(reverse('kiosk:add_to_cart'), {
            'product_id': self.product.id,
            'quantity': 1
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Get the order item ID from the cart
        cart = get_or_create_cart(self.client)
        order_item = cart.items.get(product=self.product)
        
        # Then update quantity using order_item_id
        response = self.client.post(reverse('kiosk:update_cart'), {
            'order_item_id': order_item.id,
            'quantity': 3
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Cart updated')
        
    def test_remove_from_cart(self):
        """Test removing item from cart"""
        # Add item first
        self.client.post(reverse('kiosk:add_to_cart'), {
            'product_id': self.product.id,
            'quantity': 1
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Get the order item ID
        cart = get_or_create_cart(self.client)
        order_item = cart.items.get(product=self.product)
        
        # Remove item using order_item_id
        response = self.client.post(reverse('kiosk:remove_from_cart'), {
            'order_item_id': order_item.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertIn('Test Product removed from cart', data['message'])
        
    def test_clear_cart(self):
        """Test clearing entire cart"""
        # Add items first
        self.client.post(reverse('kiosk:add_to_cart'), {
            'product_id': self.product.id,
            'quantity': 2
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Clear cart
        response = self.client.post(reverse('kiosk:clear_cart'), 
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Cart cleared')


class OrderTests(TestCase):
    """Test cases for order processing"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=Decimal('29.99'),
            is_available=True
        )
        
        # Set up session
        session = self.client.session
        session['is_21_plus'] = True
        session.save()
        
    def test_submit_order_with_items(self):
        """Test order submission with items in cart"""
        # Add items to cart
        self.client.post(reverse('kiosk:add_to_cart'), {
            'product_id': self.product.id,
            'quantity': 1
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Submit order (just change status from Pending to Submitted)
        response = self.client.post(reverse('kiosk:submit_order'), 
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # Verify order was submitted
        order = Order.objects.get(id=data['order_db_id'])
        self.assertEqual(order.status, 'Submitted')
        self.assertEqual(order.items.count(), 1)
        # Verify the order_id is the formatted order number
        self.assertEqual(data['order_id'], order.order_number)
        
    def test_submit_order_empty_cart(self):
        """Test order submission with empty cart"""
        response = self.client.post(reverse('kiosk:submit_order'), 
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('empty', data['error'].lower())


class FormTests(TestCase):
    """Test cases for forms"""
    
    def test_age_verification_form_valid(self):
        """Test age verification form with valid data"""
        form_data = {'is_21_plus': True}
        form = AgeVerificationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_age_verification_form_invalid(self):
        """Test age verification form with invalid data"""
        form_data = {'is_21_plus': False}
        form = AgeVerificationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('is_21_plus', form.errors)


class SecurityTests(TestCase):
    """Test cases for security features"""
    
    def test_csrf_protection_on_forms(self):
        """Test CSRF protection is enabled"""
        response = self.client.get(reverse('kiosk:verify_age'))
        self.assertContains(response, 'csrfmiddlewaretoken')
        
    def test_age_verification_session_protection(self):
        """Test age verification protects access to products"""
        response = self.client.get(reverse('kiosk:product_list'))
        self.assertEqual(response.status_code, 302)
        
    def test_staff_only_views_protected(self):
        """Test staff-only views are protected"""
        response = self.client.get(reverse('kiosk:budtender_dashboard'))
        self.assertEqual(response.status_code, 302)
        
    def test_ajax_requests_require_proper_headers(self):
        """Test AJAX endpoints require proper headers"""
        response = self.client.post(reverse('kiosk:add_to_cart'), {
            'product_id': 1,
            'quantity': 1
        })
        # Without AJAX header, should redirect or return error
        self.assertNotEqual(response.status_code, 200)


class IntegrationTests(TestCase):
    """Integration test cases for complete workflows"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.category = Category.objects.create(name="Integration Test")
        self.product1 = Product.objects.create(
            name="Product 1",
            category=self.category,
            price=Decimal('10.00'),
            is_available=True
        )
        self.product2 = Product.objects.create(
            name="Product 2", 
            category=self.category,
            price=Decimal('20.00'),
            is_available=True
        )
        
    def test_complete_order_workflow(self):
        """Test complete customer order workflow"""
        # 1. Age verification
        response = self.client.post(reverse('kiosk:verify_age'), {
            'is_21_plus': True
        })
        self.assertEqual(response.status_code, 302)
        
        # 2. Add items to cart
        self.client.post(reverse('kiosk:add_to_cart'), {
            'product_id': self.product1.id,
            'quantity': 2
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.client.post(reverse('kiosk:add_to_cart'), {
            'product_id': self.product2.id,
            'quantity': 1
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # 3. Submit order
        response = self.client.post(reverse('kiosk:submit_order'), 
                                  content_type='application/json',
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # 4. Verify order creation
        order = Order.objects.get(id=data['order_db_id'])
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.status, 'Submitted')
        # Verify the order_id is the formatted order number
        self.assertEqual(data['order_id'], order.order_number)
        
        # 5. Verify cart is cleared (no pending orders for this session)
        pending_orders = Order.objects.filter(session_key=self.client.session.session_key, status='Pending')
        self.assertEqual(pending_orders.count(), 0)
        
    def test_cart_persistence_across_pages(self):
        """Test cart maintains state across page navigation"""
        # Set age verification
        session = self.client.session
        session['is_21_plus'] = True
        session.save()
        
        # Add item to cart
        self.client.post(reverse('kiosk:add_to_cart'), {
            'product_id': self.product1.id,
            'quantity': 1
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Navigate to different pages
        pages = ['kiosk:about_us', 'kiosk:help', 'kiosk:specials', 'kiosk:product_list']
        for page in pages:
            response = self.client.get(reverse(page))
            self.assertEqual(response.status_code, 200)
            
        # Verify cart still has items (check pending order)
        pending_order = Order.objects.filter(session_key=self.client.session.session_key, status='Pending').first()
        self.assertIsNotNone(pending_order)
        self.assertEqual(pending_order.items.count(), 1)


if __name__ == '__main__':
    import django
    django.setup()
    from django.test.utils import get_runner
    from django.conf import settings
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["kiosk.tests"])
    
    if failures:
        exit(1)
