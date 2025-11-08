"""
Stock Notification model for product availability alerts.

This module provides a model for users to receive notifications
when out-of-stock products become available.
"""
from datetime import datetime
from app.extensions import db


class StockNotification(db.Model):
    """
    Stock Notification model for product availability alerts.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        product_id (int): Foreign key to Product
        notified (bool): Whether user has been notified
        notified_at (datetime): When notification was sent
        created_at (datetime): When notification was requested
    """
    __tablename__ = 'stock_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    notified = db.Column(db.Boolean, default=False, nullable=False)
    notified_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='stock_notifications', lazy=True)
    product = db.relationship('Product', backref='stock_notifications', lazy=True)
    
    # Unique constraint: user can only have one notification per product
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_notification'),)
    
    def mark_as_notified(self):
        """Mark notification as sent."""
        self.notified = True
        self.notified_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<StockNotification user_id={self.user_id} product_id={self.product_id}>'

