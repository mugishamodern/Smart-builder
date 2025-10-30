from datetime import datetime
from app.extensions import db


class Product(db.Model):
    """
    Product model for construction materials and building supplies.
    
    This model represents individual products sold by shops,
    including inventory management, pricing, and categorization.
    
    Attributes:
        id (int): Primary key
        name (str): Product name
        description (str): Product description
        category (str): Product category (e.g., 'cement', 'steel', 'paint')
        price (Decimal): Product price
        unit (str): Unit of measurement (e.g., 'kg', 'piece', 'bag')
        quantity_available (int): Available stock quantity
        min_order_quantity (int): Minimum order quantity
        is_available (bool): Whether product is currently available
        image_url (str): URL to product image
        brand (str): Product brand/manufacturer
        specifications (JSON): Additional product specifications
        created_at (datetime): Product creation timestamp
        updated_at (datetime): Last update timestamp
        shop_id (int): Foreign key to Shop
    
    Relationships:
        order_items: One-to-many relationship with OrderItem model
        shop: Many-to-one relationship with Shop model
    """
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
    brand = db.Column(db.String(50))  # Product brand/manufacturer
    specifications = db.Column(db.JSON)  # Store additional specs as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def is_in_stock(self):
        """
        Check if product is in stock and available.
        
        Returns:
            bool: True if product has available quantity and is marked as available
        """
        return self.quantity_available > 0 and self.is_available
    
    def __str__(self):
        return f"{self.name} - {self.brand or 'No Brand'} ({self.category})"
    
    def __repr__(self):
        return f'<Product {self.name}>'
