"""
Tax model for product tax calculations.

This module provides models for managing tax rates
and tax calculations per product.
"""
from datetime import datetime
from decimal import Decimal
from app.extensions import db


class TaxRate(db.Model):
    """
    Tax Rate model for tax configuration.
    
    Attributes:
        id (int): Primary key
        name (str): Tax name (e.g., VAT, Sales Tax, GST)
        rate (Decimal): Tax rate percentage
        tax_type (str): Type of tax (vat, sales_tax, gst, custom)
        applicable_to (str): Where tax applies (all, products, categories, shops)
        applicable_ids (JSON): IDs of applicable products/categories/shops
        is_active (bool): Whether tax is active
        created_at (datetime): When tax was created
        updated_at (datetime): Last update timestamp
    """
    __tablename__ = 'tax_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rate = db.Column(db.Numeric(5, 2), nullable=False)  # Percentage (e.g., 15.00 for 15%)
    tax_type = db.Column(db.String(50), nullable=False)  # vat, sales_tax, gst, custom
    applicable_to = db.Column(db.String(50), default='all')  # all, products, categories, shops
    applicable_ids = db.Column(db.JSON, nullable=True)  # List of IDs
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_tax(self, amount):
        """
        Calculate tax amount.
        
        Args:
            amount: Amount to calculate tax on
            
        Returns:
            Decimal: Tax amount
        """
        return (amount * self.rate) / 100
    
    def __repr__(self):
        return f'<TaxRate {self.name} {self.rate}%>'


class ProductTax(db.Model):
    """
    Product Tax model for product-specific tax rates.
    
    Attributes:
        id (int): Primary key
        product_id (int): Foreign key to Product
        tax_rate_id (int): Foreign key to TaxRate
        created_at (datetime): When tax was assigned
    """
    __tablename__ = 'product_taxes'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    tax_rate_id = db.Column(db.Integer, db.ForeignKey('tax_rates.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    product = db.relationship('Product', backref='product_taxes', lazy=True)
    tax_rate = db.relationship('TaxRate', backref='product_taxes', lazy=True)
    
    # Unique constraint: one tax rate per product
    __table_args__ = (db.UniqueConstraint('product_id', 'tax_rate_id', name='unique_product_tax'),)
    
    def __repr__(self):
        return f'<ProductTax product_id={self.product_id} tax_rate_id={self.tax_rate_id}>'

