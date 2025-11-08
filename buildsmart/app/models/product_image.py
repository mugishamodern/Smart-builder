"""
Product Image model for multiple images per product.

This module provides a model for storing multiple images
for each product with support for primary/main images.
"""
from datetime import datetime
from app.extensions import db


class ProductImage(db.Model):
    """
    Product Image model for storing multiple images per product.
    
    Attributes:
        id (int): Primary key
        product_id (int): Foreign key to Product
        image_url (str): URL to the image file
        thumbnail_url (str): URL to the thumbnail version
        is_primary (bool): Whether this is the primary/main image
        display_order (int): Order for displaying images
        created_at (datetime): Image creation timestamp
    """
    __tablename__ = 'product_images'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=True)
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    product = db.relationship('Product', backref='images', lazy=True)
    
    def __repr__(self):
        return f'<ProductImage {self.id} for product {self.product_id}>'

