from datetime import datetime
from app.extensions import db


class Review(db.Model):
    """
    Review model for user reviews of shops and products.
    
    This model represents user reviews and ratings for
    shops and products in the system.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User (reviewer)
        shop_id (int): Foreign key to Shop (nullable if product review)
        product_id (int): Foreign key to Product (nullable if shop review)
        rating (float): Rating score (0.0-5.0)
        comment (str): Review text/comment
        is_verified (bool): Whether review is verified purchase
        is_approved (bool): Whether review is approved for display
        created_at (datetime): Review creation timestamp
        updated_at (datetime): Last update timestamp
    
    Relationships:
        user: Many-to-one relationship with User model
        shop: Many-to-one relationship with Shop model
        product: Many-to-one relationship with Product model
    """
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    rating = db.Column(db.Float, nullable=False)  # 0.0 to 5.0
    comment = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=False)  # Verified purchase
    is_approved = db.Column(db.Boolean, default=True)  # Approved for display
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], overlaps="reviews")
    shop_rel = db.relationship('Shop', foreign_keys=[shop_id], overlaps="reviews,shop")  # renamed to avoid backref conflict
    product_rel = db.relationship('Product', foreign_keys=[product_id], overlaps="product,reviews")  # renamed to avoid backref conflict
    
    def __repr__(self):
        if self.product_id:
            return f'<Review product_id={self.product_id} rating={self.rating}>'
        return f'<Review shop_id={self.shop_id} rating={self.rating}>'

