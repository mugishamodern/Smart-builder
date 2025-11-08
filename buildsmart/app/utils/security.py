"""
Security utilities for input sanitization and validation.

This module provides utilities for sanitizing user input,
validating data, and implementing security best practices.
"""
import bleach
from marshmallow import Schema, fields, validate, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import User


def sanitize_html(text):
    """
    Sanitize HTML input to prevent XSS attacks.
    
    Args:
        text (str): Text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ''
    
    # Allowed tags and attributes
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ul', 'ol', 'li', 'a']
    allowed_attributes = {
        'a': ['href', 'title']
    }
    
    return bleach.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )


def sanitize_string(text, max_length=None):
    """
    Sanitize string input by removing HTML and limiting length.
    
    Args:
        text (str): String to sanitize
        max_length (int): Maximum length (optional)
        
    Returns:
        str: Sanitized string
    """
    if not text:
        return ''
    
    # Remove HTML tags
    text = bleach.clean(text, tags=[], strip=True)
    
    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password):
    """
    Validate password strength.
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'
    
    if not any(c.isupper() for c in password):
        return False, 'Password must contain at least one uppercase letter'
    
    if not any(c.islower() for c in password):
        return False, 'Password must contain at least one lowercase letter'
    
    if not any(c.isdigit() for c in password):
        return False, 'Password must contain at least one number'
    
    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        return False, 'Password must contain at least one special character'
    
    return True, None


# Marshmallow schemas for API validation
class UserSchema(SQLAlchemyAutoSchema):
    """Schema for User model validation"""
    
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash', 'two_factor_secret', 'tokens')
    
    email = fields.Email(required=True, validate=validate.Email())
    username = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=20),
        error_messages={'required': 'Username is required'}
    )
    password = fields.Str(
        required=False,
        load_only=True,
        validate=validate.Length(min=8),
        error_messages={'required': 'Password is required'}
    )


class LoginSchema(Schema):
    """Schema for login request validation"""
    email = fields.Email(required=True)  # API uses email
    password = fields.Str(required=True, validate=validate.Length(min=1))
    remember_me = fields.Bool(load_default=False)


class RegistrationSchema(Schema):
    """Schema for registration request validation"""
    username = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=20)
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8)
    )
    full_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    phone = fields.Str(required=False, validate=validate.Length(max=20))
    address = fields.Str(required=False, validate=validate.Length(max=500))
    user_type = fields.Str(
        required=True,
        validate=validate.OneOf(['customer', 'shop_owner', 'service_provider'])
    )


class PasswordResetRequestSchema(Schema):
    """Schema for password reset request validation"""
    email = fields.Email(required=True)


class PasswordResetSchema(Schema):
    """Schema for password reset validation"""
    token = fields.Str(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8)
    )


class EmailVerificationSchema(Schema):
    """Schema for email verification validation"""
    token = fields.Str(required=True)

