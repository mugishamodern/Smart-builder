"""
Authentication routes with security enhancements.

This module provides secure authentication endpoints including:
- Login with rate limiting and account lockout
- Registration with email verification
- Password reset functionality
- Email verification
- Two-Factor Authentication (2FA)
"""
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import auth_bp
from app.models import User, Token
from app.extensions import db, limiter
from app.forms.auth_forms import LoginForm, RegistrationForm
from app.utils.cart_utils import merge_guest_cart_to_user
from app.utils.security import (
    sanitize_string, validate_password_strength,
    LoginSchema, RegistrationSchema, PasswordResetRequestSchema,
    PasswordResetSchema, EmailVerificationSchema
)
from app.services.email_service import EmailService
from app.services.two_factor_service import TwoFactorService
from marshmallow import ValidationError
from datetime import datetime


# Rate limiting decorators
rate_limit_login = limiter.limit("5 per minute")
rate_limit_register = limiter.limit("3 per hour")
rate_limit_password_reset = limiter.limit("3 per hour")
rate_limit_email_verification = limiter.limit("5 per hour")


@auth_bp.route('/login', methods=['GET', 'POST'])
@rate_limit_login
def login():
    """
    User login endpoint with security enhancements.
    
    Features:
    - Rate limiting (5 attempts per minute)
    - Account lockout after 5 failed attempts
    - Two-Factor Authentication support
    - Input sanitization
    
    Returns:
        str: Login form template or redirect to next page
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Sanitize input
        username = sanitize_string(form.username.data, max_length=20)
        password = form.password.data  # Password not sanitized, but validated
        
        user = User.query.filter_by(username=username).first()
        
        # Check if account is locked
        if user and user.is_account_locked():
            flash('Account is temporarily locked due to multiple failed login attempts. Please try again later or reset your password.', 'error')
            return render_template('auth/login.html', form=form)
        
        if user and user.check_password(password):
            # Check if 2FA is enabled
            if user.two_factor_enabled:
                # Store user ID in session for 2FA verification
                session['2fa_user_id'] = user.id
                session['2fa_verified'] = False
                return redirect(url_for('auth.verify_2fa'))
            
            # Reset failed login attempts on successful login
            user.reset_failed_login_attempts()
            
            # Get session ID before login for cart merging
            session_id = session.get('session_id') or request.cookies.get('session_id')
            
            login_user(user, remember=form.remember_me.data)
            
            # Merge guest cart with user cart
            if session_id:
                merge_guest_cart_to_user(user.id, session_id)
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            # Increment failed login attempts
            if user:
                user.increment_failed_login()
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    """
    Two-Factor Authentication verification endpoint.
    
    Returns:
        str: 2FA verification template or redirect
    """
    user_id = session.get('2fa_user_id')
    if not user_id:
        flash('Please log in first', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if not user or not user.two_factor_enabled:
        flash('2FA is not enabled for this account', 'error')
        session.pop('2fa_user_id', None)
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        
        if TwoFactorService.verify_code(user, code):
            session['2fa_verified'] = True
            session.pop('2fa_user_id', None)
            
            # Reset failed login attempts
            user.reset_failed_login_attempts()
            
            # Get session ID before login for cart merging
            session_id = session.get('session_id') or request.cookies.get('session_id')
            
            login_user(user, remember=True)
            
            # Merge guest cart with user cart
            if session_id:
                merge_guest_cart_to_user(user.id, session_id)
            
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid verification code. Please try again.', 'error')
    
    return render_template('auth/verify_2fa.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
@rate_limit_register
def register():
    """
    User registration endpoint with security enhancements.
    
    Features:
    - Rate limiting (3 registrations per hour)
    - Email verification required
    - Password strength validation
    - Input sanitization
    
    Returns:
        str: Registration form template or redirect to login
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Sanitize inputs
        username = sanitize_string(form.username.data, max_length=20)
        email = sanitize_string(form.email.data, max_length=120).lower()
        full_name = sanitize_string(form.full_name.data, max_length=100)
        phone = sanitize_string(form.phone.data, max_length=20) if form.phone.data else None
        address = sanitize_string(form.address.data, max_length=500) if form.address.data else None
        
        # Validate password strength
        is_valid, error_msg = validate_password_strength(form.password.data)
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('auth/register.html', form=form)
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('auth/register.html', form=form)
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone,
            address=address,
            user_type=form.user_type.data
        )
        user.set_password(form.password.data)
        user.email_verified = False  # Require email verification
        
        db.session.add(user)
        db.session.commit()
        
        # Generate email verification token
        token = Token.generate_token(user.id, 'email_verification', expires_in_hours=48)
        
        # Send verification email
        EmailService.send_verification_email(user, token.token)
        
        flash('Registration successful! Please check your email to verify your account.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
@rate_limit_password_reset
def forgot_password():
    """
    Password reset request endpoint.
    
    Features:
    - Rate limiting (3 requests per hour)
    - Email-based password reset
    
    Returns:
        str: Password reset request template or redirect
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = sanitize_string(request.form.get('email', ''), max_length=120).lower()
        
        if not email:
            flash('Please enter your email address', 'error')
            return render_template('auth/forgot_password.html')
        
        user = User.query.filter_by(email=email).first()
        
        # Always show success message to prevent email enumeration
        if user:
            # Generate password reset token
            token = Token.generate_token(user.id, 'password_reset', expires_in_hours=1)
            
            # Send password reset email
            EmailService.send_password_reset_email(user, token.token)
        
        flash('If an account with that email exists, a password reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
@rate_limit_password_reset
def reset_password(token):
    """
    Password reset confirmation endpoint.
    
    Args:
        token: Password reset token
        
    Returns:
        str: Password reset form template or redirect
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Validate token
    token_obj = Token.validate_token(token, 'password_reset')
    
    if not token_obj:
        flash('Invalid or expired password reset link. Please request a new one.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    user = token_obj.user
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validate password strength
        is_valid, error_msg = validate_password_strength(password)
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if password != password_confirm:
            flash('Passwords do not match', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        # Update password
        user.set_password(password)
        user.unlock_account()  # Unlock account if locked
        
        # Mark token as used
        token_obj.mark_as_used()
        
        db.session.commit()
        
        flash('Password reset successful! Please log in with your new password.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)


@auth_bp.route('/verify-email/<token>')
@rate_limit_email_verification
def verify_email(token):
    """
    Email verification endpoint.
    
    Args:
        token: Email verification token
        
    Returns:
        Redirect: Redirect to login or home page
    """
    # Validate token
    token_obj = Token.validate_token(token, 'email_verification')
    
    if not token_obj:
        flash('Invalid or expired verification link. Please request a new verification email.', 'error')
        return redirect(url_for('auth.login'))
    
    user = token_obj.user
    
    # Verify email
    user.verify_email()
    
    # Mark token as used
    token_obj.mark_as_used()
    
    flash('Email verified successfully! You can now log in.', 'success')
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    return redirect(url_for('auth.login'))


@auth_bp.route('/resend-verification', methods=['GET', 'POST'])
@rate_limit_email_verification
@login_required
def resend_verification():
    """
    Resend email verification endpoint.
    
    Returns:
        Redirect: Redirect to user profile or home
    """
    if current_user.email_verified:
        flash('Your email is already verified.', 'info')
        return redirect(url_for('user.profile'))
    
    # Generate new verification token
    token = Token.generate_token(current_user.id, 'email_verification', expires_in_hours=48)
    
    # Send verification email
    EmailService.send_verification_email(current_user, token.token)
    
    flash('Verification email sent! Please check your inbox.', 'success')
    return redirect(url_for('user.profile'))


@auth_bp.route('/enable-2fa', methods=['GET', 'POST'])
@login_required
def enable_2fa():
    """
    Enable Two-Factor Authentication endpoint.
    
    Returns:
        str: 2FA setup template or redirect
    """
    if current_user.two_factor_enabled:
        flash('2FA is already enabled for your account.', 'info')
        return redirect(url_for('user.profile'))
    
    if request.method == 'POST':
        # Generate secret and QR code
        secret, qr_code = TwoFactorService.enable_2fa(current_user)
        
        flash('2FA enabled successfully! Please scan the QR code with your authenticator app.', 'success')
        return render_template('auth/enable_2fa.html', qr_code=qr_code, secret=secret)
    
    # Generate secret and QR code for setup
    secret = TwoFactorService.generate_secret()
    qr_code = TwoFactorService.generate_qr_code(current_user, secret)
    
    return render_template('auth/enable_2fa.html', qr_code=qr_code, secret=secret)


@auth_bp.route('/disable-2fa', methods=['POST'])
@login_required
def disable_2fa():
    """
    Disable Two-Factor Authentication endpoint.
    
    Returns:
        Redirect: Redirect to user profile
    """
    if not current_user.two_factor_enabled:
        flash('2FA is not enabled for your account.', 'info')
        return redirect(url_for('user.profile'))
    
    # Verify password before disabling
    password = request.form.get('password', '')
    if not current_user.check_password(password):
        flash('Incorrect password. 2FA was not disabled.', 'error')
        return redirect(url_for('user.profile'))
    
    TwoFactorService.disable_2fa(current_user)
    
    flash('2FA disabled successfully.', 'success')
    return redirect(url_for('user.profile'))
