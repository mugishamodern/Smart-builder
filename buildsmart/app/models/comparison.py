from datetime import datetime
from app.extensions import db


class Comparison(db.Model):
    """
    Comparison model for storing product comparisons.
    
    This model allows logged-in users to save products for comparison.
    Guest users will use localStorage/session storage instead.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        product_id (int): Foreign key to Product
        created_at (datetime): When product was added to comparison
    
    Relationships:
        user: Many-to-one relationship with User model
        product: Many-to-one relationship with Product model
    """
    __tablename__ = 'comparisons'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='comparisons')
    product = db.relationship('Product', backref='comparisons')
    
    # Unique constraint: one user can only add a product once
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_comparison'),)
    
    def to_dict(self):
        """Convert comparison to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': {
                'id': self.product.id,
                'name': self.product.name,
                'description': self.product.description,
                'category': self.product.category,
                'price': float(self.product.price) if self.product.price else 0.0,
                'unit': self.product.unit,
                'brand': self.product.brand,
                'quantity_available': self.product.quantity_available,
                'is_available': self.product.is_available,
                'image_url': self.product.image_url,
                'shop_id': self.product.shop_id,
                'shop_name': self.product.shop.name if self.product.shop else None,
                'specifications': self.product.specifications
            } if self.product else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Comparison user_id={self.user_id} product_id={self.product_id}>'
