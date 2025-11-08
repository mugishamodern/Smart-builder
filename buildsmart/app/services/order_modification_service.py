"""
Order modification service.

This module provides functionality for managing order modifications,
including item additions, removals, and quantity changes.
"""
from datetime import datetime
from app.extensions import db
from app.models import Order, OrderItem, OrderModification, Product
from decimal import Decimal


class OrderModificationService:
    """Service for order modifications"""
    
    @staticmethod
    def request_modification(order_id, modification_type, description, old_value, new_value, created_by):
        """
        Request an order modification.
        
        Args:
            order_id: Order ID
            modification_type: Type of modification
            description: Description of modification
            old_value: Previous order state (JSON)
            new_value: New order state (JSON)
            created_by: User ID who requested modification
            
        Returns:
            OrderModification: Created modification request
        """
        order = Order.query.get(order_id)
        if not order:
            return None
        
        modification = OrderModification(
            order_id=order_id,
            modification_type=modification_type,
            description=description,
            old_value=old_value,
            new_value=new_value,
            status='pending',
            created_by=created_by
        )
        
        db.session.add(modification)
        db.session.commit()
        
        return modification
    
    @staticmethod
    def add_item(order_id, product_id, quantity, created_by):
        """
        Request to add an item to an order.
        
        Args:
            order_id: Order ID
            product_id: Product ID to add
            quantity: Quantity to add
            created_by: User ID
            
        Returns:
            OrderModification: Created modification request
        """
        order = Order.query.get(order_id)
        product = Product.query.get(product_id)
        
        if not order or not product:
            return None
        
        # Check if product is in stock
        if product.quantity_available < quantity:
            return None
        
        # Build old and new values
        old_value = {
            'items': [{'product_id': item.product_id, 'quantity': item.quantity} for item in order.items],
            'total_amount': float(order.total_amount)
        }
        
        new_value = {
            'items': old_value['items'] + [{'product_id': product_id, 'quantity': quantity}],
            'new_item': {'product_id': product_id, 'quantity': quantity, 'price': float(product.price)}
        }
        
        modification = OrderModificationService.request_modification(
            order_id=order_id,
            modification_type='add_item',
            description=f'Add {quantity} x {product.name}',
            old_value=old_value,
            new_value=new_value,
            created_by=created_by
        )
        
        return modification
    
    @staticmethod
    def remove_item(order_id, order_item_id, created_by):
        """
        Request to remove an item from an order.
        
        Args:
            order_id: Order ID
            order_item_id: Order item ID to remove
            created_by: User ID
            
        Returns:
            OrderModification: Created modification request
        """
        order = Order.query.get(order_id)
        order_item = OrderItem.query.get(order_item_id)
        
        if not order or not order_item or order_item.order_id != order_id:
            return None
        
        # Build old and new values
        old_value = {
            'items': [{'id': item.id, 'product_id': item.product_id, 'quantity': item.quantity} for item in order.items],
            'total_amount': float(order.total_amount)
        }
        
        new_value = {
            'items': [item for item in old_value['items'] if item['id'] != order_item_id],
            'removed_item': {'id': order_item_id, 'product_id': order_item.product_id, 'quantity': order_item.quantity}
        }
        
        modification = OrderModificationService.request_modification(
            order_id=order_id,
            modification_type='remove_item',
            description=f'Remove {order_item.product.name}',
            old_value=old_value,
            new_value=new_value,
            created_by=created_by
        )
        
        return modification
    
    @staticmethod
    def update_quantity(order_id, order_item_id, new_quantity, created_by):
        """
        Request to update item quantity in an order.
        
        Args:
            order_id: Order ID
            order_item_id: Order item ID
            new_quantity: New quantity
            created_by: User ID
            
        Returns:
            OrderModification: Created modification request
        """
        order = Order.query.get(order_id)
        order_item = OrderItem.query.get(order_item_id)
        
        if not order or not order_item or order_item.order_id != order_id:
            return None
        
        product = order_item.product
        
        # Check if product is in stock
        if product.quantity_available < new_quantity:
            return None
        
        # Build old and new values
        old_value = {
            'items': [{'id': item.id, 'product_id': item.product_id, 'quantity': item.quantity} for item in order.items],
            'total_amount': float(order.total_amount)
        }
        
        new_value = {
            'items': [{'id': item.id, 'product_id': item.product_id, 'quantity': new_quantity if item.id == order_item_id else item.quantity} for item in order.items],
            'updated_item': {'id': order_item_id, 'old_quantity': order_item.quantity, 'new_quantity': new_quantity}
        }
        
        modification = OrderModificationService.request_modification(
            order_id=order_id,
            modification_type='update_quantity',
            description=f'Update quantity for {product.name} from {order_item.quantity} to {new_quantity}',
            old_value=old_value,
            new_value=new_value,
            created_by=created_by
        )
        
        return modification
    
    @staticmethod
    def approve_modification(modification_id, approver_id):
        """
        Approve an order modification and apply changes.
        
        Args:
            modification_id: Modification ID
            approver_id: User ID who approved
            
        Returns:
            bool: True if successful, False otherwise
        """
        modification = OrderModification.query.get(modification_id)
        if not modification:
            return False
        
        order = modification.order
        
        # Apply modification based on type
        if modification.modification_type == 'add_item':
            new_item = modification.new_value.get('new_item')
            if new_item:
                product = Product.query.get(new_item['product_id'])
                if product:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=new_item['quantity'],
                        unit_price=Decimal(str(product.price)),
                        total_price=Decimal(str(product.price * new_item['quantity']))
                    )
                    db.session.add(order_item)
                    
                    # Update order total
                    order.total_amount += order_item.total_price
        
        elif modification.modification_type == 'remove_item':
            removed_item = modification.new_value.get('removed_item')
            if removed_item:
                order_item = OrderItem.query.get(removed_item['id'])
                if order_item:
                    # Update order total
                    order.total_amount -= order_item.total_price
                    db.session.delete(order_item)
        
        elif modification.modification_type == 'update_quantity':
            updated_item = modification.new_value.get('updated_item')
            if updated_item:
                order_item = OrderItem.query.get(updated_item['id'])
                if order_item:
                    old_total = order_item.total_price
                    order_item.quantity = updated_item['new_quantity']
                    order_item.total_price = order_item.unit_price * updated_item['new_quantity']
                    
                    # Update order total
                    order.total_amount = order.total_amount - old_total + order_item.total_price
        
        # Approve modification
        modification.approve(approver_id)
        
        # Add status history
        order.add_status_history(
            status=order.status,
            notes=f'Order modified: {modification.description}',
            created_by=approver_id
        )
        
        db.session.commit()
        
        return True
    
    @staticmethod
    def reject_modification(modification_id, approver_id):
        """
        Reject an order modification.
        
        Args:
            modification_id: Modification ID
            approver_id: User ID who rejected
            
        Returns:
            bool: True if successful, False otherwise
        """
        modification = OrderModification.query.get(modification_id)
        if not modification:
            return False
        
        modification.reject(approver_id)
        
        return True

