from django.urls import path
from . import views

app_name = 'kiosk'

urlpatterns = [
    path('', views.age_verification_view, name='age_verification'),  # Direct to age verification
    path('verify-age/', views.age_verification_view, name='verify_age'),  # Keep for backwards compatibility
    path('clear-session/', views.clear_session_view, name='clear_session'),  # For testing
    
    # Product browsing and cart management
    path('products/', views.product_list_view, name='product_list'),
    path('cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/', views.update_cart_view, name='update_cart'),
    path('cart/remove/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/get/', views.get_cart_view, name='get_cart'),
    path('cart/clear/', views.clear_cart_server_view, name='clear_cart'),
    
    # Phase 3: Specials, ordering
    path('specials/', views.specials_view, name='specials'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('help/', views.help_view, name='help'),
    path('submit-order/', views.submit_order_view, name='submit_order'),
    path('place-order/', views.submit_order_view, name='place_order'),  # Alias for submit_order
    path('view-order/<int:order_id>/', views.view_order_view, name='view_order'),
    path('clear-session-after-order/', views.clear_session_after_order_view, name='clear_session_after_order'),
    path('debug-session/', views.debug_session_view, name='debug_session'),
    
    # Assistance requests
    path('request-assistance/', views.request_assistance_view, name='request_assistance'),
    path('check-pending-assistance/', views.check_pending_assistance_view, name='check_pending_assistance'),
    path('acknowledge-assistance/<int:request_id>/', views.acknowledge_assistance_view, name='acknowledge_assistance'),
    path('resolve-assistance/<int:request_id>/', views.resolve_assistance_view, name='resolve_assistance'),
    
    # Order notifications
    path('check-pending-orders/', views.check_pending_orders_view, name='check_pending_orders'),
    path('acknowledge-order-notification/<int:notification_id>/', views.acknowledge_order_notification_view, name='acknowledge_order_notification'),
    path('complete-order-notification/<int:notification_id>/', views.complete_order_notification_view, name='complete_order_notification'),
]
