"""
Tests for Payment & Financials features.

This module tests:
- PDF invoice generation
- Coupon/discount system
- Tax calculation
- Wallet and transaction management
"""
import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from flask import current_app
from app.models import (
    User, Order, OrderItem, Product, Shop, Category,
    Coupon, CouponUsage, TaxRate, ProductTax,
    Wallet, Transaction
)
from app.services.invoice_service import InvoiceService
from app.services.coupon_service import CouponService
from app.services.tax_service import TaxService
from app.services.wallet_service import WalletService
from app.extensions import db


@pytest.fixture
def test_shop(client, test_user):
    """Create a test shop"""
    shop = Shop(
        name='Test Shop',
        description='Test shop description',
        address='123 Test St',
        phone='1234567890',
        owner_id=test_user.id,
        is_approved=True
    )
    db.session.add(shop)
    db.session.commit()
    return shop


@pytest.fixture
def test_product(client, test_shop, test_category):
    """Create a test product"""
    product = Product(
        name='Test Product',
        description='Test product description',
        price=Decimal('100.00'),
        stock_quantity=100,
        shop_id=test_shop.id,
        category_id=test_category.id if test_category else None
    )
    db.session.add(product)
    db.session.commit()
    return product


@pytest.fixture
def test_category(client):
    """Create a test category"""
    category = Category(name='Test Category', description='Test category')
    db.session.add(category)
    db.session.commit()
    return category


@pytest.fixture
def test_order(client, test_user, test_shop, test_product):
    """Create a test order"""
    order = Order(
        order_number='ORD001',
        customer_id=test_user.id,
        shop_id=test_shop.id,
        total_amount=Decimal('200.00'),
        subtotal_amount=Decimal('200.00'),
        delivery_address='123 Test St',
        payment_status='paid',
        payment_method='mobile_money'
    )
    db.session.add(order)
    
    order_item = OrderItem(
        order_id=order.id,
        product_id=test_product.id,
        quantity=2,
        unit_price=Decimal('100.00'),
        total_price=Decimal('200.00')
    )
    db.session.add(order_item)
    db.session.commit()
    return order


class TestInvoiceService:
    """Tests for invoice generation"""
    
    def test_generate_invoice(self, client, test_order):
        """Test generating PDF invoice"""
        pdf_buffer = InvoiceService.generate_invoice(test_order.id)
        
        assert pdf_buffer is not None
        assert pdf_buffer.getvalue() is not None
        assert len(pdf_buffer.getvalue()) > 0
        
        # Check PDF header
        pdf_content = pdf_buffer.getvalue()
        assert b'%PDF' in pdf_content
    
    def test_save_invoice(self, client, test_order, tmp_path):
        """Test saving invoice to file"""
        import os
        from flask import current_app
        
        # Set upload folder to temp directory
        original_upload_folder = current_app.config.get('UPLOAD_FOLDER')
        current_app.config['UPLOAD_FOLDER'] = str(tmp_path)
        
        try:
            file_path = InvoiceService.save_invoice(test_order.id)
            
            assert file_path is not None
            assert os.path.exists(file_path)
            assert file_path.endswith('.pdf')
            
            # Check file content
            with open(file_path, 'rb') as f:
                content = f.read()
                assert len(content) > 0
                assert b'%PDF' in content
        finally:
            current_app.config['UPLOAD_FOLDER'] = original_upload_folder


