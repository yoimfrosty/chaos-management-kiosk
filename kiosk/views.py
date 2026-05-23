from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from datetime import datetime
from .forms import AgeVerificationForm
from .models import Category, Product, Order, OrderItem, SpecialOffer, AssistanceRequest
from .decorators import age_verified_required
from .cart import get_or_create_cart, clear_cart, cart_data_for_json


def _get_categories_with_strains():
    """Get list of category slugs that have products with flower_type data"""
    from django.db.models import Q
    categories_with_strains = []
    
    for category in Category.objects.all():
        has_strains = Product.objects.filter(
            category=category
        ).exclude(
            Q(flower_type__isnull=True) | Q(flower_type='')
        ).exists()
        
        if has_strains:
            categories_with_strains.append(category.slug)
    
    return categories_with_strains


def welcome_view(request):
    """Display the welcome screen"""
    # Get or create cart for order number display
    cart = None
    if request.session.get('is_21_plus'):
        cart = get_or_create_cart(request)
    return render(request, 'kiosk/welcome.html', {'cart': cart})


def age_verification_view(request):
    """Handle age verification process with customer information collection"""
    if request.method == 'POST':
        form = AgeVerificationForm(request.POST)
        if form.is_valid():
            # Store customer information and age verification in session
            request.session['is_21_plus'] = True
            request.session['age_verified_at'] = timezone.now().isoformat()
            request.session['customer_name'] = form.cleaned_data['customer_name']
            request.session['customer_contact'] = form.cleaned_data.get('customer_contact', '')
            request.session['customer_birthdate'] = form.cleaned_data['birthdate'].isoformat()
            request.session['customer_age'] = form.get_age()
            
            # Update or create a pending order with customer information
            cart = get_or_create_cart(request)
            if cart:
                cart.customer_name = form.cleaned_data['customer_name']
                cart.customer_contact = form.cleaned_data.get('customer_contact', '')
                cart.customer_birthdate = form.cleaned_data['birthdate']
                cart.age_verified_at = timezone.now()
                cart.save()
            
            # Redirect directly to product list
            messages.success(
                request, 
                f'🎉 Welcome {form.cleaned_data["customer_name"]}! Age verification successful - browse our premium cannabis products below.'
            )
            return redirect('kiosk:product_list')
        else:
            # Form validation failed
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            
    # Always show the form for GET requests or invalid POST
    form = AgeVerificationForm()
    cart = None
    if request.session.get('is_21_plus'):
        cart = get_or_create_cart(request)
    return render(request, 'kiosk/age_verification.html', {'form': form, 'cart': cart})


@require_http_methods(["GET", "POST"])
def clear_session_view(request):
    """Clear session - simple and direct approach"""
    try:
        # Clear all session data completely
        request.session.clear()
        request.session.cycle_key()
        request.session.save()
        request.session.flush()
        
        # Always redirect to age verification (no AJAX complications)
        messages.success(request, 'Session cleared successfully!')
        return redirect('kiosk:age_verification')
        
    except Exception as e:
        # Even if there's an error, still redirect to age verification
        messages.warning(request, 'Session reset.')
        return redirect('kiosk:age_verification')


@age_verified_required
def product_list_view(request):
    """Display the product browsing interface with cart"""
    try:
        cart = get_or_create_cart(request)
        products = Product.objects.filter(is_available=True)
        categories = Category.objects.all()
        
        # Filter by category
        selected_category_slug = request.GET.get('category')
        if selected_category_slug:
            products = products.filter(category__slug=selected_category_slug)
        
        # Filter by flower type (case-insensitive)
        selected_flower_type = request.GET.get('flower_type')
        if selected_flower_type:
            products = products.filter(flower_type__iexact=selected_flower_type)
        
        # Group products by category for display
        products_by_category = {}
        if not selected_category_slug:  # Show all categories when no specific category is selected
            for category in categories:
                category_products = products.filter(category=category)
                if selected_flower_type:
                    category_products = category_products.filter(flower_type__iexact=selected_flower_type)
                if category_products.exists():
                    products_by_category[category] = category_products
        else:
            # If a specific category is selected, show just that category
            try:
                category = categories.get(slug=selected_category_slug)
                products_by_category[category] = products
            except Category.DoesNotExist:
                # Handle case where category doesn't exist
                products_by_category = {}
        
        # Simple context for debugging
        context = {
            'products': products,
            'products_by_category': products_by_category,
            'categories': categories,
            'flower_types': getattr(Product, 'FLOWER_TYPES', []),
            'selected_category_slug': selected_category_slug,
            'selected_flower_type': selected_flower_type,
            'cart': cart,
            'product_discounts': {},
            'categories_with_strains': _get_categories_with_strains()
        }
        return render(request, 'kiosk/product_list.html', context)
    except Exception as e:
        # Simple error response for debugging
        from django.http import HttpResponse
        return HttpResponse(f"Error in product_list_view: {str(e)}", content_type="text/plain")


