# Import all models to make them available for import
from .user import User
from .shop import Shop
from .product import Product
from .service import Service
from .order import Order, OrderItem
from .recommendation import Recommendation

# Make models available for import
__all__ = [
    'User',
    'Shop', 
    'Product',
    'Service',
    'Order',
    'OrderItem',
    'Recommendation'
]
