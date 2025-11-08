"""
Stock notification routes for product availability alerts.

This module provides endpoints for users to subscribe to
stock notifications for out-of-stock products.
"""
from flask import jsonify, request
from flask_login import login_required, current_user
from app.blueprints.api import api_bp
from app.models import StockNotification, Product
from app.extensions import db
from app.services.stock_notification_service import StockNotificationService
from app.utils.error_handlers import handle_api_error, handle_not_found_error


@api_bp.route('/products/<int:product_id>/notify-stock', methods=['POST'])
@login_required
def subscribe_stock_notification(product_id):
    """
    Subscribe to stock notification for a product.
    
    Args:
        product_id: Product ID
        
    Returns:
        JSON response
    """
    try:
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return handle_not_found_error("Product")
        
        # Check if product is already in stock
        if product.is_in_stock():
            return jsonify({
                'message': 'Product is already in stock',
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'quantity_available': product.quantity_available
                }
            }), 200
        
        # Create notification
        notification = StockNotificationService.create_notification(
            current_user.id,
            product_id
        )
        
        if not notification:
            return jsonify({
                'error': 'Failed to create notification'
            }), 400
        
        return jsonify({
            'message': 'You will be notified when this product is back in stock',
            'notification': {
                'id': notification.id,
                'product_id': notification.product_id,
                'created_at': notification.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/products/<int:product_id>/notify-stock', methods=['DELETE'])
@login_required
def unsubscribe_stock_notification(product_id):
    """
    Unsubscribe from stock notification for a product.
    
    Args:
        product_id: Product ID
        
    Returns:
        JSON response
    """
    try:
        success = StockNotificationService.remove_notification(
            current_user.id,
            product_id
        )
        
        if not success:
            return handle_not_found_error("Stock notification")
        
        return jsonify({
            'message': 'Stock notification removed'
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/notifications/stock', methods=['GET'])
@login_required
def get_stock_notifications():
    """
    Get user's stock notifications.
    
    Returns:
        JSON response with stock notifications
    """
    try:
        notifications = StockNotification.query.filter_by(
            user_id=current_user.id,
            notified=False
        ).order_by(StockNotification.created_at.desc()).all()
        
        notifications_data = []
        for notification in notifications:
            product = notification.product
            notifications_data.append({
                'id': notification.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'image_url': product.image_url,
                    'price': float(product.price),
                    'quantity_available': product.quantity_available,
                    'is_available': product.is_available
                },
                'created_at': notification.created_at.isoformat()
            })
        
        return jsonify({
            'notifications': notifications_data,
            'count': len(notifications_data)
        }), 200
        
    except Exception as e:
        return handle_api_error(e)

