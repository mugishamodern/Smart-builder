"""
Notification service for managing in-app notifications.

This module provides functionality for creating, managing,
and sending notifications to users.
"""
from datetime import datetime
from app.extensions import db
from app.models import Notification, NotificationPreference, User
from app.services.email_service import EmailService
from flask import current_app


class NotificationService:
    """Service for managing notifications"""
    
    @staticmethod
    def create_notification(user_id, notification_type, title, message, link=None, related_id=None, related_type=None, priority='normal'):
        """
        Create an in-app notification.
        
        Args:
            user_id: User ID
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            link: Optional link/URL
            related_id: Related entity ID
            related_type: Type of related entity
            priority: Priority level
            
        Returns:
            Notification: Created notification
        """
        notification = Notification(
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link,
            related_id=related_id,
            related_type=related_type,
            priority=priority
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # Send email notification if enabled
        NotificationService._send_email_notification(notification)
        
        # Send SMS notification if enabled
        NotificationService._send_sms_notification(notification)
        
        return notification
    
    @staticmethod
    def _send_email_notification(notification):
        """Send email notification if enabled."""
        try:
            user = notification.user
            if not user or not user.email:
                return
            
            # Check user preferences
            preference = NotificationPreference.query.filter_by(
                user_id=user.id,
                notification_type=notification.notification_type
            ).first()
            
            # Default to enabled if no preference exists
            email_enabled = preference.email_enabled if preference else True
            
            if not email_enabled:
                return
            
            # Send email based on notification type
            template_map = {
                'order': 'notifications/order_notification.html',
                'system': 'notifications/system_notification.html',
                'alert': 'notifications/generic_notification.html',
                'promotion': 'notifications/generic_notification.html'
            }
            
            template = template_map.get(notification.notification_type, 'notifications/generic_notification.html')
            
            EmailService.send_email(
                subject=notification.title,
                recipients=[user.email],
                template=template,
                user=user,
                notification=notification
            )
                
        except Exception as e:
            current_app.logger.error(f'Error sending email notification: {str(e)}')
    
    @staticmethod
    def _send_sms_notification(notification):
        """Send SMS notification if enabled."""
        try:
            from app.services.sms_service import SMSService
            
            user = notification.user
            if not user or not user.phone:
                return
            
            # Check user preferences
            preference = NotificationPreference.query.filter_by(
                user_id=user.id,
                notification_type=notification.notification_type
            ).first()
            
            # Default to disabled if no preference exists
            sms_enabled = preference.sms_enabled if preference else False
            
            if not sms_enabled:
                return
            
            # Send SMS
            SMSService.send_notification(user.phone, notification.title, notification.message)
            
        except ImportError:
            # SMS service not configured
            pass
        except Exception as e:
            current_app.logger.error(f'Error sending SMS notification: {str(e)}')
    
    @staticmethod
    def notify_order_status(order, status, notes=None):
        """
        Create notification for order status change.
        
        Args:
            order: Order object
            status: New order status
            notes: Optional notes
            
        Returns:
            Notification: Created notification
        """
        title = f'Order {order.order_number} Status Update'
        message = f'Your order {order.order_number} status has been updated to {status}.'
        if notes:
            message += f'\n\n{notes}'
        
        link = f'/user/orders/{order.id}'
        
        return NotificationService.create_notification(
            user_id=order.customer_id,
            notification_type='order',
            title=title,
            message=message,
            link=link,
            related_id=order.id,
            related_type='order',
            priority='high'
        )
    
    @staticmethod
    def notify_low_stock(shop_owner, product):
        """
        Create notification for low stock.
        
        Args:
            shop_owner: Shop owner user object
            product: Product object
            
        Returns:
            Notification: Created notification
        """
        title = f'Low Stock Alert: {product.name}'
        message = f'{product.name} is running low on stock. Current quantity: {product.quantity_available}'
        
        link = f'/shop/{product.shop_id}/inventory'
        
        return NotificationService.create_notification(
            user_id=shop_owner.id,
            notification_type='alert',
            title=title,
            message=message,
            link=link,
            related_id=product.id,
            related_type='product',
            priority='high'
        )
    
    @staticmethod
    def get_user_notifications(user_id, unread_only=False, limit=None):
        """
        Get notifications for a user.
        
        Args:
            user_id: User ID
            unread_only: Only return unread notifications
            limit: Maximum number of notifications
            
        Returns:
            list: List of notifications
        """
        query = Notification.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        query = query.order_by(Notification.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_unread_count(user_id):
        """
        Get unread notification count for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Unread count
        """
        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()
    
    @staticmethod
    def mark_as_read(notification_id, user_id):
        """
        Mark notification as read.
        
        Args:
            notification_id: Notification ID
            user_id: User ID (for verification)
            
        Returns:
            bool: True if successful, False otherwise
        """
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if not notification:
            return False
        
        notification.mark_as_read()
        return True
    
    @staticmethod
    def mark_all_as_read(user_id):
        """
        Mark all notifications as read for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Number of notifications marked as read
        """
        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).all()
        
        for notification in notifications:
            notification.mark_as_read()
        
        return len(notifications)
    
    @staticmethod
    def delete_notification(notification_id, user_id):
        """
        Delete a notification.
        
        Args:
            notification_id: Notification ID
            user_id: User ID (for verification)
            
        Returns:
            bool: True if successful, False otherwise
        """
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if not notification:
            return False
        
        db.session.delete(notification)
        db.session.commit()
        
        return True

