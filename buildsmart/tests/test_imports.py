"""
Test all imports to ensure there are no import errors.

This module tests that all modules can be imported without errors.
"""
import pytest


class TestImports:
    """Test that all modules can be imported"""
    
    def test_app_imports(self):
        """Test app imports"""
        from app import create_app
        from app.extensions import db, migrate, login_manager, bcrypt, cors, socketio, limiter, mail, cache
        from app.config import config
        
        assert create_app is not None
        assert db is not None
        assert migrate is not None
        assert login_manager is not None
        assert bcrypt is not None
        assert cors is not None
        assert socketio is not None
        assert limiter is not None
        assert mail is not None
        assert cache is not None
        assert config is not None
    
    def test_models_imports(self):
        """Test models imports"""
        from app.models import (
            User, Shop, Product, Service, Order, OrderItem, Recommendation, Category,
            Cart, CartItem, Payment, Review, Message, Conversation, Comparison, Address,
            Token, ProductImage, Wishlist, StockNotification, SearchHistory, TrendingSearch, OrderStatus,
            InventoryAlert, OrderModification, OrderFulfillment, FulfillmentItem,
            ReturnRequest, ReturnItem, Dispute, DisputeMessage,
            Notification, NotificationPreference, MessageAttachment,
            Coupon, CouponUsage, TaxRate, ProductTax, Wallet, Transaction,
            AnalyticsMetric, ReportSchedule
        )
        
        assert User is not None
        assert Shop is not None
        assert Product is not None
        assert Order is not None
        assert Coupon is not None
        assert Wallet is not None
        assert AnalyticsMetric is not None
    
    def test_services_imports(self):
        """Test services imports"""
        from app.services.cache_service import CacheService
        from app.services.analytics_service import AnalyticsService
        from app.services.coupon_service import CouponService
        from app.services.tax_service import TaxService
        from app.services.wallet_service import WalletService
        from app.services.invoice_service import InvoiceService
        from app.services.report_service import ReportService
        from app.services.email_service import EmailService
        from app.services.image_service import ImageService
        
        assert CacheService is not None
        assert AnalyticsService is not None
        assert CouponService is not None
        assert TaxService is not None
        assert WalletService is not None
        assert InvoiceService is not None
        assert ReportService is not None
        assert EmailService is not None
        assert ImageService is not None
    
    def test_utils_imports(self):
        """Test utils imports"""
        from app.utils.security import sanitize_string, validate_password_strength
        from app.utils.security_headers import setup_security_headers
        from app.utils.api_docs import get_swagger_config, get_swagger_template
        from app.utils.query_optimization import QueryOptimizer
        from app.utils.response_cache import cache_response, cache_public, cache_private
        from app.utils.database_indexes import RECOMMENDED_INDEXES
        
        assert sanitize_string is not None
        assert validate_password_strength is not None
        assert setup_security_headers is not None
        assert get_swagger_config is not None
        assert get_swagger_template is not None
        assert QueryOptimizer is not None
        assert cache_response is not None
        assert RECOMMENDED_INDEXES is not None
    
    def test_blueprints_imports(self):
        """Test blueprints imports"""
        from app.blueprints.main import main_bp
        from app.blueprints.auth import auth_bp
        from app.blueprints.user import user_bp
        from app.blueprints.shop import shop_bp
        from app.blueprints.api import api_bp
        from app.blueprints.messaging import messaging_bp
        from app.blueprints.wishlist import wishlist_bp
        
        assert main_bp is not None
        assert auth_bp is not None
        assert user_bp is not None
        assert shop_bp is not None
        assert api_bp is not None
        assert messaging_bp is not None
        assert wishlist_bp is not None
    
    def test_app_creation(self):
        """Test that app can be created"""
        from app import create_app
        
        app = create_app('testing')
        assert app is not None
        assert app.config['TESTING'] is True