class TestCouponService:
    """Tests for coupon/discount system"""
    
    def test_create_coupon(self, client, test_user):
        """Test creating a coupon"""
        coupon = CouponService.create_coupon(
            code='TEST10',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            created_by=test_user.id
        )
        
        assert coupon is not None
        assert coupon.code == 'TEST10'
        assert coupon.discount_type == 'percentage'
        assert coupon.discount_value == Decimal('10.00')
        assert coupon.is_active is True
    
    def test_validate_coupon_valid(self, client, test_user):
        """Test validating a valid coupon"""
        coupon = CouponService.create_coupon(
            code='VALID10',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            valid_from=datetime.utcnow() - timedelta(days=1),
            valid_until=datetime.utcnow() + timedelta(days=1)
        )
        
        is_valid, error_msg, validated_coupon = CouponService.validate_coupon(
            'VALID10',
            test_user.id,
            order_amount=1000.00
        )
        
        assert is_valid is True
        assert error_msg is None
        assert validated_coupon.id == coupon.id
    
    def test_validate_coupon_expired(self, client, test_user):
        """Test validating an expired coupon"""
        coupon = CouponService.create_coupon(
            code='EXPIRED10',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            valid_from=datetime.utcnow() - timedelta(days=2),
            valid_until=datetime.utcnow() - timedelta(days=1)
        )
        
        is_valid, error_msg, validated_coupon = CouponService.validate_coupon(
            'EXPIRED10',
            test_user.id,
            order_amount=1000.00
        )
        
        assert is_valid is False
        assert 'expired' in error_msg.lower()
    
    def test_validate_coupon_usage_limit(self, client, test_user):
        """Test validating a coupon that reached usage limit"""
        coupon = CouponService.create_coupon(
            code='LIMIT10',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            usage_limit=1
        )
        
        # Use the coupon once
        coupon.usage_count = 1
        db.session.commit()
        
        is_valid, error_msg, validated_coupon = CouponService.validate_coupon(
            'LIMIT10',
            test_user.id,
            order_amount=1000.00
        )
        
        assert is_valid is False
        assert 'limit' in error_msg.lower()
    
    def test_calculate_discount_percentage(self, client, test_user):
        """Test calculating percentage discount"""
        coupon = CouponService.create_coupon(
            code='PERC10',
            discount_type='percentage',
            discount_value=Decimal('10.00')
        )
        
        discount = coupon.calculate_discount(Decimal('1000.00'))
        
        assert discount == Decimal('100.00')
    
    def test_calculate_discount_fixed(self, client, test_user):
        """Test calculating fixed discount"""
        coupon = CouponService.create_coupon(
            code='FIXED50',
            discount_type='fixed',
            discount_value=Decimal('50.00')
        )
        
        discount = coupon.calculate_discount(Decimal('1000.00'))
        
        assert discount == Decimal('50.00')
    
    def test_apply_coupon(self, client, test_order, test_user):
        """Test applying coupon to order"""
        coupon = CouponService.create_coupon(
            code='APPLY10',
            discount_type='percentage',
            discount_value=Decimal('10.00')
        )
        
        success, error_msg, discount_amount = CouponService.apply_coupon(
            test_order.id,
            'APPLY10'
        )
        
        assert success is True
        assert error_msg is None
        assert discount_amount > 0
        
        # Check order was updated
        order = Order.query.get(test_order.id)
        assert order.discount_amount == discount_amount
        assert order.coupon_code == 'APPLY10'
        
        # Check coupon usage was recorded
        usage = CouponUsage.query.filter_by(order_id=test_order.id).first()
        assert usage is not None
        assert usage.coupon_id == coupon.id


