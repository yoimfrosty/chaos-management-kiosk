import uuid


def generate_order_number():
    """Generate a unique order number for Ocean City Hemp"""
    return f"OCH-{str(uuid.uuid4().hex[:6]).upper()}"
