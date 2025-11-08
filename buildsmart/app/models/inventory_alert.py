"""
Inventory Alert model for low-stock notifications.

This module provides a model for tracking low-stock alerts
for products to help shop owners manage inventory.
"""
from datetime import datetime
from app.extensions import db


class InventoryAlert(db.Model):
    """
    Inventory Alert model for low-stock notifications.
    
    Attributes:
        id (int): Primary key
        product_id (int): Foreign key to Product
        shop_id (int): Foreign key to Shop
        threshold (int): Low stock threshold
        current_quantity (int): Quantity when alert was triggered
        alert_type (str): Type of alert (low_stock, out_of_stock, restocked)
        notified (bool): Whether shop owner has been notified
        notified_at (datetime): When notification was sent
        created_at (datetime): When alert was created
        resolved_at (datetime): When alert was resolved
    """
    __tablename__ = 'inventory_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    threshold = db.Column(db.Integer, nullable=False)
    current_quantity = db.Column(db.Integer, nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # low_stock, out_of_stock, restocked
    notified = db.Column(db.Boolean, default=False, nullable=False)
    notified_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    product = db.relationship('Product', backref='inventory_alerts', lazy=True)
    shop = db.relationship('Shop', backref='inventory_alerts', lazy=True)
    
    def mark_as_notified(self):
        """Mark alert as notified."""
        self.notified = True
        self.notified_at = datetime.utcnow()
        db.session.commit()
    
    def resolve(self):
        """Mark alert as resolved."""
        self.resolved_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<InventoryAlert product_id={self.product_id} type={self.alert_type} qty={self.current_quantity}>'

