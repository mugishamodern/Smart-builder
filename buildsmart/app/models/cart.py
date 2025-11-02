from datetime import datetime
from app.extensions import db
from decimal import Decimal


class Cart(db.Model):
    """
    Cart model for shopping cart management.
    
    This model represents a shopping cart, supporting both
    logged-in users and guest sessions.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User (nullable for guest carts)
        session_id (str): Session identifier for guest carts
        created_at (datetime): Cart creation timestamp
        updated_at (datetime): Last update timestamp
    
    Relationships:
        user: Many-to-one relationship with User model
        items: One-to-many relationship with CartItem model
    """
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_id = db.Column(db.String(255), nullable=True)  # For guest carts
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cart_user = db.relationship('User', foreign_keys=[user_id], overlaps="carts")
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')
    
    def get_total(self):
        """
        Calculate total cart value.
        
        Returns:
            Decimal: Total price of all items in cart
        """
        return sum(item.get_subtotal() for item in self.items)
    
    def get_items_count(self):
        """
        Get total number of items in cart.
        
        Returns:
            int: Total quantity of all items
        """
        return sum(item.quantity for item in self.items)
    
    def is_empty(self):
        """Check if cart is empty"""
        return len(self.items) == 0
    
    def __repr__(self):
        if self.user_id:
            return f'<Cart user_id={self.user_id}>'
        return f'<Cart session_id={self.session_id}>'


class CartItem(db.Model):
    """
    Cart item model for individual products in a cart.
    
    This model represents individual line items within a cart,
    storing product reference, quantity, and price snapshot.
    
    Attributes:
        id (int): Primary key
        cart_id (int): Foreign key to Cart
        product_id (int): Foreign key to Product
        quantity (int): Quantity of this product
        price_snapshot (Decimal): Price at time of adding to cart
        created_at (datetime): Item addition timestamp
        updated_at (datetime): Last update timestamp
    
    Relationships:
        cart: Many-to-one relationship with Cart model
        product: Many-to-one relationship with Product model
    """
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_snapshot = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='cart_items', lazy=True)
    
    def get_subtotal(self):
        """
        Calculate subtotal for this line item.
        
        Returns:
            Decimal: Quantity * price_snapshot
        """
        return self.quantity * self.price_snapshot
    
    def __repr__(self):
        return f'<CartItem product_id={self.product_id} quantity={self.quantity}>'

