# Import all models to make them available for import
from .user import User
from .shop import Shop
from .product import Product
from .service import Service
from .order import Order, OrderItem
from .recommendation import Recommendation
from .category import Category
from .cart import Cart, CartItem
from .payment import Payment
from .review import Review

# Make models available for import
__all__ = [
    'User',
    'Shop', 
    'Product',
    'Service',
    'Order',
    'OrderItem',
    'Recommendation',
    'Category',
    'Cart',
    'CartItem',
    'Payment',
    'Review'
]