@age_verified_required
@require_POST
def add_to_cart_view(request):
    """Add a product to the cart"""
    cart = get_or_create_cart(request)
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        product = Product.objects.get(id=product_id, is_available=True)
        
        # Get or create order item
        order_item, created = OrderItem.objects.get_or_create(
            order=cart,
            product=product,
            defaults={'price_at_purchase': product.price, 'quantity': quantity}
        )
        
        if not created:
            order_item.quantity += quantity
            order_item.save()
        
        # Recalculate cart totals without discounts
        cart.recalculate_totals()
        
        # Prepare success message
        success_msg = f'{product.name} added to your order!'
        
        # Check if request is AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'message': success_msg,
                'cart': cart_data_for_json(cart, request)
            })
        else:
            messages.success(request, success_msg)
            return redirect('kiosk:product_list')
            
    except Product.DoesNotExist:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Product not found'}, status=404)
        else:
            messages.error(request, 'Product not found')
            return redirect('kiosk:product_list')


@age_verified_required
@require_POST
def update_cart_view(request):
    """Update quantity of an item in the cart"""
    cart = get_or_create_cart(request)
    order_item_id = request.POST.get('order_item_id')
    quantity = int(request.POST.get('quantity', 0))
    
    try:
        order_item = OrderItem.objects.get(id=order_item_id, order=cart)
        
        if quantity <= 0:
            order_item.delete()
            message = 'Item removed from cart'
        else:
            order_item.quantity = quantity
            order_item.save()
            message = 'Cart updated'
        
        # Recalculate cart totals without discounts
        cart.recalculate_totals()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'message': message,
                'cart': cart_data_for_json(cart, request)
            })
        else:
            messages.success(request, message)
            return redirect('kiosk:product_list')
            
    except OrderItem.DoesNotExist:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Item not found'}, status=404)
        else:
            messages.error(request, 'Item not found')
            return redirect('kiosk:product_list')


@age_verified_required
@require_POST
def remove_from_cart_view(request):
    """Remove an item from the cart"""
    cart = get_or_create_cart(request)
    order_item_id = request.POST.get('order_item_id')
    
    try:
        order_item = OrderItem.objects.get(id=order_item_id, order=cart)
        product_name = order_item.product.name
        order_item.delete()
        
        # Recalculate cart totals without discounts
        cart.recalculate_totals()
        
        # Prepare message
        message = f'{product_name} removed from cart'
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'message': message,
                'cart': cart_data_for_json(cart, request)
            })
        else:
            messages.success(request, message)
            return redirect('kiosk:product_list')
            
    except OrderItem.DoesNotExist:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Item not found'}, status=404)
        else:
            messages.error(request, 'Item not found')
            return redirect('kiosk:product_list')


@age_verified_required
def get_cart_view(request):
    """Get current cart data as JSON"""
    cart = get_or_create_cart(request)
    return JsonResponse(cart_data_for_json(cart, request))


@age_verified_required
@require_POST
def clear_cart_server_view(request):
    """Clear the entire cart"""
    clear_cart(request)
    
    cart = get_or_create_cart(request)  # Creates a new empty cart
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'message': 'Cart cleared',
            'cart': cart_data_for_json(cart, request)
        })
    else:
        messages.success(request, 'Your order has been cleared!')
        return redirect('kiosk:product_list')


@age_verified_required
def specials_view(request):
    """Display current special offers"""
    active_offers = SpecialOffer.objects.filter(is_active=True)
    # Filter by current date if dates are set
    now = timezone.now()
    active_offers = active_offers.filter(
        Q(start_date__isnull=True) | Q(start_date__lte=now)
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=now)
    )
    
    # Get available products and categories for filtering
    available_products = Product.objects.filter(is_available=True)
    available_categories = Category.objects.all()
    
    # Add applicable products to each offer for display
    offers_with_products = []
    for offer in active_offers:
        offer_products = []
        
        # If offer applies to specific products
        if offer.applicable_products.exists():
            offer_products = offer.applicable_products.filter(is_available=True)
        
        # If offer applies to categories
        elif offer.applicable_categories.exists():
            for category in offer.applicable_categories.all():
                offer_products.extend(category.products.filter(is_available=True))
        
        # If no specific restrictions, applies to all products
        else:
            offer_products = available_products[:6]  # Show first 6 as examples
        
        offers_with_products.append({
            'offer': offer,
            'applicable_products': list(offer_products)
        })
    
    cart = get_or_create_cart(request)
    return render(request, 'kiosk/specials.html', {
        'offers_with_products': offers_with_products,
        'available_products': available_products,
        'available_categories': available_categories,
        'cart': cart
    })


