from django.shortcuts import render
from django.http import HttpResponse
from kiosk.models import Order

def simple_receipt_test(request, order_id):
    """Simple test view to debug blank receipt issue"""
    try:
        order = Order.objects.get(id=order_id)
        
        # Return basic HTML first to test
        return HttpResponse(f"""
        <html>
        <head><title>Receipt Test</title></head>
        <body>
        <h1>RECEIPT TEST</h1>
        <p>Order ID: {order.id}</p>
        <p>Order Number: {order.order_number}</p>
        <p>Total: ${order.total}</p>
        <p>Status: {order.status}</p>
        <p>Items: {order.items.count()}</p>
        </body>
        </html>
        """)
        
    except Order.DoesNotExist:
        return HttpResponse(f"<h1>Order {order_id} not found</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>Error: {str(e)}</h1>")
