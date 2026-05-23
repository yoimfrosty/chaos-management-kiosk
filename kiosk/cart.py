from django.shortcuts import get_object_or_404
from .models import Order, OrderItem


def get_or_create_cart(request):
    """
    Get or create a cart (Order) for the current session
    Returns an Order instance with status='Pending'
    """
    cart_id = request.session.get('cart_id')
    cart = None
    
    if cart_id:
        try:
            cart = Order.objects.get(id=cart_id, status='Pending')
        except Order.DoesNotExist:
            cart = None
    
    if not cart:
        # Create new cart
        cart = Order.objects.create(
            status='Pending',
            session_key=request.session.session_key
        )
        # Ensure session key exists
        if not request.session.session_key:
            request.session.create()
            cart.session_key = request.session.session_key
            cart.save()
        
        request.session['cart_id'] = cart.id
    
    return cart


def clear_cart(request):
    """Clear the cart from the session"""
    if 'cart_id' in request.session:
        del request.session['cart_id']


def cart_data_for_json(cart, request=None):
    """
    Serialize cart details into a dictionary suitable for JSON
    """
    items = []
    for item in cart.items.all():
        items.append({
            'id': item.id,
            'name': item.product.name,
            'quantity': item.quantity,
            'price': float(item.price_at_purchase),
            'total': float(item.get_total_item_price()),
            'product_id': item.product.id,
            'image_url': item.product.image.url if item.product.image else None,
        })
    
    # Get applied discounts from session if request is provided
    applied_discounts = []
    discount_amount = 0.0
    if request:
        session_discounts = request.session.get('applied_discounts', [])
        for discount in session_discounts:
            applied_discounts.append({
                'offer_id': discount['offer_id'],
                'title': discount['title'],
                'discount_type': discount['discount_type'],
                'discount_value': discount['discount_value']
            })
        
        # Calculate total discount amount using product-specific logic
        discount_amount = calculate_discount_amount(cart.subtotal, session_discounts, cart)
    
    return {
        'order_number': cart.order_number,
        'items': items,
        'subtotal': float(cart.subtotal),
        'discount_amount': discount_amount,
        'applied_discounts': applied_discounts,
        'tax_rate': float(cart.tax_rate),
        'tax_amount': float(cart.tax_amount),
        'total_amount': float(cart.total_amount),
        'item_count': sum(item.quantity for item in cart.items.all()),
    }


def calculate_discount_amount(subtotal, discounts, cart=None):
    """
    Calculate the total discount amount for given discounts.
    If cart is provided, calculates product-specific discounts.
    Otherwise falls back to simple calculation for backwards compatibility.
    """
    from decimal import Decimal
    
    total_discount = Decimal('0.00')
    subtotal_decimal = Decimal(str(subtotal))
    
    # If no cart provided, use simple calculation (backwards compatibility)
    if not cart:
        for discount in discounts:
            discount_value = Decimal(str(discount['discount_value']))
            
            if discount['discount_type'] == 'Percentage':
                discount_amount = subtotal_decimal * (discount_value / 100)
            elif discount['discount_type'] == 'Fixed Amount':
                discount_amount = discount_value
            else:  # Total Order Discount
                discount_amount = discount_value
            
            total_discount += discount_amount
    else:
        # Product-specific discount calculation
        cart_items = cart.items.all()
        
        for discount in discounts:
            discount_value = Decimal(str(discount['discount_value']))
            
            try:
                from .models import SpecialOffer
                offer = SpecialOffer.objects.get(id=discount['offer_id'])
                
                # Calculate eligible items subtotal
                eligible_subtotal = Decimal('0.00')
                
                for item in cart_items:
                    item_eligible = False
                    
                    # Check if discount applies to this specific item
                    if offer.applicable_products.exists():
                        # Product-specific discount
                        if offer.applicable_products.filter(id=item.product.id).exists():
                            item_eligible = True
                    elif offer.applicable_categories.exists():
                        # Category-specific discount
                        if offer.applicable_categories.filter(id=item.product.category.id).exists():
                            item_eligible = True
                    else:
                        # Universal discount (applies to all products)
                        item_eligible = True
                    
                    # Add this item's total to eligible subtotal if it qualifies
                    if item_eligible:
                        eligible_subtotal += item.get_total_item_price()
                
                # Apply discount only to eligible items
                if eligible_subtotal > 0:
                    if discount['discount_type'] == 'Percentage':
                        total_discount += eligible_subtotal * (discount_value / 100)
                    elif discount['discount_type'] == 'Fixed Amount':
                        # For fixed amount, apply to eligible items (but don't exceed their total)
                        total_discount += min(discount_value, eligible_subtotal)
                    else:  # Fixed Amount Off Total - applies to entire cart if any eligible items
                        total_discount += discount_value
                        
            except (SpecialOffer.DoesNotExist, ImportError):
                # Fallback to simple calculation if offer not found
                if discount['discount_type'] == 'Percentage':
                    total_discount += subtotal_decimal * (discount_value / 100)
                elif discount['discount_type'] == 'Fixed Amount':
                    total_discount += discount_value
                else:  # Total Order Discount
                    total_discount += discount_value
    
    # Ensure discount doesn't exceed subtotal
    if total_discount > subtotal_decimal:
        total_discount = subtotal_decimal
    
    return float(total_discount)
