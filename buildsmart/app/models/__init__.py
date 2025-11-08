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
from .message import Message, Conversation
from .comparison import Comparison
from .address import Address
from .token import Token
from .product_image import ProductImage
from .wishlist import Wishlist
from .stock_notification import StockNotification
from .search_history import SearchHistory, TrendingSearch
from .order_status import OrderStatus
from .inventory_alert import InventoryAlert
from .order_modification import OrderModification
from .order_fulfillment import OrderFulfillment, FulfillmentItem
from .return_exchange import ReturnRequest, ReturnItem
from .dispute import Dispute, DisputeMessage
from .notification import Notification, NotificationPreference
from .message_attachment import MessageAttachment
from .coupon import Coupon, CouponUsage
from .tax import TaxRate, ProductTax
from .wallet import Wallet, Transaction
from .analytics import AnalyticsMetric, ReportSchedule

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
    'Review',
    'Message',
    'Conversation',
    'Comparison',
    'Address',
    'Token',
    'ProductImage',
    'Wishlist',
    'StockNotification',
    'SearchHistory',
    'TrendingSearch',
    'OrderStatus',
    'InventoryAlert',
    'OrderModification',
    'OrderFulfillment',
    'FulfillmentItem',
    'ReturnRequest',
    'ReturnItem',
    'Dispute',
    'DisputeMessage',
    'Notification',
    'NotificationPreference',
    'MessageAttachment',
    'Coupon',
    'CouponUsage',
    'TaxRate',
    'ProductTax',
    'Wallet',
    'Transaction',
    'AnalyticsMetric',
    'ReportSchedule'
]
