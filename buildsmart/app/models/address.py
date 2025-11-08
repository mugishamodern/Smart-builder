from datetime import datetime
from app.extensions import db


class Address(db.Model):
    """
    Address model for storing multiple delivery addresses per user.
    
    This model allows users to save multiple delivery addresses
    for convenient checkout and order management.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        label (str): Address label (e.g., "Home", "Office", "Work")
        full_name (str): Recipient full name
        phone (str): Contact phone number
        address_line1 (str): Primary address line
        address_line2 (str): Secondary address line (optional)
        city (str): City
        state (str): State/Province
        postal_code (str): Postal/ZIP code
        country (str): Country
        is_default (bool): Whether this is the default address
        created_at (datetime): Address creation timestamp
        updated_at (datetime): Last update timestamp
    
    Relationships:
        user: Many-to-one relationship with User model
    """
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    label = db.Column(db.String(50), nullable=False)  # "Home", "Office", "Work", etc.
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address_line1 = db.Column(db.String(200), nullable=False)
    address_line2 = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), default='Uganda', nullable=False)
    is_default = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='addresses', lazy=True)
    
    def to_dict(self):
        """Convert address to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'label': self.label,
            'full_name': self.full_name,
            'phone': self.phone,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def get_full_address(self):
        """Get formatted full address string"""
        parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join([p for p in parts if p])
    
    def __repr__(self):
        return f'<Address {self.label} - {self.user_id}>'
