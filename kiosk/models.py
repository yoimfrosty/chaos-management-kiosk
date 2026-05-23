from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import uuid
from .utils import generate_order_number


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, help_text="Auto-generated from name")
    emoji = models.CharField(
        max_length=10, 
        blank=True, 
        null=True, 
        help_text="Emoji icon for this category (e.g., 🌿, 🍫, 💨)"
    )
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    FLOWER_TYPES = [
        ('Indica', 'Indica'),
        ('Sativa', 'Sativa'),
        ('Hybrid', 'Hybrid'),
        ('High CBD', 'High CBD'),
    ]

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, help_text="Auto-generated from name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    legal_notice = models.TextField(
        blank=True, 
        null=True, 
        help_text="Legal notice or disclaimer for this product"
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Second product image for carousel")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    thc_content = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,
        help_text="THC percentage (e.g., 21.50)"
    )
    cbd_content = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,
        help_text="CBD percentage (e.g., 0.50)"
    )
    flower_type = models.CharField(
        max_length=20, choices=FLOWER_TYPES, blank=True, null=True
    )
    weight = models.CharField(
        max_length=20, blank=True, null=True,
        help_text="Product weight (e.g., '3.5g', '1oz', '1/8th')"
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    

class ProductCustomField(models.Model):
    """Custom fields for products (e.g., height, dimensions, texture, etc.)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='custom_fields')
    field_name = models.CharField(
        max_length=50,
        help_text="Field name (e.g., 'Height', 'Dimensions', 'Texture')"
    )
    field_value = models.CharField(
        max_length=200,
        help_text="Field value (e.g., '6 inches', '2x4x1 cm', 'Smooth')"
    )
    display_order = models.IntegerField(
        default=0,
        help_text="Order in which to display this field"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'field_name']
        unique_together = ['product', 'field_name']

    def __str__(self):
        return f"{self.product.name} - {self.field_name}: {self.field_value}"


    def get_available_offers(self):
        """Get active special offers that apply to this product"""
        from django.utils import timezone
        
        now = timezone.now()
        
        # Get offers that apply to this specific product
        product_offers = SpecialOffer.objects.filter(
            applicable_products=self,
            is_active=True
        ).filter(
            models.Q(start_date__isnull=True) | models.Q(start_date__lte=now)
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        )
        
        # Get offers that apply to this product's category
        category_offers = SpecialOffer.objects.filter(
            applicable_categories=self.category,
            is_active=True
        ).filter(
            models.Q(start_date__isnull=True) | models.Q(start_date__lte=now)
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        )
        
        # Get universal offers (no specific products or categories)
        universal_offers = SpecialOffer.objects.filter(
            applicable_products__isnull=True,
            applicable_categories__isnull=True,
            is_active=True
        ).filter(
            models.Q(start_date__isnull=True) | models.Q(start_date__lte=now)
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        )
        
        # Combine all offers and remove duplicates
        all_offers = (product_offers | category_offers | universal_offers).distinct()
        
        return all_offers
    
    def get_offer_display_text(self):
        """Get customizable discount offer text for product cards"""
        offers = self.get_available_offers()
        
        if not offers.exists():
            return None
        
        # Get the first offer with display text or quantity requirement
        for offer in offers:
            if offer.offer_display_text:
                return offer.offer_display_text
            elif offer.minimum_quantity:
                # Generate default text for quantity-based offers
                if offer.discount_type == 'Percentage':
                    return f"Buy {offer.minimum_quantity}+ for {offer.discount_value}% off!"
                elif offer.discount_type == 'Fixed Amount':
                    return f"Buy {offer.minimum_quantity}+ save ${offer.discount_value}!"
                else:
                    return f"Buy {offer.minimum_quantity}+ for special discount!"
        
        return None


class SpecialOffer(models.Model):
    """Special offers and discounts for products or categories"""
    DISCOUNT_TYPES = [
        ('Percentage', 'Percentage'),
        ('Fixed Amount', 'Fixed Amount Off Product'),
        ('Fixed Amount Off Total', 'Fixed Amount Off Total Cart')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_type = models.CharField(max_length=30, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Percentage (e.g., 10 for 10%) or fixed amount."
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    applicable_products = models.ManyToManyField(
        Product, 
        blank=True,
        help_text="Leave blank if offer applies to categories or entire order."
    )
    applicable_categories = models.ManyToManyField(
        Category, 
        blank=True,
        help_text="Leave blank if offer applies to specific products or entire order."
    )
    minimum_spend = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Minimum cart subtotal for offer to apply."
    )
    minimum_quantity = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Minimum quantity of this product needed for the discount to apply."
    )
    offer_display_text = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Custom text to display on product cards (e.g., 'Buy 3+ for 15% off!'). Leave blank to use default text."
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def is_currently_active(self):
        """Check if offer is active and within date range"""
        if not self.is_active:
            return False
        
        now = timezone.now()
        
        # Check start date
        if self.start_date and now < self.start_date:
            return False
            
        # Check end date
        if self.end_date and now > self.end_date:
            return False
            
        return True


class Order(models.Model):
    """Order model for cart and order management"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Paid', 'Paid'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
    ]
    
    order_number = models.CharField(
        max_length=20, 
        unique=True, 
        default=generate_order_number, 
        editable=False
    )
    session_key = models.CharField(
        max_length=40, 
        null=True, 
        blank=True, 
        editable=False,
        help_text="Links to Django session if user is not authenticated"
    )
    
    # Customer Information Fields
    customer_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Customer's full name from age verification"
    )
    customer_contact = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Customer's phone number or email (optional)"
    )
    customer_birthdate = models.DateField(
        blank=True,
        null=True,
        help_text="Customer's date of birth for age verification"
    )
    age_verified_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When age was verified for this order"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Pending'
    )
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    tax_rate = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        default=0.06,
        help_text="Default tax rate, e.g., 0.06 for 6%"
    )
    tax_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Total discount amount applied to this order"
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.order_number} - {self.status}"
    
    def recalculate_totals(self, applied_discounts=None):
        """Calculate subtotal, tax, and total from order items without automatic discounts"""
        from decimal import Decimal
        
        # Calculate subtotal from all order items
        item_totals = [item.get_total_item_price() for item in self.items.all()]
        self.subtotal = sum(item_totals, Decimal('0.00'))
        
        # Only apply discounts if explicitly provided (for manual admin use)
        discount_amount = Decimal('0.00')
        if applied_discounts:
            # Keep existing discount logic for admin manual discount application
            cart_items = self.items.all()
            
            for discount in applied_discounts:
                discount_value = Decimal(str(discount['discount_value']))
                
                try:
                    offer = SpecialOffer.objects.get(id=discount['offer_id'])
                    
                    # Calculate eligible items subtotal
                    eligible_subtotal = Decimal('0.00')
                    
                    for item in cart_items:
                        item_eligible = False
                        
                        # Check if discount applies to this specific item
                        if offer.applicable_products.exists():
                            if offer.applicable_products.filter(id=item.product.id).exists():
                                item_eligible = True
                        elif offer.applicable_categories.exists():
                            if offer.applicable_categories.filter(id=item.product.category.id).exists():
                                item_eligible = True
                        else:
                            item_eligible = True
                        
                        if item_eligible:
                            eligible_subtotal += item.get_total_item_price()
                    
                    # Apply discount only to eligible items
                    if eligible_subtotal > 0:
                        if discount['discount_type'] == 'Percentage':
                            discount_amount += eligible_subtotal * (discount_value / 100)
                        elif discount['discount_type'] == 'Fixed Amount':
                            discount_amount += min(discount_value, eligible_subtotal)
                        else:  # Fixed Amount Off Total
                            discount_amount += discount_value
                
                except (SpecialOffer.DoesNotExist, ImportError):
                    if discount['discount_type'] == 'Percentage':
                        discount_amount += self.subtotal * (discount_value / 100)
                    elif discount['discount_type'] == 'Fixed Amount':
                        discount_amount += discount_value
                    else:
                        discount_amount += discount_value
        
        # Ensure discount doesn't exceed subtotal
        if discount_amount > self.subtotal:
            discount_amount = self.subtotal
        
        # Store discount amount (will be 0 for automatic orders)
        self.discount_amount = discount_amount
        
        # Calculate final amounts after discount
        discounted_subtotal = self.subtotal - discount_amount
        
        # Calculate tax on discounted amount
        tax_rate = Decimal(str(self.tax_rate))
        self.tax_amount = discounted_subtotal * tax_rate
        self.total_amount = discounted_subtotal + self.tax_amount
        self.save()
    
    def get_customer_age(self):
        """Calculate customer age from birthdate"""
        if not self.customer_birthdate:
            return None
        
        from datetime import date
        today = date.today()
        age = today.year - self.customer_birthdate.year
        
        # Adjust if birthday hasn't occurred this year
        if today.month < self.customer_birthdate.month or \
           (today.month == self.customer_birthdate.month and today.day < self.customer_birthdate.day):
            age -= 1
        
        return age


