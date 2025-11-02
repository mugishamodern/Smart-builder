"""
Payment Service for handling payment processing and escrow management.
"""

from datetime import datetime
from decimal import Decimal
from app.models import Payment, Order
from app.extensions import db
from app.utils.helpers import generate_transaction_id


class PaymentService:
    """Service class for payment processing and escrow management."""
    
    @staticmethod
    def initiate_payment(order_id, payment_method, amount):
        """
        Initiate a payment for an order.
        
        This simulates the payment process and creates a payment record.
        In production, this would integrate with a real payment gateway.
        
        Args:
            order_id: Order ID for the payment
            payment_method: Payment method (mobile_money, bank_transfer, cash)
            amount: Payment amount
        
        Returns:
            Payment: Created payment object
        """
        order = Order.query.get_or_404(order_id)
        
        # Check if payment already exists
        existing_payment = Payment.query.filter_by(order_id=order_id).first()
        if existing_payment:
            raise ValueError("Payment already exists for this order")
        
        # Generate unique transaction ID
        transaction_id = generate_transaction_id()
        
        # Simulate payment verification (in production, this would call the gateway)
        # For now, we'll auto-approve all payments
        is_paid = True
        paid_at = datetime.utcnow() if is_paid else None
        
        # Create payment record
        payment = Payment(
            order_id=order_id,
            amount=Decimal(str(amount)),
            payment_method=payment_method,
            transaction_id=transaction_id,
            status=Payment.STATUS_HELD_BY_ADMIN if is_paid else Payment.STATUS_PENDING_ADMIN,
            paid_at=paid_at
        )
        
        db.session.add(payment)
        
        # Update order payment status
        order.payment_status = 'paid'
        order.payment_method = payment_method
        
        db.session.commit()
        
        return payment
    
    @staticmethod
    def verify_payment(transaction_id):
        """
        Verify a payment transaction.
        
        This simulates payment verification. In production, this would
        check with the payment gateway.
        
        Args:
            transaction_id: Transaction ID to verify
        
        Returns:
            tuple: (is_verified: bool, payment: Payment)
        """
        payment = Payment.query.filter_by(transaction_id=transaction_id).first_or_404()
        
        # Simulate verification - in production, check with payment gateway
        if payment.paid_at is None:
            payment.paid_at = datetime.utcnow()
            payment.status = Payment.STATUS_HELD_BY_ADMIN
            db.session.commit()
        
        return True, payment
    
    @staticmethod
    def hold_in_escrow(payment_id):
        """
        Move payment to admin escrow.
        
        This is typically done automatically after verification,
        but can be called manually if needed.
        
        Args:
            payment_id: Payment ID
        
        Returns:
            Payment: Updated payment object
        """
        payment = Payment.query.get_or_404(payment_id)
        
        if payment.status != Payment.STATUS_PENDING_ADMIN:
            raise ValueError(f"Payment cannot be held in escrow. Current status: {payment.status}")
        
        payment.status = Payment.STATUS_HELD_BY_ADMIN
        db.session.commit()
        
        return payment
    
    @staticmethod
    def release_to_shop(payment_id, admin_id=None, notes=None):
        """
        Release payment from escrow to shop.
        
        Args:
            payment_id: Payment ID
            admin_id: Admin user ID who released the payment
            notes: Admin notes on the release
        
        Returns:
            Payment: Updated payment object
        """
        payment = Payment.query.get_or_404(payment_id)
        
        if payment.status != Payment.STATUS_HELD_BY_ADMIN:
            raise ValueError(f"Payment cannot be released. Current status: {payment.status}")
        
        payment.status = Payment.STATUS_RELEASED_TO_SHOP
        payment.released_at = datetime.utcnow()
        payment.admin_notes = notes
        
        # Update order status
        payment.order.status = 'confirmed'
        payment.order.admin_notes = notes
        
        db.session.commit()
        
        return payment
    
    @staticmethod
    def refund_to_customer(payment_id, reason=None):
        """
        Refund payment to customer.
        
        Args:
            payment_id: Payment ID
            reason: Reason for refund
        
        Returns:
            Payment: Updated payment object
        """
        payment = Payment.query.get_or_404(payment_id)
        
        if payment.status == Payment.STATUS_REFUNDED:
            raise ValueError("Payment has already been refunded")
        
        payment.status = Payment.STATUS_REFUNDED
        payment.refunded_at = datetime.utcnow()
        if reason:
            payment.admin_notes = f"Refund reason: {reason}"
        
        # Update order status
        payment.order.status = 'cancelled'
        payment.order.payment_status = 'refunded'
        
        db.session.commit()
        
        return payment
    
    @staticmethod
    def get_payment_status(payment_id):
        """
        Get payment status and details.
        
        Args:
            payment_id: Payment ID
        
        Returns:
            Payment: Payment object
        """
        return Payment.query.get_or_404(payment_id)


# Create a singleton instance
payment_service = PaymentService()

