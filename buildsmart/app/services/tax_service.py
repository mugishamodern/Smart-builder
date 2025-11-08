"""
Tax calculation service for product and order taxes.

This module provides functionality for calculating taxes
on products and orders based on configured tax rates.
"""
from decimal import Decimal
from app.extensions import db
from app.models import TaxRate, ProductTax, Product, Order, OrderItem


class TaxService:
    """Service for tax calculation"""
    
    @staticmethod
    def get_product_tax_rate(product_id):
        """
        Get tax rate for a product.
        
        Args:
            product_id: Product ID
            
        Returns:
            TaxRate: Tax rate or None
        """
        # Check for product-specific tax
        product_tax = ProductTax.query.filter_by(product_id=product_id).first()
        if product_tax:
            return product_tax.tax_rate
        
        # Check for category tax
        product = Product.query.get(product_id)
        if product and product.category_id:
            # Check if there's a tax rate for this category
            tax_rate = TaxRate.query.filter_by(
                applicable_to='categories',
                is_active=True
            ).first()
            
            if tax_rate and product.category_id in (tax_rate.applicable_ids or []):
                return tax_rate
        
        # Check for shop tax
        if product and product.shop_id:
            tax_rate = TaxRate.query.filter_by(
                applicable_to='shops',
                is_active=True
            ).first()
            
            if tax_rate and product.shop_id in (tax_rate.applicable_ids or []):
                return tax_rate
        
        # Get default tax rate (applies to all)
        tax_rate = TaxRate.query.filter_by(
            applicable_to='all',
            is_active=True
        ).first()
        
        return tax_rate
    
    @staticmethod
    def calculate_product_tax(product_id, amount):
        """
        Calculate tax for a product amount.
        
        Args:
            product_id: Product ID
            amount: Amount to calculate tax on
            
        Returns:
            tuple: (tax_amount, tax_rate)
        """
        tax_rate = TaxService.get_product_tax_rate(product_id)
        
        if not tax_rate:
            return Decimal('0.00'), None
        
        tax_amount = tax_rate.calculate_tax(Decimal(str(amount)))
        
        return tax_amount, tax_rate
    
    @staticmethod
    def calculate_order_tax(order_id):
        """
        Calculate total tax for an order.
        
        Args:
            order_id: Order ID
            
        Returns:
            tuple: (total_tax, tax_breakdown)
        """
        order = Order.query.get(order_id)
        if not order:
            return Decimal('0.00'), {}
        
        total_tax = Decimal('0.00')
        tax_breakdown = {}
        
        for item in order.items:
            tax_amount, tax_rate = TaxService.calculate_product_tax(
                item.product_id,
                item.total_price
            )
            
            if tax_rate:
                tax_key = f"{tax_rate.name} ({tax_rate.rate}%)"
                if tax_key not in tax_breakdown:
                    tax_breakdown[tax_key] = Decimal('0.00')
                tax_breakdown[tax_key] += tax_amount
                total_tax += tax_amount
        
        return total_tax, tax_breakdown
    
    @staticmethod
    def create_tax_rate(name, rate, tax_type='vat', applicable_to='all', applicable_ids=None):
        """
        Create a new tax rate.
        
        Args:
            name: Tax name
            rate: Tax rate percentage
            tax_type: Type of tax
            applicable_to: Where tax applies
            applicable_ids: Applicable IDs
            
        Returns:
            TaxRate: Created tax rate
        """
        tax_rate = TaxRate(
            name=name,
            rate=Decimal(str(rate)),
            tax_type=tax_type,
            applicable_to=applicable_to,
            applicable_ids=applicable_ids or []
        )
        
        db.session.add(tax_rate)
        db.session.commit()
        
        return tax_rate
    
    @staticmethod
    def assign_product_tax(product_id, tax_rate_id):
        """
        Assign tax rate to a product.
        
        Args:
            product_id: Product ID
            tax_rate_id: Tax rate ID
            
        Returns:
            ProductTax: Created product tax assignment
        """
        # Check if already assigned
        existing = ProductTax.query.filter_by(
            product_id=product_id,
            tax_rate_id=tax_rate_id
        ).first()
        
        if existing:
            return existing
        
        product_tax = ProductTax(
            product_id=product_id,
            tax_rate_id=tax_rate_id
        )
        
        db.session.add(product_tax)
        db.session.commit()
        
        return product_tax
    
    @staticmethod
    def get_all_tax_rates(active_only=True):
        """
        Get all tax rates.
        
        Args:
            active_only: Only return active tax rates
            
        Returns:
            list: List of tax rates
        """
        query = TaxRate.query
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        return query.order_by(TaxRate.created_at.desc()).all()

