"""
Wishlist/Favorites model for users to save products.

This module provides a model for users to save their
favorite products for later viewing.
"""
from datetime import datetime
from app.extensions import db


class Wishlist(db.Model):
    """
    Wishlist model for users to save favorite products.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        product_id (int): Foreign key to Product
        created_at (datetime): When item was added to wishlist
    """
    __tablename__ = 'wishlist'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='wishlist_items', lazy=True)
    product = db.relationship('Product', backref='wishlist_users', lazy=True)
    
    # Unique constraint: user can only add a product once
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_wishlist'),)
    
    def __repr__(self):
        return f'<Wishlist user_id={self.user_id} product_id={self.product_id}>'

