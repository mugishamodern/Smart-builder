"""
Order Status Tracking model for detailed order timeline.

This module provides a model for tracking detailed order status
changes with timestamps and notes.
"""
from datetime import datetime
from app.extensions import db


class OrderStatus(db.Model):
    """
    Order Status Tracking model for detailed order timeline.
    
    Attributes:
        id (int): Primary key
        order_id (int): Foreign key to Order
        status (str): Order status (pending, confirmed, processing, shipped, delivered, cancelled)
        notes (str): Additional notes about status change
        created_at (datetime): When status change occurred
        created_by (int): Foreign key to User who changed status (nullable for system)
    """
    __tablename__ = 'order_statuses'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    order = db.relationship('Order', backref='status_history', lazy=True)
    creator = db.relationship('User', foreign_keys=[created_by], lazy=True)
    
    def __repr__(self):
        return f'<OrderStatus order_id={self.order_id} status={self.status} at {self.created_at}>'

