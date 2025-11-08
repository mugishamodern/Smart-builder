"""
Coupon API routes for discount/coupon management.
"""
from flask import jsonify, request, current_app
from flask_login import login_required, current_user
from datetime import datetime
from decimal import Decimal
from app.models import Coupon, CouponUsage, Order
from app.services.coupon_service import CouponService
from app.extensions import db
from app.blueprints.api import api_bp


@api_bp.route('/coupons/validate', methods=['POST'])
@login_required
def validate_coupon():
    """
    Validate a coupon code.
    
    POST /api/coupons/validate
    Body: { "code": "COUPON123", "order_amount": 1000 }
    """
    data = request.get_json()
    code = data.get('code')
    order_amount = data.get('order_amount')
    
    if not code:
        return jsonify({'error': 'Coupon code is required'}), 400
    
    try:
        is_valid, error_msg, coupon = CouponService.validate_coupon(
            code,
            current_user.id,
            order_amount
        )
        
        if not is_valid:
            return jsonify({
                'valid': False,
                'error': error_msg
            }), 400
        
        discount_amount = coupon.calculate_discount(Decimal(str(order_amount or 0)))
        
        return jsonify({
            'valid': True,
            'coupon': {
                'id': coupon.id,
                'code': coupon.code,
                'discount_type': coupon.discount_type,
                'discount_value': float(coupon.discount_value),
                'discount_amount': float(discount_amount)
            }
        })
    except Exception as e:
        current_app.logger.error(f'Error validating coupon: {str(e)}')
        return jsonify({'error': 'Failed to validate coupon'}), 500


@api_bp.route('/coupons/apply', methods=['POST'])
@login_required
def apply_coupon():
    """
    Apply coupon to an order.
    
    POST /api/coupons/apply
    Body: { "order_id": 1, "code": "COUPON123" }
    """
    data = request.get_json()
    order_id = data.get('order_id')
    code = data.get('code')
    
    if not order_id or not code:
        return jsonify({'error': 'Order ID and coupon code are required'}), 400
    
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    if order.customer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        success, error_msg, discount_amount = CouponService.apply_coupon(order_id, code)
        
        if not success:
            return jsonify({'error': error_msg}), 400
        
        # Update order totals
        order.discount_amount = discount_amount
        order.coupon_code = code
        order.total_amount = order.subtotal_amount - discount_amount + order.tax_amount
        db.session.commit()
        
        return jsonify({
            'message': 'Coupon applied successfully',
            'discount_amount': float(discount_amount),
            'new_total': float(order.total_amount)
        })
    except Exception as e:
        current_app.logger.error(f'Error applying coupon: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to apply coupon'}), 500


@api_bp.route('/coupons', methods=['GET'])
@login_required
def get_coupons():
    """
    Get all coupons (admin only).
    
    GET /api/coupons
    """
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        coupons = Coupon.query.order_by(Coupon.created_at.desc()).all()
        
        return jsonify({
            'coupons': [{
                'id': c.id,
                'code': c.code,
                'discount_type': c.discount_type,
                'discount_value': float(c.discount_value),
                'min_order_amount': float(c.min_order_amount) if c.min_order_amount else None,
                'max_discount_amount': float(c.max_discount_amount) if c.max_discount_amount else None,
                'usage_limit': c.usage_limit,
                'usage_count': c.usage_count,
                'valid_from': c.valid_from.isoformat(),
                'valid_until': c.valid_until.isoformat() if c.valid_until else None,
                'is_active': c.is_active,
                'applicable_to': c.applicable_to,
                'applicable_ids': c.applicable_ids
            } for c in coupons]
        })
    except Exception as e:
        current_app.logger.error(f'Error getting coupons: {str(e)}')
        return jsonify({'error': 'Failed to get coupons'}), 500


@api_bp.route('/coupons', methods=['POST'])
@login_required
def create_coupon():
    """
    Create a new coupon (admin only).
    
    POST /api/coupons
    Body: { "code": "COUPON123", "discount_type": "percentage", ... }
    """
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    try:
        coupon = CouponService.create_coupon(
            code=data.get('code'),
            discount_type=data.get('discount_type'),
            discount_value=data.get('discount_value'),
            valid_from=datetime.fromisoformat(data.get('valid_from')) if data.get('valid_from') else None,
            valid_until=datetime.fromisoformat(data.get('valid_until')) if data.get('valid_until') else None,
            min_order_amount=data.get('min_order_amount'),
            max_discount_amount=data.get('max_discount_amount'),
            usage_limit=data.get('usage_limit'),
            applicable_to=data.get('applicable_to', 'all'),
            applicable_ids=data.get('applicable_ids'),
            created_by=current_user.id
        )
        
        return jsonify({
            'message': 'Coupon created successfully',
            'coupon': {
                'id': coupon.id,
                'code': coupon.code,
                'discount_type': coupon.discount_type,
                'discount_value': float(coupon.discount_value)
            }
        }), 201
    except Exception as e:
        current_app.logger.error(f'Error creating coupon: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to create coupon'}), 500


@api_bp.route('/coupons/my-coupons', methods=['GET'])
@login_required
def get_my_coupons():
    """
    Get coupons used by current user.
    
    GET /api/coupons/my-coupons
    """
    try:
        usages = CouponService.get_user_coupons(current_user.id)
        
        return jsonify({
            'coupon_usages': [{
                'id': u.id,
                'coupon_code': u.coupon.code,
                'discount_amount': float(u.discount_amount),
                'order_id': u.order_id,
                'created_at': u.created_at.isoformat()
            } for u in usages]
        })
    except Exception as e:
        current_app.logger.error(f'Error getting user coupons: {str(e)}')
        return jsonify({'error': 'Failed to get coupons'}), 500

