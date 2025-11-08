"""
Coupon/Discount service for managing coupons and discounts.

This module provides functionality for validating, applying,
and managing coupons and discounts.
"""
from datetime import datetime
from decimal import Decimal
from app.extensions import db
from app.models import Coupon, CouponUsage, Order, OrderItem, Product


class CouponService:
    """Service for coupon management"""
    
    @staticmethod
    def validate_coupon(code, user_id, order_amount=None, order_items=None):
        """
        Validate a coupon code.
        
        Args:
            code: Coupon code
            user_id: User ID
            order_amount: Order amount (optional)
            order_items: List of order items (optional)
            
        Returns:
            tuple: (is_valid, error_message, coupon)
        """
        coupon = Coupon.query.filter_by(code=code.upper().strip()).first()
        
        if not coupon:
            return False, 'Invalid coupon code', None
        
        # Check if coupon is valid
        is_valid, error_msg = coupon.is_valid(order_amount)
        if not is_valid:
            return False, error_msg, coupon
        
        # Check if coupon applies to order items
        if order_items and coupon.applicable_to != 'all':
            if coupon.applicable_to == 'products':
                product_ids = [item.product_id for item in order_items]
                if not any(pid in (coupon.applicable_ids or []) for pid in product_ids):
                    return False, 'Coupon does not apply to items in this order', coupon
            elif coupon.applicable_to == 'categories':
                category_ids = [item.product.category_id for item in order_items if item.product.category_id]
                if not any(cid in (coupon.applicable_ids or []) for cid in category_ids):
                    return False, 'Coupon does not apply to categories in this order', coupon
            elif coupon.applicable_to == 'shops':
                shop_ids = list(set([item.product.shop_id for item in order_items]))
                if not any(sid in (coupon.applicable_ids or []) for sid in shop_ids):
                    return False, 'Coupon does not apply to shops in this order', coupon
        
        return True, None, coupon
    
    @staticmethod
    def apply_coupon(order_id, coupon_code):
        """
        Apply coupon to an order.
        
        Args:
            order_id: Order ID
            coupon_code: Coupon code
            
        Returns:
            tuple: (success, error_message, discount_amount)
        """
        order = Order.query.get(order_id)
        if not order:
            return False, 'Order not found', None
        
        # Validate coupon
        is_valid, error_msg, coupon = CouponService.validate_coupon(
            coupon_code,
            order.customer_id,
            float(order.total_amount),
            order.items
        )
        
        if not is_valid:
            return False, error_msg, None
        
        # Calculate discount
        discount_amount = coupon.calculate_discount(order.total_amount)
        
        # Apply discount to order
        order.discount_amount = discount_amount
        order.coupon_code = coupon.code
        
        # Recalculate order total (subtotal - discount + tax)
        if not order.subtotal_amount:
            order.subtotal_amount = order.total_amount
        
        order.total_amount = order.subtotal_amount - discount_amount + (order.tax_amount or Decimal('0.00'))
        
        # Mark coupon as used
        coupon.apply()
        
        # Record coupon usage
        coupon_usage = CouponUsage(
            coupon_id=coupon.id,
            order_id=order_id,
            user_id=order.customer_id,
            discount_amount=discount_amount
        )
        db.session.add(coupon_usage)
        db.session.commit()
        
        return True, None, discount_amount
    
    @staticmethod
    def create_coupon(code, discount_type, discount_value, valid_from=None, valid_until=None,
                     min_order_amount=None, max_discount_amount=None, usage_limit=None,
                     applicable_to='all', applicable_ids=None, created_by=None):
        """
        Create a new coupon.
        
        Args:
            code: Coupon code
            discount_type: Type (percentage or fixed)
            discount_value: Discount value
            valid_from: Valid from date
            valid_until: Valid until date
            min_order_amount: Minimum order amount
            max_discount_amount: Maximum discount (for percentage)
            usage_limit: Usage limit
            applicable_to: Where coupon applies
            applicable_ids: Applicable IDs
            created_by: User ID who created
            
        Returns:
            Coupon: Created coupon
        """
        coupon = Coupon(
            code=code.upper().strip(),
            discount_type=discount_type,
            discount_value=Decimal(str(discount_value)),
            min_order_amount=Decimal(str(min_order_amount)) if min_order_amount else None,
            max_discount_amount=Decimal(str(max_discount_amount)) if max_discount_amount else None,
            usage_limit=usage_limit,
            valid_from=valid_from or datetime.utcnow(),
            valid_until=valid_until,
            applicable_to=applicable_to,
            applicable_ids=applicable_ids or [],
            created_by=created_by
        )
        
        db.session.add(coupon)
        db.session.commit()
        
        return coupon
    
    @staticmethod
    def get_user_coupons(user_id):
        """
        Get coupons used by a user.
        
        Args:
            user_id: User ID
            
        Returns:
            list: List of coupon usages
        """
        return CouponUsage.query.filter_by(user_id=user_id).order_by(
            CouponUsage.created_at.desc()
        ).all()
    
    @staticmethod
    def get_coupon_stats(coupon_id):
        """
        Get coupon statistics.
        
        Args:
            coupon_id: Coupon ID
            
        Returns:
            dict: Coupon statistics
        """
        coupon = Coupon.query.get(coupon_id)
        if not coupon:
            return None
        
        usages = CouponUsage.query.filter_by(coupon_id=coupon_id).all()
        total_discount = sum(usage.discount_amount for usage in usages)
        
        return {
            'coupon_id': coupon.id,
            'code': coupon.code,
            'usage_count': coupon.usage_count,
            'usage_limit': coupon.usage_limit,
            'total_discount_given': float(total_discount),
            'average_discount': float(total_discount / len(usages)) if usages else 0,
            'is_active': coupon.is_active,
            'is_valid': coupon.is_valid()[0]
        }