class TestTaxService:
    """Tests for tax calculation"""
    
    def test_create_tax_rate(self, client):
        """Test creating a tax rate"""
        tax_rate = TaxService.create_tax_rate(
            name='VAT',
            rate=Decimal('15.00'),
            tax_type='vat'
        )
        
        assert tax_rate is not None
        assert tax_rate.name == 'VAT'
        assert tax_rate.rate == Decimal('15.00')
        assert tax_rate.tax_type == 'vat'
        assert tax_rate.is_active is True
    
    def test_calculate_tax(self, client):
        """Test calculating tax amount"""
        tax_rate = TaxService.create_tax_rate(
            name='VAT',
            rate=Decimal('15.00'),
            tax_type='vat'
        )
        
        tax_amount = tax_rate.calculate_tax(Decimal('1000.00'))
        
        assert tax_amount == Decimal('150.00')
    
    def test_get_product_tax_rate(self, client, test_product):
        """Test getting tax rate for a product"""
        # Create default tax rate
        tax_rate = TaxService.create_tax_rate(
            name='VAT',
            rate=Decimal('15.00'),
            tax_type='vat',
            applicable_to='all'
        )
        
        product_tax_rate = TaxService.get_product_tax_rate(test_product.id)
        
        assert product_tax_rate is not None
        assert product_tax_rate.id == tax_rate.id
    
    def test_assign_product_tax(self, client, test_product):
        """Test assigning tax rate to product"""
        tax_rate = TaxService.create_tax_rate(
            name='VAT',
            rate=Decimal('15.00'),
            tax_type='vat'
        )
        
        product_tax = TaxService.assign_product_tax(
            test_product.id,
            tax_rate.id
        )
        
        assert product_tax is not None
        assert product_tax.product_id == test_product.id
        assert product_tax.tax_rate_id == tax_rate.id
    
    def test_calculate_order_tax(self, client, test_order, test_product):
        """Test calculating tax for an order"""
        # Create tax rate
        tax_rate = TaxService.create_tax_rate(
            name='VAT',
            rate=Decimal('15.00'),
            tax_type='vat',
            applicable_to='all'
        )
        
        # Assign tax to product
        TaxService.assign_product_tax(test_product.id, tax_rate.id)
        
        # Calculate order tax
        total_tax, tax_breakdown = TaxService.calculate_order_tax(test_order.id)
        
        assert total_tax > 0
        assert len(tax_breakdown) > 0
        
        # Check order was updated
        order = Order.query.get(test_order.id)
        assert order.tax_amount == total_tax


class TestWalletService:
    """Tests for wallet and transaction management"""
    
    def test_get_or_create_wallet(self, client, test_user):
        """Test getting or creating wallet"""
        wallet = WalletService.get_or_create_wallet(test_user.id)
        
        assert wallet is not None
        assert wallet.user_id == test_user.id
        assert wallet.balance == Decimal('0.00')
        assert wallet.currency == 'NGN'
        
        # Get existing wallet
        wallet2 = WalletService.get_or_create_wallet(test_user.id)
        assert wallet2.id == wallet.id
    
    def test_credit_wallet(self, client, test_user):
        """Test crediting wallet"""
        transaction = WalletService.credit_wallet(
            test_user.id,
            Decimal('1000.00'),
            description='Test credit'
        )
        
        assert transaction is not None
        assert transaction.transaction_type == 'credit'
        assert transaction.amount == Decimal('1000.00')
        assert transaction.status == 'completed'
        
        # Check wallet balance
        wallet = Wallet.query.filter_by(user_id=test_user.id).first()
        assert wallet.balance == Decimal('1000.00')
    
    def test_debit_wallet(self, client, test_user):
        """Test debiting wallet"""
        # First credit wallet
        WalletService.credit_wallet(test_user.id, Decimal('1000.00'))
        
        # Then debit
        transaction = WalletService.debit_wallet(
            test_user.id,
            Decimal('500.00'),
            description='Test debit'
        )
        
        assert transaction is not None
        assert transaction.transaction_type == 'debit'
        assert transaction.amount == Decimal('500.00')
        
        # Check wallet balance
        wallet = Wallet.query.filter_by(user_id=test_user.id).first()
        assert wallet.balance == Decimal('500.00')
    
    def test_debit_wallet_insufficient_balance(self, client, test_user):
        """Test debiting wallet with insufficient balance"""
        transaction = WalletService.debit_wallet(
            test_user.id,
            Decimal('1000.00'),
            description='Test debit'
        )
        
        assert transaction is None  # Should return None for insufficient balance
    
    def test_get_wallet_balance(self, client, test_user):
        """Test getting wallet balance"""
        # Credit wallet
        WalletService.credit_wallet(test_user.id, Decimal('1500.00'))
        
        balance = WalletService.get_wallet_balance(test_user.id)
        
        assert balance == Decimal('1500.00')
    
    def test_get_transactions(self, client, test_user):
        """Test getting transaction history"""
        # Create some transactions
        WalletService.credit_wallet(test_user.id, Decimal('1000.00'), 'Credit 1')
        WalletService.credit_wallet(test_user.id, Decimal('500.00'), 'Credit 2')
        WalletService.debit_wallet(test_user.id, Decimal('200.00'), 'Debit 1')
        
        transactions = WalletService.get_transactions(test_user.id, limit=10)
        
        assert len(transactions) >= 3
        
        # Check transaction types
        transaction_types = [t.transaction_type for t in transactions]
        assert 'credit' in transaction_types
        assert 'debit' in transaction_types
    
    def test_transfer_between_wallets(self, client, test_user):
        """Test transferring funds between wallets"""
        # Create another user
        user2 = User(
            username='testuser2',
            email='testuser2@example.com',
            password_hash='hashed_password'
        )
        db.session.add(user2)
        db.session.commit()
        
        # Credit first user's wallet
        WalletService.credit_wallet(test_user.id, Decimal('1000.00'))
        
        # Transfer
        success, error_msg, transactions = WalletService.transfer_between_wallets(
            test_user.id,
            user2.id,
            Decimal('500.00'),
            description='Transfer test'
        )
        
        assert success is True
        assert error_msg is None
        assert len(transactions) == 2  # One debit, one credit
        
        # Check balances
        wallet1 = Wallet.query.filter_by(user_id=test_user.id).first()
        wallet2 = Wallet.query.filter_by(user_id=user2.id).first()
        
        assert wallet1.balance == Decimal('500.00')
        assert wallet2.balance == Decimal('500.00')
    
    def test_get_wallet_summary(self, client, test_user):
        """Test getting wallet summary"""
        # Create some transactions
        WalletService.credit_wallet(test_user.id, Decimal('1000.00'), 'Credit 1')
        WalletService.debit_wallet(test_user.id, Decimal('300.00'), 'Debit 1')
        
        summary = WalletService.get_wallet_summary(test_user.id)
        
        assert summary is not None
        assert 'balance' in summary
        assert 'currency' in summary
        assert 'total_credits' in summary
        assert 'total_debits' in summary
        assert 'recent_transactions' in summary
        
        assert summary['balance'] == 700.0
        assert summary['total_credits'] == 1000.0
        assert summary['total_debits'] == 300.0


