from datetime import datetime
from app.extensions import db


class Category(db.Model):
    """
    Category model for product categorization.
    
    This model represents product categories in the system,
    supporting hierarchical categorization with parent-child relationships.
    
    Attributes:
        id (int): Primary key
        name (str): Category name
        description (str): Category description
        icon (str): Icon class or URL
        parent_id (int): Foreign key to parent Category (for subcategories)
        is_active (bool): Whether category is currently active
        created_at (datetime): Category creation timestamp
        updated_at (datetime): Last update timestamp
    
    Relationships:
        parent: Self-referential relationship for parent category
        subcategories: Reverse relationship for child categories
        products: One-to-many relationship with Product model
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))  # Icon class name or URL
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Self-referential relationship for parent-child categories
    parent = db.relationship('Category', remote_side=[id], backref='subcategories')
    
    # Note: products relationship is defined via Product.category_model backref
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def __repr__(self):
        return f'<Category {self.name}>'

