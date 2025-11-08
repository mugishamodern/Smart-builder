"""
Tests for security features.

This module tests all security features including:
- Password reset
- Email verification
- Rate limiting
- Input sanitization
- Two-Factor Authentication
- Account lockout
"""
import pytest
from datetime import datetime, timedelta
from app.models import User, Token
from app.services.email_service import EmailService
from app.services.two_factor_service import TwoFactorService
from app.utils.security import (
    sanitize_html, sanitize_string, validate_password_strength,
    validate_email
)


class TestPasswordReset:
    """Tests for password reset functionality"""
    
    def test_generate_password_reset_token(self, db_session, test_user):
        """Test generating password reset token"""
        token = Token.generate_token(test_user.id, 'password_reset', expires_in_hours=1)
        
        assert token is not None
        assert token.user_id == test_user.id
        assert token.token_type == 'password_reset'
        assert token.is_valid() is True
        assert token.used is False
    
    def test_password_reset_token_expiration(self, db_session, test_user):
        """Test password reset token expiration"""
        token = Token.generate_token(test_user.id, 'password_reset', expires_in_hours=1)
        
        # Manually expire token
        token.expires_at = datetime.utcnow() - timedelta(hours=2)
        db_session.commit()
        
        assert token.is_valid() is False
    
    def test_password_reset_token_one_time_use(self, db_session, test_user):
        """Test password reset token can only be used once"""
        token = Token.generate_token(test_user.id, 'password_reset', expires_in_hours=1)
        token_string = token.token
        
        # Mark token as used
        token.mark_as_used()
        
        # Try to validate used token
        validated_token = Token.validate_token(token_string, 'password_reset')
        assert validated_token is None


class TestEmailVerification:
    """Tests for email verification functionality"""
    
    def test_generate_email_verification_token(self, db_session, test_user):
        """Test generating email verification token"""
        token = Token.generate_token(test_user.id, 'email_verification', expires_in_hours=48)
        
        assert token is not None
        assert token.user_id == test_user.id
        assert token.token_type == 'email_verification'
        assert token.is_valid() is True
    
    def test_verify_user_email(self, db_session, test_user):
        """Test verifying user email"""
        assert test_user.email_verified is False
        
        test_user.verify_email()
        
        assert test_user.email_verified is True
        assert test_user.email_verified_at is not None
        assert test_user.is_verified is True  # Backward compatibility


class TestAccountLockout:
    """Tests for account lockout functionality"""
    
    def test_account_lockout_after_failed_attempts(self, db_session, test_user):
        """Test account lockout after multiple failed login attempts"""
        assert test_user.failed_login_attempts == 0
        assert test_user.is_account_locked() is False
        
        # Simulate 5 failed login attempts
        for i in range(5):
            test_user.increment_failed_login()
        
        assert test_user.failed_login_attempts >= 5
        assert test_user.is_account_locked() is True
        assert test_user.locked_until is not None
    
    def test_reset_failed_login_attempts(self, db_session, test_user):
        """Test resetting failed login attempts on successful login"""
        test_user.failed_login_attempts = 3
        db_session.commit()
        
        test_user.reset_failed_login_attempts()
        
        assert test_user.failed_login_attempts == 0
        assert test_user.last_login is not None
    
    def test_unlock_account(self, db_session, test_user):
        """Test unlocking user account"""
        test_user.lock_account(duration_minutes=30)
        assert test_user.is_account_locked() is True
        
        test_user.unlock_account()
        assert test_user.is_account_locked() is False
        assert test_user.failed_login_attempts == 0


class TestInputSanitization:
    """Tests for input sanitization"""
    
    def test_sanitize_html(self):
        """Test HTML sanitization"""
        malicious_input = '<script>alert("XSS")</script><p>Safe content</p>'
        sanitized = sanitize_html(malicious_input)
        
        assert '<script>' not in sanitized
        assert '<p>Safe content</p>' in sanitized
    
    def test_sanitize_string(self):
        """Test string sanitization"""
        malicious_input = '<script>alert("XSS")</script>Hello'
        sanitized = sanitize_string(malicious_input)
        
        assert '<script>' not in sanitized
        assert 'Hello' in sanitized
    
    def test_sanitize_string_max_length(self):
        """Test string sanitization with max length"""
        long_string = 'a' * 200
        sanitized = sanitize_string(long_string, max_length=100)
        
        assert len(sanitized) <= 100


class TestPasswordStrength:
    """Tests for password strength validation"""
    
    def test_weak_password(self):
        """Test weak password validation"""
        is_valid, error_msg = validate_password_strength('weak')
        assert is_valid is False
        assert error_msg is not None
    
    def test_strong_password(self):
        """Test strong password validation"""
        is_valid, error_msg = validate_password_strength('StrongP@ss123')
        assert is_valid is True
        assert error_msg is None
    
    def test_password_missing_uppercase(self):
        """Test password missing uppercase letter"""
        is_valid, error_msg = validate_password_strength('lowercase123!')
        assert is_valid is False
        assert 'uppercase' in error_msg.lower()
    
    def test_password_missing_number(self):
        """Test password missing number"""
        is_valid, error_msg = validate_password_strength('NoNumbers!')
        assert is_valid is False
        assert 'number' in error_msg.lower()
    
    def test_password_missing_special_character(self):
        """Test password missing special character"""
        is_valid, error_msg = validate_password_strength('NoSpecial123')
        assert is_valid is False
        assert 'special' in error_msg.lower()


class TestTwoFactorAuthentication:
    """Tests for Two-Factor Authentication"""
    
    def test_generate_2fa_secret(self):
        """Test generating 2FA secret"""
        secret = TwoFactorService.generate_secret()
        
        assert secret is not None
        assert len(secret) > 0
    
    def test_enable_2fa(self, db_session, test_user):
        """Test enabling 2FA for user"""
        secret, qr_code = TwoFactorService.enable_2fa(test_user)
        
        assert test_user.two_factor_enabled is True
        assert test_user.two_factor_secret is not None
        assert secret == test_user.two_factor_secret
        assert qr_code.startswith('data:image/png;base64,')
    
    def test_disable_2fa(self, db_session, test_user):
        """Test disabling 2FA for user"""
        TwoFactorService.enable_2fa(test_user)
        assert test_user.two_factor_enabled is True
        
        TwoFactorService.disable_2fa(test_user)
        
        assert test_user.two_factor_enabled is False
        assert test_user.two_factor_secret is None
    
    def test_verify_2fa_code(self, db_session, test_user):
        """Test verifying 2FA code"""
        secret, _ = TwoFactorService.enable_2fa(test_user)
        
        # Generate valid TOTP code
        import pyotp
        totp = pyotp.TOTP(secret)
        code = totp.now()
        
        assert TwoFactorService.verify_code(test_user, code) is True
        
        # Invalid code
        assert TwoFactorService.verify_code(test_user, '000000') is False


class TestEmailValidation:
    """Tests for email validation"""
    
    def test_valid_email(self):
        """Test valid email addresses"""
        assert validate_email('user@example.com') is True
        assert validate_email('user.name@example.co.uk') is True
    
    def test_invalid_email(self):
        """Test invalid email addresses"""
        assert validate_email('invalid-email') is False
        assert validate_email('user@') is False
        assert validate_email('@example.com') is False

