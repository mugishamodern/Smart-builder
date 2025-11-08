"""
Wishlist routes for managing user favorites.

This module provides endpoints for users to add, remove,
and view their favorite products.
"""
from flask import jsonify, request
from flask_login import login_required, current_user
from app.blueprints.wishlist import wishlist_bp
from app.models import Wishlist, Product
from app.extensions import db
from app.utils.error_handlers import handle_api_error, handle_validation_error, handle_not_found_error


@wishlist_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    """
    Add product to wishlist.
    
    Args:
        product_id: Product ID to add
        
    Returns:
        JSON response
    """
    try:
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return handle_not_found_error("Product")
        
        # Check if already in wishlist
        existing = Wishlist.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if existing:
            return jsonify({
                'message': 'Product already in wishlist',
                'wishlist_item': {
                    'id': existing.id,
                    'product_id': existing.product_id,
                    'created_at': existing.created_at.isoformat()
                }
            }), 200
        
        # Add to wishlist
        wishlist_item = Wishlist(
            user_id=current_user.id,
            product_id=product_id
        )
        
        db.session.add(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Product added to wishlist',
            'wishlist_item': {
                'id': wishlist_item.id,
                'product_id': wishlist_item.product_id,
                'created_at': wishlist_item.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        return handle_api_error(e)


@wishlist_bp.route('/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_wishlist(product_id):
    """
    Remove product from wishlist.
    
    Args:
        product_id: Product ID to remove
        
    Returns:
        JSON response
    """
    try:
        wishlist_item = Wishlist.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if not wishlist_item:
            return handle_not_found_error("Wishlist item")
        
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Product removed from wishlist'
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@wishlist_bp.route('/list', methods=['GET'])
@login_required
def get_wishlist():
    """
    Get user's wishlist.
    
    Returns:
        JSON response with wishlist items
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        wishlist_items = Wishlist.query.filter_by(
            user_id=current_user.id
        ).order_by(
            Wishlist.created_at.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        items_data = []
        for item in wishlist_items.items:
            product = item.product
            items_data.append({
                'id': item.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': float(product.price),
                    'unit': product.unit,
                    'quantity_available': product.quantity_available,
                    'image_url': product.image_url,
                    'brand': product.brand,
                    'is_available': product.is_available
                },
                'added_at': item.created_at.isoformat()
            })
        
        return jsonify({
            'wishlist': items_data,
            'total': wishlist_items.total,
            'page': page,
            'per_page': per_page,
            'pages': wishlist_items.pages
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@wishlist_bp.route('/check/<int:product_id>', methods=['GET'])
@login_required
def check_wishlist(product_id):
    """
    Check if product is in wishlist.
    
    Args:
        product_id: Product ID to check
        
    Returns:
        JSON response with wishlist status
    """
    try:
        wishlist_item = Wishlist.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        return jsonify({
            'in_wishlist': wishlist_item is not None,
            'wishlist_item_id': wishlist_item.id if wishlist_item else None
        }), 200
        
    except Exception as e:
        return handle_api_error(e)

