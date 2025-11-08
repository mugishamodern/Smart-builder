"""
Coupon/Discount model for promotional discounts.

This module provides models for managing coupons and discounts,
including percentage and fixed amount discounts.
"""
from datetime import datetime
from decimal import Decimal
from app.extensions import db


class Coupon(db.Model):
    """
    Coupon model for promotional discounts.
    
    Attributes:
        id (int): Primary key
        code (str): Unique coupon code
        discount_type (str): Type of discount (percentage, fixed)
        discount_value (Decimal): Discount value (percentage or amount)
        min_order_amount (Decimal): Minimum order amount to use coupon
        max_discount_amount (Decimal): Maximum discount amount (for percentage)
        usage_limit (int): Maximum number of times coupon can be used
        usage_count (int): Number of times coupon has been used
        valid_from (datetime): When coupon becomes valid
        valid_until (datetime): When coupon expires
        is_active (bool): Whether coupon is active
        applicable_to (str): Where coupon applies (all, products, categories, shops)
        applicable_ids (JSON): IDs of applicable products/categories/shops
        created_by (int): Foreign key to User (admin who created)
        created_at (datetime): When coupon was created
        updated_at (datetime): Last update timestamp
    """
    __tablename__ = 'coupons'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    discount_type = db.Column(db.String(20), nullable=False)  # percentage, fixed
    discount_value = db.Column(db.Numeric(10, 2), nullable=False)
    min_order_amount = db.Column(db.Numeric(10, 2), nullable=True)
    max_discount_amount = db.Column(db.Numeric(10, 2), nullable=True)
    usage_limit = db.Column(db.Integer, nullable=True)  # None = unlimited
    usage_count = db.Column(db.Integer, default=0, nullable=False)
    valid_from = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    applicable_to = db.Column(db.String(50), default='all')  # all, products, categories, shops
    applicable_ids = db.Column(db.JSON, nullable=True)  # List of IDs
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    creator = db.relationship('User', foreign_keys=[created_by], lazy=True)
    
    def is_valid(self, order_amount=None):
        """
        Check if coupon is valid for use.
        
        Args:
            order_amount: Order amount (optional, for min_order_amount check)
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.is_active:
            return False, 'Coupon is not active'
        
        if datetime.utcnow() < self.valid_from:
            return False, 'Coupon is not yet valid'
        
        if self.valid_until and datetime.utcnow() > self.valid_until:
            return False, 'Coupon has expired'
        
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False, 'Coupon usage limit reached'
        
        if order_amount and self.min_order_amount and order_amount < self.min_order_amount:
            return False, f'Minimum order amount is {self.min_order_amount}'
        
        return True, None
    
    def calculate_discount(self, order_amount):
        """
        Calculate discount amount for an order.
        
        Args:
            order_amount: Order amount
            
        Returns:
            Decimal: Discount amount
        """
        if self.discount_type == 'percentage':
            discount = (order_amount * self.discount_value) / 100
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return Decimal(str(discount))
        else:  # fixed
            return min(self.discount_value, order_amount)
    
    def apply(self):
        """Increment usage count when coupon is used."""
        self.usage_count += 1
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<Coupon {self.code} {self.discount_type} {self.discount_value}>'


class CouponUsage(db.Model):
    """
    Coupon Usage model for tracking coupon usage.
    
    Attributes:
        id (int): Primary key
        coupon_id (int): Foreign key to Coupon
        order_id (int): Foreign key to Order
        user_id (int): Foreign key to User
        discount_amount (Decimal): Discount amount applied
        created_at (datetime): When coupon was used
    """
    __tablename__ = 'coupon_usages'
    
    id = db.Column(db.Integer, primary_key=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    discount_amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    coupon = db.relationship('Coupon', backref='usages', lazy=True)
    order = db.relationship('Order', backref='coupon_usages', lazy=True)
    user = db.relationship('User', backref='coupon_usages', lazy=True)
    
    def __repr__(self):
        return f'<CouponUsage coupon_id={self.coupon_id} order_id={self.order_id}>'

