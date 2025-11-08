"""
Token models for email verification and password reset.

This module provides token models for secure email verification
and password reset functionality with expiration and one-time use.
"""
from datetime import datetime, timedelta
from app.extensions import db
from secrets import token_urlsafe


class Token(db.Model):
    """
    Base token model for email verification and password reset.
    
    Attributes:
        id (int): Primary key
        token (str): Unique token string
        user_id (int): Foreign key to User
        token_type (str): Type of token (email_verification, password_reset)
        expires_at (datetime): Token expiration timestamp
        used (bool): Whether token has been used
        created_at (datetime): Token creation timestamp
    """
    __tablename__ = 'tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token_type = db.Column(db.String(50), nullable=False)  # email_verification, password_reset
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    user = db.relationship('User', backref='tokens', lazy=True)
    
    def __init__(self, user_id, token_type, expires_in_hours=24):
        """
        Initialize a new token.
        
        Args:
            user_id (int): User ID
            token_type (str): Type of token
            expires_in_hours (int): Hours until token expires (default: 24)
        """
        self.user_id = user_id
        self.token_type = token_type
        self.token = token_urlsafe(32)
        self.expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
        self.used = False
    
    def is_valid(self):
        """
        Check if token is valid (not expired and not used).
        
        Returns:
            bool: True if token is valid, False otherwise
        """
        return not self.used and datetime.utcnow() < self.expires_at
    
    def mark_as_used(self):
        """Mark token as used."""
        self.used = True
        db.session.commit()
    
    @staticmethod
    def generate_token(user_id, token_type, expires_in_hours=24):
        """
        Generate a new token for a user.
        
        Args:
            user_id (int): User ID
            token_type (str): Type of token
            expires_in_hours (int): Hours until token expires
            
        Returns:
            Token: New token instance
        """
        # Invalidate existing tokens of the same type for this user
        existing_tokens = Token.query.filter_by(
            user_id=user_id,
            token_type=token_type,
            used=False
        ).all()
        
        for token in existing_tokens:
            token.used = True
        
        # Create new token
        new_token = Token(user_id, token_type, expires_in_hours)
        db.session.add(new_token)
        db.session.commit()
        
        return new_token
    
    @staticmethod
    def validate_token(token_string, token_type):
        """
        Validate a token string.
        
        Args:
            token_string (str): Token string to validate
            token_type (str): Expected token type
            
        Returns:
            Token: Token object if valid, None otherwise
        """
        token = Token.query.filter_by(
            token=token_string,
            token_type=token_type,
            used=False
        ).first()
        
        if token and token.is_valid():
            return token
        
        return None
    
    def __repr__(self):
        return f'<Token {self.token_type} for user {self.user_id}>'

