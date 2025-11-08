"""
Email service for sending transactional emails.

This module provides email functionality for password reset,
email verification, and other notifications.
"""
from flask import render_template, current_app
from flask_mail import Message
from app.extensions import mail
from app.config import Config


class EmailService:
    """Service for sending emails"""
    
    @staticmethod
    def send_email(subject, recipients, template, **kwargs):
        """
        Send an email using Flask-Mail.
        
        Args:
            subject (str): Email subject
            recipients (list): List of recipient email addresses
            template (str): Template name for email body
            **kwargs: Additional context variables for template
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            msg = Message(
                subject=subject,
                recipients=recipients,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@buildsmart.com')
            )
            msg.html = render_template(f'emails/{template}', **kwargs)
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f'Failed to send email: {str(e)}')
            return False
    
    @staticmethod
    def send_verification_email(user, token):
        """
        Send email verification link to user.
        
        Args:
            user: User object
            token: Verification token string
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        verification_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:5000')}/auth/verify-email/{token}"
        
        return EmailService.send_email(
            subject='Verify Your BuildSmart Email Address',
            recipients=[user.email],
            template='verify_email.html',
            user=user,
            verification_url=verification_url,
            token=token
        )
    
    @staticmethod
    def send_password_reset_email(user, token):
        """
        Send password reset link to user.
        
        Args:
            user: User object
            token: Password reset token string
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        reset_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:5000')}/auth/reset-password/{token}"
        
        return EmailService.send_email(
            subject='Reset Your BuildSmart Password',
            recipients=[user.email],
            template='password_reset.html',
            user=user,
            reset_url=reset_url,
            token=token
        )
    
    @staticmethod
    def send_welcome_email(user):
        """
        Send welcome email to new user.
        
        Args:
            user: User object
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        return EmailService.send_email(
            subject='Welcome to BuildSmart!',
            recipients=[user.email],
            template='welcome.html',
            user=user
        )

