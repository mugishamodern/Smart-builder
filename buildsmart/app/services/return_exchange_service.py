"""
Return & Exchange service.

This module provides functionality for managing product returns
and exchanges with approval workflow.
"""
import secrets
from datetime import datetime
from app.extensions import db
from app.models import Order, OrderItem, ReturnRequest, ReturnItem, Product


class ReturnExchangeService:
    """Service for returns and exchanges"""
    
    @staticmethod
    def generate_return_number():
        """Generate unique return number."""
        return f"RET-{secrets.token_hex(4).upper()}"
    
    @staticmethod
    def create_return_request(order_id, order_item_id, reason, description, return_type, requested_by):
        """
        Create a return request.
        
        Args:
            order_id: Order ID
            order_item_id: Order item ID to return
            reason: Reason for return
            description: Detailed description
            return_type: Type of return (refund, exchange)
            requested_by: User ID who requested return
            
        Returns:
            ReturnRequest: Created return request or None
        """
        order = Order.query.get(order_id)
        order_item = OrderItem.query.get(order_item_id)
        
        if not order or not order_item or order_item.order_id != order_id:
            return None
        
        # Check if order item can be returned (not already returned, within time limit, etc.)
        # This is a simplified check - you might want to add more validation
        
        # Generate return number
        return_number = ReturnExchangeService.generate_return_number()
        
        # Calculate refund amount
        refund_amount = None
        if return_type == 'refund':
            refund_amount = order_item.total_price
        
        # Create return request
        return_request = ReturnRequest(
            return_number=return_number,
            order_id=order_id,
            order_item_id=order_item_id,
            reason=reason,
            description=description,
            return_type=return_type,
            refund_amount=refund_amount,
            requested_by=requested_by,
            status='pending'
        )
        
        db.session.add(return_request)
        db.session.commit()
        
        return return_request
    
    @staticmethod
    def create_exchange_request(order_id, order_item_id, reason, description, exchange_product_id, requested_by):
        """
        Create an exchange request.
        
        Args:
            order_id: Order ID
            order_item_id: Order item ID to exchange
            reason: Reason for exchange
            description: Detailed description
            exchange_product_id: Product ID to exchange for
            requested_by: User ID who requested exchange
            
        Returns:
            ReturnRequest: Created exchange request or None
        """
        order = Order.query.get(order_id)
        order_item = OrderItem.query.get(order_item_id)
        exchange_product = Product.query.get(exchange_product_id)
        
        if not order or not order_item or not exchange_product:
            return None
        
        # Check if exchange product is available
        if not exchange_product.is_in_stock():
            return None
        
        # Generate return number
        return_number = ReturnExchangeService.generate_return_number()
        
        # Create return request (exchange is a type of return)
        return_request = ReturnRequest(
            return_number=return_number,
            order_id=order_id,
            order_item_id=order_item_id,
            reason=reason,
            description=description,
            return_type='exchange',
            exchange_product_id=exchange_product_id,
            requested_by=requested_by,
            status='pending'
        )
        
        db.session.add(return_request)
        db.session.commit()
        
        return return_request
    
    @staticmethod
    def approve_return(return_id, approver_id):
        """
        Approve a return request.
        
        Args:
            return_id: Return request ID
            approver_id: User ID who approved
            
        Returns:
            bool: True if successful, False otherwise
        """
        return_request = ReturnRequest.query.get(return_id)
        if not return_request:
            return False
        
        return_request.approve(approver_id)
        
        # If refund, process refund (this would integrate with payment service)
        if return_request.return_type == 'refund' and return_request.refund_amount:
            # Process refund logic here
            pass
        
        # If exchange, create new order item or update existing
        if return_request.return_type == 'exchange' and return_request.exchange_product_id:
            # Exchange logic would go here
            pass
        
        return True
    
    @staticmethod
    def reject_return(return_id, approver_id):
        """
        Reject a return request.
        
        Args:
            return_id: Return request ID
            approver_id: User ID who rejected
            
        Returns:
            bool: True if successful, False otherwise
        """
        return_request = ReturnRequest.query.get(return_id)
        if not return_request:
            return False
        
        return_request.reject(approver_id)
        
        return True
    
    @staticmethod
    def complete_return(return_id):
        """
        Mark return as completed.
        
        Args:
            return_id: Return request ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        return_request = ReturnRequest.query.get(return_id)
        if not return_request:
            return False
        
        if return_request.status != 'approved':
            return False
        
        return_request.complete()
        
        # Update product inventory if needed
        order_item = return_request.order_item
        if order_item:
            product = order_item.product
            if product:
                product.quantity_available += order_item.quantity
                db.session.commit()
        
        return True
    
    @staticmethod
    def get_user_returns(user_id, status=None):
        """
        Get return requests for a user.
        
        Args:
            user_id: User ID
            status: Filter by status (optional)
            
        Returns:
            list: List of return requests
        """
        query = ReturnRequest.query.filter_by(requested_by=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(ReturnRequest.created_at.desc()).all()
    
    @staticmethod
    def get_shop_returns(shop_id, status=None):
        """
        Get return requests for a shop.
        
        Args:
            shop_id: Shop ID
            status: Filter by status (optional)
            
        Returns:
            list: List of return requests
        """
        from app.models import Order
        query = db.session.query(ReturnRequest).join(Order).filter(Order.shop_id == shop_id)
        
        if status:
            query = query.filter(ReturnRequest.status == status)
        
        return query.order_by(ReturnRequest.created_at.desc()).all()

