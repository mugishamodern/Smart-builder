"""
Inventory management API routes with low-stock alerts.

This module provides endpoints for managing inventory
and viewing low-stock alerts.
"""
from flask import jsonify, request
from flask_login import login_required, current_user
from app.blueprints.api import api_bp
from app.models import Product, Shop, InventoryAlert
from app.extensions import db
from app.services.inventory_service import InventoryService
from app.utils.error_handlers import handle_api_error, handle_not_found_error, handle_permission_error


@api_bp.route('/shops/<int:shop_id>/inventory/alerts', methods=['GET'])
@login_required
def get_inventory_alerts(shop_id):
    """
    Get inventory alerts for a shop.
    
    Args:
        shop_id: Shop ID
        
    Returns:
        JSON response with inventory alerts
    """
    try:
        shop = Shop.query.get(shop_id)
        if not shop:
            return handle_not_found_error("Shop")
        
        # Check permissions (shop owner only)
        if not current_user.is_shop_owner() or shop.owner_id != current_user.id:
            return handle_permission_error("Only shop owners can view inventory alerts")
        
        status = request.args.get('status', 'active')  # active or all
        
        alerts = InventoryService.get_alerts(shop_id, status)
        
        alerts_data = []
        for alert in alerts:
            alerts_data.append({
                'id': alert.id,
                'product': {
                    'id': alert.product.id,
                    'name': alert.product.name,
                    'quantity_available': alert.product.quantity_available
                },
                'threshold': alert.threshold,
                'current_quantity': alert.current_quantity,
                'alert_type': alert.alert_type,
                'notified': alert.notified,
                'notified_at': alert.notified_at.isoformat() if alert.notified_at else None,
                'created_at': alert.created_at.isoformat(),
                'resolved_at': alert.resolved_at.isoformat() if alert.resolved_at else None
            })
        
        return jsonify({
            'alerts': alerts_data,
            'count': len(alerts_data)
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/products/<int:product_id>/check-stock', methods=['POST'])
@login_required
def check_product_stock(product_id):
    """
    Check product stock and create alert if needed.
    
    Args:
        product_id: Product ID
        
    Returns:
        JSON response
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return handle_not_found_error("Product")
        
        # Check permissions
        if not current_user.is_shop_owner() or product.shop.owner_id != current_user.id:
            return handle_permission_error("Only shop owners can check stock")
        
        threshold = request.json.get('threshold') if request.json else None
        
        alert = InventoryService.check_low_stock(product_id, threshold)
        
        if alert:
            return jsonify({
                'message': 'Stock alert created',
                'alert': {
                    'id': alert.id,
                    'alert_type': alert.alert_type,
                    'current_quantity': alert.current_quantity,
                    'threshold': alert.threshold
                }
            }), 201
        else:
            return jsonify({
                'message': 'Product stock is normal',
                'product': {
                    'id': product.id,
                    'quantity_available': product.quantity_available
                }
            }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/shops/<int:shop_id>/inventory/check-all', methods=['POST'])
@login_required
def check_all_products(shop_id):
    """
    Check all products in a shop for low stock.
    
    Args:
        shop_id: Shop ID
        
    Returns:
        JSON response
    """
    try:
        shop = Shop.query.get(shop_id)
        if not shop:
            return handle_not_found_error("Shop")
        
        # Check permissions
        if not current_user.is_shop_owner() or shop.owner_id != current_user.id:
            return handle_permission_error("Only shop owners can check inventory")
        
        alerts = InventoryService.check_all_products(shop_id)
        
        return jsonify({
            'message': f'Checked all products. Found {len(alerts)} alerts.',
            'alerts_count': len(alerts),
            'alerts': [{
                'id': alert.id,
                'product_id': alert.product_id,
                'alert_type': alert.alert_type,
                'current_quantity': alert.current_quantity
            } for alert in alerts]
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/inventory/alerts/<int:alert_id>/resolve', methods=['POST'])
@login_required
def resolve_inventory_alert(alert_id):
    """
    Resolve an inventory alert.
    
    Args:
        alert_id: Alert ID
        
    Returns:
        JSON response
    """
    try:
        alert = InventoryAlert.query.get(alert_id)
        if not alert:
            return handle_not_found_error("Inventory alert")
        
        # Check permissions
        if not current_user.is_shop_owner() or alert.shop.owner_id != current_user.id:
            return handle_permission_error("Only shop owners can resolve alerts")
        
        success = InventoryService.resolve_alert(alert_id)
        
        if success:
            return jsonify({
                'message': 'Alert resolved successfully'
            }), 200
        else:
            return jsonify({
                'error': 'Failed to resolve alert'
            }), 400
        
    except Exception as e:
        return handle_api_error(e)