class TestPaymentIntegration:
    """Integration tests for payment features"""
    
    def test_order_with_coupon_and_tax(self, client, test_order, test_product, test_user):
        """Test order with coupon and tax calculation"""
        # Create coupon
        coupon = CouponService.create_coupon(
            code='SAVE10',
            discount_type='percentage',
            discount_value=Decimal('10.00')
        )
        
        # Create tax rate
        tax_rate = TaxService.create_tax_rate(
            name='VAT',
            rate=Decimal('15.00'),
            tax_type='vat',
            applicable_to='all'
        )
        
        # Assign tax to product
        TaxService.assign_product_tax(test_product.id, tax_rate.id)
        
        # Apply coupon
        CouponService.apply_coupon(test_order.id, 'SAVE10')
        
        # Calculate tax
        TaxService.calculate_order_tax(test_order.id)
        
        # Check order
        order = Order.query.get(test_order.id)
        
        assert order.discount_amount > 0
        assert order.tax_amount > 0
        assert order.coupon_code == 'SAVE10'
        assert order.total_amount == order.subtotal_amount - order.discount_amount + order.tax_amount
    
    def test_invoice_with_discount_and_tax(self, client, test_order, test_product):
        """Test invoice generation with discount and tax"""
        # Set discount and tax
        test_order.discount_amount = Decimal('20.00')
        test_order.tax_amount = Decimal('30.00')
        test_order.subtotal_amount = Decimal('200.00')
        test_order.total_amount = Decimal('210.00')
        db.session.commit()
        
        # Generate invoice
        pdf_buffer = InvoiceService.generate_invoice(test_order.id)
        
        assert pdf_buffer is not None
        pdf_content = pdf_buffer.getvalue()
        assert b'Discount' in pdf_content or b'Tax' in pdf_content