@age_verified_required
def about_us_view(request):
    """Display about us page"""
    cart = get_or_create_cart(request)
    return render(request, 'kiosk/about_us.html', {'cart': cart})


@age_verified_required
def help_view(request):
    """Display help/FAQ page"""
    cart = get_or_create_cart(request)
    return render(request, 'kiosk/help.html', {'cart': cart})


@age_verified_required
@csrf_exempt
def submit_order_view(request):
    """Submit the current cart as an order or show order confirmation"""
    if request.method == 'GET':
        # Handle GET requests - redirect to welcome or show last order
        last_order_id = request.session.get('last_submitted_order_id')
        if last_order_id:
            try:
                order = Order.objects.get(id=last_order_id)
                return render(request, 'kiosk/order_submitted.html', {'order': order})
            except Order.DoesNotExist:
                pass
        # No valid order to show, redirect to welcome
        messages.info(request, "Please place an order first.")
        return redirect('kiosk:welcome')
    
    # Handle POST requests - submit the order
    try:
        cart = get_or_create_cart(request)
        
        if not cart.items.exists():
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'error': 'Your cart is empty.'
                }, status=400)
            messages.error(request, "Your cart is empty.")
            return redirect('kiosk:product_list')
        
        # Change cart status to submitted
        cart.status = 'Submitted'
        # Save customer info from session if available
        cart.customer_name = request.session.get('customer_name', cart.customer_name)
        cart.customer_contact = request.session.get('customer_contact', cart.customer_contact)
        birthdate = request.session.get('customer_birthdate')
        if birthdate:
            from datetime import date
            cart.customer_birthdate = date.fromisoformat(birthdate)
        cart.age_verified_at = request.session.get('age_verified_at', cart.age_verified_at)
        cart.save()
        
        # Store order ID in session for receipt access
        request.session['last_submitted_order_id'] = cart.id
        
        # Create order notification for admin panel
        from .models import OrderNotification
        OrderNotification.objects.get_or_create(
            order=cart,
            defaults={'status': 'pending'}
        )
        
        # Clear the cart session
        clear_cart(request)
        
        # Handle JSON request (from JavaScript)
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({
                'success': True,
                'order_id': cart.order_number,
                'order_db_id': cart.id,
                'message': 'Order submitted successfully!',
                'view_order_url': f'/view-order/{cart.id}/'
            })
        
        # Handle regular form request
        return render(request, 'kiosk/order_submitted.html', {'order': cart})
        
    except Exception as e:
        # Handle errors gracefully
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({
                'success': False,
                'error': f'Failed to submit order: {str(e)}'
            }, status=500)
        messages.error(request, "Failed to submit order. Please try again.")
        return redirect('kiosk:product_list')


@age_verified_required
def view_order_view(request, order_id):
    """Display order confirmation page (replaces receipt functionality)"""
    try:
        order = Order.objects.get(id=order_id)
        return render(request, 'kiosk/view_order.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, f"Order #{order_id} not found.")
        return redirect('kiosk:welcome')
    except Exception as e:
        messages.error(request, f"Error loading order: {str(e)}")
        return redirect('kiosk:welcome')


@csrf_exempt
def clear_session_after_order_view(request):
    """Clear session data after order completion for the next customer"""
    if request.method == 'POST':
        # Clear cart and order-related session data
        clear_cart(request)
        # Remove any order-specific session data
        request.session.pop('last_submitted_order_id', None)
        request.session.pop('applied_discounts', None)
        # Clear age verification for fresh customer experience
        request.session.pop('is_21_plus', None)
        request.session.pop('age_verified_at', None)
        
        print(f"Complete session cleared for next customer. Remaining session keys: {list(request.session.keys())}")
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True, 'message': 'Session cleared successfully'})
        return JsonResponse({'success': True, 'message': 'Session cleared successfully'})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


# End of views


