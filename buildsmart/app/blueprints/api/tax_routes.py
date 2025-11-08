"""
Tax API routes for tax calculation and management.
"""
from flask import jsonify, request, current_app
from flask_login import login_required, current_user
from decimal import Decimal
from app.models import TaxRate, ProductTax, Product, Order
from app.services.tax_service import TaxService
from app.extensions import db
from app.blueprints.api import api_bp


@api_bp.route('/tax/calculate/<int:order_id>', methods=['GET'])
@login_required
def calculate_order_tax(order_id):
    """
    Calculate tax for an order.
    
    GET /api/tax/calculate/<order_id>
    """
    order = Order.query.get_or_404(order_id)
    
    # Check if user has permission
    if not current_user.is_admin and order.customer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        total_tax, tax_breakdown = TaxService.calculate_order_tax(order_id)
        
        # Update order tax
        order.tax_amount = total_tax
        order.total_amount = order.subtotal_amount - order.discount_amount + total_tax
        db.session.commit()
        
        return jsonify({
            'total_tax': float(total_tax),
            'tax_breakdown': {k: float(v) for k, v in tax_breakdown.items()},
            'new_total': float(order.total_amount)
        })
    except Exception as e:
        current_app.logger.error(f'Error calculating tax: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to calculate tax'}), 500


@api_bp.route('/tax/product/<int:product_id>', methods=['GET'])
@login_required
def get_product_tax(product_id):
    """
    Get tax rate for a product.
    
    GET /api/tax/product/<product_id>
    """
    product = Product.query.get_or_404(product_id)
    
    try:
        tax_rate = TaxService.get_product_tax_rate(product_id)
        
        if not tax_rate:
            return jsonify({
                'tax_rate': None,
                'message': 'No tax rate configured for this product'
            })
        
        return jsonify({
            'tax_rate': {
                'id': tax_rate.id,
                'name': tax_rate.name,
                'rate': float(tax_rate.rate),
                'tax_type': tax_rate.tax_type
            }
        })
    except Exception as e:
        current_app.logger.error(f'Error getting product tax: {str(e)}')
        return jsonify({'error': 'Failed to get product tax'}), 500


@api_bp.route('/tax/rates', methods=['GET'])
@login_required
def get_tax_rates():
    """
    Get all tax rates.
    
    GET /api/tax/rates
    """
    try:
        tax_rates = TaxService.get_all_tax_rates(active_only=True)
        
        return jsonify({
            'tax_rates': [{
                'id': tr.id,
                'name': tr.name,
                'rate': float(tr.rate),
                'tax_type': tr.tax_type,
                'applicable_to': tr.applicable_to,
                'applicable_ids': tr.applicable_ids,
                'is_active': tr.is_active
            } for tr in tax_rates]
        })
    except Exception as e:
        current_app.logger.error(f'Error getting tax rates: {str(e)}')
        return jsonify({'error': 'Failed to get tax rates'}), 500


@api_bp.route('/tax/rates', methods=['POST'])
@login_required
def create_tax_rate():
    """
    Create a new tax rate (admin only).
    
    POST /api/tax/rates
    Body: { "name": "VAT", "rate": 15.0, "tax_type": "vat", ... }
    """
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    try:
        tax_rate = TaxService.create_tax_rate(
            name=data.get('name'),
            rate=data.get('rate'),
            tax_type=data.get('tax_type', 'vat'),
            applicable_to=data.get('applicable_to', 'all'),
            applicable_ids=data.get('applicable_ids')
        )
        
        return jsonify({
            'message': 'Tax rate created successfully',
            'tax_rate': {
                'id': tax_rate.id,
                'name': tax_rate.name,
                'rate': float(tax_rate.rate),
                'tax_type': tax_rate.tax_type
            }
        }), 201
    except Exception as e:
        current_app.logger.error(f'Error creating tax rate: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to create tax rate'}), 500


@api_bp.route('/tax/product/<int:product_id>', methods=['POST'])
@login_required
def assign_product_tax(product_id):
    """
    Assign tax rate to a product (admin/shop owner only).
    
    POST /api/tax/product/<product_id>
    Body: { "tax_rate_id": 1 }
    """
    product = Product.query.get_or_404(product_id)
    
    # Check if user has permission
    if not current_user.is_admin and product.shop.owner_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    tax_rate_id = data.get('tax_rate_id')
    
    if not tax_rate_id:
        return jsonify({'error': 'Tax rate ID is required'}), 400
    
    try:
        product_tax = TaxService.assign_product_tax(product_id, tax_rate_id)
        
        return jsonify({
            'message': 'Tax rate assigned successfully',
            'product_tax': {
                'id': product_tax.id,
                'product_id': product_tax.product_id,
                'tax_rate_id': product_tax.tax_rate_id
            }
        }), 201
    except Exception as e:
        current_app.logger.error(f'Error assigning product tax: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to assign tax rate'}), 500

