from django.http import HttpResponse
from kiosk.models import Order

def test_receipt_raw(request, order_id):
    """Raw test function"""
    try:
        order = Order.objects.get(id=order_id)
        html = f"""
        <html>
        <head><title>Raw Receipt Test</title></head>
        <body>
        <h1>OCEAN CITY KIOSK</h1>
        <p>Order: {order.order_number}</p>
        <p>Total: ${order.total_amount}</p>
        <p>Status: {order.status}</p>
        </body>
        </html>
        """
        return HttpResponse(html)
    except Order.DoesNotExist:
        return HttpResponse("<h1>Order not found</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>Error: {str(e)}</h1>")