def debug_session_view(request):
    """Debug view to show session and cart status"""
    try:
        session_info = {
            'is_21_plus': request.session.get('is_21_plus', False),
            'age_verified_at': request.session.get('age_verified_at', None),
            'session_key': request.session.session_key,
            'cart_id': request.session.get('cart_id', None)
        }
        
        cart = None
        cart_info = None
        if session_info['is_21_plus']:
            cart = get_or_create_cart(request)
            cart_info = cart_data_for_json(cart, request)
        
        return JsonResponse({
            'session': session_info,
            'cart': cart_info
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'session': dict(request.session)
        })


@require_POST
def request_assistance_view(request):
    """Handle assistance requests from customers"""
    try:
        # Get customer info if available
        cart = get_or_create_cart(request)
        customer_name = ""
        
        # Try to get customer name from order if age verified
        if hasattr(cart, 'customer_name') and cart.customer_name:
            customer_name = cart.customer_name
        
        # Create assistance request
        assistance_request = AssistanceRequest.objects.create(
            session_key=request.session.session_key or 'no-session',
            order=cart if cart.items.exists() else None,
            customer_name=customer_name,
            message=request.POST.get('message', 'Customer requested assistance')
        )
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Assistance requested! Staff will be with you shortly.',
                'request_id': assistance_request.id
            })
        else:
            messages.info(request, 'Assistance requested! Staff will be with you shortly.')
            return redirect('kiosk:product_list')
            
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Error requesting assistance. Please try again.'
            })
        else:
            messages.error(request, 'Error requesting assistance. Please try again.')
            return redirect('kiosk:product_list')


@require_http_methods(["GET"])
def check_pending_assistance_view(request):
    """API endpoint for admin to check pending assistance requests"""
    pending_requests = AssistanceRequest.objects.filter(status='pending').order_by('-created_at')
    
    requests_data = []
    for req in pending_requests:
        requests_data.append({
            'id': req.id,
            'customer_name': req.customer_name or f"Session {req.session_key[:8]}",
            'created_at': req.created_at.isoformat(),
            'time_elapsed': (timezone.now() - req.created_at).total_seconds(),
            'order_number': req.order.order_number if req.order else None,
            'message': req.message
        })
    
    return JsonResponse({
        'pending_requests': requests_data,
        'count': len(requests_data)
    })


@require_POST
def acknowledge_assistance_view(request, request_id):
    """Mark assistance request as acknowledged"""
    try:
        assistance_request = AssistanceRequest.objects.get(id=request_id)
        assistance_request.mark_acknowledged()
        
        return JsonResponse({
            'success': True,
            'message': 'Request acknowledged successfully'
        })
    except AssistanceRequest.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Request not found'
        })


@require_POST  
def resolve_assistance_view(request, request_id):
    """Mark assistance request as resolved"""
    try:
        assistance_request = AssistanceRequest.objects.get(id=request_id)
        resolved_by = request.user.username if request.user.is_authenticated else 'Staff'
        assistance_request.mark_resolved(resolved_by=resolved_by)
        
        return JsonResponse({
            'success': True,
            'message': 'Request resolved successfully'
        })
    except AssistanceRequest.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Request not found'
        })


# Order Notification Views
def check_pending_orders_view(request):
    """Check for pending order notifications"""
    from .models import OrderNotification
    
    pending_notifications = OrderNotification.objects.filter(status='pending').order_by('-created_at')
    
    notifications_data = []
    for notification in pending_notifications:
        order = notification.order
        notifications_data.append({
            'id': notification.id,
            'order_number': order.order_number,
            'customer_name': order.customer_name or f"Session {order.session_key[:8]}...",
            'total_amount': str(order.total_amount),
            'item_count': order.items.count(),
            'created_at': notification.created_at.isoformat(),
            'status': notification.status
        })
    
    return JsonResponse({
        'pending_notifications': notifications_data,
        'count': len(notifications_data)
    })


@require_POST
def acknowledge_order_notification_view(request, notification_id):
    """Mark order notification as acknowledged"""
    try:
        from .models import OrderNotification
        notification = OrderNotification.objects.get(id=notification_id)
        notification.mark_acknowledged()
        
        return JsonResponse({
            'success': True,
            'message': 'Order notification acknowledged successfully'
        })
    except OrderNotification.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Notification not found'
        })


@require_POST  
def complete_order_notification_view(request, notification_id):
    """Mark order notification as completed"""
    try:
        from .models import OrderNotification
        notification = OrderNotification.objects.get(id=notification_id)
        notification.mark_completed()
        
        return JsonResponse({
            'success': True,
            'message': 'Order notification completed successfully'
        })
    except OrderNotification.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Notification not found'
        })


# View removed - test functionality no longer needed
