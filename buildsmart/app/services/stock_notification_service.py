"""
Stock Notification service for product availability alerts.

This module provides functionality for users to receive
notifications when out-of-stock products become available.
"""
from app.extensions import db
from app.models import StockNotification, Product
from app.services.email_service import EmailService


class StockNotificationService:
    """Service for stock notifications"""
    
    @staticmethod
    def create_notification(user_id, product_id):
        """
        Create a stock notification request.
        
        Args:
            user_id: User ID
            product_id: Product ID
            
        Returns:
            StockNotification: Created notification or None
        """
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return None
        
        # Check if notification already exists
        existing = StockNotification.query.filter_by(
            user_id=user_id,
            product_id=product_id,
            notified=False
        ).first()
        
        if existing:
            return existing
        
        # Create new notification
        notification = StockNotification(
            user_id=user_id,
            product_id=product_id
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return notification
    
    @staticmethod
    def check_and_notify(product_id):
        """
        Check if product is back in stock and notify users.
        
        Args:
            product_id: Product ID to check
            
        Returns:
            int: Number of users notified
        """
        product = Product.query.get(product_id)
        if not product or not product.is_in_stock():
            return 0
        
        # Find all pending notifications for this product
        notifications = StockNotification.query.filter_by(
            product_id=product_id,
            notified=False
        ).all()
        
        notified_count = 0
        
        for notification in notifications:
            # Send notification email
            from flask import current_app
            frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:5000')
            EmailService.send_email(
                subject=f'{product.name} is back in stock!',
                recipients=[notification.user.email],
                template='stock_notification.html',
                user=notification.user,
                product=product,
                frontend_url=frontend_url
            )
            
            # Mark as notified
            notification.mark_as_notified()
            notified_count += 1
        
        db.session.commit()
        
        return notified_count
    
    @staticmethod
    def remove_notification(user_id, product_id):
        """
        Remove stock notification.
        
        Args:
            user_id: User ID
            product_id: Product ID
            
        Returns:
            bool: True if removed, False otherwise
        """
        notification = StockNotification.query.filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()
        
        if not notification:
            return False
        
        db.session.delete(notification)
        db.session.commit()
        
        return True

