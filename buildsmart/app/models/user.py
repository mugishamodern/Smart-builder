from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt


class User(UserMixin, db.Model):
    """
    User model for authentication and user management.
    
    This model represents all users in the system including customers,
    shop owners, and service providers. It handles authentication,
    profile management, and role-based access control.
    
    Attributes:
        id (int): Primary key
        username (str): Unique username for login
        email (str): Unique email address
        password_hash (str): Hashed password
        full_name (str): User's full name
        phone (str): Phone number
        address (str): Physical address
        latitude (float): GPS latitude
        longitude (float): GPS longitude
        user_type (str): Role type (customer, shop_owner, service_provider)
        is_active (bool): Whether user account is active
        is_verified (bool): Whether user is verified
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last update timestamp
    
    Relationships:
        shops: One-to-many relationship with Shop model
        services: One-to-many relationship with Service model
        orders: One-to-many relationship with Order model
        recommendations: One-to-many relationship with Recommendation model
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_type = db.Column(db.String(20), default='customer')  # customer, shop_owner, service_provider
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shops = db.relationship('Shop', backref='owner', lazy=True)
    services = db.relationship('Service', backref='provider', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)
    recommendations = db.relationship('Recommendation', backref='user', lazy=True)
    
    def set_password(self, password):
        """
        Set password hash using bcrypt.
        
        Args:
            password (str): Plain text password to hash
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """
        Check password against stored hash.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches hash
        """
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_shop_owner(self):
        """Check if user is a shop owner"""
        return self.user_type == 'shop_owner'
    
    def is_service_provider(self):
        """Check if user is a service provider"""
        return self.user_type == 'service_provider'
    
    def is_customer(self):
        """Check if user is a customer"""
        return self.user_type == 'customer'
    
    def __repr__(self):
        return f'<User {self.username}>'
