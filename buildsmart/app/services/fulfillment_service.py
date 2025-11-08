"""
Partial order fulfillment service.

This module provides functionality for managing partial
order fulfillment, allowing orders to be fulfilled in multiple shipments.
"""
import secrets
from datetime import datetime
from app.extensions import db
from app.models import Order, OrderItem, OrderFulfillment, FulfillmentItem


class FulfillmentService:
    """Service for partial order fulfillment"""
    
    @staticmethod
    def generate_fulfillment_number():
        """Generate unique fulfillment number."""
        return f"FULF-{secrets.token_hex(4).upper()}"
    
    @staticmethod
    def create_fulfillment(order_id, items_data):
        """
        Create a partial fulfillment for an order.
        
        Args:
            order_id: Order ID
            items_data: List of dicts with order_item_id and quantity
            
        Returns:
            OrderFulfillment: Created fulfillment or None
        """
        order = Order.query.get(order_id)
        if not order:
            return None
        
        # Generate fulfillment number
        fulfillment_number = FulfillmentService.generate_fulfillment_number()
        
        # Create fulfillment
        fulfillment = OrderFulfillment(
            order_id=order_id,
            fulfillment_number=fulfillment_number,
            status='pending'
        )
        db.session.add(fulfillment)
        db.session.flush()  # Get fulfillment ID
        
        # Add fulfillment items
        for item_data in items_data:
            order_item_id = item_data.get('order_item_id')
            quantity = item_data.get('quantity')
            
            order_item = OrderItem.query.get(order_item_id)
            if not order_item or order_item.order_id != order_id:
                continue
            
            fulfillment_item = FulfillmentItem(
                fulfillment_id=fulfillment.id,
                order_item_id=order_item_id,
                quantity=quantity
            )
            db.session.add(fulfillment_item)
        
        db.session.commit()
        
        return fulfillment
    
    @staticmethod
    def ship_fulfillment(fulfillment_id, tracking_number=None, carrier=None, notes=None):
        """
        Mark fulfillment as shipped.
        
        Args:
            fulfillment_id: Fulfillment ID
            tracking_number: Tracking number
            carrier: Shipping carrier
            notes: Additional notes
            
        Returns:
            bool: True if successful, False otherwise
        """
        fulfillment = OrderFulfillment.query.get(fulfillment_id)
        if not fulfillment:
            return False
        
        fulfillment.status = 'shipped'
        fulfillment.shipped_at = datetime.utcnow()
        fulfillment.tracking_number = tracking_number
        fulfillment.carrier = carrier
        fulfillment.notes = notes
        fulfillment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Add status history to order
        fulfillment.order.add_status_history(
            status='shipped',
            notes=f'Partial shipment: {fulfillment.fulfillment_number}',
            created_by=fulfillment.order.shop.owner_id
        )
        
        return True
    
    @staticmethod
    def deliver_fulfillment(fulfillment_id):
        """
        Mark fulfillment as delivered.
        
        Args:
            fulfillment_id: Fulfillment ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        fulfillment = OrderFulfillment.query.get(fulfillment_id)
        if not fulfillment:
            return False
        
        fulfillment.status = 'delivered'
        fulfillment.delivered_at = datetime.utcnow()
        fulfillment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Check if all fulfillments are delivered
        FulfillmentService._check_order_completion(fulfillment.order_id)
        
        return True
    
    @staticmethod
    def _check_order_completion(order_id):
        """Check if all fulfillments are delivered and update order status."""
        order = Order.query.get(order_id)
        if not order:
            return
        
        fulfillments = OrderFulfillment.query.filter_by(order_id=order_id).all()
        
        if all(f.status == 'delivered' for f in fulfillments) and fulfillments:
            # Check if order is fully fulfilled
            total_fulfilled = {}
            for fulfillment in fulfillments:
                for item in fulfillment.items:
                    order_item_id = item.order_item_id
                    if order_item_id not in total_fulfilled:
                        total_fulfilled[order_item_id] = 0
                    total_fulfilled[order_item_id] += item.quantity
            
            # Check if all items are fully fulfilled
            all_fulfilled = True
            for order_item in order.items:
                fulfilled_qty = total_fulfilled.get(order_item.id, 0)
                if fulfilled_qty < order_item.quantity:
                    all_fulfilled = False
                    break
            
            if all_fulfilled and order.status != 'delivered':
                order.status = 'delivered'
                order.updated_at = datetime.utcnow()
                db.session.commit()
                
                order.add_status_history(
                    status='delivered',
                    notes='All fulfillments delivered',
                    created_by=order.shop.owner_id
                )
    
    @staticmethod
    def get_order_fulfillments(order_id):
        """
        Get all fulfillments for an order.
        
        Args:
            order_id: Order ID
            
        Returns:
            list: List of fulfillments
        """
        return OrderFulfillment.query.filter_by(order_id=order_id).order_by(
            OrderFulfillment.created_at.asc()
        ).all()
    
    @staticmethod
    def get_fulfillment_status(order_id):
        """
        Get fulfillment status summary for an order.
        
        Args:
            order_id: Order ID
            
        Returns:
            dict: Fulfillment status summary
        """
        order = Order.query.get(order_id)
        if not order:
            return None
        
        fulfillments = FulfillmentService.get_order_fulfillments(order_id)
        
        # Calculate fulfilled quantities
        fulfilled_quantities = {}
        for fulfillment in fulfillments:
            for item in fulfillment.items:
                order_item_id = item.order_item_id
                if order_item_id not in fulfilled_quantities:
                    fulfilled_quantities[order_item_id] = 0
                fulfilled_quantities[order_item_id] += item.quantity
        
        # Build status summary
        items_status = []
        for order_item in order.items:
            fulfilled_qty = fulfilled_quantities.get(order_item.id, 0)
            items_status.append({
                'order_item_id': order_item.id,
                'product_id': order_item.product_id,
                'product_name': order_item.product.name,
                'ordered_quantity': order_item.quantity,
                'fulfilled_quantity': fulfilled_qty,
                'pending_quantity': order_item.quantity - fulfilled_qty,
                'is_fully_fulfilled': fulfilled_qty >= order_item.quantity
            })
        
        return {
            'order_id': order_id,
            'total_fulfillments': len(fulfillments),
            'items_status': items_status,
            'is_fully_fulfilled': all(item['is_fully_fulfilled'] for item in items_status)
        }

