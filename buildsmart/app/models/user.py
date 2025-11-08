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
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    two_factor_enabled = db.Column(db.Boolean, default=False, nullable=False)
    two_factor_secret = db.Column(db.String(32), nullable=True)  # TOTP secret key
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)  # Account lockout timestamp
    last_login = db.Column(db.DateTime, nullable=True)
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
    
    def is_admin_user(self):
        """Check if user is an admin"""
        return self.user_type == 'admin'
    
    def is_account_locked(self):
        """
        Check if user account is locked due to failed login attempts.
        
        Returns:
            bool: True if account is locked, False otherwise
        """
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    def lock_account(self, duration_minutes=30):
        """
        Lock user account for a specified duration.
        
        Args:
            duration_minutes (int): Minutes to lock account (default: 30)
        """
        from datetime import timedelta
        self.locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        db.session.commit()
    
    def unlock_account(self):
        """Unlock user account and reset failed login attempts."""
        self.locked_until = None
        self.failed_login_attempts = 0
        db.session.commit()
    
    def increment_failed_login(self):
        """
        Increment failed login attempts and lock account if threshold reached.
        
        Returns:
            bool: True if account should be locked, False otherwise
        """
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.lock_account()
            db.session.commit()
            return True
        db.session.commit()
        return False
    
    def reset_failed_login_attempts(self):
        """Reset failed login attempts on successful login."""
        self.failed_login_attempts = 0
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def verify_email(self):
        """Mark user's email as verified."""
        self.email_verified = True
        self.email_verified_at = datetime.utcnow()
        self.is_verified = True  # Keep backward compatibility
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'
