"""
Order Modification model for tracking order changes.

This module provides models for tracking order modifications,
including item additions, removals, and quantity changes.
"""
from datetime import datetime
from app.extensions import db


class OrderModification(db.Model):
    """
    Order Modification model for tracking order changes.
    
    Attributes:
        id (int): Primary key
        order_id (int): Foreign key to Order
        modification_type (str): Type of modification (add_item, remove_item, update_quantity, update_address, cancel)
        description (str): Description of modification
        old_value (JSON): Previous order state
        new_value (JSON): New order state
        status (str): Modification status (pending, approved, rejected)
        created_by (int): Foreign key to User who requested modification
        approved_by (int): Foreign key to User who approved/rejected
        created_at (datetime): When modification was requested
        updated_at (datetime): When modification was processed
    """
    __tablename__ = 'order_modifications'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    modification_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    old_value = db.Column(db.JSON, nullable=True)  # Previous order state
    new_value = db.Column(db.JSON, nullable=True)  # New order state
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref='modifications', lazy=True)
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_modifications', lazy=True)
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_modifications', lazy=True)
    
    def approve(self, approver_id):
        """Approve modification."""
        self.status = 'approved'
        self.approved_by = approver_id
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def reject(self, approver_id):
        """Reject modification."""
        self.status = 'rejected'
        self.approved_by = approver_id
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<OrderModification order_id={self.order_id} type={self.modification_type} status={self.status}>'

