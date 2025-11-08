"""
Invoice API routes for PDF invoice generation.
"""
from flask import jsonify, send_file, request, current_app
from flask_login import login_required, current_user
from app.models import Order
from app.services.invoice_service import InvoiceService
from app.extensions import db
from app.blueprints.api import api_bp


@api_bp.route('/invoices/<int:order_id>', methods=['GET'])
@login_required
def generate_invoice(order_id):
    """
    Generate PDF invoice for an order.
    
    GET /api/invoices/<order_id>
    """
    order = Order.query.get_or_404(order_id)
    
    # Check if user has permission to view this invoice
    if not current_user.is_admin and order.customer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Generate invoice
        pdf_buffer = InvoiceService.generate_invoice(order_id)
        
        if not pdf_buffer:
            return jsonify({'error': 'Failed to generate invoice'}), 500
        
        # Return PDF
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'invoice_{order.order_number}.pdf'
        )
    except Exception as e:
        current_app.logger.error(f'Error generating invoice: {str(e)}')
        return jsonify({'error': 'Failed to generate invoice'}), 500


@api_bp.route('/invoices/<int:order_id>/download', methods=['GET'])
@login_required
def download_invoice(order_id):
    """
    Download invoice PDF for an order.
    
    GET /api/invoices/<order_id>/download
    """
    order = Order.query.get_or_404(order_id)
    
    # Check if user has permission to view this invoice
    if not current_user.is_admin and order.customer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Save invoice to file
        file_path = InvoiceService.save_invoice(order_id)
        
        if not file_path:
            return jsonify({'error': 'Failed to save invoice'}), 500
        
        # Return file path or send file
        return jsonify({
            'message': 'Invoice generated successfully',
            'file_path': file_path
        })
    except Exception as e:
        current_app.logger.error(f'Error saving invoice: {str(e)}')
        return jsonify({'error': 'Failed to save invoice'}), 500

