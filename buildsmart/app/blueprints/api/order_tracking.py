"""
Order tracking routes with detailed status timeline.

This module provides endpoints for tracking order status
with detailed timeline and status updates.
"""
from flask import jsonify, request
from flask_login import login_required, current_user
from app.blueprints.api import api_bp
from app.models import Order, OrderStatus, OrderItem
from app.extensions import db
from app.utils.error_handlers import handle_api_error, handle_not_found_error
from app.services.notification_service import NotificationService
from datetime import datetime


@api_bp.route('/orders/<int:order_id>/track', methods=['GET'])
@login_required
def track_order(order_id):
    """
    Get detailed order tracking information.
    
    Args:
        order_id: Order ID
        
    Returns:
        JSON response with order tracking details
    """
    try:
        order = Order.query.get(order_id)
        
        if not order:
            return handle_not_found_error("Order")
        
        # Check permissions
        if order.customer_id != current_user.id and not current_user.is_shop_owner():
            return jsonify({
                'error': 'Unauthorized',
                'message': 'You do not have permission to view this order'
            }), 403
        
        # Get status history
        status_history = OrderStatus.query.filter_by(
            order_id=order_id
        ).order_by(OrderStatus.created_at.asc()).all()
        
        # Build timeline
        timeline = []
        for status in status_history:
            timeline.append({
                'status': status.status,
                'notes': status.notes,
                'created_at': status.created_at.isoformat(),
                'created_by': {
                    'id': status.creator.id if status.creator else None,
                    'name': status.creator.full_name if status.creator else 'System'
                } if status.creator else None
            })
        
        # Add current status
        current_status = {
            'status': order.status,
            'created_at': order.updated_at.isoformat() if order.updated_at else order.created_at.isoformat(),
            'is_current': True
        }
        
        # Get order items
        items = OrderItem.query.filter_by(order_id=order_id).all()
        items_data = [{
            'id': item.id,
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'image_url': item.product.image_url
            },
            'quantity': item.quantity,
            'unit_price': float(item.unit_price),
            'total_price': float(item.total_price)
        } for item in items]
        
        return jsonify({
            'order': {
                'id': order.id,
                'order_number': order.order_number,
                'status': order.status,
                'payment_status': order.payment_status,
                'total_amount': float(order.total_amount),
                'delivery_address': order.delivery_address,
                'delivery_notes': order.delivery_notes,
                'created_at': order.created_at.isoformat(),
                'updated_at': order.updated_at.isoformat() if order.updated_at else None,
                'items': items_data
            },
            'timeline': timeline,
            'current_status': current_status
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
def update_order_status(order_id):
    """
    Update order status (for shop owners).
    
    Args:
        order_id: Order ID
        
    Returns:
        JSON response
    """
    try:
        order = Order.query.get(order_id)
        
        if not order:
            return handle_not_found_error("Order")
        
        # Check permissions (shop owner only)
        if not current_user.is_shop_owner() or order.shop.owner_id != current_user.id:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Only shop owners can update order status'
            }), 403
        
        # Get request data
        data = request.get_json() or {}
        new_status = data.get('status')
        notes = data.get('notes', '')
        
        if not new_status:
            return jsonify({
                'error': 'Validation error',
                'message': 'Status is required'
            }), 400
        
        # Validate status
        valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({
                'error': 'Validation error',
                'message': f'Invalid status. Valid statuses: {", ".join(valid_statuses)}'
            }), 400
        
        # Update order status
        order.status = new_status
        order.updated_at = datetime.utcnow()
        
        # Create status history entry
        status_entry = OrderStatus(
            order_id=order_id,
            status=new_status,
            notes=notes,
            created_by=current_user.id
        )
        
        db.session.add(status_entry)
        db.session.commit()
        
        # Send notification to customer
        NotificationService.notify_order_status(order, new_status, notes)
        
        return jsonify({
            'message': 'Order status updated',
            'order': {
                'id': order.id,
                'status': order.status,
                'updated_at': order.updated_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return handle_api_error(e)