class OrderItem(models.Model):
    """Individual items within an order"""
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        help_text="Price of the product when this item was added to the cart"
    )
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.order_number}"
    
    def get_total_item_price(self):
        """Calculate total price for this item"""
        return self.price_at_purchase * self.quantity


class AssistanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
    ]
    
    session_key = models.CharField(max_length=40, help_text="Session ID of the customer")
    order = models.ForeignKey(
        Order, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assistance_requests',
        help_text="Associated order if customer has items in cart"
    )
    customer_name = models.CharField(max_length=100, blank=True, help_text="Customer name if available")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text="Optional message from customer")
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.CharField(max_length=100, blank=True, help_text="Staff member who resolved")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Assistance Request"
        verbose_name_plural = "Assistance Requests"
    
    def __str__(self):
        customer_info = self.customer_name or f"Session {self.session_key[:8]}"
        return f"Assistance Request from {customer_info} - {self.status}"
    
    def mark_acknowledged(self):
        """Mark the request as acknowledged by staff"""
        if self.status == 'pending':
            self.status = 'acknowledged'
            self.acknowledged_at = timezone.now()
            self.save()
    
    def mark_resolved(self, resolved_by=None):
        """Mark the request as resolved"""
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        if resolved_by:
            self.resolved_by = resolved_by
        self.save()


class OrderNotification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('acknowledged', 'Acknowledged'),
        ('completed', 'Completed'),
    ]
    
    order = models.OneToOneField(
        Order, 
        on_delete=models.CASCADE, 
        related_name='notification'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order Notification"
        verbose_name_plural = "Order Notifications"
    
    def __str__(self):
        return f"Order {self.order.order_number} - {self.status}"
    
    def mark_acknowledged(self):
        """Mark the notification as acknowledged"""
        if self.status == 'pending':
            self.status = 'acknowledged'
            self.acknowledged_at = timezone.now()
            self.save()
    
    def mark_completed(self):
        """Mark the notification as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
