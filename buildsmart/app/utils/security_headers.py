"""
Security headers middleware for Flask application.

This module provides middleware to add security headers
to all HTTP responses to prevent common attacks.
"""
from flask import current_app


def setup_security_headers(app):
    """
    Set up security headers middleware.
    
    Args:
        app: Flask application instance
    """
    @app.after_request
    def set_security_headers(response):
        """
        Add security headers to all responses.
        
        Args:
            response: Flask response object
            
        Returns:
            Response: Response with security headers
        """
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdn.socket.io https://maps.googleapis.com https://maps.gstatic.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' data: https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none';"
        )
        response.headers['Content-Security-Policy'] = csp
        
        # Strict Transport Security (only in production with HTTPS)
        if not app.config.get('DEBUG', False):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response.headers['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'payment=()'
        )
        
        return response

