"""
Dispute Resolution model for order and service disputes.

This module provides models for managing disputes between
customers and shop owners/service providers.
"""
from datetime import datetime
from app.extensions import db


class Dispute(db.Model):
    """
    Dispute model for managing disputes.
    
    Attributes:
        id (int): Primary key
        dispute_number (str): Unique dispute number
        dispute_type (str): Type of dispute (order, service, payment, delivery)
        order_id (int): Foreign key to Order (if order-related)
        service_id (int): Foreign key to Service (if service-related)
        title (str): Dispute title
        description (str): Detailed description
        status (str): Dispute status (open, in_review, resolved, closed, escalated)
        priority (str): Priority level (low, medium, high, urgent)
        raised_by (int): Foreign key to User (who raised dispute)
        against (int): Foreign key to User (who dispute is against)
        assigned_to (int): Foreign key to User (admin assigned to resolve)
        resolution (str): Resolution description
        resolved_by (int): Foreign key to User (who resolved)
        resolved_at (datetime): When dispute was resolved
        created_at (datetime): When dispute was created
        updated_at (datetime): Last update timestamp
    """
    __tablename__ = 'disputes'
    
    id = db.Column(db.Integer, primary_key=True)
    dispute_number = db.Column(db.String(20), unique=True, nullable=False)
    dispute_type = db.Column(db.String(50), nullable=False)  # order, service, payment, delivery
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')  # open, in_review, resolved, closed, escalated
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    raised_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    against = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    resolution = db.Column(db.Text, nullable=True)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref='disputes', lazy=True)
    service = db.relationship('Service', backref='disputes', lazy=True)
    raiser = db.relationship('User', foreign_keys=[raised_by], backref='disputes_raised', lazy=True)
    opponent = db.relationship('User', foreign_keys=[against], backref='disputes_against', lazy=True)
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_disputes', lazy=True)
    resolver = db.relationship('User', foreign_keys=[resolved_by], backref='resolved_disputes', lazy=True)
    
    # Relationship to dispute messages
    messages = db.relationship('DisputeMessage', backref='dispute', lazy=True, cascade='all, delete-orphan')
    
    def assign(self, user_id):
        """Assign dispute to a user."""
        self.assigned_to = user_id
        self.status = 'in_review'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def resolve(self, resolver_id, resolution_text):
        """Resolve dispute."""
        self.status = 'resolved'
        self.resolution = resolution_text
        self.resolved_by = resolver_id
        self.resolved_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def close(self):
        """Close dispute."""
        self.status = 'closed'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def escalate(self):
        """Escalate dispute."""
        self.status = 'escalated'
        self.priority = 'urgent'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<Dispute {self.dispute_number} status={self.status} priority={self.priority}>'


class DisputeMessage(db.Model):
    """
    Dispute Message model for communication within disputes.
    
    Attributes:
        id (int): Primary key
        dispute_id (int): Foreign key to Dispute
        sender_id (int): Foreign key to User
        message (str): Message content
        attachments (JSON): Attachments (file paths, URLs)
        created_at (datetime): When message was sent
    """
    __tablename__ = 'dispute_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    dispute_id = db.Column(db.Integer, db.ForeignKey('disputes.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    attachments = db.Column(db.JSON, nullable=True)  # List of file paths/URLs
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    sender = db.relationship('User', backref='dispute_messages', lazy=True)
    
    def __repr__(self):
        return f'<DisputeMessage dispute_id={self.dispute_id} sender_id={self.sender_id}>'

