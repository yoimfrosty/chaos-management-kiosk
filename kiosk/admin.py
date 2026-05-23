from django.contrib import admin
from django.utils.html import mark_safe, format_html
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta
from .models import Category, Product, ProductCustomField, Order, OrderItem, SpecialOffer, AssistanceRequest, OrderNotification


class ProductCustomFieldInline(admin.TabularInline):
    """Inline for managing custom product fields"""
    model = ProductCustomField
    extra = 3
    fields = ('field_name', 'field_value', 'display_order')
    ordering = ('display_order', 'field_name')
    verbose_name = "Product Detail Field"
    verbose_name_plural = "Product Detail Fields"
    
    class Media:
        css = {
            'all': ('admin/css/custom_fields.css',)
        }


@admin.register(ProductCustomField)
class ProductCustomFieldAdmin(admin.ModelAdmin):
    """Admin for managing custom product fields"""
    list_display = ('product', 'field_name', 'field_value', 'display_order')
    list_filter = ('field_name', 'product__category')
    search_fields = ('product__name', 'field_name', 'field_value')
    list_editable = ('display_order',)
    ordering = ('product__name', 'display_order')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'emoji_display', 'slug', 'product_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('name', 'emoji', 'slug', 'description', 'image', 'created_at', 'updated_at')
    
    def emoji_display(self, obj):
        """Display emoji with fallback"""
        return obj.emoji if obj.emoji else "No emoji"
    emoji_display.short_description = 'Emoji'
    
    def product_count(self, obj):
        """Display the number of products in this category"""
        return obj.products.count()
    product_count.short_description = 'Products Count'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight', 'is_available', 'flower_type', 'image_thumbnail_preview', 'updated_at')
    list_filter = ('is_available', 'category', 'flower_type')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_available')
    readonly_fields = ('image_thumbnail_preview', 'image2_thumbnail_preview', 'created_at', 'updated_at')
    actions = ['mark_as_available', 'mark_as_unavailable']
    inlines = [ProductCustomFieldInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'price', 'is_available')
        }),
        ('Legal Notice', {
            'fields': ('legal_notice',),
            'description': 'Optional legal notice or disclaimer for this product'
        }),
        ('Legacy Fields (Optional)', {
            'fields': ('flower_type', 'thc_content', 'cbd_content', 'weight'),
            'classes': ('collapse',),
            'description': 'Legacy fields - Use Custom Fields below for new product information'
        }),
        ('Images', {
            'fields': ('image', 'image_thumbnail_preview', 'image2', 'image2_thumbnail_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def image_thumbnail_preview(self, obj):
        """Display a small thumbnail of the product image"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />')
        return "No Image"
    image_thumbnail_preview.short_description = 'Image 1 Preview'

    def image2_thumbnail_preview(self, obj):
        """Display a small thumbnail of the second product image"""
        if obj.image2:
            return mark_safe(f'<img src="{obj.image2.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />')
        return "No Image 2"
    image2_thumbnail_preview.short_description = 'Image 2 Preview'

    @admin.action(description='Mark selected products as Available')
    def mark_as_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} products were successfully marked as available.')

    @admin.action(description='Mark selected products as Unavailable')
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} products were successfully marked as unavailable.')


class OrderItemInline(admin.TabularInline):
    """Inline for Order Items in Order admin"""
    model = OrderItem
    readonly_fields = ('product', 'product_name', 'product_category', 'price_at_purchase', 'get_total_item_price_display')
    fields = ('product', 'product_name', 'product_category', 'quantity', 'price_at_purchase', 'get_total_item_price_display')
    extra = 0  # Don't show empty extra forms
    can_delete = False  # Usually manage items through kiosk
    
    def product_name(self, obj):
        """Display the product name for easier identification"""
        return obj.product.name if obj.product else "-"
    product_name.short_description = 'Product Name'
    
    def product_category(self, obj):
        """Display the product category for easier identification"""
        return obj.product.category.name if obj.product and obj.product.category else "-"
    product_category.short_description = 'Category'
    
    def get_total_item_price_display(self, obj):
        """Display the total price for this item"""
        if obj.pk:
            return f"${obj.get_total_item_price():.2f}"
        return "-"
    get_total_item_price_display.short_description = 'Item Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Orders"""
    list_display = ('order_number', 'customer_name', 'customer_age_display', 'status', 'receipt_link', 'item_count', 'total_amount', 'created_at', 'get_session_info')
    list_filter = ('status', 'created_at', 'age_verified_at')
    search_fields = ('order_number', 'session_key', 'customer_name', 'customer_contact')
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    readonly_fields = ('order_number', 'session_key', 'subtotal', 'discount_amount', 'tax_amount', 'total_amount', 'calculation_breakdown', 'customer_age_display', 'created_at', 'updated_at')
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'status', 'session_key')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_contact', 'customer_birthdate', 'age_verified_at', 'customer_age_display'),
        }),
        ('Order Totals', {
            'fields': (('subtotal', 'discount_amount'), ('tax_rate', 'tax_amount'), 'total_amount', 'calculation_breakdown')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    actions = ['mark_as_ready', 'mark_as_completed', 'recalculate_order_totals', 'view_receipt']
    
    def get_urls(self):
        """Add custom URLs for admin actions"""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/receipt/', self.admin_site.admin_view(self.receipt_view), name='kiosk_order_receipt'),
        ]
        return custom_urls + urls
    
    def receipt_view(self, request, order_id):
        """Display order receipt"""
        from django.shortcuts import get_object_or_404, render
        
        order = get_object_or_404(Order, id=order_id)
        
        # Recalculate totals to ensure accuracy
        order.recalculate_totals()
        
        context = {
            'order': order,
            'title': f'Receipt - Order {order.order_number}',
            'opts': self.model._meta,
        }
        
        return render(request, 'admin/kiosk/order_receipt.html', context)
    
    def customer_age_display(self, obj):
        """Calculate and display customer's current age"""
        if obj.customer_birthdate:
            age = obj.get_customer_age()
            if age is not None:
                return "{} years old".format(age)
            else:
                return "Invalid birthdate"
        return "Not provided"
    customer_age_display.short_description = 'Customer Age'
    
    def calculation_breakdown(self, obj):
        """Show detailed calculation breakdown"""
        from django.utils.html import format_html
        from decimal import Decimal
        
        # Calculate actual subtotal from items
        actual_subtotal = sum(item.get_total_item_price() for item in obj.items.all())
        
        # Show calculation without automatic discounts
        tax_rate = Decimal(str(obj.tax_rate))
        calculated_tax = actual_subtotal * tax_rate
        calculated_total = actual_subtotal + calculated_tax
        
        # Build breakdown parts - simple dark theme styling
        parts = [
            '<div style="font-family: monospace; font-size: 13px; padding: 15px; margin: 10px 0; color: #fff; background: transparent;">',
            '<strong>Calculation Breakdown:</strong><br><br>',
            'Items Subtotal: <strong>${}</strong><br>'.format(actual_subtotal),
        ]
        
        # Show manual discount if applied by receptionist
        if obj.discount_amount > 0:
            after_discount = actual_subtotal - obj.discount_amount
            discount_tax = after_discount * tax_rate
            discount_total = after_discount + discount_tax
            parts.extend([
                '<span style="color: #ff6b6b; font-weight: bold;">Manual Discount: -${}</span><br>'.format(obj.discount_amount),
                'After Discount: <strong>${}</strong><br>'.format(after_discount),
                'Tax ({}%): <strong>${:.2f}</strong><br>'.format(float(obj.tax_rate) * 100, discount_tax),
                '<strong style="color: #4ecdc4;">Total with Discount: ${:.2f}</strong><br>'.format(discount_total),
                '<hr style="border: none; border-top: 1px solid #666; margin: 10px 0;">',
            ])
        
        parts.extend([
            'Tax ({}%): <strong>${:.2f}</strong><br>'.format(float(obj.tax_rate) * 100, calculated_tax),
            '<strong style="color: #4ecdc4;">Full Price Total: ${:.2f}</strong>'.format(calculated_total),
            '</div>'
        ])
        
        breakdown = ''.join(parts)
        return format_html(breakdown)
    calculation_breakdown.short_description = 'Calculation Details'
    
    def discount_display(self, obj):
        """Display discount information clearly"""
        from django.utils.html import format_html
        if obj.discount_amount and obj.discount_amount > 0:
            percentage = (obj.discount_amount / obj.subtotal * 100) if obj.subtotal > 0 else 0
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">-${} ({}% off)</span>',
                "{:.2f}".format(float(obj.discount_amount)), 
                "{:.1f}".format(float(percentage))
            )
        return format_html('<span style="color: #6c757d;">None (Full Price)</span>')
    discount_display.short_description = 'Discount Applied'
    
    def item_count(self, obj):
        """Display the number of items in this order"""
        return obj.items.count()
    item_count.short_description = 'Items'
    
    def get_session_info(self, obj):
        """Display session information in a more readable format"""
        if obj.session_key:
            return f"Session: {obj.session_key[:8]}..."
        return "No Session"
    get_session_info.short_description = 'Session Info'
    
    def receipt_link(self, obj):
        """Display link to order receipt with improved styling"""
        from django.utils.html import format_html
        return format_html(
            '<a href="/admin/kiosk/order/{}/receipt/" target="_blank" style="background: #007cba; color: white; padding: 4px 8px; border-radius: 3px; text-decoration: none; font-size: 11px; font-weight: bold; display: inline-block;">🧾 View</a>',
            obj.id
        )
    receipt_link.short_description = 'Receipt'
    
    @admin.action(description='Mark selected orders as Ready')
    def mark_as_ready(self, request, queryset):
        updated = queryset.update(status='Ready')
        self.message_user(request, f'{updated} orders were successfully marked as ready.')
    
    @admin.action(description='Mark selected orders as Completed')
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='Completed')
        self.message_user(request, f'{updated} orders were successfully marked as completed.')
    
    @admin.action(description='Recalculate totals for selected orders (full price)')
    def recalculate_order_totals(self, request, queryset):
        updated_count = 0
        error_count = 0
        messages = []
        
        for order in queryset:
            try:
                # Store old values for comparison
                old_values = {
                    'subtotal': order.subtotal,
                    'discount_amount': order.discount_amount,
                    'tax_amount': order.tax_amount,
                    'total_amount': order.total_amount
                }
                
                # Force recalculation without automatic discounts
                order.recalculate_totals()
                
                # Check if anything changed
                changes = []
                if old_values['subtotal'] != order.subtotal:
                    changes.append(f"subtotal: ${old_values['subtotal']} → ${order.subtotal}")
                if old_values['discount_amount'] != order.discount_amount:
                    changes.append(f"discount: ${old_values['discount_amount']} → ${order.discount_amount}")
                if old_values['tax_amount'] != order.tax_amount:
                    changes.append(f"tax: ${old_values['tax_amount']} → ${order.tax_amount}")
                if old_values['total_amount'] != order.total_amount:
                    changes.append(f"total: ${old_values['total_amount']} → ${order.total_amount}")
                
                if changes:
                    updated_count += 1
                    messages.append(f"Order {order.order_number}: {', '.join(changes)}")
                    
            except Exception as e:
                error_count += 1
                messages.append(f"Order {order.order_number}: Error - {str(e)}")
        
        # Provide detailed feedback
        if updated_count > 0:
            self.message_user(
                request, 
                f'Successfully recalculated {updated_count} orders to full price. Details: {"; ".join(messages[:5])}{"..." if len(messages) > 5 else ""}'
            )
        elif error_count > 0:
            self.message_user(request, f'Errors occurred with {error_count} orders: {"; ".join(messages[:3])}', level='ERROR')
        else:
            self.message_user(request, f'All {queryset.count()} orders already had correct full-price totals - no changes needed.')
        
        if error_count > 0:
            self.message_user(request, f'{error_count} orders had errors during recalculation.', level='WARNING')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for Order Items"""
    list_display = ('order', 'product', 'product_name', 'product_category', 'quantity', 'price_at_purchase', 'get_total_item_price_display')
    list_filter = ('product__category', 'order__status', 'order__created_at')
    search_fields = ('product__name', 'order__order_number')
    readonly_fields = ('get_total_item_price_display', 'price_at_purchase')
    raw_id_fields = ('order', 'product')
    
    def product_name(self, obj):
        """Display the product name for easier identification"""
        return obj.product.name if obj.product else "-"
    product_name.short_description = 'Product Name'
    
    def product_category(self, obj):
        """Display the product category for easier identification"""
        return obj.product.category.name if obj.product and obj.product.category else "-"
    product_category.short_description = 'Category'
    
    def get_total_item_price_display(self, obj):
        """Display the total price for this item"""
        if obj.pk:
            return f"${obj.get_total_item_price():.2f}"
        return "-"
    get_total_item_price_display.short_description = 'Item Total'


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_type', 'discount_value', 'minimum_quantity', 'start_date', 'end_date', 'is_active', 'is_currently_active_display')
    list_filter = ('is_active', 'discount_type', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'offer_display_text')
    filter_horizontal = ('applicable_products', 'applicable_categories')
    readonly_fields = ('created_at', 'updated_at', 'is_currently_active_display')
    actions = ['activate_offers', 'deactivate_offers']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Display Options', {
            'fields': ('offer_display_text', 'minimum_quantity'),
            'description': 'Customize how this offer appears on product cards and set quantity requirements'
        }),
        ('Applicability', {
            'fields': ('applicable_products', 'applicable_categories'),
            'description': 'Leave both empty for universal offers'
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',)
        }),
        ('Advanced Settings', {
            'fields': ('discount_type', 'discount_value', 'minimum_spend'),
            'classes': ('collapse',),
            'description': 'Advanced discount configuration (usually managed by system administrators)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def is_currently_active_display(self, obj):
        """Display if the offer is currently active (considering dates)"""
        if obj.is_currently_active():
            return mark_safe('<span style="color: green; font-weight: bold;">✓ Active</span>')
        else:
            return mark_safe('<span style="color: red; font-weight: bold;">✗ Inactive</span>')
    is_currently_active_display.short_description = 'Currently Active'
    
    @admin.action(description='Activate selected offers')
    def activate_offers(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} offers were successfully activated.')
    
    @admin.action(description='Deactivate selected offers')
    def deactivate_offers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} offers were successfully deactivated.')


@admin.register(AssistanceRequest)
class AssistanceRequestAdmin(admin.ModelAdmin):
    list_display = ('customer_info', 'status_badge', 'order_link', 'created_at', 'time_elapsed', 'action_buttons')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'session_key', 'message')
    readonly_fields = ('session_key', 'created_at', 'acknowledged_at', 'resolved_at', 'time_elapsed_detailed')
    actions = ['mark_acknowledged', 'mark_resolved']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('customer_name', 'session_key', 'message', 'order')
        }),
        ('Status', {
            'fields': ('status', 'resolved_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'acknowledged_at', 'resolved_at', 'time_elapsed_detailed'),
            'classes': ('collapse',)
        })
    )
    
    def customer_info(self, obj):
        """Display customer information"""
        if obj.customer_name:
            return f"{obj.customer_name}"
        return f"Session {obj.session_key[:8]}..."
    customer_info.short_description = 'Customer'
    
    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': '#dc3545',  # Red
            'acknowledged': '#ffc107',  # Yellow
            'resolved': '#28a745'  # Green
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def order_link(self, obj):
        """Link to associated order if exists"""
        if obj.order:
            return format_html(
                '<a href="/admin/kiosk/order/{}/change/" target="_blank">{}</a>',
                obj.order.id,
                obj.order.order_number
            )
        return "No order"
    order_link.short_description = 'Order'
    
    def time_elapsed(self, obj):
        """Show time elapsed since request"""
        elapsed = timezone.now() - obj.created_at
        if elapsed.total_seconds() < 60:
            return f"{int(elapsed.total_seconds())}s ago"
        elif elapsed.total_seconds() < 3600:
            return f"{int(elapsed.total_seconds() // 60)}m ago"
        else:
            return f"{int(elapsed.total_seconds() // 3600)}h ago"
    time_elapsed.short_description = 'Time Elapsed'
    
    def time_elapsed_detailed(self, obj):
        """Detailed time information"""
        now = timezone.now()
        created = f"Created: {obj.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        elapsed = now - obj.created_at
        
        details = [created]
        details.append(f"Elapsed: {elapsed}")
        
        if obj.acknowledged_at:
            details.append(f"Acknowledged: {obj.acknowledged_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if obj.resolved_at:
            details.append(f"Resolved: {obj.resolved_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
        return mark_safe("<br>".join(details))
    time_elapsed_detailed.short_description = 'Timeline'
    
    def action_buttons(self, obj):
        """Quick action buttons"""
        buttons = []
        if obj.status == 'pending':
            buttons.append(
                f'<a href="/admin/kiosk/assistancerequest/{obj.id}/acknowledge/" '
                f'onclick="return confirm(\'Mark as acknowledged?\')" '
                f'style="background: #ffc107; color: black; padding: 2px 6px; border-radius: 3px; text-decoration: none; font-size: 11px; margin-right: 5px;">ACK</a>'
            )
        if obj.status in ['pending', 'acknowledged']:
            buttons.append(
                f'<a href="/admin/kiosk/assistancerequest/{obj.id}/resolve/" '
                f'onclick="return confirm(\'Mark as resolved?\')" '
                f'style="background: #28a745; color: white; padding: 2px 6px; border-radius: 3px; text-decoration: none; font-size: 11px;">RESOLVE</a>'
            )
        return format_html(''.join(buttons)) if buttons else "No actions"
    action_buttons.short_description = 'Quick Actions'
    
    @admin.action(description='Mark selected requests as Acknowledged')
    def mark_acknowledged(self, request, queryset):
        updated = 0
        for req in queryset.filter(status='pending'):
            req.mark_acknowledged()
            updated += 1
        self.message_user(request, f'{updated} requests were marked as acknowledged.')
    
    @admin.action(description='Mark selected requests as Resolved')
    def mark_resolved(self, request, queryset):
        updated = 0
        for req in queryset.filter(status__in=['pending', 'acknowledged']):
            req.mark_resolved(resolved_by=request.user.username)
            updated += 1
        self.message_user(request, f'{updated} requests were marked as resolved.')


@admin.register(OrderNotification)
class OrderNotificationAdmin(admin.ModelAdmin):
    list_display = ('order_info', 'customer_info', 'status_badge', 'total_amount', 'created_at', 'time_elapsed', 'action_buttons')
    list_filter = ('status', 'created_at', 'order__status')
    search_fields = ('order__order_number', 'order__customer_name', 'order__customer_contact')
    readonly_fields = ('order', 'created_at', 'acknowledged_at', 'completed_at', 'time_elapsed_detailed')
    actions = ['mark_acknowledged', 'mark_completed']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'acknowledged_at', 'completed_at', 'time_elapsed_detailed'),
            'classes': ('collapse',)
        })
    )
    
    def order_info(self, obj):
        """Display order number and link"""
        return format_html(
            '<a href="/admin/kiosk/order/{}/change/" target="_blank">{}</a>',
            obj.order.id,
            obj.order.order_number
        )
    order_info.short_description = 'Order'
    
    def customer_info(self, obj):
        """Display customer information"""
        if obj.order.customer_name:
            return f"{obj.order.customer_name}"
        return f"Session {obj.order.session_key[:8]}..."
    customer_info.short_description = 'Customer'
    
    def total_amount(self, obj):
        """Display order total"""
        return f"${obj.order.total_amount:.2f}"
    total_amount.short_description = 'Total'
    
    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': '#dc3545',     # Red
            'acknowledged': '#ffc107', # Yellow  
            'completed': '#28a745'    # Green
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def time_elapsed(self, obj):
        """Show time elapsed since notification"""
        elapsed = timezone.now() - obj.created_at
        if elapsed.total_seconds() < 60:
            return f"{int(elapsed.total_seconds())}s ago"
        elif elapsed.total_seconds() < 3600:
            return f"{int(elapsed.total_seconds() // 60)}m ago"
        else:
            return f"{int(elapsed.total_seconds() // 3600)}h ago"
    time_elapsed.short_description = 'Time Elapsed'
    
    def time_elapsed_detailed(self, obj):
        """Detailed time information"""
        now = timezone.now()
        created = f"Created: {obj.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        elapsed = now - obj.created_at
        
        details = [created]
        details.append(f"Elapsed: {elapsed}")
        
        if obj.acknowledged_at:
            details.append(f"Acknowledged: {obj.acknowledged_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if obj.completed_at:
            details.append(f"Completed: {obj.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
        return mark_safe("<br>".join(details))
    time_elapsed_detailed.short_description = 'Timeline'
    
    def action_buttons(self, obj):
        """Quick action buttons"""
        buttons = []
        if obj.status == 'pending':
            buttons.append(
                f'<a href="/kiosk/acknowledge-order-notification/{obj.id}/" '
                f'onclick="return confirm(\'Mark as acknowledged?\')" '
                f'style="background: #ffc107; color: black; padding: 2px 6px; border-radius: 3px; text-decoration: none; font-size: 11px; margin-right: 5px;">ACK</a>'
            )
        if obj.status in ['pending', 'acknowledged']:
            buttons.append(
                f'<a href="/kiosk/complete-order-notification/{obj.id}/" '
                f'onclick="return confirm(\'Mark as completed?\')" '
                f'style="background: #28a745; color: white; padding: 2px 6px; border-radius: 3px; text-decoration: none; font-size: 11px;">COMPLETE</a>'
            )
        return format_html(''.join(buttons)) if buttons else "No actions"
    action_buttons.short_description = 'Quick Actions'
    
    @admin.action(description='Mark selected notifications as Acknowledged')
    def mark_acknowledged(self, request, queryset):
        updated = 0
        for notification in queryset.filter(status='pending'):
            notification.mark_acknowledged()
            updated += 1
        self.message_user(request, f'{updated} notifications were marked as acknowledged.')
    
    @admin.action(description='Mark selected notifications as Completed')
    def mark_completed(self, request, queryset):
        updated = 0
        for notification in queryset.filter(status__in=['pending', 'acknowledged']):
            notification.mark_completed()
            updated += 1
        self.message_user(request, f'{updated} notifications were marked as completed.')


# Customize the admin site header and title
admin.site.site_header = "Ocean City Hemp Kiosk Admin"
admin.site.site_title = "OCH Kiosk Admin"
admin.site.index_title = "Welcome to Ocean City Hemp Kiosk Administration"
