from datetime import datetime
from app.extensions import db


class Product(db.Model):
    """Product model for construction materials"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # e.g., 'kg', 'piece', 'bag', 'm2'
    quantity_available = db.Column(db.Integer, default=0)
    min_order_quantity = db.Column(db.Integer, default=1)
    is_available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255))
    specifications = db.Column(db.JSON)  # Store additional specs as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'
