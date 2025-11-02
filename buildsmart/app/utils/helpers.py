from datetime import datetime
import random
import string
from decimal import Decimal


def generate_order_number():
    """
    Generate a unique order number.
    
    Returns:
        str: Unique order number in format ORD{YYYYMMDD}{RANDOM}
    """
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD{date_str}{random_str}"


def generate_transaction_id():
    """
    Generate a unique transaction ID for payments.
    
    Returns:
        str: Unique transaction ID in format TXN{YYYYMMDD}{RANDOM}
    """
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    return f"TXN{date_str}{random_str}"


def calculate_cart_total(cart_items):
    """
    Calculate total cart value with optional tax.
    
    Args:
        cart_items: List of CartItem objects
    
    Returns:
        dict: Dictionary containing subtotal, tax, and total
    """
    subtotal = sum(item.get_subtotal() for item in cart_items)
    
    # Assume 18% tax (this can be made configurable)
    tax_rate = Decimal('0.18')
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    return {
        'subtotal': round(subtotal, 2),
        'tax': round(tax, 2),
        'tax_rate': tax_rate,
        'total': round(total, 2)
    }


def calculate_order_total(order_items):
    """
    Calculate total order value.
    
    Args:
        order_items: List of OrderItem objects
    
    Returns:
        Decimal: Total amount
    """
    return sum(item.total_price for item in order_items)


def format_price(price):
    """
    Format price for display.
    
    Args:
        price: Decimal price value
    
    Returns:
        str: Formatted price string
    """
    if price is None:
        return "0.00"
    return f"{price:,.2f}"


def format_currency(price, currency='UGX'):
    """
    Format price as currency for display.
    
    Args:
        price: Decimal price value
        currency: Currency code (default: UGX)
    
    Returns:
        str: Formatted currency string
    """
    if price is None:
        return f"{currency} 0.00"
    return f"{currency} {price:,.2f}"


def send_admin_notification(subject, message, app=None):
    """
    Send notification to admin (placeholder for future email integration).
    
    Args:
        subject: Email subject
        message: Email message
        app: Flask app instance (optional)
    """
    # TODO: Implement actual email notification
    # This is a placeholder for future email integration
    print(f"Admin Notification: {subject}")
    print(f"Message: {message}")


def send_shop_notification(shop_id, subject, message):
    """
    Send notification to shop owner (placeholder for future email integration).
    
    Args:
        shop_id: Shop ID
        subject: Email subject
        message: Email message
    """
    # TODO: Implement actual email notification
    # This is a placeholder for future email integration
    print(f"Shop {shop_id} Notification: {subject}")
    print(f"Message: {message}")


def validate_stock_availability(product, requested_quantity):
    """
    Validate if requested quantity is available in stock.
    
    Args:
        product: Product object
        requested_quantity: Integer quantity requested
    
    Returns:
        tuple: (is_available: bool, message: str)
    """
    if not product.is_available:
        return False, "Product is currently unavailable"
    
    if product.quantity_available < requested_quantity:
        return False, f"Only {product.quantity_available} units available"
    
    if requested_quantity < product.min_order_quantity:
        return False, f"Minimum order quantity is {product.min_order_quantity}"
    
    return True, "Available"


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula.
    
    Args:
        lat1: Latitude of point 1
        lon1: Longitude of point 1
        lat2: Latitude of point 2
        lon2: Longitude of point 2
    
    Returns:
        float: Distance in kilometers
    """
    import math
    
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

