"""
Order Fulfillment model for partial order fulfillment.

This module provides models for tracking partial order fulfillment,
allowing orders to be fulfilled in multiple shipments.
"""
from datetime import datetime
from app.extensions import db


class OrderFulfillment(db.Model):
    """
    Order Fulfillment model for tracking partial order fulfillment.
    
    Attributes:
        id (int): Primary key
        order_id (int): Foreign key to Order
        fulfillment_number (str): Unique fulfillment number
        status (str): Fulfillment status (pending, shipped, delivered, cancelled)
        shipped_at (datetime): When shipment was sent
        delivered_at (datetime): When shipment was delivered
        tracking_number (str): Shipping tracking number
        carrier (str): Shipping carrier name
        notes (str): Additional notes
        created_at (datetime): When fulfillment was created
        updated_at (datetime): Last update timestamp
    """
    __tablename__ = 'order_fulfillments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    fulfillment_number = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, shipped, delivered, cancelled
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    tracking_number = db.Column(db.String(100), nullable=True)
    carrier = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    order = db.relationship('Order', backref='fulfillments', lazy=True)
    
    # Relationship to fulfillment items
    items = db.relationship('FulfillmentItem', backref='fulfillment', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<OrderFulfillment {self.fulfillment_number} status={self.status}>'


class FulfillmentItem(db.Model):
    """
    Fulfillment Item model for items in a fulfillment.
    
    Attributes:
        id (int): Primary key
        fulfillment_id (int): Foreign key to OrderFulfillment
        order_item_id (int): Foreign key to OrderItem
        quantity (int): Quantity fulfilled in this shipment
    """
    __tablename__ = 'fulfillment_items'
    
    id = db.Column(db.Integer, primary_key=True)
    fulfillment_id = db.Column(db.Integer, db.ForeignKey('order_fulfillments.id'), nullable=False)
    order_item_id = db.Column(db.Integer, db.ForeignKey('order_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Relationships
    order_item = db.relationship('OrderItem', backref='fulfillment_items', lazy=True)
    
    def __repr__(self):
        return f'<FulfillmentItem order_item_id={self.order_item_id} quantity={self.quantity}>'

