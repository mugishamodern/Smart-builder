"""
Invoice generation service using ReportLab.

This module provides functionality for generating PDF invoices
for orders with detailed itemization, tax, and discount information.
"""
from io import BytesIO
from datetime import datetime
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from flask import current_app
from app.models import Order, OrderItem


class InvoiceService:
    """Service for generating PDF invoices"""
    
    @staticmethod
    def generate_invoice(order_id):
        """
        Generate PDF invoice for an order.
        
        Args:
            order_id: Order ID
            
        Returns:
            BytesIO: PDF file buffer
        """
        order = Order.query.get(order_id)
        if not order:
            return None
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Header
        elements.append(Paragraph("BuildSmart", title_style))
        elements.append(Paragraph("INVOICE", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Invoice details
        invoice_data = [
            ['Invoice Number:', order.order_number],
            ['Invoice Date:', order.created_at.strftime('%B %d, %Y')],
            ['Order Date:', order.created_at.strftime('%B %d, %Y')],
        ]
        
        invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
        invoice_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(invoice_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Customer and Shop information
        customer_data = [
            ['Bill To:', 'Ship From:'],
            [order.customer.full_name or order.customer.username, order.shop.name],
            [order.customer.email, order.shop.address or ''],
            [order.delivery_address or '', order.shop.phone or ''],
        ]
        
        customer_table = Table(customer_data, colWidths=[3*inch, 3*inch])
        customer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(customer_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Order items
        items_data = [['Item', 'Quantity', 'Unit Price', 'Total']]
        
        # Calculate subtotal from items if not set
        if order.subtotal_amount:
            subtotal = order.subtotal_amount
        else:
            subtotal = Decimal('0.00')
            for item in order.items:
                subtotal += item.total_price
        
        for item in order.items:
            items_data.append([
                item.product.name,
                str(item.quantity),
                f"₦{item.unit_price:.2f}",
                f"₦{item.total_price:.2f}"
            ])
        
        # Add discount if any
        discount = order.discount_amount or Decimal('0.00')
        
        # Add tax if any
        tax = order.tax_amount or Decimal('0.00')
        
        # Calculate totals
        total_before_tax = subtotal - discount
        total = total_before_tax + tax
        
        items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary
        summary_data = [
            ['Subtotal:', f"₦{subtotal:.2f}"],
        ]
        
        if discount > 0:
            summary_data.append(['Discount:', f"-₦{discount:.2f}"])
        
        if tax > 0:
            summary_data.append(['Tax:', f"₦{tax:.2f}"])
        
        summary_data.append(['Total:', f"₦{total:.2f}"])
        
        summary_table = Table(summary_data, colWidths=[4*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
            ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTSIZE', (-1, -1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Payment information
        payment_data = [
            ['Payment Status:', order.payment_status.upper()],
            ['Payment Method:', order.payment_method or 'N/A'],
        ]
        
        if order.payment:
            payment_data.append(['Transaction ID:', order.payment.transaction_id])
            if order.payment.paid_at:
                payment_data.append(['Paid At:', order.payment.paid_at.strftime('%B %d, %Y %I:%M %p')])
        
        payment_table = Table(payment_data, colWidths=[2*inch, 3*inch])
        payment_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(payment_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Thank you for your business!", footer_style))
        elements.append(Paragraph("BuildSmart - Your Trusted Construction Materials Partner", footer_style))
        
        # Build PDF
        doc.build(elements)
        
        # Reset buffer position
        buffer.seek(0)
        
        return buffer
    
    @staticmethod
    def save_invoice(order_id, file_path=None):
        """
        Save invoice PDF to file.
        
        Args:
            order_id: Order ID
            file_path: File path (optional, generates if not provided)
            
        Returns:
            str: File path to saved invoice
        """
        buffer = InvoiceService.generate_invoice(order_id)
        if not buffer:
            return None
        
        if not file_path:
            from flask import current_app
            import os
            invoice_folder = os.path.join(
                current_app.config.get('UPLOAD_FOLDER', 'uploads'),
                'invoices'
            )
            os.makedirs(invoice_folder, exist_ok=True)
            
            order = Order.query.get(order_id)
            filename = f"invoice_{order.order_number}_{datetime.utcnow().strftime('%Y%m%d')}.pdf"
            file_path = os.path.join(invoice_folder, filename)
        
        # Write buffer to file
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())
        
        return file_path

