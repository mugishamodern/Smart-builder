"""
Image upload routes for product images.

This module provides endpoints for uploading and managing
product images with validation and resizing.
"""
from flask import jsonify, request
from flask_login import login_required, current_user
from app.blueprints.api import api_bp
from app.models import Product, ProductImage
from app.extensions import db
from app.services.image_service import ImageService
from app.utils.error_handlers import handle_api_error, handle_not_found_error, handle_permission_error


@api_bp.route('/products/<int:product_id>/images', methods=['POST'])
@login_required
def upload_product_images(product_id):
    """
    Upload images for a product.
    
    Args:
        product_id: Product ID
        
    Returns:
        JSON response with uploaded images
    """
    try:
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return handle_not_found_error("Product")
        
        # Check permissions (shop owner only)
        if not current_user.is_shop_owner() or product.shop.owner_id != current_user.id:
            return handle_permission_error("Only shop owners can upload product images")
        
        # Check if files were uploaded
        if 'images' not in request.files:
            return jsonify({
                'error': 'Validation error',
                'message': 'No images provided'
            }), 400
        
        files = request.files.getlist('images')
        
        if not files or files[0].filename == '':
            return jsonify({
                'error': 'Validation error',
                'message': 'No images selected'
            }), 400
        
        # Validate and save images
        saved_images = []
        errors = []
        
        for i, file in enumerate(files):
            is_primary = (i == 0)  # First image is primary
            
            # Validate image
            is_valid, error_msg = ImageService.validate_image(file)
            if not is_valid:
                errors.append(f'Image {i + 1}: {error_msg}')
                continue
            
            # Save image
            product_image = ImageService.save_image(file, product_id, is_primary=is_primary)
            
            if product_image:
                product_image.display_order = i
                db.session.commit()
                saved_images.append({
                    'id': product_image.id,
                    'image_url': product_image.image_url,
                    'thumbnail_url': product_image.thumbnail_url,
                    'is_primary': product_image.is_primary,
                    'display_order': product_image.display_order
                })
            else:
                errors.append(f'Image {i + 1}: Failed to save')
        
        return jsonify({
            'message': f'Uploaded {len(saved_images)} image(s)',
            'images': saved_images,
            'errors': errors if errors else None
        }), 201 if saved_images else 400
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/products/<int:product_id>/images', methods=['GET'])
def get_product_images(product_id):
    """
    Get all images for a product.
    
    Args:
        product_id: Product ID
        
    Returns:
        JSON response with product images
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return handle_not_found_error("Product")
        
        images = ProductImage.query.filter_by(
            product_id=product_id
        ).order_by(ProductImage.display_order.asc()).all()
        
        images_data = [{
            'id': img.id,
            'image_url': img.image_url,
            'thumbnail_url': img.thumbnail_url,
            'is_primary': img.is_primary,
            'display_order': img.display_order,
            'created_at': img.created_at.isoformat()
        } for img in images]
        
        return jsonify({
            'images': images_data,
            'count': len(images_data)
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/products/<int:product_id>/images/<int:image_id>', methods=['DELETE'])
@login_required
def delete_product_image(product_id, image_id):
    """
    Delete a product image.
    
    Args:
        product_id: Product ID
        image_id: Image ID
        
    Returns:
        JSON response
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return handle_not_found_error("Product")
        
        # Check permissions
        if not current_user.is_shop_owner() or product.shop.owner_id != current_user.id:
            return handle_permission_error("Only shop owners can delete product images")
        
        product_image = ProductImage.query.filter_by(
            id=image_id,
            product_id=product_id
        ).first()
        
        if not product_image:
            return handle_not_found_error("Product image")
        
        # Delete image
        success = ImageService.delete_image(image_id)
        
        if not success:
            return jsonify({
                'error': 'Failed to delete image'
            }), 400
        
        return jsonify({
            'message': 'Image deleted successfully'
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/products/<int:product_id>/images/<int:image_id>/set-primary', methods=['POST'])
@login_required
def set_primary_image(product_id, image_id):
    """
    Set an image as primary.
    
    Args:
        product_id: Product ID
        image_id: Image ID
        
    Returns:
        JSON response
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return handle_not_found_error("Product")
        
        # Check permissions
        if not current_user.is_shop_owner() or product.shop.owner_id != current_user.id:
            return handle_permission_error("Only shop owners can set primary images")
        
        product_image = ProductImage.query.filter_by(
            id=image_id,
            product_id=product_id
        ).first()
        
        if not product_image:
            return handle_not_found_error("Product image")
        
        # Unset other primary images
        ProductImage.query.filter_by(
            product_id=product_id
        ).filter(
            ProductImage.id != image_id
        ).update({'is_primary': False})
        
        # Set this image as primary
        product_image.is_primary = True
        db.session.commit()
        
        return jsonify({
            'message': 'Primary image updated',
            'image': {
                'id': product_image.id,
                'is_primary': product_image.is_primary
            }
        }), 200
        
    except Exception as e:
        return handle_api_error(e)

