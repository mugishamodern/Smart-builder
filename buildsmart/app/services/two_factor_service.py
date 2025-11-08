"""
Two-Factor Authentication service using TOTP.

This module provides 2FA functionality using pyotp
for generating and verifying TOTP codes.
"""
import pyotp
import qrcode
import io
import base64
from app.extensions import db
from app.models import User


class TwoFactorService:
    """Service for Two-Factor Authentication"""
    
    @staticmethod
    def generate_secret():
        """
        Generate a new TOTP secret key.
        
        Returns:
            str: TOTP secret key
        """
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(user, secret):
        """
        Generate QR code for 2FA setup.
        
        Args:
            user: User object
            secret: TOTP secret key
            
        Returns:
            str: Base64 encoded QR code image
        """
        # Create TOTP URI
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name='BuildSmart'
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def enable_2fa(user, secret=None):
        """
        Enable 2FA for a user.
        
        Args:
            user: User object
            secret: TOTP secret key (optional, generates new if not provided)
            
        Returns:
            tuple: (secret, qr_code_base64)
        """
        if secret is None:
            secret = TwoFactorService.generate_secret()
        
        user.two_factor_secret = secret
        user.two_factor_enabled = True
        db.session.commit()
        
        qr_code = TwoFactorService.generate_qr_code(user, secret)
        
        return secret, qr_code
    
    @staticmethod
    def disable_2fa(user):
        """
        Disable 2FA for a user.
        
        Args:
            user: User object
        """
        user.two_factor_enabled = False
        user.two_factor_secret = None
        db.session.commit()
    
    @staticmethod
    def verify_code(user, code):
        """
        Verify TOTP code for a user.
        
        Args:
            user: User object
            code: TOTP code to verify
            
        Returns:
            bool: True if code is valid, False otherwise
        """
        if not user.two_factor_enabled or not user.two_factor_secret:
            return False
        
        totp = pyotp.TOTP(user.two_factor_secret)
        return totp.verify(code, valid_window=1)  # Allow 1 time step window
    
    @staticmethod
    def generate_backup_codes(user, count=10):
        """
        Generate backup codes for 2FA.
        
        Args:
            user: User object
            count: Number of backup codes to generate
            
        Returns:
            list: List of backup codes
        """
        import secrets
        codes = []
        for _ in range(count):
            code = secrets.token_hex(4).upper()  # 8 character code
            codes.append(code)
        
        # Store backup codes in user model (you might want a separate model for this)
        # For now, we'll store as comma-separated string
        # In production, consider encrypting these
        if not hasattr(user, 'backup_codes'):
            # Add backup_codes field to User model if needed
            pass
        
        return codes

