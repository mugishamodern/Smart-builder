"""
Return & Exchange model for product returns and exchanges.

This module provides models for managing product returns
and exchanges with detailed tracking and approval workflow.
"""
from datetime import datetime
from app.extensions import db


class ReturnRequest(db.Model):
    """
    Return Request model for product returns.
    
    Attributes:
        id (int): Primary key
        return_number (str): Unique return number
        order_id (int): Foreign key to Order
        order_item_id (int): Foreign key to OrderItem
        reason (str): Reason for return
        description (str): Detailed description
        status (str): Return status (pending, approved, rejected, processing, completed, cancelled)
        return_type (str): Type of return (refund, exchange)
        refund_amount (Decimal): Amount to be refunded
        exchange_product_id (int): Foreign key to Product (for exchanges)
        requested_by (int): Foreign key to User (customer)
        approved_by (int): Foreign key to User (shop owner/admin)
        created_at (datetime): When return was requested
        updated_at (datetime): Last update timestamp
        processed_at (datetime): When return was processed
    """
    __tablename__ = 'return_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    return_number = db.Column(db.String(20), unique=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order_item_id = db.Column(db.Integer, db.ForeignKey('order_items.id'), nullable=False)
    reason = db.Column(db.String(100), nullable=False)  # damaged, wrong_item, defective, not_as_described, other
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, processing, completed, cancelled
    return_type = db.Column(db.String(20), nullable=False)  # refund, exchange
    refund_amount = db.Column(db.Numeric(10, 2), nullable=True)
    exchange_product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    order = db.relationship('Order', backref='return_requests', lazy=True)
    order_item = db.relationship('OrderItem', backref='return_requests', lazy=True)
    requester = db.relationship('User', foreign_keys=[requested_by], backref='return_requests', lazy=True)
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_returns', lazy=True)
    exchange_product = db.relationship('Product', foreign_keys=[exchange_product_id], lazy=True)
    
    def approve(self, approver_id):
        """Approve return request."""
        self.status = 'approved'
        self.approved_by = approver_id
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def reject(self, approver_id):
        """Reject return request."""
        self.status = 'rejected'
        self.approved_by = approver_id
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def complete(self):
        """Mark return as completed."""
        self.status = 'completed'
        self.processed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<ReturnRequest {self.return_number} status={self.status}>'


class ReturnItem(db.Model):
    """
    Return Item model for tracking returned items.
    
    Attributes:
        id (int): Primary key
        return_request_id (int): Foreign key to ReturnRequest
        product_id (int): Foreign key to Product
        quantity (int): Quantity returned
        condition (str): Item condition (new, used, damaged, defective)
        notes (str): Additional notes about item condition
    """
    __tablename__ = 'return_items'
    
    id = db.Column(db.Integer, primary_key=True)
    return_request_id = db.Column(db.Integer, db.ForeignKey('return_requests.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(50), nullable=False)  # new, used, damaged, defective
    notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    return_request = db.relationship('ReturnRequest', backref='return_items', lazy=True)
    product = db.relationship('Product', backref='return_items', lazy=True)
    
    def __repr__(self):
        return f'<ReturnItem return_request_id={self.return_request_id} product_id={self.product_id}>'

